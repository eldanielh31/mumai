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

## Verificación final y publicación — 1 de noviembre de 2026

- Base bfffc94: 32 pruebas nativas aprobadas en 7,588 s y cinco referencias con siete criterios aprobados. Revisión estática, formato y dependencias sin errores.
- Integridad comprobada antes de actualizar este índice: 202 archivos del cierre semanal, 26 documentos académicos, 14 archivos de exportación real y ambos videos intactos. No se repitió el análisis real en esta verificación.
- Se agregaron registros nuevos y lista de cambios acumulados en verificacion-final-2026-11-01/. Sin cambios funcionales adicionales; pendientes formales conservados.

## Publicación de entradas autorizada — 1 de noviembre de 2026

- Daniel solicitó incluir data/input/ en Git y mantener data/output/ excluido. Esta autorización sustituye la exclusión previa de las grabaciones de entrada.
- Se incorporaron ocho videos mediante Git LFS, incluidos motor.mp4 y motor_30fps.avi, y cinco JSON de referencias mediante Git normal. No se alteró el contenido de las entradas.
- Se actualizaron reglas de exclusión, atributos LFS, instrucciones de clonación y política del repositorio. Los resultados locales siguen excluidos; únicamente su marcador vacío permanece versionado.
- Sin cambios al código de la aplicación; la suite 32/32 del cierre anterior sigue siendo la referencia de pruebas funcionales. Esta entrega verifica almacenamiento e integridad, no repite el análisis.

## ACT-PRU-02 — ejecución del 2 de noviembre de 2026

- Se leyeron plan y diseño originales en Proyecto y se ejecutó el protocolo de pruebas funcionales de esta semana.
- Regresión final 35/35; cinco escenarios/siete criterios; M01–M15 por Qt/X11 con 51 comprobaciones; siete pruebas nativas de escritorio. No se suman repeticiones como requisitos nuevos.
- Se revisaron visualmente cuatro capturas sintéticas. M13 simula la respuesta de cancelación del selector, pero analiza, reproduce y exporta realmente. M15 canceló durante procesamiento al 5 %, sin resultados parciales y con recuperación.
- Repetición real sin red: 18/18 comprobaciones, igualdad exacta de CSV, patrones, matrices y métricas respecto de la exportación de Daniel; 212,996 s de procesamiento. Cuatro exportaciones verificadas mediante lectura completa de 12 videos, huellas y coherencia de métricas. Los 14 archivos de entrada quedaron intactos.
- Ensayo separado de 33 regresiones sin acceso a GPU ni red; dos pruebas de preparación añadidas después completan 35 en el entorno normal. No se confunde la ejecución real sin red con el ensayo de GPU bloqueada.
- INC-015: mensaje específico de descarga LFS pendiente y guía. INC-016: Python se comprueba antes de instalar paquetes, con dos pruebas de rechazo temprano.
- Daniel confirma luz de día, acepta justificar CPU en su equipo con RTX 3050 y mantiene público el repositorio con los videos del motor. Ordena no hacer commit ni push sin solicitud explícita; AGENTS actualizado. REP-002 resuelto por confirmación, sin cambiar la visibilidad.
- Se crean reporte en Proyecto/Informes, matriz de 35 requisitos, anexo de confirmaciones y paquete de evidencia nuevo. Se conservan originales académicos y auditorías. Las modificaciones previas del MP4 y del log de instalación no se sobrescriben.
- No se inventan horas, aprobación del profesor ni diagnóstico. PRU-03/04 y entrega final mantienen calendario. No se ejecutaron commit ni push.

## Contraste estricto de alcance y README — 2 de noviembre de 2026

- Se contrastaron plan, requisitos (35 IDs), diseño, ficha, informes, riesgos, guion, presentación y guías. Inventario inicial de 61 documentos; extracción de 26 originales académicos, incluidos 146 páginas PDF.
- Se comprobó que la arquitectura y el flujo implementados corresponden al diseño híbrido. TF/PyTorch son condicionales; cuatro métricas, HTML y recibos concretan consulta, resultados y trazabilidad, sin añadir un servicio externo.
- Se corrigió la explicación vigente de alternativas, «daño visible», cronograma y componente de captura en una fe de erratas con guion alineado; los originales fechados se conservaron. Se documentan diferencias de horas/fechas sin reconstruirlas.
- README renovado: alcance, funcionamiento, preparación WSL/LFS, parámetros sintéticos y motor, recuperación y explicación de todos los formatos exportados. Incluye filtros CSV, P95/RMS agregados, unidades, patrones, integridad y límites de interpretación.
- Índices y guías separan estado actual e histórico. Pendientes se limitan a PRU-03/04, documentación, presentación y revisión previstas; no se añade una campaña diagnóstica etiquetada como condición nueva de cierre.
- Código de ejecución sin cambios respecto de la versión que aprobó 35 pruebas; se validaron ayuda/carga y promedios del CSV real para documentar el uso de datos. Nueva evidencia en alcance-2026-11-02/.
- No se ejecutaron commit ni push y no se alteraron entradas, exportaciones previas ni horas registradas.

## Desempeño e integración del 9 de noviembre de 2026

- PRU-03 registró 17 análisis, seis casos, medición de tiempo/RSS/disco y comparación original/magnificado.
- PRU-04 completó 35 pruebas, 15 casos Qt, 7 criterios sintéticos y verificación de 19 paquetes.
- [Reporte y evidencia](pru03-pru04-2026-11-09/README.md). Las fechas del cronograma permanecen como línea base.
