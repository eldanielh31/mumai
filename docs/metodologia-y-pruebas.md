# Método y protocolo de validación

## Fundamento y decisiones

El módulo EVM sigue el principio de descomposición espacial, filtrado temporal y
amplificación descrito por Wu et al. (2012). La implementación propia usa una escala
gaussiana y luminancia, con procesamiento secuencial. No se presenta como una réplica
completa del código de los autores ni de su variante multiescala o por fase.

Se seleccionó una reducción espacial por defecto: en el escenario de desplazamiento
sutil de 0,25 píxeles, dos reducciones suavizaban demasiado la textura y daban una razón
de movimiento de 1,16; una reducción produjo aproximadamente 2,44. El parámetro puede
ajustarse. Esta razón corresponde a la medida de flujo, no a una calibración geométrica.

La magnitud del flujo Farnebäck utiliza parámetros fijos y compartidos: escala 0,5,
3 niveles, ventana 15, 3 iteraciones, poly_n=5 y poly_sigma=1,2. Resolución y FPS son
idénticos en las dos ramas. No se sustrae movimiento global ni se corrige iluminación.

La detección de patrones se apoya en RMS y percentil 95 del flujo del original,
promediados en ventanas de medio segundo. Una referencia inicial seleccionada por la
persona usuaria establece mediana y MAD; después se evalúan únicamente ventanas que
no se solapan con esa referencia. Se excluye el transitorio de EVM de ambas ramas.
Se necesita confirmar externamente que el tramo de referencia sea representativo.

El umbral robusto de 6 y piso de escala 0,02 px/fotograma son decisiones de ingeniería
para este prototipo; no son umbrales clínicos ni industriales. Isolation Forest con
semilla 42, 100 árboles y contamination=auto produce un indicador auxiliar. La alerta
se define con el criterio robusto para evitar depender de extrapolaciones del bosque
cuando la referencia es constante. No se afirma clasificación de tipos de daño.

## ACT-PRU-01 — Escenario controlado

Generador: `scripts/create_reference_videos.py`. Semilla 42, 20 FPS, 20 s, 160 × 120,
textura sintética central, cámara fija, códec sin pérdida FFV1. Metadatos JSON junto
al video registran desplazamiento y etiqueta por fotograma.

| Escenario | Condición conocida | Comprobación |
|---|---|---|
| static | Sin desplazamiento ni variación luminosa | Movimiento menor a 0,001 px/fotograma; sin alertas |
| subtle | Sinusoide de 1 Hz, amplitud 0,25 px | Razón de movimiento magnificado/original mayor que 1,5; sin alertas |
| out_of_band | Sinusoide de 5 Hz, amplitud 0,25 px | Ganancia menor que la del caso de 1 Hz |
| amplitude_change | 1 Hz; amplitud pasa de 0,25 a 2 px en segundo 13 | Alerta posterior al cambio y ninguna anterior a 12,5 s |
| lighting | Intensidad sinusoidal, sin desplazamiento geométrico | Documentar respuesta y limitación por iluminación; no confundir con daño |

La suite ejecuta los mismos parámetros sin entrenar con las etiquetas de evaluación.
Las etiquetas solo se usan para comprobar los resultados. El archivo
`docs/validacion-2026-10-18.json` registra resultados y rutas de evidencia.

## Pruebas automáticas

Además de las entradas y la interfaz, se comprueba selectividad temporal con señales
conocidas, control estático, amplificación cero, parámetros inválidos, desplazamiento
de 1 px, escala compartida, separación referencia/evaluación, rechazo de temporización
variable, exportación completa, cancelación sin resultados parciales y videos cortos.
La lectura completa de cada video exportado comprueba su cantidad de fotogramas.

## Protocolo para videos reales

1. Grabar con cámara fija y exposición/foco bloqueados si es posible; documentar equipo,
   escena, distancia, iluminación, FPS, resolución y códec, sin modificar la maquinaria.
2. Obtener un tramo de referencia cuya condición sea conocida; no asumir que un video
   cualquiera muestra un funcionamiento normal. Registrar quién confirmó la condición.
3. Seleccionar una banda por debajo de FPS/2 compatible con la vibración de interés.
   Usar duración suficiente para transitorio, referencia y evaluación separada.
4. Ejecutar con parámetros registrados; revisar saturación, movimiento global,
   iluminación y compresión. Comparar original y magnificado con la misma escala.
5. Contrastar las alertas con observación o referencia independiente. Si no existe,
   informar cambios de patrón sin atribuirlos a fallas. Registrar falsos positivos,
   falsos negativos y limitaciones cuando haya etiquetas fiables.

Este protocolo está preparado; no se afirma haberlo ejecutado con maquinaria real.
Las fases formales de pruebas del cronograma permanecen programadas para noviembre.

## Fuentes técnicas

- Wu et al. (2012), Eulerian Video Magnification for Revealing Subtle Changes in the World:
  https://people.csail.mit.edu/mrub/papers/vidmag.pdf
- Proyecto y descripción del método EVM: https://people.csail.mit.edu/mrub/evm/
- OpenCV, `calcOpticalFlowFarneback`:
  https://docs.opencv.org/4.5.3/dc/d6b/group__video__track.html

## Registro de esfuerzo

Las horas del plan son presupuesto, no horas reales ejecutadas. No se reconstruye ni
inventa AC. Registrar desde ahora fecha, ID de actividad, horas reales y evidencia;
el valor ganado debe actualizarse con la revisión de entregables y los registros reales.

## Actualización del protocolo — 1 de noviembre de 2026

El protocolo real ya se ejecutó en el alcance de compatibilidad, consulta, exportación y repetibilidad; véase [cierre semanal](cierre-semana-2026-11-01/README.md). No se reemplaza el estado histórico anterior. El nuevo script `validate_real_workflow.py` conserva la configuración exacta de un reporte y compara resultados, preservando la evidencia existente. La próxima fase dispone de [protocolo PRU-02](cierre-semana-2026-11-01/protocolo-pru02.md).
