# Sistema de identificación de daños en maquinaria usando magnificación Euleriana e inteligencia artificial

Prototipo académico local para **hacer visibles y medir movimientos sutiles en videos**
de maquinaria o estructuras. Carga un archivo, genera una versión magnificada,
compara el movimiento de ambas y permite guardar evidencia visual y numérica.
Los resultados apoyan una inspección: una región brillante o una alerta no demuestra
por sí sola que exista un daño.

## Alcance del proyecto

El [Plan de Proyecto](Proyecto/Plan/Plan_de_Proyecto_Daniel_Brenes.pdf), los
[requisitos](Proyecto/Requerimientos/Proyecto_Requer.pdf) y el
[diseño](Proyecto/Diseño/Documento_de_Diseno_CE1114_Daniel_Brenes_v2.pdf)
definen estas capacidades:

| Capacidad prevista | Qué hace la versión implementada |
|---|---|
| Cargar y preparar videos locales | Comprueba lectura, informa FPS/resolución/duración y reduce el tamaño de manera proporcional. |
| Magnificación Euleriana de Video (EVM) | Amplifica variaciones temporales dentro de una banda configurable. |
| Medición comparable | Aplica el mismo flujo óptico al original y al magnificado, con igual resolución y FPS. |
| Mapas y métricas | Representa dónde y cuánto movimiento se midió; incluye evolución temporal. |
| Patrones opcionales | Señala diferencias respecto a un tramo inicial de referencia. |
| Consulta y exportación | Permite revisar ambos videos, mapas y métricas antes de guardar resultados y configuración. |

La solución es modular, funciona en Linux/Python y ejecuta su análisis localmente,
sin conexión a internet ni GPU obligatorias. La entrada son **archivos ya grabados**;
la aplicación no controla la cámara ni la maquinaria. El diseño no incluye servicio
en nube, monitoreo industrial en vivo, diagnóstico certificado, medición física en
milímetros o un clasificador entrenado para nombrar tipos de avería.

El diseño seleccionado es **híbrido**: procesamiento clásico interpretable y análisis
de patrones opcional. Esta versión utiliza un criterio estadístico robusto y un
indicador auxiliar de Isolation Forest. TensorFlow/PyTorch aparecen en las fuentes
como alternativas condicionales; no son dependencias obligatorias del diseño elegido.
No hay entrenamiento supervisado con etiquetas de daños reales.

La [revisión de alcance del 2 de noviembre](docs/alcance-2026-11-02/README.md)
relaciona cada capacidad con sus fuentes y distingue documentos vigentes e históricos.

## Cómo funciona

1. **Valida la entrada.** Lee todos los fotogramas y obtiene metadatos. Al analizar,
   exige una temporización compatible con FPS constantes.
2. **Prepara dos ramas comparables.** Reduce la imagen si corresponde, sin aumentar
   su resolución; una rama conserva el contenido original y la otra recibe EVM.
3. **Aplica EVM.** Filtra variaciones de luminancia en la banda elegida y suma una
   versión amplificada. El parámetro de amplificación no garantiza ese mismo aumento
   geométrico del movimiento.
4. **Mide movimiento.** El flujo óptico estima desplazamientos entre imágenes
   consecutivas en ambas ramas. Con ellos calcula métricas y mapas promedio.
5. **Evalúa patrones, si se habilitan.** Aprende una referencia de las métricas del
   original al comienzo del video y señala ventanas posteriores que se apartan de ella.
6. **Muestra resultados.** Presenta mapas, gráfico temporal, comparación sincronizada
   y una tabla numérica. Los resultados de la interfaz siguen siendo temporales.
7. **Exporta cuando lo pides.** Crea una carpeta nueva, verifica las copias y conserva
   parámetros, identidad de la entrada y versiones. No sobrescribe exportaciones previas.

Los estados de la interfaz son **En espera → Entrada válida → Configurado →
Procesando → Resultados disponibles**, con **Error controlado** cuando no puede
continuar. Después de un error permite volver a En espera e iniciar otra ejecución.

