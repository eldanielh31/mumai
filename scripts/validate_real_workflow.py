"""Repite por interfaz una captura local y verifica exportación y reproducibilidad.

El reporte previo conserva la configuración exacta. La evidencia es textual;
los videos y resultados reales permanecen en el destino local indicado.
"""

import argparse
import hashlib
import json
import platform
import sys
import time
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import cv2
from PySide6.QtWidgets import QApplication

from video_analysis.gui.main_window import MainWindow


def digest(path):
    sha = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path, help="Carpeta del análisis previo con informe.json")
    parser.add_argument("--output", type=Path, required=True, help="Destino local de exportación")
    parser.add_argument(
        "--evidence", type=Path, required=True, help="JSON nuevo; nunca sobrescrito"
    )
    parser.add_argument("--date", help="Fecha de corte AAAA-MM-DD")
    parser.add_argument("--timeout", type=float, default=600)
    args = parser.parse_args()
    cutoff = args.date or datetime.now(ZoneInfo("America/Costa_Rica")).date().isoformat()
    date.fromisoformat(cutoff)
    if args.evidence.exists():
        parser.error("La evidencia ya existe; elige otra ruta.")
    if args.timeout <= 0:
        parser.error("El tiempo máximo debe ser positivo.")
    prior = json.loads((args.reference / "informe.json").read_text(encoding="utf-8"))
    source = Path(prior["input"]["path"])
    if digest(source) != prior["input_sha256"]:
        parser.error("La entrada no coincide con la huella del análisis previo.")
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    checks = {}
    evidence = {
        "date": cutoff,
        "type": "Captura real; verificación técnica, no diagnóstico ni aceptación externa",
        "reference": str(args.reference.resolve()),
        "checks": checks,
        "environment": {
            "python": platform.python_version(),
            "system": platform.platform(),
            "qt_platform": app.platformName(),
            "opencv_opencl_enabled": cv2.ocl.useOpenCL(),
            "visible_gpu_devices": [str(p) for p in Path("/dev").glob("nvidia*")]
            + ([str(p) for p in Path("/dev/dri").iterdir()] if Path("/dev/dri").exists() else []),
            "network_interfaces": [p.name for p in Path("/sys/class/net").iterdir()],
            "network_counters": Path("/proc/net/dev").read_text(),
            "memory": Path("/proc/meminfo").read_text().splitlines()[:3],
            "cpu": next(
                (
                    line.split(":", 1)[1].strip()
                    for line in Path("/proc/cpuinfo").read_text().splitlines()
                    if line.startswith("model name")
                ),
                "No identificado",
            ),
        },
    }

    def wait():
        deadline = time.monotonic() + args.timeout
        while window.worker is not None and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.01)
        if window.worker is not None:
            raise RuntimeError("La operación excedió el tiempo máximo.")

    try:
        config = prior["config"]
        for attr, key in (
            ("low", "low_hz"),
            ("high", "high_hz"),
            ("alpha", "alpha"),
            ("baseline", "baseline_seconds"),
            ("dimension", "max_dimension"),
            ("spatial_level", "spatial_level"),
        ):
            getattr(window, attr).setValue(config[key])
        window.patterns.setChecked(config["patterns_enabled"])
        window.notes.setText(config["capture_notes"])
        window.show()
        window.load_video(str(source))
        wait()
        checks["load_real_video"] = window.state == "Entrada válida"
        window.configure()
        checks["configuration"] = window.state == "Configurado"
        window.start_analysis()
        wait()
        if window.result_path is None:
            raise RuntimeError(window.status.text())
        result = window.result_path
        report = json.loads((result / "informe.json").read_text(encoding="utf-8"))
        checks["result_before_export"] = (
            window.state == "Resultados disponibles" and window.exported_path is None
        )
        checks["four_metrics"] = window.metrics_table.rowCount() == 4
        checks["maps_and_chart"] = (
            not window.preview.pixmap().isNull() and not window.chart.pixmap().isNull()
        )
        checks["same_input_and_config"] = (
            report["input_sha256"] == prior["input_sha256"] and report["config"] == config
        )
        checks["repeat_summary"] = all(
            report[key] == prior[key]
            for key in (
                "original",
                "magnified",
                "mean_motion_ratio",
                "flagged_windows",
                "clipped_pixel_fraction",
            )
        )
        for filename in (
            "metricas.csv",
            "patrones.json",
            "movimiento_original.npy",
            "movimiento_magnificado.npy",
        ):
            checks[f"repeat_{filename}"] = digest(result / filename) == digest(
                args.reference / filename
            )
        window.tabs.setCurrentWidget(window.player)
        target = min(int(report["input"]["fps"] * 14), report["input"]["frame_count"] - 2)
        window.player.seek(target)
        checks["seek_comparison"] = window.player.frame_index == target
        window.player.toggle()
        deadline = time.monotonic() + 2
        while window.player.frame_index <= target and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.01)
        window.player.pause()
        checks["play_pause_comparison"] = (
            window.player.frame_index > target and not window.player.timer.isActive()
        )
        window.start_export(args.output)
        wait()
        if window.exported_path is None:
            raise RuntimeError(window.status.text())
        saved = window.exported_path
        receipt = json.loads((saved / "exportacion.json").read_text(encoding="utf-8"))
        checks["export_hashes"] = all(
            digest(saved / name) == item["sha256"]
            and (saved / name).stat().st_size == item["bytes"]
            for name, item in receipt["files"].items()
        )
        checks["receipt_complete"] = set(receipt["files"]) == {p.name for p in saved.iterdir()} - {
            "exportacion.json"
        }
        checks["local_summary"] = (saved / "resumen.html").is_file()
        checks["input_unchanged"] = digest(source) == prior["input_sha256"]
        evidence["report"] = report
        evidence["exported"] = str(saved.resolve())
        evidence["receipt"] = receipt
        window.reset()
        checks["reset_preserves_export"] = (
            window.state == "En espera"
            and (saved / "informe.json").exists()
            and not result.exists()
        )
    except Exception as exc:
        evidence["error"] = str(exc)
        raise
    finally:
        if window.worker is not None:
            window.cancel()
            window.worker.wait()
            app.processEvents()
        window.close()
        args.evidence.parent.mkdir(parents=True, exist_ok=True)
        with args.evidence.open("x", encoding="utf-8") as stream:
            json.dump(evidence, stream, ensure_ascii=False, indent=2)
        print(
            json.dumps(
                {"checks": checks, "error": evidence.get("error")}, ensure_ascii=False, indent=2
            )
        )
    if not all(checks.values()):
        raise SystemExit("Hay comprobaciones fallidas; consulta la evidencia.")


if __name__ == "__main__":
    main()
