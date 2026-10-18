# Evidencia de las correcciones — 18 de octubre de 2026

| Archivo | Contenido |
|---|---|
| pruebas.txt | 25 pruebas automáticas de algoritmos, pipeline, archivos e interfaz. |
| interfaz-nativa.txt | Cuatro pruebas GUI con Qt/X11 del escritorio. |
| interfaz-sin-acceso-escritorio.txt | Primer intento sin acceso al display; conservar como contexto, no como prueba aprobada. |
| referencias.json / referencias.txt | Cinco escenarios sintéticos y siete criterios después de las correcciones. |
| instalacion-limpia.txt | Instalación completa de dependencias fijadas en entorno nuevo desde paquetes locales. |
| pruebas-entorno-nuevo.txt | Dos pruebas integradas ejecutadas con ese entorno. |
| entorno.json | Python, sistema y versiones; alcance de la instalación. |
| repetibilidad-sin-red.json / .log | Dos análisis iguales, fallo de publicación y recuperación en espacio de red aislado. |
| mapas_comparados.png / mapa_original.png | Ejemplo de mapas con títulos, escala y unidades; escenario sintético de cambio de amplitud. |
| capturar_interfaz.py / captura.txt | Procedimiento y registro de captura de una ejecución completa desde la ventana. |
| interfaz.png | Captura de la aplicación para revisión visual; modo offscreen. |
| informe.json / patrones.json | Datos del escenario sintético representado. |
| manifiesto.json | Huellas SHA-256 de código, documentación y evidencia de la versión corregida. |

## Reproducción

Desde la raíz del repositorio, usando el entorno instalado:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
QT_QPA_PLATFORM=xcb PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p test_gui.py -v
.venv/bin/python scripts/validate_reference_suite.py --evidence /ruta/nueva/referencias.json
unshare -Urn env PYTHONPATH=src .venv/bin/python docs/auditoria-2026-10-18/comprobar_pipeline.py
```

La prueba Qt/X11 necesita permiso de acceso al escritorio; el aislamiento de red requiere que el sistema permita espacios de usuario/red. Si falla una condición del entorno, registrarla por separado de los resultados del producto. `MPLCONFIGDIR=/tmp/daniel-fixes-mpl` se utilizó como caché escribible de gráficos.

La instalación se verificó con `PROJECT_PYTHON` apuntando al Python 3.13 local, `PROJECT_VENV=/tmp/daniel-install-clean`, `PIP_NO_INDEX=1` y `PIP_FIND_LINKS=/tmp/daniel-wheelhouse`, mediante `bash scripts/complete-setup.sh --skip-system`. Los paquetes de ese repositorio temporal se recuperaron de la caché ya disponible. El entorno y repositorio temporal no forman parte de la entrega; en instalación normal se utiliza el índice de paquetes configurado.

La captura de ventana se utiliza para comprobar la presentación, no como prueba de captura de cámara real. Todos los videos de referencia de esta carpeta siguen siendo sintéticos.

Para una nueva versión, genera un manifiesto en otra ruta con `.venv/bin/python scripts/create_evidence_manifest.py docs/nueva-evidencia/manifiesto.json`. El script rechaza sobrescribir registros existentes.