## Preparar y abrir en Ubuntu o WSL

Desde la carpeta del proyecto, por ejemplo en esta computadora:

```bash
cd ~/mumai
bash run.sh
```

`bash run.sh` no requiere cambiar el permiso ejecutable del archivo. Si falta `.venv`,
prepara el entorno antes de abrir la aplicación. La versión evaluada usa **Python
3.13** y versiones exactas de dependencias en [requirements.txt](requirements.txt).
No requiere servidor, base de datos, VS Code ni GPU para procesar.

### Instalación del entorno

1. Instala Python 3.13 con soporte para entornos virtuales mediante el mecanismo
   que hayas elegido para tu equipo. El proyecto no descarga un intérprete ni añade
   repositorios del sistema automáticamente.
2. Desde el proyecto, ejecuta:

```bash
bash scripts/complete-setup.sh
```

El script comprueba Python antes de modificar paquetes; instala bibliotecas del
sistema con sudo, crea `.venv`, instala las versiones fijadas y verifica el entorno.
La preparación puede requerir internet; el análisis posterior no lo necesita.

Si el intérprete está en otra ubicación:

```bash
PROJECT_PYTHON=/ruta/a/python3.13 bash scripts/complete-setup.sh
```

Si ya instalaste Python mediante uv, puedes utilizar su ruta sin cambiar el Python
principal de Ubuntu:

```bash
PROJECT_PYTHON="$("$HOME/.local/bin/uv" python find 3.13)" bash scripts/complete-setup.sh
```

