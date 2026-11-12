# Fe de erratas de alcance de la presentación intermedia

Revisión del **2 de noviembre de 2026**. Fuentes de alcance: Plan de Proyecto,
secciones 1.4–1.6 y 2.1–2.5; Diseño v2, secciones 6.2, 10 y 11; Requerimientos,
secciones 1.2, 1.3, 3 y 4. Esta fe de erratas corrige la explicación vigente sin
atribuir cambios a la fecha de la exposición ni modificar sus archivos originales.

## Textos que deben sustituirse al reutilizar la presentación

| Ubicación histórica | Discrepancia | Texto o criterio corregido |
|---|---|---|
| PPTX, diapositiva 1: «Video de maquinaria → EVM → Daño visible» | EVM hace más visibles variaciones; no demuestra daño. | «Video local → EVM → Movimiento visible». La interpretación de posibles daños requiere revisión adicional. |
| PPTX, diapositiva 4 y guion, sección 3 | El objetivo general se reduce a diseñar y los cinco objetivos no corresponden exactamente al plan. | Objetivo general: desarrollar el sistema de análisis con EVM, medición, mapas y patrones para apoyar la identificación no invasiva de comportamientos potencialmente anómalos. Objetivos específicos: arquitectura modular; EVM/medición comparable; mapas/métricas; patrones/IA; evaluación controlada. |
| PPTX, diapositiva 5 y guion, sección 4 | Presentan revisión manual, sistema EVM y sensores como tres alternativas. | El Diseño §11 compara dos alternativas: procesamiento clásico y enfoque centrado en IA. Selecciona un enfoque híbrido que conserva EVM, medición comparable, mapas/métricas y patrones opcionales. Los sensores externos no son una alternativa seleccionada del diseño aprobado. |
| PPTX, diapositiva 6 | El esquema abreviado omite la medida compartida de movimiento y puede hacer parecer obligatoria la IA. | Carga/validación y configuración; ramas original/EVM; misma medida de movimiento en ambas; mapas/métricas; patrones opcionales desde características; consulta y exportación con configuración. |
| PPTX, diapositiva 7: separación de «captura» | Puede interpretarse como control de cámara dentro del producto. | «Carga de archivos locales, preprocesamiento, EVM, análisis y exportación». La cámara produce los archivos fuera de la aplicación. |
| PPTX, diapositiva 9 y guion, sección 8: «al día con el cronograma y sin atrasos importantes» | No concuerda con el retraso y SPI 0,46 que declara el Informe 1 al 11/10. | «El avance se contrasta con el cronograma mediante los informes de cada periodo; se conservan las desviaciones registradas». No se afirma puntualidad general ni se trasladan pruebas posteriores a esa fecha. |
| Guion, secciones de cierre y preguntas | «Validar resultados» puede confundirse con certificar daños o añadir una campaña diagnóstica obligatoria. | «Verificar las funciones, comparar resultados y documentar desempeño y límites dentro de las actividades PRU-02/03/04». |

## Guion de referencia alineado

Este texto sirve para explicar el alcance actual; no representa una nueva aprobación
académica ni sustituye la presentación final programada para noviembre.

**Propósito.** Desarrollamos un prototipo local que procesa videos de maquinaria o
estructuras para hacer visibles y medir movimientos sutiles. Sus resultados ayudan
a decidir qué observación merece revisión; no certifican daños.

**Diseño.** Se compararon una alternativa clásica y otra centrada en IA. Se seleccionó
un enfoque híbrido: EVM y medición interpretable, con patrones opcionales. La aplicación
sigue funcionando cuando esa evaluación se desactiva. El diseño no obliga a usar
TensorFlow o PyTorch cuando el método seleccionado no los necesita.

**Flujo.** El usuario carga un archivo ya capturado y configura parámetros. El sistema
valida, prepara una rama original y otra magnificada, y aplica el mismo flujo óptico
a ambas. Genera mapas, métricas y cambios respecto a una referencia inicial cuando
hay datos suficientes. El usuario revisa los resultados y solicita su exportación.

**Resultados.** Los videos muestran la comparación; los mapas localizan movimiento;
el CSV conserva mediciones por fotograma; los JSON identifican entrada, parámetros,
versiones y eventos. Los colores y alertas no identifican automáticamente una pieza
averiada, una magnitud física calibrada o una causa mecánica.

**Estado al 2 de noviembre.** SW-01 a SW-06 están implementadas y PRU-02 tiene campaña
técnica ejecutada: 35 regresiones, 15 casos funcionales y 18 comprobaciones del motor.
Se conserva el historial de retrasos y no se atribuye aceptación al profesor.

**Cierre previsto.** PRU-03 medirá desempeño y recursos; PRU-04 consolidará integración
y regresión. Después se completarán informe técnico, evidencia y presentación final.
No se incorporan nube, sensores, control industrial, clasificación de averías ni
nuevos entregables para cerrar el alcance existente.

Los DOCX/PPTX históricos se conservan como evidencia de lo aportado; para explicar el
producto hoy se utiliza este guion junto al README y al diseño. Antes de reutilizar
las diapositivas originales hay que aplicar las sustituciones de esta fe de erratas.
