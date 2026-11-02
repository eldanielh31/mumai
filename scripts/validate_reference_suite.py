"""Ejecuta cinco escenarios etiquetados y guarda evidencia reproducible."""

import json
import sys
import uuid
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from create_reference_videos import generate_reference

from video_analysis.pipeline import AnalysisConfig, analyze_video


def run(evidence_path=None, cutoff_date=None):
    project = Path(__file__).resolve().parents[1]
    cutoff_date = cutoff_date or datetime.now(ZoneInfo("America/Costa_Rica")).date().isoformat()
    date.fromisoformat(cutoff_date)
    target = (
        Path(evidence_path)
        if evidence_path
        else project / f"docs/validacion-{cutoff_date}-{uuid.uuid4().hex[:8]}.json"
    )
    if target.exists():
        raise SystemExit(
            f"La evidencia ya existe: {target}. Usa otra ruta para conservar el historial."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    inputs = project / "data/input/referencias"
    outputs = project / "data/output/validacion"
    summaries = {}
    for kind in ("static", "subtle", "out_of_band", "amplitude_change", "lighting"):
        path = inputs / f"{kind}.avi"
        if not path.exists():
            generate_reference(path, kind)
        result = analyze_video(
            path,
            outputs,
            AnalysisConfig(
                max_dimension=160,
                capture_notes="Escenario sintético, semilla 42; cámara fija; iluminación constante salvo lighting; FFV1 sin pérdida.",
            ),
        )
        report = json.loads((result / "informe.json").read_text())
        patterns = json.loads((result / "patrones.json").read_text())
        summaries[kind] = {
            "output": str(result.relative_to(project)),
            "original_mean": report["original"]["mean_px_frame"],
            "magnified_mean": report["magnified"]["mean_px_frame"],
            "motion_ratio": report["mean_motion_ratio"],
            "flagged_windows": report["flagged_windows"],
            "events": patterns["events"],
            "elapsed_seconds": report["elapsed_seconds"],
            "clipping_fraction": report["clipped_pixel_fraction"],
        }
        print(
            kind,
            json.dumps({k: v for k, v in summaries[kind].items() if k != "events"}),
            flush=True,
        )
    checks = {
        "static_has_no_alerts": summaries["static"]["flagged_windows"] == 0,
        "static_motion_below_0_001": summaries["static"]["magnified_mean"] < 0.001,
        "in_band_motion_increases": summaries["subtle"]["motion_ratio"] > 1.5,
        "in_band_gain_exceeds_out_of_band": summaries["subtle"]["motion_ratio"]
        > summaries["out_of_band"]["motion_ratio"] * 1.5,
        "stable_subtle_has_no_alerts": summaries["subtle"]["flagged_windows"] == 0,
        "amplitude_change_detected_after_13_seconds": any(
            e["start_seconds"] >= 13 for e in summaries["amplitude_change"]["events"]
        ),
        "no_early_amplitude_alerts": all(
            e["start_seconds"] >= 12.5 for e in summaries["amplitude_change"]["events"]
        ),
    }
    evidence = {
        "date": cutoff_date,
        "scenario": "Simulación; no maquinaria real",
        "checks": checks,
        "results": summaries,
        "limitations": [
            "Las alertas no demuestran daño real.",
            "Iluminación y movimiento de cámara pueden contaminar EVM y flujo óptico.",
            "No se han estimado sensibilidad ni especificidad sobre maquinaria real.",
        ],
    }
    target.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    if not all(checks.values()):
        raise SystemExit(f"Comprobaciones fallidas: {[k for k, v in checks.items() if not v]}")
    print("Todas las comprobaciones de referencia pasaron.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--evidence", help="Archivo nuevo para conservar el historial de validaciones"
    )
    parser.add_argument("--date", help="Fecha de corte AAAA-MM-DD; por defecto fecha de Costa Rica")
    args = parser.parse_args()
    run(args.evidence, args.date)
