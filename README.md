# Proyecto Final — Magnificación y análisis de video

Aplicación local en Python para cargar un video, magnificar variaciones pequeñas,
comparar movimiento, generar mapas y métricas y señalar cambios respecto a una
referencia inicial. Los resultados son apoyo a la inspección y no un diagnóstico de daños.

## Abrir la aplicación

Desde esta carpeta:

```bash
bash run.sh
```

1. Pulsa **Seleccionar video**. Para la demostración usa
   `data/input/referencias/amplitude_change.avi` (20 segundos).
2. Mantén los parámetros iniciales para esa demostración: 0,7–1,5 Hz, amplificación 5,
   referencia de 8 segundos y nivel espacial 1.
3. Describe las condiciones de captura y pulsa **Analizar y guardar resultados**.
4. Revisa los mapas y la pestaña **Métricas en el tiempo**. Abre la carpeta de resultados
   o el video comparativo con los botones de la aplicación.

Los parámetros deben elegirse según el video real. La frecuencia máxima debe ser
menor que FPS/2. La referencia inicial debe representar el comportamiento que quieras
usar como normal; la aplicación no puede comprobar por sí misma esa condición.
El video original no se modifica. Cada ejecución crea una carpeta nueva dentro de
`data/output/`. El análisis puede cancelarse; los resultados incompletos no se publican.

## Uso por consola

Solo comprobar la entrada:

```bash
bash run.sh data/input/referencias/subtle.avi --json
```

Ejecutar el análisis completo:

```bash
bash run.sh data/input/referencias/amplitude_change.avi --analyze --low 0.7 --high 1.5 --alpha 5 --baseline 8 --spatial-level 1 --capture-notes "Escenario sintético controlado" --json
```

Opciones adicionales: `--output carpeta`, `--max-dimension 480`, `--no-patterns`.
La ayuda completa está en `bash run.sh --help`.

## Qué contiene una ejecución

| Archivo | Contenido |
|---|---|
| `original.avi` | Entrada ajustada a la resolución de procesamiento |
| `magnificado.avi` | Resultado de EVM |
| `comparacion.avi` | Original a la izquierda y magnificado a la derecha |
| `mapa_original.png`, `mapa_magnificado.png` | Movimiento promedio con escala común |
| `mapas_comparados.png` | Ambos mapas, en el mismo orden |
| `movimiento.png` | Gráfico temporal, referencia y ventanas con cambios |
| `metricas.csv` | Media, percentil 95, RMS y media en píxeles/segundo por fotograma |
| `movimiento_*.npy` | Matrices numéricas de los mapas |
| `patrones.json` | Tramo de referencia, características, puntuaciones y alertas |
| `informe.json` | Parámetros, versiones, SHA-256 de entrada, resumen, tiempo y límites |
| `LEEME.txt` | Interpretación de los resultados y escala de los mapas |

## Método y límites

- Preprocesamiento: resolución proporcional, dimensiones pares y conservación de FPS.
  Durante el análisis se comprueba la regularidad de las marcas temporales informadas
  por OpenCV. Se rechazan intervalos incompatibles con FPS constantes o timestamps ausentes.
- EVM lineal de una escala gaussiana: reducción espacial, filtro Butterworth pasabanda
  causal de segundo orden de diseño y adición de la variación amplificada en luminancia.
  No es EVM por fase. El factor configurado no equivale a una ganancia geométrica garantizada.
- Movimiento: flujo óptico denso de Farnebäck, exactamente los mismos parámetros en ambos
  videos. Las unidades son píxeles de procesamiento, no milímetros ni vibración física calibrada.
- Se excluyen los primeros `2/frecuencia_mínima` segundos de las métricas agregadas para
  reducir el transitorio. El filtro causal tiene desfase temporal. Los videos conservan
  todos los fotogramas y el CSV marca los incluidos en el resumen.
- Mapas: media temporal de magnitud de flujo; escala común desde cero al máximo de ambos.
- Patrones: ventanas de 0,5 s, con referencia anterior a evaluación. Se requieren al menos
  8 ventanas completas de referencia y una posterior. La alerta usa desviación absoluta
  respecto a mediana/MAD, piso de escala de 0,02 px/fotograma y umbral 6. Isolation Forest
  aporta una puntuación auxiliar; no determina por sí solo la alerta. Las características
  proceden del original para no confundir artefactos de magnificación con anomalías.
- Si la referencia no alcanza, el informe lo indica y no presenta una evaluación de patrones.
  Con la configuración inicial usa videos de al menos 10 s; la demostración tiene 20 s.
- Se informa saturación de píxeles. Ruido, iluminación y movimiento de cámara pueden
  amplificarse o afectar el flujo. No se aplica estabilización automática.
- Los AVI de salida usan MJPEG sin audio; el análisis ocurre antes de comprimirlos.
  El gráfico puede muestrear videos largos; el CSV conserva todas las medidas.
- Se conserva un número acotado de imágenes en memoria; las ventanas estadísticas crecen
  con la duración. El disco debe permitir tres videos de salida, incluido el comparativo.
- La validación completa de lectura no detecta toda corrupción tolerada por el decodificador.
  MP4, AVI, MOV, MKV, M4V y WebM dependen de los códecs disponibles en OpenCV/FFmpeg.

## Reproducir las pruebas

```bash
.venv/bin/python scripts/create_reference_videos.py
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/validate_reference_suite.py
.venv/bin/python -m pip check
```

La suite de referencia incluye escena estática, vibración de 1 Hz, vibración fuera de
banda a 5 Hz, cambio de amplitud a los 13 s e iluminación variable sin movimiento real.
Todos son escenarios simulados, no videos de maquinaria real.

Ver `docs/avance-2026-10-18.md` para el estado contra el plan y
`docs/metodologia-y-pruebas.md` para protocolos, referencias y criterios.

## Entorno y estructura

Python 3.13 en `.python` y `.venv`; versiones exactas en `requirements.txt`.
VS Code usa `.venv`. No requiere nube, servidor, base de datos ni GPU.
Para otra instalación Ubuntu, `bash scripts/complete-setup.sh` instala dependencias
del sistema con contraseña de administrador. Las librerías se reinstalan con
`.venv/bin/python -m pip install -r requirements.txt`.

Los componentes están en `src/video_analysis/`: `video`, `magnification`, `motion`,
`heatmaps`, `anomalies`, `export`, `gui`; `pipeline.py` los integra.
Los videos y ejecuciones locales están excluidos de Git; los generadores, pruebas,
código y documentación quedan versionados.
