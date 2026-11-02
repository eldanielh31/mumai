"""Genera un video sintético reproducible; no representa datos de maquinaria."""

from pathlib import Path

import cv2
import numpy as np


def create_sample(path, codec="MJPG", frames=30, fps=10, size=(320, 240)):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*codec), fps, size)
    if not writer.isOpened():
        raise RuntimeError(f"No se pudo crear el video con el códec {codec}.")
    try:
        for index in range(frames):
            frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
            x = 20 + index * 5 % (size[0] - 40)
            cv2.circle(frame, (x, size[1] // 2), 15, (80, 200, 250), -1)
            cv2.putText(
                frame,
                f"Prueba {index + 1}/{frames}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )
            writer.write(frame)
    finally:
        writer.release()
    return path


if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1] / "data/input/prueba_movimiento.avi"
    if target.exists():
        raise SystemExit(f"El archivo ya existe; se conserva: {target}")
    print(create_sample(target))
