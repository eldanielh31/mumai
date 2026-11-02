# Matriz de requisitos al 1 de noviembre de 2026

Documento nuevo; la matriz del 21 de octubre se conserva intacta. Corte en America/Costa_Rica. Los 35 requisitos se contrastaron con los documentos académicos de requerimientos y diseño.

Evidencia: [cierre semanal](cierre-semana-2026-11-01/README.md), [revisión de código](revision-2026-11-01/README.md) y [correcciones históricas](correcciones-2026-10-18/README.md). Base actual: 32 pruebas, siete pruebas nativas, cinco escenarios/siete criterios y 18 verificaciones de captura real. “Verificado” siempre se limita al escenario documentado.

| Requisito | Estado | Evidencia y alcance |
|---|---|---|
| REQ-FUNC-001 | Verificado | Carga local válida en pruebas AVI/MP4 y captura real adaptada. |
| REQ-FUNC-002 | Verificado | Entradas ausentes, vacías, ilegibles y truncadas rechazadas; sin análisis exitoso falso. |
| REQ-FUNC-003 | Verificado | Parámetros validados; misma configuración completa reproducida por interfaz. |
| REQ-FUNC-004 | Verificado | EVM, control estático, selectividad temporal, alpha cero y video real procesados. |
| REQ-FUNC-005 | Verificado | Misma definición de flujo en ambas ramas, mismas dimensiones y FPS; prueba de desplazamiento conocido. |
| REQ-FUNC-006 | Verificado | Mapas, media, percentil 95, RMS, CSV, matrices y gráfico disponibles. |
| REQ-FUNC-007 | Verificado con alcance | 14 ventanas sintéticas posteriores al cambio; dos ventanas reales con aceleración declarada. No se atribuyen a daños. |
| REQ-FUNC-008 | Verificado | Comparación integrada, búsqueda y reproducción reales; siete pruebas nativas de escritorio aprobadas. |
| REQ-FUNC-009 | Verificado | Exportación explícita real, recibo completo y hashes correctos; reinicio conserva la copia. |
| REQ-USAB-001 | Verificado | Carga, configuración, procesamiento y consulta identificables; flujo nativo y automatizado. |
| REQ-USAB-002 | Verificado | Estados, errores y limpieza de vistas comprobados; recuperación posterior. |
| REQ-USAB-003 | Verificado | Mapas con títulos, unidades y escala común; ramas identificadas en comparación. |
| REQ-REND-001 | Verificado | Reloj por ejecución: repetición real 129,88 s. No son horas de ingeniería ni campaña PRU-03 completa. |
| REQ-REND-002 | Verificado en conjunto definido | Cinco escenarios sintéticos y captura real de 54,8 s completados; sin extrapolar a otros tamaños. |
| REQ-INT-001 | Verificado con alcance | Formatos documentados; AVI y MP4 probados. No se afirma cobertura exhaustiva de todos los códecs. |
| REQ-INT-002 | Verificado | Resultados guardados localmente, huellas comprobadas. |
| REQ-HUM-001 | Verificado | Flujo por interfaz sin editar código; Daniel informó que le funciona. |
| REQ-MANT-001 | Verificado | Componentes identificables y trazados al diseño; revisión de código documentada. |
| REQ-MANT-002 | Verificado | Versiones fijadas y pip check sin incompatibilidades; instrucciones de instalación disponibles. |
| REQ-CONF-001 | Verificado | Errores de lectura/configuración/procesamiento controlados en pruebas. |
| REQ-CONF-002 | Verificado | Reintento de exportación, recuperación y nueva ejecución comprobados. |
| REQ-CAL-001 | Verificado en proceso aislado | Flujo real completo con namespace de red sin interfaces externas; /proc/net/dev solo loopback. |
| REQ-CAL-002 | Verificado en captura real y simulación | Igualdad exacta de CSV, dos NPY, patrones y resumen numérico; rutas, fechas y tiempos no se consideran resultados repetibles. |
| REQ-MOD-001 | Verificado | Seis estados del diseño disponibles y comprobados en pruebas de interfaz. |
| REQ-MOD-002 | Verificado | Reinicio real a En espera elimina temporales y conserva la exportación. |
| REQ-FIS-001 | Verificado en captura real | Samsung Galaxy S25 Ultra, grabación de Daniel del 28/10, procesada en equipo i7-1165G7; original intacto y copia normalizada. |
| REQ-FIS-002 | Verificado funcionalmente; método físico pendiente | Flujo sin dispositivos GPU accesibles y OpenCL desactivado. No demuestra equipo físicamente sin GPU: ensayo literal o aceptación de equivalencia pendiente. |
| REQ-AMB-001 | Documentado con límites | Teléfono, fecha, soporte independiente y ralentí/aceleración confirmados. Fuente de luz, exposición y RPM no confirmadas; desconocidos explícitos. |
| REQ-AMB-002 | Verificado para comparaciones ejecutadas | Repetición de los mismos bytes y parámetros; no se presupone un régimen constante del motor. |
| REQ-SEG-001 | Verificado por inspección | No hay función de control de maquinaria; archivos locales como entrada. |
| REQ-SEG-002 | Verificado | Advertencias en interfaz, reportes y guías: apoyo a inspección, no certificación mecánica. |
| REQ-INF-001 | Verificado | Fuente, SHA, parámetros, versiones y recibo vinculados; nueva información de captura en anexo, sin alterar reportes previos. |
| REQ-INF-002 | Verificado | Errores, cancelación y copia corrupta comprobados; reexportación corregida; paquete real validado por hashes y tamaños. |
| REQ-CV-001 | Verificado con alcance histórico | Instalación en entorno limpio previamente comprobada con Python/sistema existentes; guía y versiones disponibles. No se reinstaló Ubuntu en esta sesión. |
| REQ-CV-002 | Verificado | Historial preservado, nueva evidencia, matriz y protocolo; GitHub privado. Grabaciones reales y sus imágenes solo locales. |

La implementación SW-01 a SW-06 está disponible y verificada en el alcance señalado. Las pruebas formales, medición de desempeño y entrega final mantienen su calendario. El método físico literal sin GPU y la validación mecánica externa no se declaran realizados.

GitHub privado está conectado. Daniel confirma aprobación del plan; no se crea una firma o captura del supervisor. Las horas del Informe 2 se preservan como reportadas, sin convertir estimaciones en horas reales.
