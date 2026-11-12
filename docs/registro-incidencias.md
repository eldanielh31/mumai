# Registro de incidencias y acciones

Corte: 18 de octubre de 2026. Origen: auditoría de requisitos y diseño sobre `2c9eaba`. El cierre técnico significa corrección verificada en el alcance descrito; no sustituye la aceptación del proyecto.

| ID | Hallazgo | Estado | Requisitos / diseño | Evidencia de cierre |
|---|---|---|---|---|
| INC-001 | Resultados anteriores visibles tras fallo de nuevo análisis | Corregido y probado | USAB-002, CONF-001 | Prueba de interfaz: éxito → nuevo análisis fallido → mapas/gráfico/métricas vacíos. |
| INC-002 | Estados incompletos y retorno a En espera no explícito | Corregido y probado | MOD-001/002, diseño §10.11 | Se recorren los seis estados; reinicio vuelve a En espera y conserva exportaciones. |
| INC-003 | Mapas PNG sin etiquetas ni escala incorporadas | Corregido; inspección visual realizada | USAB-003 | PNG individuales/comparativo con título, unidades y barra común. |
| INC-004 | Análisis y exportación unidos | Corregido y probado | FUNC-008/009, INF-002, diseño §10.10 | Revisión temporal previa, exportación explícita, fallo/reintento/cancelación sin sobrescribir. |
| INC-005 | Instalación presupone entorno Python existente | Corregido; probado nuevo entorno Python | CV-001, MANT-002 | Instalación exacta desde paquetes locales y ejecución integrada en entorno nuevo. Sistema operativo nuevo no ensayado. |
| INC-006 | Tiempo excluye últimas escrituras/publicación | Corregido y probado | REND-001 | Prueba con demora artificial en última salida; medición tomada después de publicación. |
| VAL-001 | Falta video de cámara convencional | Pendiente de material real | FIS-001, AMB-001/002 | No hay evidencia real incorporada. Ver protocolo y criterios abajo. |
| VAL-002 | Ensayo físico en equipo sin GPU | Pendiente de equipo/evidencia | FIS-002, método de verificación | Código y pruebas CPU; no afirmar prueba en equipo físicamente sin GPU. |
| VAL-003 | Evaluación formal y aceptación | Programado para fases del plan | PRU-02/03/04, DOC-01 | Las pruebas actuales no sustituyen evaluación formal de noviembre ni aprobación de contraparte. |

## INC-001 — Resultados obsoletos

**Antes y causa:** `start_analysis` desactivaba botones pero no borraba las visualizaciones. Un fallo posterior dejaba la imagen y métricas de una ejecución previa.

**Impacto:** interpretación equivocada de qué ejecución produjo los datos, aun cuando el mensaje sí decía que había error.

**Solución:** centralizar la limpieza de resultados; ejecutarla al cargar, modificar parámetros o iniciar otro análisis. Borrar también referencias de exportación en la sesión. Después de un error de exportación se conserva deliberadamente el análisis actual y se indica que puede reintentarse: esto no es un resultado anterior de otro análisis.

**Prueba:** `test_review_export_error_recovery_and_states`; comprueba los tres elementos visuales vacíos después de provocar fallo de análisis. Los archivos ya exportados permanecen intactos.

## INC-002 — Estados

**Antes:** mensajes informales y recuperación mediante nueva carga; sin secuencia explícita ni acción de retorno.

**Solución:** indicador separado de estado: En espera, Entrada válida, Configurado, Procesando, Resultados disponibles y Error controlado. Acción Validar configuración; botón Volver a En espera. Los controles incompatibles quedan deshabilitados mientras trabaja un proceso. La lectura inicial permanece En espera hasta aceptar una entrada válida; su actividad se explica en el mensaje.

**Prueba:** secuencia de estados, fallo de exportación, reintento y reinicio. El reinicio descarta resultados temporales, no exportaciones.

## INC-003 — Mapas

