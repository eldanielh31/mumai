# Revisión de alcance y coherencia documental

Corte: **2 de noviembre de 2026**. Solicitud de Daniel: contrastar el proyecto con
plan, diseño y documentación, corregir desviaciones y ampliar el README. Esta revisión
no cambia la línea base para acomodarla al código. No se hicieron commit ni push.

## Resultado

El flujo implementado corresponde al prototipo local del plan y al diseño híbrido.
**No se identificó una función que exigiera retirarse o sustituirse para volver al
alcance.** Las desviaciones encontradas estaban en la explicación de la presentación,
los enlaces a estados antiguos y la interpretación o separación de pendientes.
Se corrigieron mediante README, guías vigentes, índices y notas de coherencia.

Esto no significa que todo el proyecto esté terminado: PRU-03/04, documento final,
presentación y revisión académica mantienen sus actividades y calendario. La evidencia
funcional acredita el alcance probado, sin convertirlo en diagnóstico de daños.

## Fuentes y cobertura de revisión

- Plan de Proyecto: restricciones y objetivos §1.4–1.6; solución §2.1; ocho entregables
  §2.2; actividades, presupuesto y cronograma §2.3–2.5.
- Documento de Diseño v2: alcance §6.2; composición, dependencias, datos e interfaces
  §10.2–10.9; interacción, estados, algoritmos y recursos §10.10–10.13; alternativas §11.
- Requerimientos: alcance/interfaces §1.2–1.3; los 35 requisitos de §3 y sus métodos §4.
- Ficha, informes de avance, riesgos, guion y presentación; instrucciones, plantillas
  y referencias del curso; documentación Markdown y evidencia fechada de docs/.

Se inventariaron **61 documentos** iniciales entre Proyecto/ y docs/. Los **26 archivos
académicos originales** se pudieron extraer: PDF, DOCX y PPTX; los PDF suman **146 páginas**.
La lectura detallada de las fuentes normativas se complementó con búsqueda de
consistencia en las guías y antecedentes. La extracción no equivale a validar firmas,
horas o el cumplimiento de cada rúbrica del curso, ni a una auditoría visual de todas
las páginas. Se revisaron visualmente los diagramas principales: Plan, página 5;
Diseño, páginas 5, 6, 7, 9 y 10. La figura de flujo de Diseño §10.12 es una vista
simplificada; el texto conserva expresamente patrones opcionales y exportación.

[Inventario inicial](inventario-inicial.json), [lectura de originales](lectura-documentos.json)
y [cobertura de requisitos](cobertura-requisitos.json) conservan fuentes y alcance.
Los 35 identificadores del PDF coinciden con los de la matriz vigente, sin nuevos IDs.

## Trazabilidad de la solución

| Definición prevista | Implementación y documentación correspondiente | Decisión |
|---|---|---|
| Archivo local y validación; REQ-FUNC-001/002, INT-001 | video/loader.py; selector y metadatos; rechazo de entradas y punteros LFS | Dentro del alcance. No se requiere controlar una cámara. |
| Configuración; REQ-FUNC-003 | AnalysisConfig y controles de banda, amplificación, referencia y resolución | Son parámetros concretos de la implementación, no nuevos objetivos. |
| EVM; REQ-FUNC-004 | magnification/eulerian.py: luminancia, escala gaussiana y filtrado temporal causal | Implementa el método previsto; no se promete EVM por fase o ganancia geométrica exacta. |
| Misma medida en ambas ramas; REQ-FUNC-005 | Dos MotionAnalyzer con idéntico flujo Farnebäck y misma resolución/FPS | Original y magnificado son comparables en la escala de procesamiento. |
| Mapas/métricas; REQ-FUNC-006 | heatmaps/, motion/ y export/charts.py | Cuatro métricas, PNG, CSV y NPY concretan «al menos una métrica»; no cambian el entregable. |
| Patrones opcionales; REQ-FUNC-007 | anomalies/patterns.py: MAD robusta e Isolation Forest auxiliar, características del original | Diseño híbrido; TF/PyTorch condicionales. No se requiere añadir un clasificador de averías. |
| Consulta y comparación; REQ-FUNC-008 y USAB | gui/main_window.py y comparison.py: cuatro vistas, reproducción sincronizada | La interfaz sigue siendo el modo de usuario del diseño. |
| Exportación y trazabilidad; REQ-FUNC-009 e INF | export/package.py y summary.py; carpeta local, parámetros y huellas | HTML local y recibo de copia apoyan consulta/exportación; no son un servicio web nuevo. |
| Estados y recuperación; REQ-MOD/CONF | En espera, Entrada válida, Configurado, Procesando, Resultados disponibles y Error controlado | Conserva los seis estados y permite reiniciar/reintentar. |
| Linux, CPU y ejecución sin red; REQ-FIS/CAL | Python 3.13 en Ubuntu/WSL; pruebas aisladas y repetibilidad documentada | Compatible con la restricción local y GPU opcional. |
| Evidencia y entorno; REQ-MANT/CV, REND y AMB | Dependencias fijadas, pruebas, metadatos, condiciones y relojes registrados | PRU-03 medirá formalmente recursos; no se añaden umbrales arbitrarios. |
| Apoyo a inspección; REQ-SEG | Advertencias, límites, datos relativos a referencia; sin control físico | No diagnóstico certificado, inferencia de piezas dañadas ni calibración física. |

