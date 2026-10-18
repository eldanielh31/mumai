"""La misma medida de flujo óptico para original y magnificado."""
import cv2
import numpy as np


class MotionAnalyzer:
    def __init__(self):
        self.previous = None

    def process(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.previous is None:
            self.previous = gray
            return None
        flow = cv2.calcOpticalFlowFarneback(
            self.previous, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0,
        )
        self.previous = gray
        magnitude = np.linalg.norm(flow, axis=2)
        if not np.isfinite(magnitude).all():
            raise ValueError("El análisis de movimiento produjo valores no finitos.")
        return magnitude


def metrics(magnitude, fps):
    return {
        "mean_px_frame": float(magnitude.mean()),
        "p95_px_frame": float(np.percentile(magnitude, 95)),
        "rms_px_frame": float(np.sqrt(np.mean(magnitude ** 2))),
        "mean_px_second": float(magnitude.mean() * fps),
    }
