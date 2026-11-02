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

## Revalidación y guía manual — 21 de octubre de 2026

- Ante la consulta de Daniel, se repitió la suite completa: 31 pruebas aprobadas. Se repitieron los cinco escenarios de referencia con siete criterios aprobados.
- Se comprobaron adicionalmente reducción proporcional a 80×60, conservación de 20 FPS/400 fotogramas, entrada intacta, patrones desactivados y referencia insuficiente: cinco comprobaciones aprobadas en tres ejecuciones.
- Se prepararon 15 casos manuales con pasos, valores esperados, límites y una hoja en blanco para registrar la revisión de Daniel.
- Se encontró que el generador de evidencia mantenía una fecha fija del 18 de octubre y podía sobrescribir un resultado. Se corrigió para usar fecha de Costa Rica o fecha explícita y rutas nuevas; se verificó que rechaza una ruta existente sin modificarla.
- La aplicación y sus algoritmos no cambiaron en esta revisión. No se atribuyeron a Daniel pruebas que todavía no ejecutó.
- Se actualizó el procedimiento de publicación para continuar sin el plugin de GitHub, según su decisión. La publicación remota sigue pendiente de autenticación confirmada.

## Traslado al Escritorio — 23 de octubre de 2026

- A solicitud de Daniel, se trasladó el proyecto completo a `/home/daniel/Desktop/proyecto-final`, incluyendo Git, entorno, videos y resultados existentes.
- Se ajustaron los enlaces y rutas del entorno Python y la guía manual. La ubicación anterior conserva un enlace de compatibilidad hacia la única copia del proyecto en el Escritorio.
- No se modificaron algoritmos ni evidencias históricas. La verificación del traslado se guarda en `traslado-2026-10-23.txt`.

## Captura real de motor — 1 de noviembre de 2026

- Daniel aportó motor.mp4, grabado con su teléfono. Se validaron lectura completa y marcas temporales: el original se carga pero se rechaza al analizar por un intervalo inicial de 125,7 ms.
- Se conservó el original y se generó motor_30fps.avi, FFV1 a 30 FPS constantes, con 1644 fotogramas comprobados.
- Se ejecutó el flujo completo con amplificación 5 y se decidió probar 2 por saturación superior al 1 %. Configuraciones, resultados y límites se registran en motor-2026-11-01/. No se modificó código.
- Videos reales, derivados y salidas permanecen en data/, excluidos de Git; solo se versionan registros textuales. La carpeta no versionada Proyecto/ ya existía y no se modificó.

## Revisión y publicación — 1 de noviembre de 2026

- Daniel informó que la prueba del motor funciona y solicitó revisión de código, organización y publicación privada con todos los documentos de Proyecto.
- Se corrigieron INC-013 (recibo de reexportación) e INC-014 (fecha fija de SW-06), se eliminaron dos importaciones sin uso y se unificó el formato.
- Se verificaron 32 pruebas, nueve criterios de interfaz y la integridad de los documentos reorganizados. Evidencia en revision-2026-11-01/.
- Se autenticó GitHub CLI en la cuenta eldanielh31. La URL y estado verificado se mantienen en repositorio.md.

- Publicación privada comprobada: commit `c3842af2f4d3818be937a2a6961d09f46a8eca7c` coincide entre el repositorio local y GitHub. Se enviaron código, historial y los 26 documentos académicos, además de sus índices y evidencias.

## Cierre semanal 26/10–01/11 — ejecución del 1 de noviembre de 2026

- Se contrastaron las 19 actividades y ocho entregables del plan con requisitos, diseño, informes y código. SW-06 vence el 31/10; PRU-02 comienza el 2/11.
- Se completó la evidencia de cierre con 32 pruebas, siete pruebas nativas, cinco referencias/siete criterios y 18 comprobaciones del flujo real por interfaz. CSV, matrices, patrones y métricas reales resultaron idénticos a la ejecución previa.
- Se comprobó el flujo real en proceso sin interfaces de red externas ni dispositivos GPU accesibles; no se confundió con un equipo físicamente sin GPU. Exportación y conservación tras reinicio verificadas.
- Daniel confirmó Samsung Galaxy S25 Ultra, grabación del 28/10, soporte independiente, ralentí y aceleración; aprobación del plan declarada por el usuario. No se inventaron tiempos de aceleración ni normalidad del tramo inicial.
- Se añadieron script de repetibilidad, matriz vigente, conciliación del cronograma, protocolo PRU-02 y distribución de esfuerzo expresamente estimada. El registro de horas reales no se rellenó con cifras inventadas.
- Se preservaron PDFs/DOCX y matrices históricas. La aprobación automática inicialmente rechazó una escritura al interpretar que sustituía una matriz antigua; se comprobó su huella y se crearon archivos nuevos con escritura exclusiva. No quedó bloqueado el trabajo.
- Evidencia completa en cierre-semana-2026-11-01/. No se modificó el comportamiento de la aplicación ni se ejecutaron por anticipado las etapas finales como si ya estuvieran cerradas.
