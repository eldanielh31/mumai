"""Carga local y lectura secuencial de videos sin acumularlos en memoria."""

import math
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


class VideoError(ValueError):
    """El archivo no se puede utilizar como entrada del análisis."""


class ValidationCancelled(VideoError):
    """La persona canceló la validación."""


@dataclass(frozen=True)
class VideoInfo:
    path: Path
    fps: float
    width: int
    height: int
    frame_count: int

    @property
    def duration_seconds(self) -> float:
        """Duración estimada; presupone una tasa de fotogramas constante."""
        return self.frame_count / self.fps

    def as_dict(self) -> dict:
        return {
            "path": str(self.path),
            "fps": self.fps,
            "width": self.width,
            "height": self.height,
            "frame_count": self.frame_count,
            "duration_seconds": self.duration_seconds,
        }


def _open(path: str | Path):
    file = Path(path).expanduser().resolve()
    if not file.exists():
        raise VideoError(f"El archivo no existe: {file}")
    if not file.is_file():
        raise VideoError("Selecciona un archivo de video, no una carpeta.")
    if file.suffix.lower() not in {".mp4", ".avi", ".mov", ".mkv", ".m4v", ".webm"}:
        raise VideoError("Formato no admitido. Usa MP4, AVI, MOV, MKV, M4V o WebM.")
    try:
        with file.open("rb") as source:
            header = source.read(256)
            if not header:
                raise VideoError("El archivo está vacío.")
            if header.startswith(b"version https://git-lfs.github.com/spec/v1"):
                raise VideoError(
                    "El video está pendiente de descarga con Git LFS. "
                    "Consulta la sección Git LFS del README para descargarlo."
                )
    except OSError as exc:
        raise VideoError(f"No se puede acceder al archivo: {exc}") from exc
    capture = cv2.VideoCapture(str(file), cv2.CAP_FFMPEG)
    if not capture.isOpened():
        capture.release()
        raise VideoError(
            "No se pudo abrir el video. Puede estar dañado o usar un códec no compatible."
        )
    return file, capture


def inspect_video(
    path: str | Path,
    cancelled: Callable[[], bool] = lambda: False,
) -> tuple[VideoInfo, np.ndarray]:
    """Decodifica el video completo; conserva únicamente el primer fotograma BGR.

    OpenCV no distingue siempre fin de archivo de error de decodificación.
    Si el contenedor declara más fotogramas que los leídos, se rechaza la entrada.
    Esto no garantiza detectar toda corrupción tolerada por el decodificador.
    """
    file, capture = _open(path)
    try:
        fps = capture.get(cv2.CAP_PROP_FPS)
        if not math.isfinite(fps) or fps <= 0:
            raise VideoError("El video no informa una tasa de fotogramas (FPS) válida.")
        declared = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        count, first = 0, None
        while True:
            if cancelled():
                raise ValidationCancelled("Validación cancelada.")
            ok, frame = capture.read()
            if not ok:
                break
            if frame is None or frame.size == 0:
                raise VideoError("Se encontró un fotograma vacío.")
            if first is None:
                first = frame.copy()
            elif frame.shape != first.shape:
                raise VideoError(
                    "La resolución cambia durante el video. Usa una resolución constante."
                )
            count += 1
        if first is None:
            raise VideoError("El archivo no contiene fotogramas que se puedan leer.")
        if math.isfinite(declared) and declared > 0 and count < round(declared):
            raise VideoError(
                f"Lectura incompleta: se leyeron {count} de {round(declared)} fotogramas declarados."
            )
        height, width = first.shape[:2]
        return VideoInfo(file, fps, width, height, count), first
    except cv2.error as exc:
        raise VideoError("Ocurrió un error al decodificar el video.") from exc
    finally:
        capture.release()


def iter_frames(info: VideoInfo, require_constant_fps=False) -> Iterator[np.ndarray]:
    """Entrega fotogramas BGR en orden para los siguientes módulos.

    Consumir hasta el final verifica el conteo. Si se interrumpe la iteración,
    cerrar el generador con close() para liberar el archivo inmediatamente.
    """
    _, capture = _open(info.path)
    count = 0
    previous_time = None
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if frame is None or frame.shape[:2] != (info.height, info.width):
                raise VideoError("Los fotogramas no coinciden con el video validado.")
            count += 1
            if require_constant_fps:
                timestamp = capture.get(cv2.CAP_PROP_POS_MSEC) / 1000
                if not math.isfinite(timestamp):
                    raise VideoError("No se pudo verificar la temporización del video.")
                if previous_time is not None and abs(
                    timestamp - previous_time - 1 / info.fps
                ) > max(0.002, 0.15 / info.fps):
                    raise VideoError(
                        "Tasa de fotogramas variable o marcas temporales no disponibles. Convierte el video a FPS constantes antes del análisis."
                    )
                previous_time = timestamp
            if count > info.frame_count:
                raise VideoError("El video cambió después de la validación.")
            yield frame
        if count != info.frame_count:
            raise VideoError("Lectura incompleta o video modificado después de la validación.")
    except cv2.error as exc:
        raise VideoError("Ocurrió un error al leer los fotogramas.") from exc
    finally:
        capture.release()
