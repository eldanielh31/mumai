"""Flujo local reproducible y cancelable con publicación atómica de resultados."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import importlib.metadata
import json
import math
import os
import shutil
import tempfile
import time
import uuid

import cv2
import numpy as np

from video_analysis.video import inspect_video, iter_frames, ValidationCancelled
from video_analysis.video.preprocess import prepare_frame
from video_analysis.magnification.eulerian import EulerianMagnifier
from video_analysis.motion.optical_flow import MotionAnalyzer, metrics
from video_analysis.heatmaps.maps import HeatmapAccumulator, render_pair
from video_analysis.anomalies.patterns import detect_patterns
from video_analysis.export.charts import save_motion_chart


@dataclass(frozen=True)
class AnalysisConfig:
    low_hz: float = 0.7
    high_hz: float = 1.5
    alpha: float = 5.0
    spatial_level: int = 1
    max_dimension: int = 480
    baseline_seconds: float = 8.0
    patterns_enabled: bool = True
    capture_notes: str = "Condiciones de captura no documentadas por el usuario."

    def validate(self, fps):
        EulerianMagnifier(fps, self.low_hz, self.high_hz, self.alpha, self.spatial_level)
        if not isinstance(self.max_dimension, int) or not 64 <= self.max_dimension <= 1280:
            raise ValueError("La dimensión máxima debe estar entre 64 y 1280 píxeles.")
        if not math.isfinite(self.baseline_seconds) or self.baseline_seconds <= 0:
            raise ValueError("La duración de referencia debe ser positiva y finita.")


def _digest(path, cancelled):
    sha = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            if cancelled():
                raise ValidationCancelled("Análisis cancelado.")
            sha.update(block)
    return sha.hexdigest()


def analyze_video(path, output_root, config=None, cancelled=lambda: False, progress=lambda p: None):
    config = config or AnalysisConfig()
    started = time.perf_counter()
    info, first = inspect_video(path, cancelled=cancelled)
    config.validate(info.fps)
    warmup = 2 / config.low_hz
    warmup_frames = math.ceil(warmup * info.fps)
    if info.frame_count <= warmup_frames + max(2, math.ceil(info.fps * 0.5)):
        raise ValueError(f"Video demasiado corto: usa más de {warmup + 0.5:.1f} segundos para esta frecuencia mínima.")
    identity = info.path.stat()
    source_hash = _digest(info.path, cancelled)
    first = prepare_frame(first, config.max_dimension)
    h, w = first.shape[:2]
    root = Path(output_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".processing-", dir=root))
    final = root / ("analisis-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:8])
    writers = []
    frames = None
    try:
        for name, size in [("original.avi", (w, h)), ("magnificado.avi", (w, h)),
                           ("comparacion.avi", (2 * w, h))]:
            writer = cv2.VideoWriter(str(staging / name), cv2.VideoWriter_fourcc(*"MJPG"), info.fps, size)
            writers.append(writer)
            if not writer.isOpened():
                raise ValueError("No se pudo crear el video de salida con MJPEG.")
        evm = EulerianMagnifier(info.fps, config.low_hz, config.high_hz, config.alpha, config.spatial_level)
        analyzers = [MotionAnalyzer(), MotionAnalyzer()]
        accumulators = [HeatmapAccumulator(), HeatmapAccumulator()]
        sums = [{"mean_px_frame": 0., "p95_px_frame": 0., "rms_px_frame": 0., "mean_px_second": 0.} for _ in range(2)]
        windows, bucket, bucket_id = [], [], None
        fields = ["frame", "time_seconds", "included"] + [f"{tag}_{key}" for tag in ("original", "magnified") for key in sums[0]]
        frames = iter_frames(info, require_constant_fps=True)

        def flush_window():
            if not bucket:
                return
            # Solo ventanas completas de al menos 0.4 s después del transitorio.
            if len(bucket) < math.ceil(info.fps * 0.4):
                return
            windows.append({
                "start_seconds": bucket[0][0], "end_seconds": bucket[-1][0] + 1 / info.fps,
                "original_rms": float(np.mean([r[1]["rms_px_frame"] for r in bucket])),
                "original_p95": float(np.mean([r[1]["p95_px_frame"] for r in bucket])),
            })

        with (staging / "metricas.csv").open("w", newline="", encoding="utf-8") as output:
            csv_writer = csv.DictWriter(output, fieldnames=fields)
            csv_writer.writeheader()
            useful = 0
            for index, frame in enumerate(frames):
                if cancelled():
                    raise ValidationCancelled("Análisis cancelado. No se publicaron resultados incompletos.")
                original = prepare_frame(frame, config.max_dimension)
                amplified = evm.process(original)
                pair = np.hstack((original, amplified))
                cv2.putText(pair, "Original", (8, 18), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 255), 1)
                cv2.putText(pair, "Magnificado", (w + 8, 18), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 255), 1)
                for writer, image in zip(writers, (original, amplified, pair)):
                    writer.write(image)
                magnitudes = [analyzer.process(image) for analyzer, image in zip(analyzers, (original, amplified))]
                included = index >= warmup_frames and index > 0
                row = {"frame": index, "time_seconds": index / info.fps, "included": int(included)}
                measured = []
                for tag, magnitude, accumulator, total in zip(("original", "magnified"), magnitudes, accumulators, sums):
                    values = metrics(magnitude, info.fps) if magnitude is not None else {key: 0. for key in total}
                    measured.append(values)
                    row.update({f"{tag}_{key}": value for key, value in values.items()})
                    if included:
                        accumulator.add(magnitude)
                        for key in total:
                            total[key] += values[key]
                if included:
                    useful += 1
                    new_id = int((index / info.fps) / .5)
                    if bucket_id is not None and bucket_id != new_id:
                        flush_window()
                        bucket = []
                    bucket_id = new_id
                    bucket.append((index / info.fps, measured[0]))
                csv_writer.writerow(row)
                if index % max(1, round(info.fps)) == 0:
                    progress(int(100 * (index + 1) / info.frame_count))
            flush_window()
        for writer in writers:
            writer.release()
        writers = []
        current = info.path.stat()
        if (identity.st_size, identity.st_mtime_ns) != (current.st_size, current.st_mtime_ns):
            raise ValueError("El archivo de entrada cambió durante el procesamiento.")
        # Verificar que los archivos de video realmente pueden decodificarse.
        for name in ("original.avi", "magnificado.avi", "comparacion.avi"):
            exported, _ = inspect_video(staging / name, cancelled=cancelled)
            if exported.frame_count != info.frame_count:
                raise ValueError("La exportación de video quedó incompleta.")
        values = [acc.mean() for acc in accumulators]
        images = render_pair(*values)
        for tag, matrix, heatmap in zip(("original", "magnificado"), values, images[:2]):
            np.save(staging / f"movimiento_{tag}.npy", matrix)
            if not cv2.imwrite(str(staging / f"mapa_{tag}.png"), heatmap):
                raise OSError("No se pudo guardar el mapa de calor.")
        map_pair = np.hstack(images[:2])
        if not cv2.imwrite(str(staging / "mapas_comparados.png"), map_pair):
            raise OSError("No se pudo guardar la comparación de mapas.")
        patterns = detect_patterns(windows, config.baseline_seconds, config.patterns_enabled)
        chart_stride = save_motion_chart(staging / "metricas.csv", staging / "movimiento.png",
                                         info.frame_count, warmup, config.baseline_seconds, patterns)
        (staging / "patrones.json").write_text(json.dumps(patterns, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
        summary = [{key: value / useful for key, value in total.items()} for total in sums]
        warnings = [
            "Los indicadores apoyan la inspección; no certifican daños ni seguridad mecánica.",
            "Flujo expresado en píxeles de procesamiento; no equivale a desplazamiento físico sin calibración.",
            "EVM lineal de una escala gaussiana: puede amplificar iluminación, ruido y movimiento de cámara.",
            "Filtro causal: tiene desfase y transitorio; las métricas excluyen los primeros 2/frecuencia_mínima segundos.",
            "Los videos de salida son MJPEG sin audio; las métricas se calculan antes de su compresión.",
        ]
        if patterns["status"] == "insufficient_reference":
            warnings.append(patterns["message"])
        clipping = evm.clipped_pixels / evm.total_pixels
        if clipping > .01:
            warnings.append("Más del 1 % de los píxeles se saturaron; reduce la amplificación.")
        report = {
            "schema_version": 1, "created_utc": datetime.now(timezone.utc).isoformat(),
            "input": info.as_dict(), "input_sha256": source_hash, "config": asdict(config),
            "processing_size": [w, h], "warmup_seconds": warmup, "analyzed_frame_pairs": useful,
            "original": summary[0], "magnified": summary[1],
            "mean_motion_ratio": summary[1]["mean_px_frame"] / summary[0]["mean_px_frame"] if summary[0]["mean_px_frame"] > 1e-6 else None,
            "heatmap_scale": {"min": 0, "max": images[2], "unit": "px/frame", "colormap": "inferno", "shared": True},
            "clipped_pixel_fraction": clipping, "patterns_status": patterns["status"],
            "chart_sample_stride": chart_stride,
            "flagged_windows": len(patterns["events"]), "elapsed_seconds": time.perf_counter() - started,
            "versions": {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "opencv-python", "scikit-learn")},
            "warnings": warnings,
        }
        (staging / "informe.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
        (staging / "LEEME.txt").write_text(
            "RESULTADOS DEL ANÁLISIS\n\nComparación: original a la izquierda, magnificado a la derecha.\n"
            f"Mapas: misma escala de 0 a {images[2]:.6f} px/fotograma; negro = menor y amarillo = mayor movimiento.\n"
            "metricas.csv: valores por fotograma; included=1 indica datos usados en el resumen.\n"
            "movimiento.png: comparación temporal; los intervalos rojos son cambios respecto a referencia.\n"
            "informe.json: parámetros, huella del video, versiones, resumen y advertencias.\n"
            "patrones.json: referencia, intervalos evaluados y alertas de cambios.\n\n" + "\n".join(warnings), encoding="utf-8")
        if cancelled():
            raise ValidationCancelled("Análisis cancelado.")
        os.rename(staging, final)
        progress(100)
        return final
    except BaseException:
        for writer in writers:
            writer.release()
        shutil.rmtree(staging, ignore_errors=True)
        raise
    finally:
        if frames is not None:
            frames.close()
