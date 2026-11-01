# Prueba con captura real: motor de Daniel

Fecha: 1 de noviembre de 2026, Costa Rica. Código base: `9abec77`.

## Entrada y hallazgo INC-012

Daniel aportó `data/input/motor.mp4`, grabado con su teléfono del motor de su automóvil. Se leyeron los 1642 fotogramas: 848×478, aproximadamente 54,8024 segundos, H.264, media de 29,962191 FPS. La captura tiene audio, que el análisis no utiliza.

La carga inicial acepta el archivo, pero el análisis exige temporización constante y rechaza el salto de 0,1257 segundos entre los dos primeros fotogramas. La mediana de intervalos es 0,033322 segundos; solo un intervalo supera 0,04 segundos. No se atribuye este problema a corrupción ni a variabilidad durante toda la grabación. Es una incompatibilidad de temporización de entrada, no evidencia de un fallo del motor.

Se creó `data/input/motor_30fps.avi` con FFmpeg, filtro `fps=30` y códec FFV1. El original permanece intacto. FFV1 evita otra compresión con pérdidas de la imagen decodificada; la normalización temporal puede duplicar o descartar fotogramas y no recupera información ausente. La copia es mayor que el MP4 y no contiene audio. No se modificó el programa ni se relajó su validación.

Se inspeccionaron imágenes de los segundos 0, 10, 20, 30, 40 y 50: motor visible, bordes y textura, encuadre aproximadamente estable. Esta revisión no demuestra cámara perfectamente inmóvil ni sustituye una medición independiente. Modelo de teléfono, soporte, RPM, iluminación y fecha efectiva de captura no confirmados.

## Cómo repetirlo en la interfaz

1. Abrir una terminal y ejecutar `cd /home/daniel/Desktop/proyecto-final` y luego `bash run.sh`.
2. Seleccionar `/home/daniel/Desktop/proyecto-final/data/input/motor_30fps.avi`.
3. Configurar mínima **0,7 Hz**, máxima **1,5 Hz**, amplificación **2**, referencia **10 segundos**, dimensión máxima **480**, reducción espacial **1**, detección de cambios activada.
4. Indicar en condiciones: “Motor de automóvil grabado con teléfono; copia normalizada a 30 FPS; RPM y estabilidad no verificadas; exploración de movimiento lento”.
5. Pulsar **Validar configuración**, después **Analizar**, y esperar a Resultados disponibles.
6. Revisar las cuatro pestañas, comparar ambos videos y consultar métricas y mapas. Pulsar **Exportar resultados** para conservar la revisión antes de cambiar parámetros o cerrar.

La banda 0,7–1,5 Hz es exploratoria: permite reproducir una prueba del flujo y observar movimiento lento; no se ha identificado como frecuencia de vibración del motor. La dimensión 480 conserva más detalle que los 160 usados para los videos sintéticos. La referencia de 10 segundos presupone un comienzo representativo; Daniel debe confirmar las condiciones. Con 30 FPS el programa admite un límite superior estrictamente menor de 15 Hz; ello no garantiza que vibraciones más rápidas no produzcan aliasing.

## Alcance

Esta prueba no permite concluir que el motor esté sano o averiado, ni medir desplazamiento físico sin calibración. Las alertas son diferencias respecto al tramo inicial y pueden incluir cámara o iluminación. No existen etiquetas de fallas ni referencia externa para calcular exactitud diagnóstica. La captura real y sus resultados se mantienen locales en `data/`, excluidos de Git. No se publican imágenes del automóvil.

Los resultados de la ejecución y las huellas se registran en `evidencia.json`. VAL-001 avanza a captura real disponible y prueba exploratoria; siguen pendientes las condiciones completas, repetibilidad y contraste externo del protocolo. Las pruebas formales y la aceptación no se dan por concluidas.

## Primera ejecución y ajuste

Con amplificación 5, el procesamiento completo terminó en 134,85 s, tamaño 480×270, 1558 pares analizados, relación de movimiento medio 1,425. Se observó 1,152 % de saturación y se decidió comprobar amplificación 2 antes de recomendarla. El gráfico temporal se inspeccionó visualmente. Se señalaron dos ventanas, 42,5–43,0 s y 51,0–51,5 s; no hay etiquetas externas que permitan atribuirlas a fallas. El tramo inicial también presenta cambios, por lo que su representatividad debe confirmarse.

## Resultado de la configuración recomendada

Con amplificación **2**, el flujo completo terminó correctamente en **131,13 s**, procesando 1644 fotogramas a 480×270. Saturación **0,922 %**, por debajo del umbral de advertencia del 1 %; no equivale a ausencia total de recorte. Relación de movimiento medio **1,127**. Se mantuvieron las dos ventanas señaladas (la detección usa el original). Se generaron videos, CSV, mapas, gráfico, JSON y resumen HTML. No se ejecutó exportación mediante el selector gráfico en esta revisión: los resultados se guardaron directamente con la interfaz de comandos.

Resultados recomendados: `/home/daniel/Desktop/proyecto-final/data/output/motor-validacion-2026-11-01/analisis-20261101T201740Z-96f59e0b/resumen.html`. Las salidas se verificaron mediante el control de decodificación y conteo incluido en el flujo. Se confirmó que la huella del original se conservó. No se repitió la suite sintética porque no cambió el código; se probaron dos configuraciones sobre esta entrada real.
