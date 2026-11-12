# Desempeño e integración del prototipo

Fecha efectiva de ejecución y cierre técnico **9 de noviembre de 2026**, hora de Guatemala.

| Actividad | Ventana del plan | Resultado del 9/11 |
|---|---|---|
| ACT-PRU-03 | 9–14 de noviembre | Medición de desempeño y comparación original/magnificado completadas. |
| ACT-PRU-04 | 9–16 de noviembre | Integración final y regresión completadas en los escenarios ejecutados. |

Esta evidencia complementa el [reporte funcional PRU-02](Reporte_Pruebas_Funcionales_PRU02_2026-11-02.md)
para ENT-PRU-01. También aporta verificación de ENT-PRO-01 y ejemplos trazables de
ENT-EVI-01. [Plan de proyecto](../Plan/Plan_de_Proyecto_Daniel_Brenes.pdf).

## Condiciones de medición

Se ejecutaron 17 análisis consecutivos, cada uno en un proceso nuevo. Se usaron las
cinco referencias de 20 s y 20 FPS con tres repeticiones por caso, y la captura
regularizada del motor de 54,8 s y 30 FPS con dos repeticiones. La banda fue de
0,7–1,5 Hz con nivel espacial 1 y detección de patrones habilitada. Para los casos
sintéticos se usaron alpha 5 y referencia de 8 s. Para el motor se usaron alpha 2,
referencia de 10 s y dimensión máxima 480 px. La captura real se tomó con luz de día
y soporte independiente según Daniel.

Se usó un AMD Ryzen 7 6800HS with Radeon Graphics con Ubuntu 24.04 en WSL, 15,25 GiB visibles y
Python 3.13.18. OpenCL se desactivó para la campaña. El tiempo
de pared incluye arranque del proceso y análisis completo por consola. La columna
de proceso proviene de elapsed_seconds del informe. RSS es el máximo reportado por
GNU time entre las repeticiones. Disco es la mediana de bytes de los archivos del
paquete persistido en MiB. Los tiempos corresponden a esta combinación de equipo,
archivos y ajustes. [Protocolo](../../docs/pru03-pru04-2026-11-09/procedimiento.md).

## Resultados de desempeño

| Caso | n | Procesamiento | Pared mediana (s) | Pared rango (s) | Análisis mediana (s) | RSS máximo (MiB) | Salida mediana (MiB) |
|---|---:|---|---:|---:|---:|---:|---:|
| Estático | 3 | 160×120 | 6,72 | 6,22–7,05 | 4,75 | 226,6 | 4,48 |
| Movimiento sutil a 1 Hz | 3 | 160×120 | 6,62 | 6,50–7,22 | 5,09 | 224,4 | 4,51 |
| Movimiento a 5 Hz | 3 | 160×120 | 6,47 | 6,32–7,07 | 4,90 | 225,4 | 4,41 |
| Cambio de amplitud | 3 | 160×120 | 6,14 | 5,82–6,79 | 4,48 | 224,1 | 4,57 |
| Iluminación variable | 3 | 160×120 | 6,60 | 6,54–6,62 | 5,02 | 226,3 | 4,68 |
| Motor a 30 FPS | 2 | 480×270 | 136,92 | 136,90–136,93 | 134,49 | 278,5 | 232,19 |

Para el motor, el tiempo de pared mediano fue **136,92 s**,
el RSS máximo **278,5 MiB** y cada paquete ocupó aproximadamente
**232,19 MiB**. La medición incluye los tres videos generados
y sus resultados numéricos y visuales. Los requisitos prevén medir desempeño en un
conjunto definido. [Registros de cada ejecución](../../docs/pru03-pru04-2026-11-09/mediciones.jsonl).

## Comparación de movimiento

| Caso | Original (px/fotograma) | Magnificado (px/fotograma) | Razón | Ventanas señaladas |
|---|---:|---:|---:|---:|
| Estático | 0,000000 | 0,000000 | Indefinida (media original cero) | 0 |
| Movimiento sutil a 1 Hz | 0,020536 | 0,050072 | 2,438 | 0 |
| Movimiento a 5 Hz | 0,095403 | 0,095403 | 1,000 | 0 |
| Cambio de amplitud | 0,074210 | 0,098838 | 1,332 | 14 |
| Iluminación variable | 0,000083 | 0,000675 | 8,087 | 0 |
| Motor a 30 FPS | 0,021122 | 0,023797 | 1,127 | 2 |

Las medias se calculan sobre los pares incluidos tras el transitorio y se comparan
a la misma resolución dentro de cada caso. El escenario de 1 Hz muestra una razón
mayor que el de 5 Hz. El cambio de amplitud señala 14 ventanas a partir de 13 s.
En iluminación variable la razón elevada parte de un movimiento original de apenas
0,000083 px/fotograma. El motor señala ventanas de cambio respecto a su referencia
inicial. Sus causas mecánicas requieren evidencia independiente.

En cada caso coincidieron las huellas del CSV, las dos matrices NPY y el JSON de
patrones de todas las repeticiones. Los 4 archivos numéricos del motor coinciden además con la exportación de referencia del 2/11.

## Integración y regresión

- **35 pruebas automáticas aprobadas**, con dependencias verificadas mediante pip check.
- **15 casos funcionales aprobados** en Qt offscreen, con reproducción, consulta,
  exportación, cancelación y recuperación comprobadas.
- **7 criterios de referencia aprobados** en la suite sintética.
- **19 paquetes verificados**, incluidos 17 resultados medidos
  y las exportaciones de Qt. Se decodificaron completamente los tres AVI de cada
  paquete y se contrastaron métricas, mapas, enlaces y recibos donde aplicaba.
- **14 archivos de entrada** verificados por SHA-256 antes y después.
  Los 37 archivos técnicos registrados en PRU-02 conservan sus huellas.

El cierre técnico se apoya en la campaña por consola y la regresión sintética por Qt
de esta fecha. El recorrido real por interfaz y la prueba de CPU aislada siguen
documentados en [PRU-02](../../docs/pru02-2026-11-02/README.md).
La revisión académica se registra cuando exista. La documentación final y la
presentación mantienen sus ventanas del 16–20 y 18–21 de noviembre, respectivamente.
[Evidencia de esta semana](../../docs/pru03-pru04-2026-11-09/README.md).
