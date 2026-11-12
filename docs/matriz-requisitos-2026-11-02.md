# Matriz de requisitos al 2 de noviembre de 2026

ACT-PRU-02 ejecutada dentro del periodo 2–7/11. Se conserva la matriz del 1/11.
Evidencia: [reporte](../Proyecto/Informes/Reporte_Pruebas_Funcionales_PRU02_2026-11-02.md)
y [paquete PRU-02](pru02-2026-11-02/README.md). La verificación se limita a los
escenarios y métodos descritos; no es aceptación académica ni validación diagnóstica.

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
| REQ-REND-001 | Verificado funcionalmente | Informe real: 212,996 s de procesamiento. No sustituye campaña PRU-03 ni mide horas de ingeniería. |
| REQ-REND-002 | Verificado en conjunto definido | Cinco referencias y captura de 54,8 s completadas. PRU-03 sigue prevista 9–14/11. |
| REQ-INT-001 | Verificado con alcance | AVI/MP4 en regresión y AVI real. No se afirma cobertura de todos los códecs. |
| REQ-INT-002 | Verificado | Cuatro exportaciones locales, hashes y tamaños comprobados. |
| REQ-HUM-001 | Verificado en flujo | Daniel ejecutó y exportó el motor; automatización Qt ejecutó M01–M15 sin editar código durante el uso. |
| REQ-MANT-001 | Verificado | Módulos trazados al diseño, revisión F/I y formato sin errores; scripts reproducibles. |
| REQ-MANT-002 | Verificado | pip check correcto, Python 3.13.18; INC-016 y dos regresiones de preparación; guía WSL/LFS actualizada. |
| REQ-CONF-001 | Verificado | M02/M03/M14 y regresión: errores de entrada, configuración y procesamiento; LFS diferenciado. |
| REQ-CONF-002 | Verificado | M13–M15: recuperación y nueva ejecución; pruebas de reintento de exportación. |
| REQ-CAL-001 | Verificado en proceso aislado | Motor completo sin interfaces externas: /proc/net/dev solo loopback. No se cambia la red del usuario. |
| REQ-CAL-002 | Verificado | CSV, patrones, dos NPY y resúmenes reales idénticos a la exportación de Daniel; 18 comprobaciones. |
| REQ-MOD-001 | Verificado | Seis estados del diseño cubiertos por M01–M15 y tests/test_gui.py. |
| REQ-MOD-002 | Verificado | M13 y motor: reinicio elimina sesión temporal y conserva exportaciones. |
| REQ-FIS-001 | Verificado en captura real | Video del teléfono de Daniel, copia normalizada a 30 FPS; entrada y exportación originales intactas. |
| REQ-FIS-002 | Verificado por método acordado | 33 regresiones con /dev/dri vacío, /dev/dxg sustituido por /dev/null y OpenCL desactivado. Daniel acepta justificar CPU en su equipo con RTX 3050; no se atribuye aceptación al profesor. |
| REQ-AMB-001 | Documentado con límites | Daniel confirma luz de día el 2/11; teléfono/soporte y régimen constan en antecedentes. Exposición, RPM e intervalos desconocidos. |
| REQ-AMB-002 | Verificado para repeticiones | Mismos bytes y parámetros, con comparación exacta; no se presupone régimen constante del motor. |
| REQ-SEG-001 | Verificado por inspección | El producto solo procesa archivos; no hay funciones de control de maquinaria. |
| REQ-SEG-002 | Verificado | Advertencias en interfaz, informes y resumen local; cambios respecto a referencia no equivalen a daños. |
| REQ-INF-001 | Verificado | Identidad, parámetros, versiones y recibos vinculados; luz de día registrada como anexo sin reescribir reportes previos. |
| REQ-INF-002 | Verificado | M13/M15 y regresión de copia corrupta: no publicación parcial; cuatro paquetes íntegros. |
| REQ-CV-001 | Verificado con alcance de entorno preparado | Ubuntu WSL con Python 3.13 y dependencias correctas; preflight probado. No se reinstaló Ubuntu ni se afirma instalación limpia nueva. |
| REQ-CV-002 | Verificado localmente | Historial conservado, reporte, matriz y manifiesto. Público y videos autorizados por Daniel; no commit ni push sin solicitud explícita. |

La equivalencia del método funcional sin GPU fue aceptada por Daniel en esta sesión.
El equipo no carece físicamente de GPU; el aislamiento impide usarla en el proceso
probado. La captura real sin red es otra ejecución con OpenCL desactivado, en la que
los dispositivos GPU permanecían visibles. Ambos alcances se distinguen en el reporte.

Pendientes posteriores: campaña de rendimiento/RAM PRU-03, integración final PRU-04,
documentación y presentación según calendario. No se dispone de etiquetas mecánicas
externas ni se fabrican sensibilidad, especificidad, aprobación del profesor u horas
reales. No hay commit ni push en esta entrega por instrucción explícita de Daniel.
