"""Resumen local legible para revisión y anexos; datos de usuario escapados."""

from html import escape
from pathlib import Path


def save_summary(report, target):
    def safe(value):
        return escape(str(value), quote=True)

    labels = {
        "mean_px_frame": "Media (px/fotograma)",
        "p95_px_frame": "Percentil 95 medio (px/fotograma)",
        "rms_px_frame": "RMS medio (px/fotograma)",
        "mean_px_second": "Media (px/s)",
    }
    rows = "".join(
        f"<tr><th>{label}</th><td>{report['original'][key]:.6g}</td><td>{report['magnified'][key]:.6g}</td></tr>"
        for key, label in labels.items()
    )
    config = "".join(
        f"<tr><th>{safe(key)}</th><td>{safe(value)}</td></tr>"
        for key, value in report["config"].items()
    )
    warnings = "".join(f"<li>{safe(value)}</li>" for value in report["warnings"])
    pattern = {
        "evaluated": f"{report['flagged_windows']} ventanas con cambios respecto a la referencia.",
        "disabled": "Análisis de patrones desactivado.",
        "insufficient_reference": "Referencia insuficiente: no se evaluaron patrones.",
    }[report["patterns_status"]]
    document = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'unsafe-inline'">
<title>Resumen del análisis de video</title><style>
body{{font:16px/1.6 system-ui,sans-serif;max-width:1050px;margin:32px auto;padding:0 20px;color:#172536;background:#fff}}
h1,h2{{color:#164e63}}table{{border-collapse:collapse;width:100%;margin:18px 0}}td,th{{border:1px solid #bdcbd2;padding:9px;text-align:left;overflow-wrap:anywhere}}
th{{background:#edf5f8}}img{{max-width:100%;height:auto}}.notice{{padding:16px;background:#fff6dd;border-left:5px solid #ad7400}}code{{overflow-wrap:anywhere}}
@media print{{body{{margin:0;font-size:11pt}}h2{{break-after:avoid}}tr,img{{break-inside:avoid}}}}
</style></head><body>
<h1>Comparación de movimiento</h1><p class="notice">Información de apoyo a la inspección; no constituye un diagnóstico de daños.</p>
<p><strong>Entrada:</strong> {safe(Path(report["input"]["path"]).name)}<br><strong>Creación (UTC):</strong> {safe(report["created_utc"])}<br>
<strong>Identidad SHA-256:</strong> <code>{safe(report["input_sha256"])}</code></p>
<h2>Resultados comparables</h2><p>Resolución de procesamiento: {safe(report["processing_size"])}. Se aplicó el mismo método de movimiento a ambas versiones.</p>
<table><thead><tr><th>Indicador</th><th>Original</th><th>Magnificado</th></tr></thead><tbody>{rows}</tbody></table>
<p>{safe(pattern)} Las ventanas señaladas no equivalen a daños independientes.</p>
<h2>Mapas de movimiento</h2><img src="mapas_comparados.png" alt="Mapas original y magnificado con escala común en píxeles por fotograma">
<h2>Evolución temporal</h2><img src="movimiento.png" alt="Comparación temporal y ventanas señaladas">
<h2>Configuración utilizada</h2><table>{config}</table>
<h2>Interpretación y límites</h2><ul>{warnings}</ul>
<h2>Archivos de respaldo</h2><p>Consulta <a href="informe.json">informe.json</a> para duración y alcance del reloj, versiones y valores completos;
<a href="metricas.csv">metricas.csv</a> para cada fotograma; <a href="patrones.json">patrones.json</a> para intervalos y puntuaciones.
Abre <a href="comparacion.avi">comparacion.avi</a> en el reproductor de escritorio para ver ambos videos sincronizados.</p>
<p>Conserva esta página junto con los demás archivos de la carpeta. Funciona sin internet y puede imprimirse desde el navegador.</p>
</body></html>"""
    Path(target).write_text(document, encoding="utf-8")
