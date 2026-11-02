"""EVM lineal de una escala gaussiana, luminancia y filtro temporal causal.

Basado en la descomposición espacial + filtrado temporal de Wu et al. (2012).
No implementa la variante por fase ni garantiza ganancia geométrica exacta.
"""

import cv2
import numpy as np
from scipy.signal import butter, sosfilt, sosfilt_zi


class EulerianMagnifier:
    def __init__(self, fps, low_hz=0.7, high_hz=1.5, alpha=5.0, level=1):
        if not all(np.isfinite(x) for x in (fps, low_hz, high_hz, alpha)):
            raise ValueError("Los parámetros deben ser números finitos.")
        if not 0 < low_hz < high_hz < fps / 2:
            raise ValueError("Las frecuencias deben cumplir 0 < mínima < máxima < FPS/2.")
        if not 0 <= alpha <= 30 or not isinstance(level, int) or not 0 <= level <= 4:
            raise ValueError("Amplificación permitida: 0–30; nivel espacial: 0–4.")
        self.sos = butter(2, [low_hz, high_hz], btype="bandpass", fs=fps, output="sos")
        self.alpha, self.level = alpha, level
        self.state = None
        self.shape = None
        self.clipped_pixels = 0
        self.total_pixels = 0

    def process(self, frame):
        if self.shape is None:
            self.shape = frame.shape
        if frame.shape != self.shape:
            raise ValueError("La resolución debe permanecer constante.")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float64) / 255
        small = gray
        sizes = []
        for _ in range(self.level):
            sizes.append((small.shape[1], small.shape[0]))
            small = cv2.pyrDown(small)
        if self.state is None:
            self.state = sosfilt_zi(self.sos)[:, :, None, None] * small[None, None]
        filtered, self.state = sosfilt(self.sos, small[None], axis=0, zi=self.state)
        delta = filtered[0]
        for size in reversed(sizes):
            delta = cv2.pyrUp(delta, dstsize=size)
        # Sumar el mismo delta a B, G y R amplifica luminancia sin escalar crominancia.
        result = frame.astype(np.float64) + self.alpha * delta[:, :, None] * 255
        self.clipped_pixels += int(np.any((result < 0) | (result > 255), axis=2).sum())
        self.total_pixels += frame.shape[0] * frame.shape[1]
        return np.rint(np.clip(result, 0, 255)).astype(np.uint8)