**Antes:** la interpretación dependía de la ventana o LEEME; PNG aislado sin contexto.

**Solución:** figuras independientes con títulos Original/Magnificado, barra y unidades px/fotograma; mismo mínimo y máximo para los dos mapas. Los archivos NPY mantienen los valores originales; decoración no altera las métricas.

**Prueba:** cinco referencias siguen pasando; inspección visual de mapas individual/comparativo y captura de ventana. Evidencia PNG en `correcciones-2026-10-18/`.

## INC-004 — Revisión antes de exportar

**Antes:** el análisis guardaba directamente en la carpeta definitiva y luego permitía consulta.

**Solución:** análisis en directorio temporal privado de la sesión; resultados consultables; botón Exportar resultados con selector de destino. Copia en carpeta temporal del destino y publicación al terminar. Cada exportación recibe nombre único. Hilo de exportación para mantener respuesta de la ventana. Ante error se limpia la copia parcial y se preserva el análisis revisable.

**Pruebas:** no hay exportación permanente antes de solicitarla; se conservan los datos al reintentar; error de copia no deja paquete parcial; dos exportaciones no se sobrescriben; cancelación no publica salida.

**Límite explícito:** el análisis sin exportar es temporal y se descarta al cerrar/reiniciar. La ventana y README lo indican. La consola mantiene análisis y guardado en una sola orden, adecuado para ejecución por lotes; la separación solicitada por el diseño se implementa en el flujo interactivo.

## INC-005 — Instalación

**Antes:** se activaba `.venv` sin crearlo ni instalar requisitos, y se suponía la ruta de Qt bajo Python 3.13. La verificación también exigía VS Code aunque no es necesario para usar el producto.

**Solución:** crear entorno cuando falta, instalar `requirements.txt`, comprobar versión, dependencias, Qt/códecs y localizar plugin Qt dinámicamente. Separar paquetes de sistema mediante `--skip-system`. Documentar Python 3.13 como prerrequisito explícito y permitir rutas de intérprete/entorno. Retirar VS Code como condición de ejecución.

**Prueba:** entorno nuevo `/tmp/daniel-install-clean`; instalación de todas las versiones fijadas usando paquetes locales y pruebas de análisis/interfaz. No se reemplazó `.venv` ni se reinstalaron paquetes del sistema.

**Límite:** no se hizo instalación completa de Ubuntu desde cero. Las bibliotecas del sistema y Python 3.13 ya estaban disponibles. Primer intento del repositorio local de prueba tenía un nombre de paquete compatible solo con Python 2; se corrigió la selección de etiqueta de la herramienta temporal y se repitió con éxito. No fue fallo del instalador del proyecto.

## INC-006 — Duración

**Antes:** el reloj se leía antes de escribir informe/LEEME y publicar la carpeta.

**Solución:** medición monotónica después de las escrituras y publicación. `informe.json` schema 2 define `timing_scope`; la persistencia de la propia medición queda fuera del intervalo por definición. Si falla esa escritura se retira la carpeta recién creada y no se devuelve éxito.

**Prueba:** retraso artificial de 150 ms en LEEME y comparación con reloj externo. El tiempo incluye esa demora. Se conserva el límite de que exportar manualmente es una copia posterior y no pertenece al tiempo de cálculo.

## Pendientes y criterio de cierre

**VAL-001:** recibir video real con procedencia y condiciones; ejecutar flujo, revisar calidad, comparación y anomalías con referencia independiente; guardar parámetros, hash, evidencia y conclusiones. No se puede cerrar con otro video sintético.

**VAL-002:** ejecutar funciones principales en equipo documentado sin GPU y conservar especificaciones y resultados. CPU en equipo con GPU no demuestra literalmente ese método de verificación.

**VAL-003:** completar protocolos de noviembre, mediciones de desempeño y registros de aceptación. No hay aprobación de contraparte registrada y no se ha enviado ninguna comunicación externa.

## Seguimiento del 21 de octubre — SW-06

