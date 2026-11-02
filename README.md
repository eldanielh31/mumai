# Sistema de identificación de daños en maquinaria usando magnificación Euleriana e inteligencia artificial

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
3. Describe las condiciones de captura y pulsa **Validar configuración** y luego **Analizar**.
4. Revisa los mapas, **Métricas en el tiempo**, **Video comparativo** (reproducir/pausar y buscar un instante) y **Resumen numérico**.
5. Pulsa **Exportar resultados…** y elige una carpeta. Después puedes abrirla desde la aplicación.
6. **Volver a En espera** descarta el análisis temporal y permite comenzar otra ejecución.

Los parámetros deben elegirse según el video real. La frecuencia máxima debe ser
menor que FPS/2. La referencia inicial debe representar el comportamiento que quieras
usar como normal; la aplicación no puede comprobar por sí misma esa condición.
El video original no se modifica. En la interfaz los resultados son temporales hasta
que pulsas **Exportar resultados…**; se eliminan al cerrar o reiniciar. Cada exportación
crea una carpeta nueva y no sobrescribe otras. Si falla, puedes revisar el análisis y
reintentar. Al cambiar parámetros se retira la visualización anterior. En consola se
guarda automáticamente en `data/output/` o en `--output`. El análisis puede cancelarse.

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
| `resumen.html` | Resumen local imprimible con métricas, figuras, configuración y límites |
| `exportacion.json` | Huellas SHA-256 y tamaños de los archivos al exportar desde la interfaz |

El resumen HTML funciona sin internet: abre el archivo desde la carpeta exportada y
conserva sus imágenes junto a él. La comparación integrada utiliza un único video con
ambas versiones sincronizadas. En equipos lentos la reproducción puede omitir imágenes
para seguir el reloj; usa pausa y el control de posición para inspeccionar un instante.
Esto no cambia las métricas calculadas. La copia exportada se verifica antes de publicarse.

## Entrega del 19–31 de octubre

La actividad SW-06 está descrita en [el avance del 21 de octubre](docs/avance-2026-10-21-sw06.md).
Hay un [ejemplo sintético completo](docs/sw06-2026-10-21/README.md), una
[guía para tu primer video real](docs/guia-video-real.md) y el
[estado de publicación en GitHub](docs/repositorio.md).

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

## Probarlo tú mismo

Sigue la [guía manual de 15 casos](docs/guia-pruebas-manuales.md) y completa la
[hoja de registro](docs/plantillas/registro-prueba-manual.md). Incluye pasos, valores
esperados, recuperación ante errores y exportación, usando los videos de demostración.

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

La versión verificada utiliza **Python 3.13**, con versiones exactas en `requirements.txt`.
No requiere nube, servidor, base de datos, VS Code ni GPU para ejecutar el análisis.

Para una instalación nueva en Ubuntu:

1. Instala Python 3.13 con su módulo `venv` mediante el mecanismo aprobado para tu
   distribución. El proyecto no añade repositorios externos ni descarga un intérprete
   automáticamente. Comprueba `python3.13 --version`.
2. Desde la carpeta del proyecto ejecuta `bash scripts/complete-setup.sh`. Instala las
   dependencias del sistema (solicita contraseña de administrador), crea `.venv`,
   instala las versiones fijadas y comprueba Python, Qt y los códecs.
3. Ejecuta `bash run.sh`.

Si Python 3.13 está en otra ruta:

```bash
PROJECT_PYTHON=/ruta/a/python3.13 bash scripts/complete-setup.sh
```

Si los paquetes del sistema ya están instalados, usa `--skip-system`. Para comprobar
una instalación aislada sin reemplazar `.venv`, define `PROJECT_VENV=/ruta/nueva`.
La instalación de paquetes requiere conexión o un repositorio local de paquetes;
el funcionamiento posterior del análisis no requiere internet. El script no descarga
videos de demostración: puedes generarlos con `.venv/bin/python scripts/create_reference_videos.py`.
La comparación dispone de reproductor integrado; la apertura externa es opcional.

`informe.json` registra el tiempo desde la validación hasta la publicación del análisis,
incluyendo los archivos de resultados. Solo excluye la escritura de su propia medición
y, en la interfaz, la exportación manual posterior (copia del paquete ya analizado).

La documentación de seguimiento se encuentra en **[docs/README.md](docs/README.md)**:
incidencias, decisiones, pruebas, pendientes y plantillas para futuros informes.

Los componentes están en `src/video_analysis/`: `video`, `magnification`, `motion`,
`heatmaps`, `anomalies`, `export`, `gui`; `pipeline.py` los integra.
Los videos y ejecuciones locales están excluidos de Git; los generadores, pruebas,
código y documentación quedan versionados.

## Documentos y revisión del código

- [Documentos académicos aportados por Daniel](Proyecto/README.md).
- [Revisión y limpieza del 1 de noviembre](docs/revision-2026-11-01/README.md).
- [Prueba con el motor del automóvil](docs/motor-2026-11-01/README.md).

Para mantener el estilo, instala Ruff 0.14.3 en un entorno de desarrollo y ejecuta
`ruff check src scripts tests` y `ruff format --check src scripts tests`.
La configuración está en `ruff.toml`; Ruff no es una dependencia para usar la aplicación.
