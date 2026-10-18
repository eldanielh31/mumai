"""Escenario simulado determinista y etiquetas conocidas para ACT-PRU-01."""
from pathlib import Path
import json
import cv2
import numpy as np


def generate_reference(path, kind="subtle", seconds=20, fps=20, size=(160, 120)):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    width, height = size
    base = np.full((height, width), 128, dtype=np.uint8)
    texture = rng.integers(45, 210, (height // 2, width // 2), dtype=np.uint8)
    texture = cv2.GaussianBlur(texture, (3, 3), .6)
    y, x = height // 4, width // 4
    base[y:y + texture.shape[0], x:x + texture.shape[1]] = texture
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"FFV1"), fps, size)
    if not writer.isOpened():
        raise RuntimeError("No se pudo generar el video sin pérdida FFV1.")
    truth = []
    try:
        for index in range(round(seconds * fps)):
            t = index / fps
            frequency = 5.0 if kind == "out_of_band" else 1.0
            amplitude = 0 if kind in ("static", "lighting") else .25
            anomalous = kind == "amplitude_change" and t >= seconds * .65
            if anomalous:
                amplitude = 2.0
            dx = amplitude * np.sin(2 * np.pi * frequency * t)
            frame = cv2.warpAffine(base, np.float32([[1, 0, dx], [0, 1, 0]]), size,
                                   flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            if kind == "lighting":
                frame = np.clip(frame.astype(float) + 8 * np.sin(2 * np.pi * t), 0, 255).astype(np.uint8)
            writer.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
            truth.append({"frame": index, "time_seconds": t, "dx_pixels": float(dx), "change": anomalous})
    finally:
        writer.release()
    metadata = {"kind": kind, "synthetic": True, "seed": 42, "fps": fps,
                "size": size, "seconds": seconds, "codec": "FFV1", "frames": truth,
                "conditions": "Cámara fija simulada; luz constante salvo caso lighting; sin ruido temporal ni compresión con pérdida.",
                "limitation": "No representa daño real ni valida sensibilidad clínica, mecánica o industrial."}
    path.with_suffix(".json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1] / "data/input/referencias"
    for kind in ("static", "subtle", "out_of_band", "amplitude_change", "lighting"):
        target = root / f"{kind}.avi"
        if target.exists():
            print(f"Conservado: {target}")
        else:
            print(generate_reference(target, kind))
