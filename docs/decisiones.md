# Decisiones de implementación

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
