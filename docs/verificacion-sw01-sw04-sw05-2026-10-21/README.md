# Revalidación de SW-01, SW-04 y SW-05

Fecha de corte: 21 de octubre de 2026, Costa Rica. Versión de aplicación: `e72e850`. Se repitieron las pruebas por solicitud de Daniel; los algoritmos y la interfaz no se modificaron en esta revisión. Se ajustó únicamente el generador de evidencia para no usar una fecha fija ni sobrescribir registros históricos.

## Dictamen

Las tres actividades están implementadas y verificadas técnicamente en el alcance controlado disponible. Son dependencias de SW-06, no trabajo pendiente de comenzar. No se considera terminada la validación con captura real ni la aceptación final. SW-05 continúa dentro de su periodo previsto hasta el 24 de octubre; disponer de su implementación no cambia las fechas ni equivale a aceptación externa.

| Actividad | Qué se comprobó de nuevo | Resultado |
|---|---|---|
| ACT-SW-01 | Carga AVI/MP4, metadatos, errores, cancelación, regularidad temporal; reducción 160×120 a 80×60 conservando 20 FPS y 400 fotogramas; entrada intacta | Aprobado en los casos ejecutados |
| ACT-SW-04 | Métricas original/magnificado, mapa con escala compartida, resumen y exportación; control estático y movimiento conocido | Aprobado en los casos ejecutados |
| ACT-SW-05 | Escena estable, cambio de amplitud, separación de referencia/evaluación, desactivación y referencia insuficiente | Aprobado en los casos ejecutados |

## Evidencia nueva

- `pruebas.txt`: **31 pruebas** de la suite completa, resultado OK.
- `referencias.json` / `referencias.txt`: **cinco escenarios** y **siete criterios** aprobados.
- `casos-adicionales.json`: **cinco comprobaciones** aprobadas en tres ejecuciones: reducción proporcional, conservación temporal, original intacto, patrones desactivados y referencia insuficiente.
- `proteccion-historial.json`: el generador rechaza una ruta de evidencia existente y conserva sus bytes.
- `manifiesto.json`: identificación de código y documentación mediante huellas.

## Resultados de las referencias

| Escenario | Media original (px/fotograma) | Media magnificada | Ventanas señaladas |
|---|---:|---:|---:|
| Estático | 0 | 0 | 0 |
| Movimiento sutil, 1 Hz | 0,02054 | 0,05007 | 0 |
| Fuera de banda, 5 Hz | 0,09540 | 0,09540 | 0 |
| Cambio de amplitud desde 13 s | 0,07421 | 0,09884 | 14, entre 13 y 20 s |
| Iluminación variable | 0,0000834 | 0,0006746 | 0 |

Las cifras están redondeadas; los JSON conservan los valores completos. El incremento de movimiento o una alerta no demuestran daño mecánico. Los videos están generados sintéticamente con condiciones controladas.

## Reproducir

Desde la raíz del proyecto:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/validate_reference_suite.py --evidence docs/otra-verificacion/referencias.json
```

Usar siempre una ruta nueva. Las ejecuciones adicionales emplearon `subtle.avi` con `AnalysisConfig(max_dimension=80)`, otra ejecución agregando `patterns_enabled=False` y una tercera con `baseline_seconds=1`. Se revisó la metadata de `original.avi`, el hash de entrada y el estado del informe; las salidas temporales de esos tres casos se eliminaron tras verificarse.

## Revisión de Daniel

La [guía manual](../guia-pruebas-manuales.md) contiene 15 casos con pasos y criterios. La [hoja de registro](../plantillas/registro-prueba-manual.md) queda pendiente de completar por Daniel. No se registran esas pruebas manuales como ejecutadas por la existencia de una guía.

Continúan pendientes: captura real (VAL-001), ensayo físico específico sin GPU (VAL-002), protocolos y aceptación formales (VAL-003). La disponibilidad de una grabación real sigue condicionando la comprobación del comportamiento físico, pero no impidió probar los módulos con las referencias controladas.
