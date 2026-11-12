# Matriz de requisitos al 9 de noviembre de 2026

La matriz conserva la base del 2/11 e incorpora el cierre técnico de PRU-03 y PRU-04.
[Campaña y regresión](pru03-pru04-2026-11-09/README.md). [Verificación previa](pru02-2026-11-02/README.md).

| Requisito | Estado al corte | Evidencia y alcance |
|---|---|---|
| REQ-FUNC-001 | Verificado | M01/M03 por Qt y captura real: carga, metadatos y reducción correctos. |
| REQ-FUNC-002 | Verificado | M02/M14, regresión de archivos inválidos y nuevo rechazo específico de punteros LFS (INC-015). |
| REQ-FUNC-003 | Verificado | M03/M14, validación de banda y repetición exacta de configuración real. |
| REQ-FUNC-004 | Verificado | M04–M07 y M11; controles estático, selectividad y alpha cero. Motor completado. |
| REQ-FUNC-005 | Verificado | M07, prueba de traslación conocida y CSV comparable en ambas ramas. |
| REQ-FUNC-006 | Verificado | M12 e integridad: cuatro métricas, mapas, CSV y NPY coherentes. |
| REQ-FUNC-007 | Verificado en alcance controlado | M08–M11: 14 ventanas sintéticas; dos ventanas reales reproducibles, sin etiquetas de falla. |
| REQ-FUNC-008 | Verificado | M12 por Qt/X11, capturas revisadas, búsqueda, reproducción, pausa y reinicio. |
| REQ-FUNC-009 | Verificado | M13 y motor: copias íntegras, exportaciones únicas y conservación después de reiniciar. |
| REQ-USAB-001 | Verificado técnicamente | M01–M15 por interfaz Qt; no se atribuye ejecución manual ni aceptación a Daniel. |
| REQ-USAB-002 | Verificado | M02/M14/M15 y regresión: errores identificados, vistas retiradas y recuperación. |
| REQ-USAB-003 | Verificado | Inspección de cuatro capturas sintéticas: títulos, unidades, escala común y ramas identificadas. |
| REQ-REND-001 | Verificado por campaña | 17 mediciones de pared, tiempo interno, RSS y disco en seis casos. |
| REQ-REND-002 | Verificado en conjunto definido | Cinco referencias con tres repeticiones y motor con dos. 7 criterios sintéticos aprobados. |
| REQ-INT-001 | Verificado con alcance | AVI/MP4 en regresión y AVI real. No se afirma cobertura de todos los códecs. |
| REQ-INT-002 | Verificado | Cuatro exportaciones locales, hashes y tamaños comprobados. |
| REQ-HUM-001 | Verificado en flujo | Daniel ejecutó y exportó el motor; automatización Qt ejecutó M01–M15 sin editar código durante el uso. |
| REQ-MANT-001 | Verificado | Módulos trazados al diseño, revisión F/I y formato sin errores; scripts reproducibles. |
| REQ-MANT-002 | Verificado | pip check correcto, Python 3.13.18; INC-016 y dos regresiones de preparación; guía WSL/LFS actualizada. |
| REQ-CONF-001 | Verificado | M02/M03/M14 y regresión: errores de entrada, configuración y procesamiento; LFS diferenciado. |
| REQ-CONF-002 | Verificado | M13–M15: recuperación y nueva ejecución; pruebas de reintento de exportación. |
| REQ-CAL-001 | Verificado en proceso aislado | Motor completo sin interfaces externas: /proc/net/dev solo loopback. No se cambia la red del usuario. |
| REQ-CAL-002 | Verificado | CSV, matrices NPY y patrones coincidentes en las repeticiones de PRU-03 y evidencia real previa de PRU-02. |
| REQ-MOD-001 | Verificado | Seis estados del diseño cubiertos por M01–M15 y tests/test_gui.py. |
| REQ-MOD-002 | Verificado | M13 y motor: reinicio elimina sesión temporal y conserva exportaciones. |
| REQ-FIS-001 | Verificado en captura real | Video del teléfono de Daniel, copia normalizada a 30 FPS; entrada y exportación originales intactas. |
| REQ-FIS-002 | Verificado por método acordado | 33 regresiones con /dev/dri vacío, /dev/dxg sustituido por /dev/null y OpenCL desactivado. Daniel acepta justificar CPU en su equipo con RTX 3050; no se atribuye aceptación al profesor. |
| REQ-AMB-001 | Documentado con límites | Daniel confirma luz de día el 2/11; teléfono/soporte y régimen constan en antecedentes. Exposición, RPM e intervalos desconocidos. |
| REQ-AMB-002 | Verificado para repeticiones | Mismos bytes y parámetros, con comparación exacta; no se presupone régimen constante del motor. |
| REQ-SEG-001 | Verificado por inspección | El producto solo procesa archivos; no hay funciones de control de maquinaria. |
| REQ-SEG-002 | Verificado | Advertencias en interfaz, informes y resumen local; cambios respecto a referencia no equivalen a daños. |
| REQ-INF-001 | Verificado | Paquetes de PRU-03 y exportaciones Qt de PRU-04 vinculados a entrada y configuración. Integridad por archivos y métricas. |
| REQ-INF-002 | Verificado | M13/M15 y regresión de copia corrupta: no publicación parcial; cuatro paquetes íntegros. |
| REQ-CV-001 | Verificado con alcance de entorno preparado | Ubuntu WSL con Python 3.13 y dependencias correctas; preflight probado. No se reinstaló Ubuntu ni se afirma instalación limpia nueva. |
| REQ-CV-002 | Verificado localmente | Historial conservado, reporte, matriz y manifiesto. Público y videos autorizados por Daniel; no commit ni push sin solicitud explícita. |

Las verificaciones de red y CPU aisladas corresponden a PRU-02. Continúan la documentación final, la presentación y la revisión académica conforme al plan.
