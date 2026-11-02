"""Gráfico reproducible de movimiento con referencia y eventos señalados."""

import csv

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def save_motion_chart(csv_path, target, frame_count, warmup, baseline, patterns):
    times, original, magnified = [], [], []
    stride = max(1, (frame_count + 1999) // 2000)
    with open(csv_path, encoding="utf-8") as source:
        for index, row in enumerate(csv.DictReader(source)):
            if index % stride == 0:
                times.append(float(row["time_seconds"]))
                original.append(float(row["original_mean_px_frame"]))
                magnified.append(float(row["magnified_mean_px_frame"]))
    figure = Figure(figsize=(10, 4), layout="constrained")
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    axis.plot(times, original, label="Original", color="#2563eb", linewidth=1)
    axis.plot(times, magnified, label="Magnificado", color="#c2410c", linewidth=1)
    axis.axvspan(0, warmup, color="#cbd5e1", alpha=0.5, label="Transitorio excluido")
    if patterns["status"] == "evaluated":
        axis.axvline(baseline, color="#334155", linestyle="--", label="Fin de referencia")
        for index, event in enumerate(patterns["events"]):
            axis.axvspan(
                event["start_seconds"],
                event["end_seconds"],
                color="#dc2626",
                alpha=0.12,
                label="Cambio respecto a referencia" if index == 0 else None,
            )
    axis.set(
        xlabel="Tiempo (s)",
        ylabel="Movimiento medio (px/fotograma)",
        title="Comparación de movimiento — misma resolución y método",
    )
    axis.set_xlim(0, times[-1])
    axis.set_ylim(bottom=0)
    axis.legend(fontsize=8, loc="upper left")
    axis.grid(alpha=0.2)
    figure.savefig(target, dpi=130)
    figure.clear()
    return stride


def save_heatmaps(original, magnified, maximum, directory):
    """Cada PNG conserva identificación, unidades y escala incluso separado del paquete."""
    from pathlib import Path

    directory = Path(directory)
    for filename, matrices, titles in (
        ("mapa_original.png", [original], ["Original"]),
        ("mapa_magnificado.png", [magnified], ["Magnificado"]),
        ("mapas_comparados.png", [original, magnified], ["Original", "Magnificado"]),
    ):
        figure = Figure(figsize=(6 * len(matrices), 4), layout="constrained")
        FigureCanvasAgg(figure)
        axes = figure.subplots(1, len(matrices), squeeze=False)[0]
        for axis, matrix, title in zip(axes, matrices, titles):
            picture = axis.imshow(matrix, cmap="inferno", vmin=0, vmax=maximum)
            axis.set_title(title)
            axis.set_axis_off()
        figure.colorbar(
            picture, ax=list(axes), label="Movimiento medio (px/fotograma)", shrink=0.85
        )
        figure.suptitle("Movimiento — escala común")
        figure.savefig(directory / filename, dpi=130)
        figure.clear()