| ID | Problema u oportunidad | Acción | Estado / evidencia |
|---|---|---|---|
| INC-007 | Dependencia de reproductor externo para ver la comparación | Reproductor integrado sincronizado, pausa y búsqueda temporal; aviso si apertura externa falla | Corregido; pruebas de reproducción, búsqueda y recuperación. |
| INC-008 | Métricas completas poco accesibles y anexos manuales | Tabla de cuatro indicadores y resumen HTML local con imágenes/configuración/límites | Implementado; comparación con JSON e inspección visual. |
| INC-009 | Una copia corrupta podía publicarse sin comparación con la fuente | Verificación SHA-256 por archivo y recibo de exportación, limpieza si no coincide | Corregido; corrupción inducida rechazada y recibo del ejemplo verificado. |
| INC-010 | La ventana seguía indicando análisis pendiente después de exportar | Actualizar ruta y estado; impedir exportar dentro de sesión temporal que se eliminará | Corregido; flujo y destino temporal probados. |
| REP-001 | No existe conexión autenticada para crear/subir a GitHub | Preparación local, solicitud de conexión y elección privada confirmada | Pendiente; `repositorio.md`. No es una falla del análisis. |

La entrada de INC-008 es una mejora de consulta de SW-06, no una afirmación de que antes faltaran métricas numéricas. Los resultados de las incidencias anteriores permanecen como historial. VAL-001, VAL-002 y VAL-003 siguen abiertos.

## INC-011 — Fecha y preservación de evidencia de referencias

Detectado en la revalidación del 21 de octubre: el generador de referencias escribía la fecha fija `2026-10-18` y permitía reemplazar archivos de evidencia. Esto afectaba la trazabilidad documental, no el resultado del algoritmo.

Corregido: fecha predeterminada de Costa Rica con opción explícita `--date`, nombre nuevo por defecto y rechazo de rutas existentes antes de procesar. Se guardaron referencias con corte correcto y se comprobó que un intento de reemplazo no modifica sus bytes. Evidencia: `verificacion-sw01-sw04-sw05-2026-10-21/proteccion-historial.json`. Los registros antiguos se conservaron.

## INC-012 — Temporización de la captura real del teléfono

1 de noviembre de 2026: motor.mp4 se decodifica, pero el análisis rechaza el intervalo inicial de 0,1257 s. La carga y la comprobación temporal ocurren en fases distintas; no se debe interpretar carga válida como análisis garantizado. Se creó una copia derivada a 30 FPS sin cambiar el original ni relajar el control del programa. Copia verificada: 1644 fotogramas, 54,8 s. Adaptación de esta entrada resuelta; no se añadió conversión automática a la interfaz. Actividades relacionadas: SW-01 y prueba del flujo SW-02–SW-06. Evidencia y procedimiento: motor-2026-11-01/README.md.

## Revisión del 1 de noviembre de 2026

- **INC-013 — Recibo inconsistente al reexportar:** reproducido mediante prueba; se excluye el recibo previo y se genera uno nuevo. Regresión aprobada.
- **INC-014 — Fecha fija en validación SW-06:** reemplazada por fecha de Costa Rica u opción explícita; flujo comprobado con corte 2026-11-01.

Detalles y evidencia en [revisión de código](revision-2026-11-01/README.md).

## Estado consolidado — cierre del 1 de noviembre de 2026

INC-001 a INC-011 e INC-013/014 conservan sus correcciones y regresiones; INC-012 se resolvió para la entrada mediante copia a FPS constantes, sin conversión automática en el producto. No se identificó un nuevo defecto de implementación en este cierre.

REP-001 queda **resuelto**: GitHub privado conectado y publicado. VAL-001 avanza a captura real documentada y repetibilidad exacta comprobada; siguen sin existir etiquetas de fallas ni intervalos de aceleración/RPM confirmados. VAL-002 tiene ejecución funcional sin acceso a GPU, pero falta el método físico literal o aceptación de equivalencia. VAL-003 conserva las fechas de noviembre; no se atribuye a Daniel la ejecución de todos los casos manuales. Véase [cierre semanal](cierre-semana-2026-11-01/README.md).

