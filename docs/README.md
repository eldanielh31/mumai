# Documentación del proyecto Daniel Proyecto Final

Este índice reúne evidencia reutilizable para informes, seguimiento del cronograma y entrega final. Fecha de actualización: **21 de octubre de 2026**.

## Cómo probar y estado de las dependencias

- [Guía manual completa para Daniel: 15 casos](guia-pruebas-manuales.md).
- [Hoja para registrar tus resultados](plantillas/registro-prueba-manual.md).
- [Revalidación de SW-01, SW-04 y SW-05](verificacion-sw01-sw04-sw05-2026-10-21/README.md).

## Entrega vigente

- [Avance de SW-06, 19–31 de octubre](avance-2026-10-21-sw06.md).
- [Matriz de los 35 requisitos al 21 de octubre](matriz-requisitos-2026-10-21.md).
- [Evidencia y ejemplo completo](sw06-2026-10-21/README.md).
- [Qué video grabar o conseguir](guia-video-real.md).
- [Estado del repositorio privado](repositorio.md).

## Documentación de base e historial

1. [Estado actual después de las correcciones](estado-2026-10-18-corregido.md): qué funciona, qué se corrigió y qué falta comprobar.
2. [Registro de incidencias](registro-incidencias.md): problema, causa, impacto, solución, requisitos, evidencia y criterio de cierre.
3. [Bitácora de trabajo](bitacora.md): cambios realizados y pruebas, sin inventar horas trabajadas.
4. [Decisiones de implementación](decisiones.md): motivos y límites de las soluciones elegidas.
5. [Matriz actual de requisitos](matriz-requisitos-2026-10-18.md): los 35 requisitos después de corregir.
6. [Pendientes de validación real](validacion-real-pendiente.md): datos necesarios y procedimiento para completar la evidencia.
7. [Plantilla de informe de avance](plantillas/informe-avance.md): estructura para informes futuros.
8. [Plantilla de sesión de pruebas](plantillas/sesion-pruebas.md): condiciones, resultados, archivos y anomalías.

## Evidencia conservada

- [Auditoría original](auditoria-2026-10-18.md) y carpeta `auditoria-2026-10-18/`: diagnóstico de la versión anterior. Se conservan sin reescribir sus conclusiones históricas.
- [Evidencia de correcciones](correcciones-2026-10-18/README.md): registros automáticos, instalación nueva, interfaz y mapas revisados.
- [Avance anterior](avance-2026-10-18.md), `tests-2026-10-18.txt`, `interfaz-2026-10-18.txt` y `validacion-2026-10-18.json`: resultados anteriores a estas correcciones. Sus instrucciones de interfaz corresponden a aquella versión.
- [Metodología y pruebas](metodologia-y-pruebas.md): fundamentos y protocolo.
- [Plan original](referencias/Plan_de_Proyecto_Daniel_Brenes.pdf): línea base de fechas. Recuperar funciones no elimina retrasos históricos.
- [Registro de horas](registro-horas.csv): completar únicamente con horas reales conocidas.

## Cómo mantener este historial

Por cada cambio relevante: asignar una incidencia o decisión, describir antes/después, vincular requisitos y actividad del plan, guardar las pruebas en una **carpeta nueva**, actualizar la matriz y registrar los pendientes. No sustituir registros anteriores para que parezca que una corrección ya existía.

Para un informe, utilizar el estado correspondiente a su fecha de corte. Distinguir **implementado**, **probado en simulación**, **probado con captura real** y **aceptado por la contraparte**. No convertir cantidad de pruebas en porcentaje de cumplimiento, ni tiempo automático de procesamiento en horas de trabajo. Identificar el commit o conservar un manifiesto de archivos de la versión probada.

Las grabaciones y resultados de trabajo permanecen en `data/` y no se versionan. La excepción documentada es el pequeño ejemplo sintético de SW-06. Los resultados pequeños y los generadores sí quedan en la documentación. No incluir videos privados o datos de terceros en un informe público sin revisar su contenido.
