"""ACT-PRU-02: casos M01-M15 automatizados por Qt; no aceptación del usuario."""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtWidgets import QApplication

from video_analysis.gui.main_window import MainWindow


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    root = Path(__file__).resolve().parents[1]
    inputs = root / "data/input/referencias"
    output = root / "data/output" / evidence.name
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    cases = {}
    result = {
        "activity": "ACT-PRU-02",
        "date_local": datetime.now(ZoneInfo("America/Guatemala")).isoformat(),
        "executor": "Codex; automatización de Qt, no ejecución manual de Daniel",
        "qt_platform": app.platformName(),
        "selector_scope": "M13 simula únicamente la respuesta de cancelar del selector; exportaciones y procesamiento reales",
        "cases": cases,
    }

    def wait():
        deadline = time.monotonic() + 180
        while window.worker is not None and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.01)
        if window.worker is not None:
            raise RuntimeError("Operación excedió 180 segundos")

    def record(case, **checks):
        cases[case] = {"checks": checks, "passed": all(checks.values())}
        print(case, json.dumps(cases[case]), flush=True)
        if not cases[case]["passed"]:
            raise AssertionError(case)

    def load(kind="subtle"):
        window.reset()
        window.dimension.setValue(160)
        window.low.setValue(0.7)
        window.high.setValue(1.5)
        window.alpha.setValue(5)
        window.baseline.setValue(8)
        window.spatial_level.setValue(1)
        window.patterns.setChecked(True)
        window.notes.setText("Referencia sintética; cámara fija simulada; sin diagnóstico mecánico")
        window.load_video(str(inputs / (kind + ".avi")))
        wait()
        if window.state != "Entrada válida":
            raise RuntimeError(window.status.text())

    def analyze():
        window.start_analysis()
        wait()
        if window.result_path is None:
            raise RuntimeError(window.status.text())
        return json.loads((window.result_path / "informe.json").read_text())

    def export():
        window.start_export(output)
        wait()
        if window.exported_path is None:
            raise RuntimeError(window.status.text())
        saved = window.exported_path
        receipt = json.loads((saved / "exportacion.json").read_text())
        assert set(receipt["files"]) == {p.name for p in saved.iterdir()} - {"exportacion.json"}
        assert all(
            digest(saved / n) == v["sha256"] and (saved / n).stat().st_size == v["bytes"]
            for n, v in receipt["files"].items()
        )
        return saved

    try:
        window.show()
        load()
        window.configure()
        record(
            "M01",
            metadata=(
                window.info.width,
                window.info.height,
                window.info.frame_count,
                window.info.fps,
            )
            == (160, 120, 400, 20),
            configured=window.state == "Configurado",
            no_automatic_analysis=window.result_path is None,
        )
        window.load_video(str(root / "README.md"))
        wait()
        rejected = (
            window.state == "Error controlado"
            and window.info is None
            and not window.analyze_button.isEnabled()
        )
        load()
        window.configure()
        record("M02", invalid_format_rejected=rejected, recovered=window.state == "Configurado")
        before = digest(inputs / "subtle.avi")
        window.high.setValue(11)
        window.configure()
        invalid = window.state == "Error controlado" and window.worker is None
        window.high.setValue(1.5)
        window.dimension.setValue(80)
        report = analyze()
        record(
            "M03",
            nyquist_rejected=invalid,
            proportional_size=report["processing_size"] == [80, 60],
            input_unchanged=digest(inputs / "subtle.avi") == before,
        )
        load("static")
        report = analyze()
        record(
            "M04",
            static_motion=report["magnified"]["mean_px_frame"] < 0.001,
            no_events=report["flagged_windows"] == 0,
        )
        load()
        report = analyze()
        inside = report["mean_motion_ratio"]
        record(
            "M05",
            in_band_gain=inside > 1.5,
            no_events=report["flagged_windows"] == 0,
            shared_scale=report["heatmap_scale"]["shared"],
        )
        load("out_of_band")
        report = analyze()
        record(
            "M06",
            lower_gain=inside > report["mean_motion_ratio"] * 1.5,
            no_events=report["flagged_windows"] == 0,
        )
        load()
        window.alpha.setValue(0)
        report = analyze()
        record(
            "M07",
            equal_metrics=report["original"] == report["magnified"],
            equal_maps=digest(window.result_path / "movimiento_original.npy")
            == digest(window.result_path / "movimiento_magnificado.npy"),
        )
        load("amplitude_change")
        report = analyze()
        patterns = json.loads((window.result_path / "patrones.json").read_text())
        record(
            "M08",
            evaluated=report["patterns_status"] == "evaluated",
            fourteen_windows=len(patterns["events"]) == 14,
            no_early_events=all(e["start_seconds"] >= 13 for e in patterns["events"]),
        )
        window.tabs.setCurrentWidget(window.player)
        window.player.seek(280)
        seek = window.player.frame_index == 280
        window.player.toggle()
        deadline = time.monotonic() + 2
        while window.player.frame_index <= 280 and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.01)
        playing = window.player.frame_index > 280
        window.player.pause()
        paused = not window.player.timer.isActive()
        window.player.seek(399)
        window.player.toggle()
        restarted = window.player.frame_index == 0
        window.player.pause()
        window.player.seek(280)
        for i, name in enumerate(("mapas", "metricas", "comparacion", "tabla")):
            window.tabs.setCurrentIndex(i)
            app.processEvents()
            assert window.grab().save(str(evidence / (name + ".png")))
        record(
            "M12",
            four_tabs=window.tabs.count() == 4,
            four_metrics=window.metrics_table.rowCount() == 4,
            maps_and_chart=not window.preview.pixmap().isNull()
            and not window.chart.pixmap().isNull(),
            seek=seek,
            playback=playing,
            pause=paused,
            restart=restarted,
        )
        original = window.result_path
        with patch(
            "video_analysis.gui.main_window.QFileDialog.getExistingDirectory", return_value=""
        ):
            window.choose_export()
        cancelled_selector = window.result_path == original and window.worker is None
        first = export()
        second = export()
        html = (second / "resumen.html").read_text()
        window.reset()
        record(
            "M13",
            cancel_selector_keeps_analysis=cancelled_selector,
            unique_exports=first != second,
            complete_verified_exports=True,
            reset_preserves_both=(first / "informe.json").is_file()
            and (second / "informe.json").is_file(),
            reset_removes_temporary=not original.exists(),
            local_html="https://" not in html and 'src="mapas_comparados.png"' in html,
        )
        load("amplitude_change")
        window.patterns.setChecked(False)
        report = analyze()
        record(
            "M09",
            disabled=report["patterns_status"] == "disabled",
            visible_disabled="desactivado" in window.status.text(),
            other_results=window.metrics_table.rowCount() == 4,
        )
        load("amplitude_change")
        window.baseline.setValue(1)
        report = analyze()
        record(
            "M10",
            insufficient=report["patterns_status"] == "insufficient_reference",
            visible_warning="insuficiente" in window.status.text(),
            other_results=window.metrics_table.rowCount() == 4,
        )
        load("lighting")
        report = analyze()
        record(
            "M11",
            small_residual=report["magnified"]["mean_px_frame"] < 0.001,
            no_events=report["flagged_windows"] == 0,
            illumination_warning=any("iluminación" in w for w in report["warnings"]),
        )
        window.alpha.setValue(2)
        cleared = (
            window.result_path is None
            and window.player.capture is None
            and window.metrics_table.rowCount() == 0
            and window.preview.pixmap().isNull()
            and window.chart.pixmap().isNull()
        )
        window.high.setValue(11)
        window.start_analysis()
        invalid = window.state == "Error controlado" and window.worker is None
        window.high.setValue(1.5)
        window.configure()
        recovered = window.state == "Configurado"
        short = root / "data/input/prueba_movimiento.avi"
        window.load_video(str(short))
        wait()
        window.start_analysis()
        wait()
        short_error = window.state == "Error controlado" and window.result_path is None
        load()
        window.configure()
        record(
            "M14",
            views_cleared=cleared,
            bad_configuration_rejected=invalid,
            configuration_recovered=recovered,
            short_video_error=short_error,
            new_input_recovers=window.state == "Configurado",
        )
        window.start_analysis()
        deadline = time.monotonic() + 30
        while (
            window.worker is not None
            and window.progress_bar.value() < 5
            and time.monotonic() < deadline
        ):
            app.processEvents()
            time.sleep(0.001)
        active = window.worker is not None and window.progress_bar.value() >= 5
        observed_progress = window.progress_bar.value()
        window.cancel()
        wait()
        status = window.status.text()
        clean = not list(Path(window._session.name).iterdir())
        cancelled = (
            window.state == "Error controlado"
            and "cancelad" in status.lower()
            and window.result_path is None
        )
        load("static")
        analyze()
        record(
            "M15",
            cancelled_while_processing=active,
            cancellation_reported=cancelled,
            no_partial_result=clean,
            next_analysis_succeeds=window.state == "Resultados disponibles",
        )
        result["cancellation_observed_progress"] = observed_progress
        result["exports"] = [str(first), str(second)]
    except Exception as exc:
        result["error"] = str(exc)
        raise
    finally:
        if window.worker is not None:
            window.cancel()
            window.worker.wait()
            app.processEvents()
        window.close()
        (evidence / "casos.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    assert len(cases) == 15 and all(c["passed"] for c in cases.values())


if __name__ == "__main__":
    main()