## ACT-PRU-02 — 2 de noviembre de 2026

### INC-015 — Punteros Git LFS confundidos con videos dañados

Daniel informó que los ejemplos no abrían tras clonar. Se comprobó que los AVI de
132 bytes contenían punteros LFS; no eran los videos reales. Git LFS no funcionaba
en ese Ubuntu. La descarga con LFS recuperó los archivos; Daniel confirmó después
que pudo ejecutar y exportar motor_30fps.avi. Se conserva el motor.mp4 que repuso.
La aplicación ahora informa descarga pendiente antes de intentar decodificar un
puntero. README incorpora preparación LFS y exclusión de una entrada reemplazada.
Regresión: test_lfs_pointer_reports_missing_download_before_decoding.
Requisitos: REQ-FUNC-002, REQ-CONF-001, REQ-MANT-002, REQ-CV-001.

### INC-016 — Preparación instalaba paquetes antes de comprobar Python

El script ejecutaba apt/sudo antes de detectar que faltaba Python 3.13. Ubuntu tenía
3.12.3 y el primer intento no podía crear el entorno. Se mueve la comprobación del
intérprete al inicio, manteniendo versiones y sin descargar un intérprete por cuenta
del proyecto. Se documenta PROJECT_PYTHON para una instalación mediante uv. Dos
pruebas reproducen intérprete ausente/incompatible y comprueban que no se invoca
la instalación del sistema ni se crea el entorno. REQ-MANT-002 y REQ-CV-001.

### REP-002 — Visibilidad del remoto actual distinta de la política privada

La API de GitHub muestra el remoto actual eldanielh31/mumai como público. El histórico
se refiere a otro nombre de repositorio privado. No se supone que la privacidad
anterior siga vigente. Se pidió aclaración a Daniel; no se cambia la visibilidad ni
se publica esta entrega sin resolverlo. Evidencia: pru02-2026-11-02/remoto.json.

Las evidencias y el alcance de las pruebas nuevas se conservan en
[PRU-02](pru02-2026-11-02/README.md). No se alteran las conclusiones históricas.

### Confirmación posterior de Daniel en la sesión del 2 de noviembre

REP-002 resuelto: Daniel confirma repositorio público y videos del motor públicos.
No se cambia la visibilidad. Nueva política persistente: no hacer commit ni push
salvo solicitud explícita; queda actualizada en AGENTS.md. No se ejecutó ninguna
de esas acciones en esta sesión.

VAL-002 se verifica mediante equivalencia funcional acordada con Daniel: esta
computadora tiene una RTX 3050 según su declaración y permite justificar el uso de
CPU. La regresión aisló GPU y red mediante namespaces, /dev/dri vacío y /dev/dxg
sustituido por /dev/null; el resto del equipo conserva su GPU. No se atribuye
aprobación al profesor. Para VAL-001 se confirma luz de día; exposición, RPM e
intervalos exactos siguen desconocidos. Confirmaciones en pru02-2026-11-02/.

## Revisión de alcance y documentación — 2 de noviembre de 2026

DOC-001 a DOC-006 se registran en [alcance-2026-11-02](alcance-2026-11-02/README.md):
alternativas de presentación ajenas al Diseño §11, lenguaje de daño no demostrado,
estados antiguos llamados vigentes, uso de datos exportados sin explicar,
validación diagnóstica confundida con entregable y divergencias de cronología/esfuerzo.
Se corrigen README, guías e índices y se añaden fe de erratas y notas de coherencia.
Los documentos académicos originales y las evidencias fechadas se conservan.
No se identificó un desvío funcional que exigiera cambiar algoritmos o retirar módulos;
no se amplía el alcance con sensores, nube, clasificación de averías o nuevos entregables.
