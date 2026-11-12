# Decisiones de implementación

Lectura vigente al 2 de noviembre: las decisiones fechadas conservan su contexto.
La política actual permite el remoto público con entradas autorizadas y prohíbe
commit/push sin solicitud explícita de Daniel; sustituye DEC-013 para el repositorio
actual. La [revisión de alcance](alcance-2026-11-02/README.md) mantiene plan, diseño y
requisitos como base, sin ampliar los entregables.


Fecha: 18 de octubre de 2026. Relación con el registro: INC-001 a INC-006.

| ID | Decisión y motivo | Consecuencia / límite |
|---|---|---|
| DEC-001 | Separar análisis temporal de exportación interactiva para ajustarse al diseño. | Permite revisar antes de guardar; hay que exportar antes de cerrar o reiniciar. |
| DEC-002 | Conservar el análisis actual si falla su exportación. | Se puede reintentar sin recalcular; mensaje explícito evita confundirlo con exportación exitosa. |
| DEC-003 | Invalidar la vista al cambiar parámetros o iniciar nuevo análisis. | Impide atribuir métricas anteriores a una configuración nueva; archivos exportados no se borran. |
| DEC-004 | Publicar exportaciones nuevas mediante carpeta temporal y renombrado, sin sobrescritura. | Requiere espacio para otra copia. Cancelación se comprueba entre archivos y antes de publicación. |
| DEC-005 | Incluir leyendas dentro de PNG manteniendo matrices NPY separadas. | Figuras comprensibles fuera de la aplicación; datos numéricos sin decoración. |
| DEC-006 | Mantener Python 3.13 como entorno verificado y requerir instalación explícita del intérprete. | No añadir repositorios del sistema ni prometer compatibilidad con versiones no probadas. |
| DEC-007 | Medir hasta publicación y declarar el alcance del reloj en el informe. | Escritura de la medición y exportación manual posterior excluidas de forma expresa. |
| DEC-008 | Conservar auditoría y resultados previos; añadir nueva matriz y evidencias. | Los informes históricos conservan su contexto; usar documento vigente para estado actual. |

No se alteraron el algoritmo EVM, parámetros de flujo óptico ni umbrales de patrones. Las correcciones se concentran en presentación, manejo de estados, exportación, instalación, medición y documentación. No se añadieron diagnóstico mecánico certificado ni control de maquinaria.

## Decisiones del 21 de octubre — SW-06

| ID | Decisión | Motivo y límite |
|---|---|---|
| DEC-009 | Reproducir el video compuesto con OpenCV y un reloj de interfaz | Mantiene ambas mitades sincronizadas y evita agregar dependencias multimedia. Puede saltar imágenes de visualización si el equipo se retrasa; no altera el cálculo. |
| DEC-010 | Resumen HTML local, sin recursos externos | Permite revisión/impresión y anexos sin servidor ni internet. Mantener la carpeta completa. Texto de entrada escapado. |
| DEC-011 | Verificar copias mediante SHA-256 antes de publicarlas | Detecta diferencias de contenido en la exportación. No certifica validez física de los resultados. |
| DEC-012 | Incluir un paquete pequeño sintético en documentación | Facilita revisar el entregable recién clonado sin publicar capturas reales. |
| DEC-013 | GitHub privado, historial local hasta conexión | Preferencia explícita de Daniel. No inventar URL ni afirmar subida sin confirmación remota. |

## Decisiones de alcance del 2 de noviembre de 2026

| ID | Decisión | Fundamento y límite |
|---|---|---|
| DEC-014 | Mantener criterio robusto e Isolation Forest auxiliar, sin añadir TensorFlow/PyTorch obligatorios. | Plan §1.4 y Diseño §11 permiten patrones/IA cuando corresponda; el enfoque elegido es híbrido, no clasificación supervisada de averías. |
| DEC-015 | La consola y los validadores son herramientas de reproducción del mismo flujo, no un servicio o modo adicional del producto. | El usuario principal opera en la interfaz con los seis estados del diseño. No se añade nube ni ejecución industrial en vivo. |
| DEC-016 | Corregir las alternativas y el lenguaje de la presentación en una fe de erratas vigente. | Se conservan archivos fechados; el alcance se rige por plan, requisitos y diseño, no por una diapositiva contradictoria. |
| DEC-017 | Separar validación funcional/desempeño de investigación diagnóstica futura. | No se exige un conjunto de fallas etiquetadas como entregable adicional; tampoco se afirma exactitud de diagnóstico sin datos. |
| DEC-018 | Explicar agregación y unidades de todos los datos exportados en README. | P95 y RMS del resumen son promedios temporales de estadísticas espaciales; los valores son de píxeles de procesamiento y las alertas son relativas a referencia. |