uv es una herramienta externa opcional; su documentación está en
[Instalar Python con uv](https://docs.astral.sh/uv/guides/install-python/).
Si las bibliotecas del sistema ya están instaladas, añade `--skip-system`.
`PROJECT_VENV=/ruta/nueva` permite preparar otro entorno sin reemplazar `.venv`;
`run.sh` utiliza siempre el entorno `.venv` del proyecto.

### Descargar los videos con Git LFS

Los videos de `data/input/` utilizan Git LFS. Después de clonar, antes de reemplazar
entradas por archivos propios:

```bash
sudo apt-get install -y git-lfs
git lfs install --local
git lfs pull
```

Un AVI o MP4 de unos 130 bytes que empieza con
`version https://git-lfs.github.com/spec/v1` es un **puntero pendiente de descarga**,
no un video reproducible. La aplicación informa esta condición. Los generadores
conservan archivos existentes; ejecutarlos sobre un puntero no descarga el video.

Si ya repusiste `motor.mp4`, consérvalo y exclúyelo al descargar el resto:

```bash
git lfs pull --exclude="data/input/motor.mp4"
```

Haz una copia de tus entradas propias antes de operaciones de recuperación.
Las entradas actuales están en un repositorio público por autorización de Daniel,
incluidos los videos del motor. `data/output/` permanece fuera del versionado.

## Primera prueba en la interfaz

1. Pulsa **Seleccionar video** y abre
   `data/input/referencias/amplitude_change.avi`, una simulación de 20 segundos.
2. Usa la columna «Referencia sintética» de la tabla siguiente.
3. Describe las condiciones de captura y pulsa **Validar configuración**.
4. Pulsa **Analizar** y espera a **Resultados disponibles**.
5. Revisa las cuatro pestañas. En el comparativo, original está a la izquierda y
   magnificado a la derecha; puedes reproducir, pausar y buscar un instante.
6. Pulsa **Exportar resultados…** y elige una carpeta permanente, por ejemplo
   `data/output/mis-pruebas`. Espera **Exportación completada**.
7. Usa **Abrir carpeta de resultados** y abre `resumen.html` para comenzar la revisión.

| Parámetro | Referencia sintética | Motor normalizado a 30 FPS |
|---|---:|---:|
| Archivo | `referencias/amplitude_change.avi` | `motor_30fps.avi` |
| Frecuencia mínima | 0,7 Hz | 0,7 Hz |
| Frecuencia máxima | 1,5 Hz | 1,5 Hz |
| Amplificación | 5 | 2 |
| Referencia inicial | 8 s | 10 s |
| Dimensión máxima | 160 px | 480 px |
| Reducción espacial | 1 | 1 |
| Detectar cambios | Activado | Activado |

Los archivos de la tabla están dentro de `data/input/`. Las dimensiones de la
referencia se eligen explícitamente en 160 px para repetir sus cifras documentadas;
el valor inicial de la interfaz es 480 px.

Para la simulación escribe: «Escenario sintético; cámara fija simulada; cambio de
amplitud desde el segundo 13». Para el motor puedes registrar: «Motor de automóvil,
grabado con teléfono y soporte independiente, luz de día; copia normalizada a 30 FPS;
exposición, RPM e intervalos de aceleración no confirmados; banda exploratoria».
Esto incorpora los datos que Daniel confirmó, sin modificar reportes anteriores.

La prueba del motor utiliza una copia a FPS constantes: 1644 fotogramas, 54,8 s.
El MP4 del teléfono presenta un salto temporal inicial que el análisis rechaza;
la copia normalizada puede duplicar o descartar imágenes y no recupera información
que no fue capturada. El original se conserva. La banda 0,7–1,5 Hz sirve aquí para
explorar movimiento lento, no se ha identificado como frecuencia mecánica del motor.
Cambiar las notas produce una configuración documental distinta aunque no altere
los algoritmos; para repetir exactamente una ejecución conserva su configuración.

### Cómo elegir parámetros para otro video

- **Banda de frecuencia:** debe cumplir `0 < mínima < máxima < FPS/2`. Con 30 FPS,
  la máxima debe ser estrictamente menor de 15 Hz. La cámara puede ocultar o representar
  incorrectamente movimiento más rápido; el programa no estima RPM automáticamente.
- **Amplificación:** se admite 0–30. Cero permite comprobar la igualdad de las ramas.
  Si aparecen recortes de brillo o artefactos, reduce el valor; alpha 2 no significa
  necesariamente que la vibración medida se duplique.
- **Referencia inicial:** es el final, medido desde el comienzo del video, del tramo
  que usarás para comparar. El programa no puede certificar que represente un estado sano.
- **Dimensión máxima:** se admite 64–1280 px. Una reducción cambia las unidades de
  píxel utilizadas; no compares valores de distintas resoluciones como si fueran equivalentes.
- **Reducción espacial:** se admite 0–4. Controla la escala espacial de EVM y debe
  mantenerse igual cuando quieras repetir una comparación.
- **Patrones:** pueden desactivarse; las métricas y mapas siguen disponibles.

El filtro tiene un transitorio: se excluyen de los agregados los primeros
`2 / frecuencia_mínima` segundos, aproximadamente 2,86 s con mínima 0,7 Hz.
Los patrones necesitan ocho ventanas completas útiles de referencia y al menos una
posterior. Un video puede servir para medir movimiento y aun así tener referencia
insuficiente para patrones. Con la configuración inicial usa al menos 10 s; los
videos de referencia de 20 s tienen margen suficiente.

### Conservar resultados y recuperarse de errores

En la interfaz, **cerrar o volver a En espera elimina los análisis sin exportar**.
Cambiar un parámetro retira las vistas anteriores; exporta antes si quieres conservarlas.
Una exportación completada permanece en disco después de reiniciar.
Si falla la copia, el análisis sigue disponible para reintentar. El botón Cancelar
permite interrumpir operaciones; una cancelación no debe presentarse como éxito ni
dejar un paquete parcial publicado.

## Archivos exportados y para qué sirven

Conserva la carpeta completa. No hace falta usar todos los formatos para revisar una
prueba: comienza por `resumen.html`, el comparativo y las figuras; consulta CSV/JSON
cuando necesites respaldar cifras o reproducir el procedimiento.

| Archivo | Contenido y uso |
|---|---|
| `resumen.html` | Resumen local imprimible con métricas, imágenes, configuración y advertencias. Mantén sus imágenes junto a él. |
| `original.avi` | Copia de la entrada a resolución de procesamiento, recodificada a MJPEG y sin audio. No reemplaza el archivo original de cámara. |
| `magnificado.avi` | Versión EVM a la misma resolución y FPS, también MJPEG sin audio. |
| `comparacion.avi` | Ambas ramas sincronizadas en una imagen: original a la izquierda y magnificado a la derecha. |
| `mapa_original.png`, `mapa_magnificado.png` | Figuras individuales con título, escala y unidades. |
| `mapas_comparados.png` | Los dos mapas con una escala común dentro de esa ejecución. |
| `movimiento.png` | Evolución de la media de movimiento, transitorio, referencia y ventanas señaladas cuando se evaluaron patrones. |
| `metricas.csv` | Mediciones por fotograma para hojas de cálculo o análisis adicional. |
| `movimiento_original.npy`, `movimiento_magnificado.npy` | Matrices numéricas de los mapas promedio, sin colores ni leyendas. Para análisis con NumPy. |
| `patrones.json` | Estado de la evaluación, referencia, ventanas, puntuaciones y eventos. |
| `informe.json` | Entrada, SHA-256, configuración, versiones, resumen numérico, tiempo y límites del análisis. |
| `LEEME.txt` | Guía breve de lectura del paquete. |
| `exportacion.json` | Recibo de tamaños y SHA-256 de los archivos copiados mediante exportación explícita. |

El análisis calcula sus métricas **antes de comprimir los AVI de salida**. Recalcular
el flujo desde esos AVI MJPEG puede dar diferencias por compresión. La reproducción
integrada puede saltar imágenes para seguir el reloj en un equipo lento; eso no cambia
las métricas calculadas. Para inspeccionar un instante, pausa y utiliza la barra.

### Leer los mapas y el gráfico

Los mapas representan **magnitud media de movimiento**, después del transitorio.
Negro significa menor magnitud y amarillo mayor magnitud según la barra, en píxeles
por fotograma. Un color brillante localiza actividad, sin identificar su causa.
Original y magnificado comparten escala en cada ejecución; ejecuciones distintas
pueden tener máximos diferentes. Para compararlas usa valores numéricos y condiciones
equivalentes, no solo el color.

En `movimiento.png`, el eje horizontal muestra segundos y el vertical movimiento
medio en px/fotograma. Las dos líneas corresponden a original y magnificado. La zona
del transitorio queda excluida de agregados; cuando se evalúan patrones, una línea
marca el fin de referencia y las franjas rojas señalan ventanas con cambios.
El gráfico puede muestrear videos largos; el CSV conserva todas las filas.

### Usar metricas.csv en una hoja de cálculo

Importa el archivo indicando **separador coma y decimal punto**. Si tu configuración
regional utiliza coma decimal, comprueba que las columnas se importen como números.

| Columna o grupo | Interpretación |
|---|---|
| `frame` | Índice del fotograma, comenzando en 0. |
| `time_seconds` | Instante del fotograma en segundos: índice/FPS. |
| `included` | 1 si la fila entra en los resúmenes y mapas; 0 si está excluida por transitorio o corresponde al primer fotograma sin par previo. |
| `original_mean_px_frame`, `magnified_mean_px_frame` | Media espacial de la magnitud del flujo del par de fotogramas. |
| `original_p95_px_frame`, `magnified_p95_px_frame` | Percentil 95 espacial del flujo del par: resume la parte de mayor movimiento. |
| `original_rms_px_frame`, `magnified_rms_px_frame` | Raíz de la media de los cuadrados de la magnitud espacial del flujo del par. |
| `original_mean_px_second`, `magnified_mean_px_second` | Media en px/fotograma multiplicada por los FPS, expresada en px/s. |

Para rehacer el resumen:

1. Filtra `included = 1`.
2. Calcula el promedio de cada columna de movimiento por separado.
3. Grafica `time_seconds` frente a las dos columnas `*_mean_px_frame` para comparar
   evolución temporal. Para reproducir exactamente el gráfico del programa conserva
   también las filas excluidas y marca el transitorio por separado.
4. Contrasta tus promedios con `original` y `magnified` en `informe.json`.

El percentil 95 del resumen es el **promedio temporal de los percentiles espaciales**,
no el percentil 95 de todas las filas del video. Lo mismo ocurre con RMS: el resumen
promedia los RMS de cada par; no calcula un único RMS global. El primer fotograma
no tiene par anterior y contiene ceros de inicialización, no una medición de reposo.

Trabaja sobre una copia si guardas el CSV desde una hoja de cálculo: cambiar formato,
separadores o decimales modifica sus bytes y deja de coincidir con el recibo original.
Las unidades son de la resolución de procesamiento; no equivalen a milímetros,
velocidad física o amplitud calibrada de vibración.

### Interpretar informe.json

- `input` y `input_sha256` identifican el archivo analizado; el hash permite comprobar
  si dos análisis usaron exactamente los mismos bytes aunque cambie su nombre.
- `config` conserva todos los parámetros y las notas; `processing_size` registra
  `[ancho, alto]` de cálculo. Para repetir conserva también versiones y entorno.
- `original` y `magnified` contienen los promedios de las filas con `included=1`.
  `analyzed_frame_pairs` informa cuántas filas útiles se incluyeron.
- `mean_motion_ratio` es media magnificada/media original. Si el denominador es
  demasiado pequeño se registra `null`. Una razón grande con movimiento casi cero
  no prueba un movimiento físico importante.
- `clipped_pixel_fraction × 100` es el porcentaje de posiciones de píxel acumuladas
  en el tiempo que requirieron recorte durante EVM por salir del rango de brillo.
  No es un porcentaje de daño ni de fotogramas dañados. El aviso sobre 1 % es un
  criterio de revisión del prototipo, no un límite de seguridad industrial.
- `elapsed_seconds` mide desde la validación hasta dejar el análisis completo en su
  carpeta. `timing_scope` declara las exclusiones: escritura de la propia medición
  y copia de exportación manual posterior. No representa horas de trabajo humano.
- `warnings`, `patterns_status`, `flagged_windows` y `versions` registran límites,
  estado de patrones, cantidad de ventanas y versiones del procesamiento.

Ejemplo comprobado del motor con amplificación 2: media original aproximadamente
**0,02112 px/fotograma**, magnificada **0,02380**, razón **1,12665**. Esa medida creció
aproximadamente 12,7 %, sin equivaler a duplicar físicamente la vibración ni a medir
daño. La saturación fue aproximadamente **0,922 %**. Distintas métricas no tienen
por qué aumentar todas a la vez.

### Interpretar patrones.json

| `status` | Qué puedes concluir |
|---|---|
| `evaluated` | Había referencia y evaluación suficientes; revisa `events` y `windows`. |
| `disabled` | No se solicitó evaluación de patrones; no significa «evaluado y sin cambios». |
| `insufficient_reference` | No se pudo establecer la comparación; consulta el mensaje y ajusta referencia o duración. |

Cuando se evalúa, cada evento indica `start_seconds`, `end_seconds` y `score`.
Son intervalos con cambios respecto a la referencia, no fallas individuales.
En las ventanas, `robust_score` compara RMS y percentil 95 del **original** con su
referencia mediante mediana/MAD; el máximo desvío normalizado define la puntuación
y se señala cuando es mayor de 6. Se aplica un piso de escala de 0,02 px/fotograma.
Es una decisión de ingeniería para estas pruebas, no un umbral mecánico universal.

`isolation_forest_decision` es un indicador auxiliar aprendido de las ventanas de
referencia. No es una probabilidad de avería ni determina por sí solo la alerta.
La detección utiliza el original para evitar tomar artefactos de EVM como anomalías.

En el motor se señalaron **42,5–43,0 s y 51,0–51,5 s**. Revisa esos instantes en
`comparacion.avi` y contrástalos con lo que ocurrió durante la captura. Aceleración,
movimiento de cámara o cambios de luz también pueden producir diferencias.
Sin referencia independiente no atribuyas las ventanas a una pieza dañada.

### Usar matrices NPY y comprobar integridad

Las matrices tienen forma `[alto, ancho]` y contienen magnitud promedio en
px/fotograma. Se pueden cargar con `numpy.load`; cada posición corresponde a un
píxel de procesamiento, sin títulos o barra de color. Conserva ambas matrices y
`processing_size` si vas a calcular estadísticas espaciales adicionales.

`exportacion.json` registra tamaños y SHA-256 de los 14 archivos del paquete,
sin incluirse a sí mismo. Permite detectar cambios de bytes o copias incompletas;
no certifica corrección física o exactitud diagnóstica. Conserva el recibo junto
con el paquete sin editar. Los nombres de carpeta usan UTC y pueden indicar el día
siguiente respecto a la fecha local de Guatemala/Costa Rica.

Para usar los datos en un informe: identifica entrada, fecha, condiciones,
configuración y versiones; incluye mapas con escala y gráfico con unidades; cita
los valores del CSV/informe y describe las ventanas como cambios respecto a
referencia. Conserva la carpeta completa como respaldo y separa observación,
interpretación y limitaciones.

## Herramientas técnicas por consola

La interfaz gráfica es el modo de usuario del diseño. La consola es una herramienta
auxiliar para validación y reproducción del mismo procesamiento; no añade otro
servicio ni requiere modificar código.

```bash
# Solo validar la entrada
bash run.sh data/input/referencias/subtle.avi --json

# Ejecutar el análisis sintético con la resolución de referencia
bash run.sh data/input/referencias/amplitude_change.avi --analyze --low 0.7 --high 1.5 --alpha 5 --baseline 8 --spatial-level 1 --max-dimension 160 --capture-notes "Escenario sintético controlado" --json
```

La consola guarda directamente en `data/output/` o en `--output carpeta` y no crea
el recibo de copia interactiva `exportacion.json`. `--no-patterns` desactiva patrones;
`bash run.sh --help` muestra las opciones completas.

## Método implementado y límites

- EVM lineal de una escala gaussiana, luminancia y filtro Butterworth pasabanda
  causal de segundo orden de diseño. No implementa EVM por fase; el filtro tiene
  desfase y transitorio.
- Flujo óptico denso Farnebäck con los mismos parámetros en ambas ramas.
- Reducción proporcional con dimensiones pares; no estabiliza cámara, calibra
  desplazamiento físico ni corrige iluminación automáticamente.
- Ventanas de patrones de aproximadamente 0,5 s; al menos ocho completas de referencia
  y una posterior. Isolation Forest usa semilla 42 y 100 árboles como apoyo auxiliar.
- MP4, AVI, MOV, MKV, M4V y WebM dependen de los códecs disponibles. La validación de
  lectura no detecta toda corrupción tolerada por un decodificador.
- Se trabaja secuencialmente con pocos fotogramas, pero estadísticas y archivos crecen
  con la duración. Debe haber espacio para tres videos de salida y su copia al exportar.
- Ruido, compresión, iluminación y movimiento de cámara pueden afectar los resultados.
  Las condiciones de captura deben documentarse y las comparaciones deben mantenerlas
  equivalentes o registrar sus diferencias.

## Pruebas y estado frente al plan

Al **2 de noviembre de 2026**, SW-01 a SW-06 están implementadas y la campaña técnica
funcional ACT-PRU-02 dispone de **35 pruebas, 15 casos funcionales y 18 comprobaciones
del flujo real aprobadas**. Las cinco referencias sintéticas cumplen siete criterios.
Las repeticiones de una prueba no cuentan como requisitos adicionales.

- [Reporte funcional](Proyecto/Informes/Reporte_Pruebas_Funcionales_PRU02_2026-11-02.md).
- [Evidencia PRU-02](docs/pru02-2026-11-02/README.md).
- [Matriz vigente de los 35 requisitos](docs/matriz-requisitos-2026-11-09.md).
- [Desempeño e integración del 9/11](docs/pru03-pru04-2026-11-09/README.md).
- [Guía de 15 casos manuales](docs/guia-pruebas-manuales.md) y [registro personal](docs/plantillas/registro-prueba-manual.md).

Para repetir las verificaciones utiliza rutas nuevas de evidencia:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/validate_reference_suite.py --evidence docs/NUEVA_SESION/referencias.json
QT_QPA_PLATFORM=xcb .venv/bin/python scripts/validate_functional_week.py --evidence docs/NUEVA_SESION/funcionales
.venv/bin/python -m pip check
```

La prueba xcb necesita escritorio accesible; `offscreen` sirve para automatización
sin ventana visible, registrando esa diferencia. Las referencias son simulaciones
identificadas como tales: estático, 1 Hz, 5 Hz, cambio de amplitud e iluminación variable.
La plantilla personal no se da por completada por haber ejecutado automatización.

PRU-03 y PRU-04 se completaron técnicamente el 9 de noviembre. Se registraron 17
análisis medidos y la regresión de integración.

### Qué falta dentro del alcance planificado

| Actividad | Fechas del plan | Trabajo pendiente |
|---|---|---|
| ACT-DOC-01 | 16–20 de noviembre | Informe técnico final y consolidación de evidencia. |
| ACT-PRE-01 | 18–21 de noviembre | Preparación y presentación final según el curso. |

Se conserva el presupuesto de 192 h del plan; no se inventan horas reales ni se
retrofechan pruebas. La revisión académica y la constancia de aprobación se registran
cuando existan. El funcionamiento con CPU se justificó con un proceso sin acceso
a GPU, mediante el método aceptado por Daniel; su computadora sí tiene GPU.

Una validación de diagnóstico con fallas etiquetadas sería trabajo adicional para
poder afirmar exactitud mecánica. No se convierte en una nueva fase obligatoria
ni en un entregable no previsto para cerrar este prototipo de apoyo a inspección.

## Organización y documentación

- `src/video_analysis/`: `video`, `magnification`, `motion`, `heatmaps`, `anomalies`,
  `export` y `gui`; `pipeline.py` integra el procesamiento.
- `scripts/`: preparación, generadores y validadores; `tests/`: pruebas automatizadas.
- `data/input/`: entradas autorizadas y metadatos; `data/output/`: resultados locales.
- [Proyecto/README.md](Proyecto/README.md): plan, diseño, requisitos, informes y curso.
- [docs/README.md](docs/README.md): estado vigente, decisiones, incidencias y evidencia.

Los informes y presentaciones fechados son históricos; no sustituyen al plan/diseño
como definición del producto. Las discrepancias detectadas se explican en la
[fe de erratas de alcance](Proyecto/Presentacion/Fe_de_erratas_alcance_2026-11-02.md).
Las [notas de coherencia documental](Proyecto/Informes/Notas_de_coherencia_documental_2026-11-02.md)
explican también las diferencias de fechas y esfuerzo entre registros sin reconstruirlos.
Para desarrollo se utiliza Ruff con reglas y longitud definidas en `ruff.toml`;
no es una dependencia necesaria para usar la aplicación.

El repositorio actual es público por decisión de Daniel. **No se hace commit ni push
salvo que Daniel lo solicite explícitamente.** La autorización para publicar entradas
no se extiende a subir automáticamente resultados de `data/output/`.
