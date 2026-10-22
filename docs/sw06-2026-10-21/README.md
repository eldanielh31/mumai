# Evidencia de ACT-SW-06 al 21 de octubre de 2026

Datos utilizados: simulación de cambio de amplitud a partir del segundo 13, 20 segundos, 20 FPS, 160 × 120, cámara fija e iluminación constante. No es captura de maquinaria real. Los videos de ejemplo son generados por el proyecto y se incluyen únicamente como demostración técnica.

| Archivo | Contenido |
|---|---|
| pruebas.txt | Suite completa: 31 pruebas aprobadas. |
| interfaz-nativa.txt | Seis pruebas de SW-06 con Qt/X11 del escritorio. |
| flujo.json / flujo.txt | Nueve criterios de carga, análisis, revisión, exportación y reinicio. |
| comparacion-interfaz.png | Comparación integrada detenida en el segundo 14. |
| metricas-interfaz.png | Cuatro indicadores comparados con sus unidades. |
| resumen-navegador.png | Inspección visual de la página exportada completa. |
| ejemplo/ | Paquete completo exportado, incluidos videos sintéticos pequeños, mapas, CSV, JSON y resumen HTML. |
| manifiesto.json | Huellas de los archivos de esta versión y sus evidencias. |

Para revisar la demostración abre `ejemplo/resumen.html` en el navegador o `ejemplo/comparacion.avi` en un reproductor. Conserva la carpeta completa para que funcionen las imágenes y enlaces.

## Reproducir

Desde la raíz del repositorio:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
QT_QPA_PLATFORM=xcb PYTHONPATH=src:tests .venv/bin/python -m unittest test_sw06 -v
QT_QPA_PLATFORM=offscreen .venv/bin/python scripts/validate_sw06.py --evidence docs/nueva-evidencia-sw06
```

La segunda orden requiere acceso al escritorio. Se utilizó `MPLCONFIGDIR=/tmp/daniel-sw06-mpl` para una caché escribible. El generador rechaza sobrescribir un ejemplo/registro existente. Las pruebas de error/copia corrupta son provocadas de forma controlada; no representan daños a archivos reales del usuario.

Los sellos UTC de los archivos pueden indicar el 22 de octubre; el corte de esta sesión en Costa Rica es el 21 de octubre. Las fechas del plan se conservan con el calendario del usuario.
