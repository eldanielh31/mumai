"""Verificación de entradas y exportaciones de esta sesión; solo lectura del material."""

import csv
import hashlib
import json
import math
import re
from pathlib import Path

import cv2
import numpy as np

root = Path(__file__).resolve().parents[2]
evidence = Path(__file__).resolve().parent
target = evidence / "integridad.json"
if target.exists():
    raise SystemExit("La evidencia ya existe; no se sobrescribe")


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


prior = json.loads((evidence / "entorno.json").read_text())
inputs = {n: sha(root / n) == h for n, h in prior["input_hashes"].items()}
motor = json.loads((evidence / "motor-sin-red.json").read_text())
functional = json.loads((evidence / "funcionales/casos.json").read_text())
exports = [Path(motor["reference"]), Path(motor["exported"])] + list(
    map(Path, functional["exports"])
)
results = {}
for folder in exports:
    report = json.loads((folder / "informe.json").read_text())
    receipt = json.loads((folder / "exportacion.json").read_text())
    checks = {
        "all_files_listed": set(receipt["files"])
        == {p.name for p in folder.iterdir()} - {"exportacion.json"},
        "hashes_and_sizes": all(
            sha(folder / n) == v["sha256"] and (folder / n).stat().st_size == v["bytes"]
            for n, v in receipt["files"].items()
        ),
        "source_matches": sha(report["input"]["path"]) == report["input_sha256"],
    }
    videos = {}
    width, height = report["processing_size"]
    for name in ("original.avi", "magnificado.avi", "comparacion.avi"):
        capture = cv2.VideoCapture(str(folder / name))
        count = 0
        valid_size = True
        fps = capture.get(cv2.CAP_PROP_FPS)
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            count += 1
            valid_size &= frame.shape[:2] == (
                height,
                width * (2 if name == "comparacion.avi" else 1),
            )
        capture.release()
        videos[name] = {"frames": count, "fps": fps, "valid_size": valid_size}
        checks[name] = (
            count == report["input"]["frame_count"] and fps == report["input"]["fps"] and valid_size
        )
    for file in folder.glob("*.png"):
        checks[file.name] = cv2.imread(str(file)) is not None
    for file in folder.glob("*.npy"):
        matrix = np.load(file)
        checks[file.name] = matrix.shape == (height, width) and bool(np.isfinite(matrix).all())
    with (folder / "metricas.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    included = [row for row in rows if row["included"] == "1"]
    checks["csv_count"] = (
        len(rows) == report["input"]["frame_count"]
        and len(included) == report["analyzed_frame_pairs"]
    )
    checks["csv_finite"] = all(math.isfinite(float(v)) for row in rows for v in row.values())
    checks["all_four_summary_metrics"] = all(
        math.isclose(
            sum(float(row[tag + "_" + metric]) for row in included) / len(included),
            value,
            rel_tol=1e-9,
            abs_tol=1e-12,
        )
        for tag in ("original", "magnified")
        for metric, value in report[tag].items()
    )
    links = re.findall(r'(?:src|href)="([^"]+)"', (folder / "resumen.html").read_text())
    checks["html_local_links_exist"] = all((folder / link).is_file() for link in links)
    results[str(folder)] = {"checks": checks, "videos": videos, "passed": all(checks.values())}
result = {
    "inputs_unchanged": inputs,
    "exports": results,
    "passed": all(inputs.values()) and all(v["passed"] for v in results.values()),
}
target.write_text(json.dumps(result, indent=2, ensure_ascii=False))
print(json.dumps({"inputs": len(inputs), "exports": len(results), "passed": result["passed"]}))
if not result["passed"]:
    raise SystemExit(1)
