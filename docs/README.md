# Documentación del proyecto

Estado vigente al **9 de noviembre de 2026**. Este índice separa la definición del
producto, las guías de uso, las pruebas y el historial. El repositorio actual es
público por autorización de Daniel, incluidos los videos del motor. **No hacer
commit ni push sin solicitud explícita de Daniel.**

## Alcance y fuentes vigentes

- [Plan, requisitos, diseño y documentos académicos](../Proyecto/README.md).
- [Revisión de alcance y trazabilidad del 2/11](alcance-2026-11-02/README.md).
- [Notas de coherencia documental](../Proyecto/Informes/Notas_de_coherencia_documental_2026-11-02.md).
- [Fe de erratas y guion alineado de presentación](../Proyecto/Presentacion/Fe_de_erratas_alcance_2026-11-02.md).

Plan, requisitos y diseño definen el prototipo local: entrada, EVM, medida compartida
de movimiento, mapas/métricas, patrones opcionales, comparación y exportación.
No se convierten diagnóstico mecánico, sensores, nube o entrenamiento con fallas
etiquetadas en nuevas condiciones de cierre. Los informes fechados conservan su corte.

## Uso y datos exportados

- [README: preparación, operación e interpretación de cada archivo](../README.md).
- [Guía de 15 casos manuales](guia-pruebas-manuales.md) y [hoja personal](plantillas/registro-prueba-manual.md).
- [Capturas nuevas y sus condiciones](guia-video-real.md).
- [Método y protocolos](metodologia-y-pruebas.md).
- [Validación del prototipo y límites](validacion-real-pendiente.md).

## Estado técnico y pendientes del plan

- [Reporte ACT-PRU-02](../Proyecto/Informes/Reporte_Pruebas_Funcionales_PRU02_2026-11-02.md).
- [Evidencia PRU-02: 35 pruebas, 15 casos y repetición real](pru02-2026-11-02/README.md).
- [Matriz vigente de los 35 requisitos](matriz-requisitos-2026-11-09.md).
- [Desempeño e integración PRU-03/04](pru03-pru04-2026-11-09/README.md).
- [Confirmaciones: luz de día, método CPU y política Git](pru02-2026-11-02/confirmaciones-daniel.json).

SW-01 a SW-06 están implementadas y PRU-02 tiene campaña técnica ejecutada el 2/11.
PRU-03 y PRU-04 se completaron técnicamente el 9/11 dentro de sus ventanas del plan.
La documentación final está prevista para 16–20/11 y la presentación para 18–21/11. La revisión académica se registra cuando
exista. Los tiempos automáticos no se convierten en horas reales de ingeniería.

## Seguimiento y registros

- [Bitácora](bitacora.md), [incidencias](registro-incidencias.md) y [decisiones](decisiones.md).
- [Estado del repositorio y política vigente](repositorio.md).
- [Registro de horas reales](registro-horas.csv), sin completar con estimaciones.
- [Plantilla de informe](plantillas/informe-avance.md) y [sesión de pruebas](plantillas/sesion-pruebas.md).

## Historial y evidencia conservada

Estos documentos describen su fecha; no sustituyen el estado vigente anterior.

| Corte | Documentos y evidencia |
|---|---|
| 6 de octubre | [Avance inicial](avance-2026-10-06.md). |
| 18 de octubre | [Avance](avance-2026-10-18.md), [auditoría original](auditoria-2026-10-18.md), [correcciones](correcciones-2026-10-18/README.md), [estado corregido](estado-2026-10-18-corregido.md), [matriz](matriz-requisitos-2026-10-18.md). |
| 21 de octubre | [SW-06](avance-2026-10-21-sw06.md), [ejemplo sintético completo](sw06-2026-10-21/README.md), [revalidación de dependencias](verificacion-sw01-sw04-sw05-2026-10-21/README.md), [matriz](matriz-requisitos-2026-10-21.md). |
| 1 de noviembre | [Revisión](revision-2026-11-01/README.md), [motor](motor-2026-11-01/README.md), [cierre semanal](cierre-semana-2026-11-01/README.md), [verificación final](verificacion-final-2026-11-01/README.md), [matriz](matriz-requisitos-2026-11-01.md). |

La [conciliación de actividades y entregables](cierre-semana-2026-11-01/cronograma-y-entregables.md)
y el [protocolo PRU-02](cierre-semana-2026-11-01/protocolo-pru02.md) se conservan con
su fecha de preparación. Las [estimaciones de esfuerzo](cierre-semana-2026-11-01/esfuerzo-estimado.md)
no son horas reales. La copia del [plan original](referencias/Plan_de_Proyecto_Daniel_Brenes.pdf)
permanece disponible. No se borran auditorías por contener hallazgos ya corregidos.

## Cómo mantener el historial

Crear una carpeta nueva por revisión. Registrar problema, causa, solución, requisito,
prueba y pendiente; conservar versiones anteriores. Distinguir implementado, probado
en simulación, probado con captura y aceptado. Identificar versión por commit o
manifiesto, sin inventar porcentajes, horas, aprobación o datos de cámara.

`data/input/` contiene las entradas autorizadas con Git LFS. `data/output/` conserva
resultados locales y sigue excluido del versionado, salvo su marcador vacío. Los
pequeños ejemplos sintéticos de documentación mantienen su excepción. No publicar
otras grabaciones, imágenes privadas o resultados reales por esa excepción.
