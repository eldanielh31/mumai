# Reporte de pruebas funcionales PRU02

Fecha de ejecución y corte: **2 de noviembre de 2026**, America/Guatemala.
Actividad: **ACT-PRU-02**, prevista del **2 al 7 de noviembre de 2026**.
Entregable relacionado: **ENT-PRU-01**, componente de verificación funcional.
Ejecutor de esta campaña: **Codex mediante automatización técnica**. La exportación
usada como referencia fue ejecutada por Daniel. No se atribuyen a Daniel los casos
automatizados ni se declara aceptación del profesor.

## Resultado y alcance

Se completó la campaña técnica funcional de esta semana: **35 pruebas de regresión,
15 casos funcionales M01–M15 y 18 comprobaciones de repetibilidad del video real,
todos aprobados**. Las cinco referencias sintéticas cumplieron sus siete criterios.
Se verificó lectura completa, integridad y coherencia de cuatro exportaciones.
Las dos incidencias de preparación detectadas al utilizar el proyecto en WSL tienen
corrección y regresión. No quedó un fallo funcional reproducible en el alcance probado.

El cierre técnico de PRU-02 no equivale a aceptación externa, diagnóstico mecánico
ni terminación de todo ENT-PRU-01: la campaña de rendimiento PRU-03 y la integración
final PRU-04 conservan sus fechas. Daniel confirmó mantener público el remoto actual, incluidos los videos del motor.
Por instrucción suya, esta entrega se conserva local: no se hace commit ni push
salvo solicitud explícita.

## Fuentes y método

Se consultaron el Plan de Proyecto de `Proyecto/Plan/`, especialmente entregables,
actividades y cronograma, y el Documento de Diseño v2 de `Proyecto/Diseño/`, en
particular interfaces, interacción, estados y flujo algorítmico. Se usó el protocolo
preparado el 1 de noviembre, la guía M01–M15 y la matriz de los 35 requisitos.
Los documentos académicos originales y las evidencias históricas se conservaron.

Base Git: `be0cbf8bcd83372de0bb974ab4840d9b6530a3cb`. La identidad final del árbol
probado se conserva en `docs/pru02-2026-11-02/manifiesto.json`. Las modificaciones
preexistentes de `motor.mp4` y `verification-install-latest.txt` quedaron fuera
de los cambios preparados en esta campaña. No se restauraron ni sobrescribieron.

Entorno: Ubuntu 24.04 en WSL2, Python 3.13.18,
AMD Ryzen 7 6800HS, memoria total informada de aproximadamente 15,25 GiB.
La GPU RTX 3050 fue declarada por Daniel; el ensayo acordado comprueba uso funcional
de CPU mediante aislamiento por proceso. Las versiones de bibliotecas constan en el informe del motor y requirements.txt.
La memoria total no es una medición de RAM máxima del proceso.

## Resultados de la campaña

| Comprobación | Resultado | Evidencia en docs/pru02-2026-11-02 |
|---|---|---|
| Regresión final | 35/35 aprobadas | regresion-final.txt |
| Casos funcionales por Qt/X11 | M01–M15 aprobados, 51 criterios | funcionales/casos.json y capturas |
| Referencias sintéticas | Cinco escenarios, 7/7 criterios | referencias.json |
| Pruebas de escritorio previas | 7/7 aprobadas | escritorio-base.txt |
| Regresión sin red y sin acceso a GPU | 33/33 aprobadas antes de añadir los dos casos de preparación | cpu-sin-red.txt |
| Flujo real sin red | 18/18 comprobaciones aprobadas | motor-sin-red.json |
| Integridad de exportaciones | Cuatro paquetes correctos; 12 videos decodificados completos | integridad.json |
| Conservación de entradas | Los 14 archivos de entrada, incluidos los ocho videos, intactos | entorno.json e integridad.json |
| Dependencias | pip check sin incompatibilidades | dependencias.txt |
| Calidad y formato | Reglas F/I y formato correctos | calidad.txt y formato.txt |
| Preparación del entorno | Rechazo de Python ausente o incompatible antes de cambios del sistema | preparacion.json y tests/test_setup.py |

Las siete pruebas de escritorio y las 33 pruebas aisladas son repeticiones o
subconjuntos de la regresión; no se suman como requisitos adicionales. Tampoco se
convierte el porcentaje de pruebas aprobadas en porcentaje de avance del proyecto.

## Casos funcionales

| Caso | Función y resultado observado |
|---|---|
| M01 | Carga de referencia válida: 160×120, 20 FPS y 400 fotogramas; configura sin iniciar análisis automáticamente. |
| M02 | Rechaza README como entrada y recupera la configuración con video válido. |
| M03 | Rechaza frecuencia máxima de 11 Hz a 20 FPS; reduce proporcionalmente a 80×60 y conserva la fuente. |
| M04 | Escena estática con movimiento menor de 0,001 px/fotograma y sin alertas. |
| M05 | Movimiento en banda con ganancia mayor de 1,5, sin alertas y mapas con escala común. |
| M06 | Ganancia fuera de banda inferior a la de la referencia en banda, sin alertas. |
| M07 | Amplificación cero: igualdad de las cuatro métricas y de las matrices de ambos mapas. |
| M08 | Detecta las 14 ventanas del cambio sintético, todas desde 13 s. |
| M09 | Patrones desactivados se informan como desactivados y se conservan las demás salidas. |
| M10 | Referencia insuficiente se informa sin inventar detección ni retirar las otras salidas. |
| M11 | Iluminación variable con residuo pequeño, sin alertas y con advertencia de interpretación. |
| M12 | Cuatro pestañas consultables, búsqueda a 14 s, reproducción, pausa y reinicio desde el final. |
| M13 | Cancelar selector conserva análisis; dos exportaciones distintas e íntegras persisten tras reiniciar. |
| M14 | Cambiar configuración retira vistas obsoletas; errores de parámetros y video corto permiten recuperación. |
| M15 | Cancelación real al 5 % del procesamiento, sin resultado parcial; análisis posterior exitoso. |

