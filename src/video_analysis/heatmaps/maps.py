"""Mapas de desplazamiento promedio con escala compartida."""
import cv2
import numpy as np


class HeatmapAccumulator:
    def __init__(self):
        self.total = None
        self.count = 0

    def add(self, magnitude):
        if self.total is None:
            self.total = np.zeros_like(magnitude, dtype=np.float64)
        self.total += magnitude
        self.count += 1

    def mean(self):
        if not self.count:
            raise ValueError("No hay fotogramas útiles para el mapa de calor.")
        return (self.total / self.count).astype(np.float32)


def render_pair(original, magnified):
    maximum = max(float(original.max()), float(magnified.max()), 1e-6)
    maps = []
    for values in (original, magnified):
        scaled = np.rint(np.clip(values / maximum, 0, 1) * 255).astype(np.uint8)
        maps.append(cv2.applyColorMap(scaled, cv2.COLORMAP_INFERNO))
    return maps[0], maps[1], maximum
