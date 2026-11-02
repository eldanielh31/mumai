# Conciliación del cronograma al 1 de noviembre de 2026

Semana de referencia: lunes 26 de octubre a domingo 1 de noviembre, Costa Rica. Fuente: Plan de Proyecto, secciones 2.2, 2.3 y 2.5, páginas 6–8. La actividad con vencimiento esta semana es ACT-SW-06 (31 de octubre). La evidencia nueva se ejecutó el 1 de noviembre; no se retrofecha al día 31 ni demuestra por sí sola un cierre histórico en otra fecha.

## Actividades de la línea base

| ID | Fin previsto | Estado técnico al corte / evidencia |
|---|---|---|
| ACT-PLAN-01 | 08/08 | Documento disponible en Proyecto/Plan; aprobación confirmada por Daniel en el chat. La copia PDF no contiene constancia gráfica del supervisor; no se fabrica. |
| ACT-INV-01 | 15/08 | Fundamentos y decisiones en docs/metodologia-y-pruebas.md, documentos de requerimientos y diseño; fuentes del método identificadas. |
| ACT-REQ-01 | 29/08 | Documento con 35 requisitos y métodos de verificación; nueva matriz enlaza evidencia actual. |
| ACT-DIS-01 | 05/09 | Alternativa clásica documentada en sección 11 del diseño. |
| ACT-DIS-02 | 05/09 | Alternativa centrada en IA documentada y contrastada. |
| ACT-DIS-03 | 12/09 | Diseño híbrido elegido, arquitectura, datos, interfaces, estados y flujo definidos. Implementación trazable a componentes. |
| ACT-SW-01 | 19/09 | Carga, validación y reducción; entradas erróneas comprobadas. Captura real adaptada sin modificar original; conversión manual documentada. |
| ACT-PRU-01 | 26/09 | Cinco referencias sintéticas reproducibles y etiquetas; captura real disponible con condiciones declaradas, sin etiquetas mecánicas. |
| ACT-SW-02 | 26/09 | EVM configurable, selectividad, control estático y amplificación cero verificados; no EVM por fase. |
| ACT-SW-03 | 03/10 | Mismo flujo óptico en ambas ramas; traducción conocida y comparabilidad verificadas. |
| ACT-SW-04 | 10/10 | Mapas con escala común, métricas, CSV, NPY y gráfico; evidencia sintética y real. |
| ACT-SW-05 | 24/10 | MAD robusta con Isolation Forest auxiliar, separación referencia/evaluación, estados desactivado/insuficiente, cambio sintético detectado; no clasificación de daños. |
| **ACT-SW-06** | **31/10** | **Implementación cerrada técnicamente al corte actual:** comparación integrada, mapas, cuatro métricas, revisión y exportación explícita, resumen HTML, verificación de copias y recuperación. Evidencia de regresión, escritorio y captura real en esta carpeta. |
| ACT-PRU-02 | 07/11 | Programada 02–07/11; protocolo completo preparado. Las comprobaciones de esta semana se conservan como evidencia previa, no como trabajo con fecha futura. |
| ACT-PRU-03 | 14/11 | Programada 09–14/11. Hay tiempos por ejecución; falta campaña comparativa formal de recursos y rendimiento. |
| ACT-PRU-04 | 16/11 | Programada 09–16/11; se conservan correcciones y regresiones tempranas, sin declarar cerrada la integración final futura. |
| ACT-DOC-01 | 20/11 | Programada 16–20/11; documentación técnica actualizada continuamente, informe final aún no vencido. |
| ACT-PRE-01 | 21/11 | Programada 18–21/11. Presentación intermedia preservada; no se confunde con presentación final. |
| RSV-RIE-01 | 21/11 | Reserva 16 h; no se registra consumo sin horas reales. |

Estas filas distinguen disponibilidad del producto de la aceptación académica y del esfuerzo. No se asignan porcentajes ni fechas reales de terminación nuevas a trabajos antiguos. El Informe de Avance 2 declara cierres hasta el 30/10; se conserva como documento aportado, sin retrofechar las comprobaciones actuales ni validar automáticamente sus horas.

## Criterios de los entregables

| Entregable | Situación al cierre de la semana |
|---|---|
| ENT-INF-01 | Contexto, investigación, plan e informes parciales disponibles; el informe técnico final depende de pruebas de noviembre. |
| ENT-REQ-01 | Documento académico disponible y matriz de 35 requisitos actualizada. |
| ENT-DIS-01 | Diseño disponible con dos alternativas y selección; relación arquitectura/código registrada. |
| ENT-COD-01 | Código modular, dependencias fijadas, instrucciones, pruebas, revisión y GitHub privado. |
| ENT-PRO-01 | Flujo completo disponible, probado sintéticamente y con captura de teléfono; cierre técnico de implementación, no certificación de diagnóstico. |
| ENT-PRU-01 | Evidencias previas completas para el alcance ejecutado; campaña formal funcional/desempeño pendiente según cronograma. |
| ENT-EVI-01 | Paquetes sintéticos versionados y resultados reales locales trazables; no se publica la grabación del carro. |
| ENT-PRE-01 | Presentación final no vencida; existe presentación intermedia. |

## Trazabilidad de diseño

- Entrada/validación: `src/video_analysis/video/`.
- Configuración e integración: `pipeline.py`, `__main__.py`, `gui/main_window.py`.
- Magnificación: `magnification/eulerian.py`.
- Movimiento, métricas y mapas: `motion/`, `heatmaps/`, `export/charts.py`.
- Patrones: `anomalies/patterns.py`; reglas explicables e IA auxiliar, coherentes con el diseño híbrido.
- Visualización/comparación: `gui/main_window.py`, `gui/comparison.py`.
- Persistencia: `export/package.py`, `export/summary.py` y salida de `pipeline.py`.

No se identificó una función de SW-01 a SW-06 ausente respecto del plan. Permanecen límites de verificación que se detallan en la matriz y el protocolo siguiente, no se ocultan con una declaración de “todo perfecto”.