En M13 se simula únicamente la respuesta de cancelar del selector de carpeta. Las
exportaciones, el procesamiento, los hilos Qt y la reproducción se ejecutaron realmente.
Se inspeccionaron visualmente las cuatro capturas de resultados sintéticos; textos,
unidades, escala compartida, tabla y controles son legibles. No se rellenó la hoja
personal de pruebas de Daniel ni se simuló una aprobación humana.

## Video real del motor

Se repitió exactamente la configuración de la exportación de Daniel sobre
`data/input/motor_30fps.avi`: 30 FPS, 1644 fotogramas, 54,8 s, entrada 848×478;
banda 0,7–1,5 Hz, amplificación 2, referencia 10 s, dimensión 480 y nivel espacial 1.
Se conserva también el texto de condiciones de esa exportación: «Condiciones no
documentadas». Los datos de captura confirmados anteriormente permanecen en
`docs/cierre-semana-2026-11-01/condiciones-captura.json`; no se reescribió el reporte
original para agregar información posterior. Daniel confirmó el 2/11 que se grabó
con luz de día; la exposición sigue desconocida. El nuevo dato y el acuerdo de ensayo
con CPU constan en `docs/pru02-2026-11-02/confirmaciones-daniel.json`.

El procesamiento produjo 480×270 y tardó **213.00 s**.
La relación de movimiento medio es **1.126655** y la
saturación **0.922 %**. Se mantienen los intervalos
42,5–43,0 s y 51,0–51,5 s. El CSV, patrones, dos matrices y resúmenes numéricos
coinciden exactamente con la ejecución de Daniel. La exportación nueva persiste
tras reiniciar; la fuente y la exportación de referencia siguen intactas.

Salida real nueva: `/home/danbg/mumai/data/output/pru02-2026-11-02/motor/analisis-20261103T005808Z-7cc2ba7c-export-b85e2d30`.
Los videos y resultados reales permanecen en `data/output/` y no se incorporan al
commit. La evidencia publicada localmente en docs es textual y no contiene imágenes
reales del automóvil. Las alertas describen diferencias respecto a referencia, no
fallas demostradas; no hay etiquetas mecánicas externas para medir exactitud diagnóstica.

## Aislamiento y límites de verificación

El flujo real completo se ejecutó con `unshare --user --map-root-user --net` y Qt
offscreen. `/proc/net/dev` solo muestra loopback; no se desconectó la red del usuario.
`/sys/class/net` puede mostrar interfaces del host, por lo que no se usa como prueba
de conectividad. OpenCL estuvo desactivado; los dispositivos GPU seguían visibles
en esta ejecución real y no se afirma que estuvieran bloqueados.

Por separado, la regresión de 33 pruebas se ejecutó con namespaces de red y montajes,
`/dev/dri` vacío y `/dev/dxg` sustituido por `/dev/null` (dispositivo 1:3), con OpenCL
desactivado. Los montajes solo afectaron al proceso aislado. Esa evidencia verifica
funcionamiento funcional sin acceso a GPU; no demuestra un equipo físicamente sin GPU.
Daniel aceptó expresamente esta equivalencia funcional en la misma computadora:
el ensayo no exige otro equipo físico. Se justifica con bloqueo de los dispositivos
y ejecución satisfactoria del flujo de análisis en las pruebas aisladas. Esta
aceptación del método por Daniel no se atribuye al profesor.

## Correcciones realizadas

**INC-015:** se identifica un puntero Git LFS antes de abrirlo como video y se informa
que falta descargarlo. Se añade regresión y guía LFS, incluida exclusión de una entrada
reemplazada por el usuario. No se regeneraron ni alteraron los videos de entrada.

**INC-016:** se comprueba Python 3.13 antes de pedir sudo o ejecutar apt. Se conserva
PROJECT_PYTHON y no se instala automáticamente otro intérprete. Dos regresiones
comprueban ausencia/incompatibilidad sin ejecutar la instalación del sistema.

Se añade `scripts/validate_functional_week.py` para reproducir M01–M15 y se actualizan
las rutas WSL de la guía. No se cambian algoritmos, umbrales, versiones fijadas ni
los criterios de diagnóstico.

## Pendientes y decisión de cierre

La campaña técnica de ACT-PRU-02 está ejecutada y documentada el 2 de noviembre,
dentro de su ventana prevista. Quedan separados de este cierre:

- Aceptación externa del reporte de pruebas; el método con CPU está acordado con Daniel.
- Bloqueo de exposición, RPM e intervalos exactos del motor no confirmados; luz de día confirmada.
- Commit y push reservados para una solicitud explícita de Daniel; no se ejecutaron.
  REP-002 quedó resuelto: visibilidad pública y videos autorizados.
- PRU-03 del 9–14/11: campaña comparativa de tiempo, RAM máxima y almacenamiento.
- PRU-04 del 9–16/11: integración final y regresión de las correcciones que surjan.
- Documentación final del 16–20/11 y presentación del 18–21/11.

No se declaran realizadas las etapas futuras. Las 12 horas del plan son presupuesto;
no se inventan horas efectivas ni se llena el registro con tiempos de ejecución.