La matriz completa de [35 requisitos](../matriz-requisitos-2026-11-02.md) mantiene
la evidencia detallada de cada ID. La selección de biblioteca de IA, el número de
métricas y los formatos auxiliares están dentro de las decisiones de implementación
permitidas: no se borra trabajo útil solo por no aparecer como formato obligatorio.

El «Uso de patrones» de Diseño §10.6 trata patrones de colaboración de software;
su «No aplica» no elimina el módulo de análisis de patrones del §10.2 y del §11.
La consola y validadores son herramientas técnicas para repetir el mismo flujo,
no otro modo industrial o un nuevo servicio del producto.

## Hallazgos y correcciones

| Hallazgo | Corrección vigente |
|---|---|
| DOC-001: presentación describe tres alternativas distintas a las del Diseño §11 | Fe de erratas con clásico, IA centrada e híbrido seleccionado; guion de referencia corregido. |
| DOC-002: «Daño visible» y frases que exceden evidencia | Sustitución por movimiento visible y cambios respecto a referencia; límites explícitos en README y fe de erratas. |
| DOC-003: índices llamaban vigentes a varios cortes antiguos | docs/README y Proyecto/README separan fuentes, estado actual e historial; guías con estado actual al inicio. |
| DOC-004: faltaba explicar cómo utilizar los datos | README define cada archivo, unidades, filtro included, agregados P95/RMS, patrones, saturación, trazabilidad y ejemplo del motor. |
| DOC-005: referencia externa diagnóstica se confundía con un pendiente obligatorio del prototipo | Se distinguen etapas reales del plan de investigación diagnóstica adicional; no se inventa un entregable con fallas etiquetadas. |
| DOC-006: cronología, horas y «sin atrasos» entre fuentes no son conciliables automáticamente | Notas de coherencia; se preservan datos declarados, discrepancias y evidencia, sin reconstruir horas ni retrofechar pruebas. |

No se modifican plan, requisitos, diseño o informes fechados para ocultar diferencias.
Las [notas de coherencia](../../Proyecto/Informes/Notas_de_coherencia_documental_2026-11-02.md)
y la [fe de erratas](../../Proyecto/Presentacion/Fe_de_erratas_alcance_2026-11-02.md)
son la corrección vigente para leer y reutilizar esos antecedentes. La presentación
histórica no debe reutilizarse como explicación del diseño sin aplicar la fe de erratas.

## Entregables y pendientes conservados

| Entregable del plan | Estado dentro del alcance |
|---|---|
| ENT-INF-01, informe técnico | Antecedentes disponibles; documento final previsto 16–20/11. |
| ENT-REQ-01, requisitos | Documento original conservado y matriz de 35 IDs trazable. |
| ENT-DIS-01, diseño | Original conservado con dos alternativas y enfoque híbrido seleccionado. |
| ENT-COD-01, código documentado | Módulos identificables, versiones y README de funcionamiento/uso/datos. |
| ENT-PRO-01, prototipo | Flujo implementado y probado; no se atribuye aceptación externa. |
| ENT-PRU-01, reporte funcional y desempeño | Campaña funcional PRU-02 ejecutada; PRU-03 prevista 9–14/11 y PRU-04 9–16/11. |
| ENT-EVI-01, ejemplos | Referencias sintéticas identificadas y captura real con entrada/configuración trazables. |
| ENT-PRE-01, presentación final | Prevista 18–21/11; presentación intermedia conservada con correcciones de lectura. |

El presupuesto sigue siendo 192 h, con reserva de 16 h. Los números de tiempo de
procesamiento no se utilizan como AC ni se convierten en horas trabajadas. El método
funcional de CPU aislada se documenta como aceptado por Daniel; no modifica el requisito
de GPU opcional ni se presenta como aprobación de un tercero.

## Verificación de esta revisión

No hubo cambios de ejecución. Las huellas de los **37 archivos de src/, scripts/ y
tests/** registrados en el manifiesto de PRU-02 siguen iguales; esa versión pasó las
35 pruebas. No se repitió la suite por cambios exclusivamente documentales.
Los comandos de ayuda y carga del README se ejecutaron correctamente. Los ocho
promedios de las dos ramas se recalcularon desde el CSV real filtrado por included=1:
coinciden con informe.json; también se confirmaron la razón, saturación y los 14
archivos del recibo. Véase [verificación del README](verificacion-datos-readme.json).

La comprobación final conserva huellas de originales, enlaces, sintaxis de comandos,
entradas sin cambios y ausencia de commit/push. El manifiesto identifica esta nueva
revisión documental sin reescribir los manifiestos históricos.


[Comprobación final](validacion.json) y [manifiesto de esta revisión](manifiesto.json).
