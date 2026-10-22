# Matriz de requisitos después de las correcciones

Corte: 21 de octubre de 2026. Actualiza el estado actual sin sustituir la auditoría histórica de `2c9eaba`. Contiene los **35 requisitos** del documento proporcionado.

“Verificado” se limita a los escenarios y entorno registrados. No equivale a aprobación de la contraparte ni a diagnóstico industrial validado. Evidencia de base: [correcciones del 18 de octubre](correcciones-2026-10-18/README.md). Evidencia adicional: [SW-06 del 21 de octubre](sw06-2026-10-21/README.md). Problemas y criterios: [registro de incidencias](registro-incidencias.md).

| Requisito | Estado actual | Evidencia y alcance |
|---|---|---|
| REQ-FUNC-001 | Verificado | Carga local, metadatos y vista previa; pruebas AVI y MP4. |
| REQ-FUNC-002 | Verificado | Archivos inexistentes, vacíos, corruptos y truncados rechazados; no inicia análisis. |
| REQ-FUNC-003 | Verificado | Frecuencias, amplificación, escala, resolución, referencia y patrones configurables y validados. |
| REQ-FUNC-004 | Verificado | EVM gaussiana, salida decodificable, selectividad dentro/fuera de banda y control estático. |
| REQ-FUNC-005 | Verificado | Farneback y mismas métricas/resolución/FPS en original y magnificado. |
| REQ-FUNC-006 | Verificado | Mapas temporales y métricas media, percentil 95 y RMS, CSV y gráfico. |
| REQ-FUNC-007 | Verificado con alcance | Cambio de amplitud detectado en datos sintéticos válidos; no diagnóstico mecánico. Si falta referencia suficiente se informa y no se inventan alertas. |
| REQ-FUNC-008 | Verificado con alcance | Revisión de mapas/gráfico/tabla y reproductor integrado sincronizado con pausa y búsqueda temporal; alternativa externa. |
| REQ-FUNC-009 | Corregido y verificado | Exportación explícita tras revisar, con configuración, resumen HTML y verificación de copias; INC-004/008/009. |
| REQ-USAB-001 | Verificado | Carga, configuración, procesamiento y consulta identificables. |
| REQ-USAB-002 | Corregido y verificado | Estados/mensajes y limpieza de visualizaciones ante nueva ejecución fallida; INC-001. |
| REQ-USAB-003 | Corregido y verificado | PNG individuales y comparativo incluyen títulos, escala y unidades; inspección visual INC-003. |
| REQ-REND-001 | Corregido y verificado | Reloj hasta publicación del análisis; alcance explícito y prueba con demora en última escritura; INC-006. |
| REQ-REND-002 | Verificado con alcance | Cinco escenarios de referencia procesados; sin extrapolar a cualquier video o resolución. |
| REQ-INT-001 | Verificado con alcance | Formatos documentados; AVI/MP4 comprobados. No se afirma cobertura de todos los códecs. |
| REQ-INT-002 | Verificado | Resultados almacenados localmente. |
| REQ-HUM-001 | Verificado | Flujo por interfaz sin modificar código; registros de pruebas de ventana. |
| REQ-MANT-001 | Verificado | Componentes separados de carga, EVM, movimiento, mapas, patrones, exportación e interfaz. |
| REQ-MANT-002 | Verificado | Versiones fijadas en requirements y registradas en resultados. |
| REQ-CONF-001 | Verificado | Errores controlados sin presentar nueva ejecución como exitosa; vistas anteriores retiradas. |
| REQ-CONF-002 | Verificado | Error de exportación permite reintentar sin recalcular; reinicio permite nueva carga. |
| REQ-CAL-001 | Verificado con alcance | Análisis, patrones y exportación ejecutados en espacio de red aislado sin interfaces externas; no se desconectó la red del usuario. |
| REQ-CAL-002 | Verificado con alcance | Dos ejecuciones de misma entrada/configuración: comparación exacta de métricas, matrices y patrones. Metadatos de fecha, ruta y duración no se consideran resultados numéricos repetibles. |
| REQ-MOD-001 | Corregido y verificado | Seis estados visibles; configuración validada explícitamente; prueba de recorrido INC-002. |
| REQ-MOD-002 | Corregido y verificado | Botón Volver a En espera, probado después de error; limpia sesión temporal y preserva exportaciones. |
| REQ-FIS-001 | Pendiente de captura real | Usuario confirmó que no dispone de video real; protocolo preparado, VAL-001 abierto. |
| REQ-FIS-002 | Pendiente de ensayo físico específico | Funciones CPU verificadas; falta ejecutar en equipo documentado físicamente sin GPU, VAL-002. |
| REQ-AMB-001 | Verificado en simulación | Condiciones de escenarios sintéticos documentadas; las capturas reales futuras requieren iluminación y estabilidad registradas. |
| REQ-AMB-002 | Verificado en simulación | Original/magnificado proceden de misma entrada y preparación; escenarios controlados documentados. |
| REQ-SEG-001 | Verificado | No existe función de control físico de maquinaria. |
| REQ-SEG-002 | Verificado | Advertencias en interfaz, informes y documentación: apoyo a inspección, no diagnóstico certificado. |
| REQ-INF-001 | Verificado | Entrada, SHA-256, configuración y versiones asociados al paquete de salida. |
| REQ-INF-002 | Verificado | Fallo de copia/publicación, copia corrupta y cancelación no publican salida parcial; mensaje y reintento. Recibo SHA-256 por archivo. |
| REQ-CV-001 | Corregido; alcance documentado | Creación e instalación de entorno limpio con versiones fijadas, Qt/códecs y pruebas integradas. Python/sistema preinstalados; no ensayo de Ubuntu desde cero. |
| REQ-CV-002 | Verificado | Histórico preservado, nuevas evidencias, incidencias, bitácora, decisiones, matriz y plantillas. |

La validación formal de noviembre, los ensayos físicos pendientes y la aceptación final siguen abiertos. La arquitectura y flujo interactivo ahora incorporan revisión antes de exportar y estados explícitos conforme al diseño.

La publicación en GitHub está pendiente de autenticación; no se confunde con REQ-INT-002, que exige almacenamiento local y sí está disponible. El usuario eligió repositorio privado.
