"""Preparación reproducible, sin estabilización automática ni interpolación temporal."""

import cv2


def prepare_frame(frame, max_dimension=480):
    h, w = frame.shape[:2]
    scale = min(1.0, max_dimension / max(h, w))
    width, height = max(2, int(w * scale) // 2 * 2), max(2, int(h * scale) // 2 * 2)
    if (width, height) == (w, h):
        return frame.copy()
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
