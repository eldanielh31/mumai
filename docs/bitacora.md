# Bitácora de trabajo

No se registran horas de trabajo estimadas como si fueran horas reales. Fecha de esta sesión: 18 de octubre de 2026. Versión base de la auditoría: `2c9eaba`. Alcance autorizado: corregir hallazgos y documentar el trabajo para informes posteriores.

| Orden | Trabajo | Resultado / evidencia |
|---|---|---|
| 1 | Revisar auditoría, código, pruebas e instrucciones | Identificados seis hallazgos corregibles y pendientes de validación. |
| 2 | Separar revisión de exportación y controlar estados | Módulo de exportación, hilo de trabajo, estados visibles y reinicio. |
| 3 | Limpiar vistas anteriores | Caso de fallo de nuevo análisis ya no conserva mapas/métricas anteriores. |
| 4 | Añadir etiquetas y escala a PNG | Tres figuras con unidades y escala común, inspeccionadas visualmente. |
| 5 | Ajustar reloj | Tiempo incluye últimas salidas/publicación; campo de alcance y schema 2. |
| 6 | Completar instalación y guía de uso | Creación de entorno, instalación exacta, localización de Qt y eliminación de dependencia obligatoria de VS Code. |
| 7 | Pruebas de regresión | 25 casos aprobados, cuatro de interfaz ejecutados también en escritorio. |
| 8 | Repetir referencias | Cinco escenarios y siete criterios aprobados, sin modificar algoritmos/umbrales. |
| 9 | Instalar en entorno nuevo | Paquetes locales y dos pruebas integradas aprobadas; sistema operativo preexistente. |
| 10 | Verificar aislamiento de red, repetición y error de publicación | Evidencia en repetibilidad-sin-red.json; no se desconectó la red del usuario. |
| 11 | Confirmar disponibilidad de video real | Daniel respondió “No”; VAL-001 permanece abierto y se preparó protocolo. |
| 12 | Organizar documentación reutilizable | Índice, estado vigente, matriz de 35 requisitos, incidencias, decisiones, protocolos y plantillas. |

## Incidencias durante la verificación

- La ejecución nativa dentro del aislamiento no pudo conectarse al escritorio. Se repitió con acceso al display y pasó; ambos registros se conservan. No se infirió falta de bibliotecas a partir del mensaje genérico de Qt.
- El repositorio temporal de paquetes para la instalación inicialmente eligió una etiqueta Python 2 de un paquete compatible con Python 2/3. Se corrigió esa herramienta auxiliar y la instalación final pasó. No se modificaron las versiones fijadas del proyecto.
- Se intentó capturar una imagen antes de que terminara de generarse la evidencia; el archivo aún no existía. Se esperó la terminación y se repitió. No afectó al producto ni se registró esa captura incompleta como evidencia.

## Alcance y preservación

No se modificaron los PDF proporcionados ni archivos sincronizados en `sources/`. No se alteraron entregables históricos para cambiar su fecha o conclusión. No se inventaron horas, aprobación ni resultados reales. No se enviaron mensajes a terceros. La documentación actualiza el estado sin dar por terminadas las pruebas formales futuras.
