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

## Sesión del 21 de octubre de 2026 — ACT-SW-06

- Se confirmó directamente en el plan la actividad del 19–31 de octubre y su presupuesto original de 12 horas; no se registran como horas reales.
- Se añadieron comparación integrada con navegación temporal, tabla de métricas, resumen HTML local e integridad de copias exportadas.
- Se corrigieron mensajes de apertura externa y destino temporal; el paquete exportado permanece después de reiniciar.
- Se ejecutaron 31 pruebas completas, seis de SW-06 también en escritorio y nueve criterios del flujo de demostración. Se conservaron capturas y paquete sintético completo.
- Se preparó una guía de captura y se actualizaron documentos de seguimiento. Captura real y aprobación siguen pendientes.
- Daniel autorizó GitHub privado. Se verificó que no había conexión autenticada ni remoto; publicación pendiente de conectar su cuenta. Se guardará el avance local con evidencia de versión.
- Se añadieron instrucciones persistentes de documentación y publicación en `AGENTS.md`. No se programó sincronización en segundo plano.
- Para revisar el HTML se levantó temporalmente un servidor solo en la computadora; el primer intento aislado no permitía abrir sockets, y se repitió con acceso local autorizado. El resumen fue revisado en navegador.

- La revisión de formato de Git señaló CRLF del CSV exportado como espacios finales. Se conservaron los bytes originales y se añadió una regla específica de atributos, en lugar de modificar la evidencia y sus huellas.
