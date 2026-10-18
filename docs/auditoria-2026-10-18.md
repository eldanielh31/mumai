# Auditoría de requisitos y diseño — 18 de octubre de 2026

Versión revisada: `2c9eaba`. Se inspeccionaron los dos PDF proporcionados, el plan, código, interfaz y evidencia de pruebas. Esta auditoría no modifica la implementación. Los archivos auxiliares son evidencia reproducible de verificación.

## Dictamen

El núcleo previsto hasta esta fecha está implementado y dispone de evidencia funcional en escenarios sintéticos. No se puede declarar cumplimiento total ni funcionamiento perfecto. Hay diferencias concretas frente al diseño y requisitos, y falta validación con captura real. La existencia del código y pruebas técnicas no equivale a aceptación final de los entregables.

Fuentes: `/home/daniel/Downloads/Proyecto_Requer.pdf`, `/home/daniel/Downloads/Documento_de_Diseno_CE1114_Daniel_Brenes_v2.pdf` y `docs/referencias/Plan_de_Proyecto_Daniel_Brenes.pdf`. Se inspeccionaron también las tablas y diagramas renderizados de los documentos.

## Hallazgos que requieren atención

1. **Resultados anteriores visibles tras un nuevo análisis fallido.** Reproducción: completar un análisis, cambiar la salida a una ruta que sea archivo e iniciar otra ejecución. La ventana comunica el error y desactiva los botones de resultados, pero conserva las métricas y mapas anteriores. No publica falsamente una nueva exportación, aunque puede confundir al usuario. Confirmado mediante ejecución de la interfaz en modo offscreen; véase `auditoria-2026-10-18/interfaz.json`. Corregir limpiando o marcando explícitamente los resultados previos al iniciar otra ejecución. Relación: REQ-USAB-002 y manejo de estados.
2. **Estados incompletamente representados.** Hay mensajes y controles habilitados/deshabilitados, pero no se representa de manera clara la secuencia completa definida, especialmente Configurado y el retorno a En espera después de un error. Es posible cargar otro video y recuperarse; esto no demuestra por sí solo la transición exacta exigida. REQ-MOD-001/002 y diseño §10.11.
3. **Mapas exportados sin leyenda incorporada.** Los PNG son imágenes de color sin rótulos ni barra de escala. La ventana y LEEME sí identifican las posiciones y el rango común; el JSON registra la escala. Al separar una imagen de ese contexto, pierde esa información. Cumplimiento parcial de REQ-USAB-003; incorporar etiquetas y escala en las visualizaciones exportadas.
4. **Procesamiento y exportación unidos.** El botón “Analizar y guardar resultados” guarda antes de mostrar los resultados. El diseño §10.10 muestra consulta/comparación seguida de una solicitud de exportación. La función de guardar existe, pero ese flujo no coincide completamente con el diseño. Alinear el flujo o aprobar una revisión documentada del diseño. Un fallo de guardado impide acceder al nuevo resultado en la ventana.
5. **Instalación desde cero incompleta.** `scripts/complete-setup.sh` presupone `.venv` y una ruta Python 3.13. No crea el entorno ni instala las dependencias Python. Las instrucciones funcionan con el entorno ya preparado, pero no constituyen una instalación limpia reproducible. REQ-CV-001. Hallazgo por inspección, sin alterar el equipo ni intentar una instalación del sistema.
6. **Medición de tiempo ligeramente incompleta.** `elapsed_seconds` se toma antes de escribir el informe, LEEME y publicar el directorio definitivo. Registra la mayor parte del procesamiento, pero no toda la ejecución de extremo a extremo. Precisar el alcance o añadir duración completa para REQ-REND-001. No se afirma que este desfase sea grande.
7. **Captura convencional y condiciones reales pendientes.** Los cinco videos de referencia son sintéticos. Demuestran propiedades del algoritmo bajo condiciones controladas, pero no validan todavía videos de una cámara convencional ni desempeño ante cámara inestable, iluminación real o maquinaria. REQ-FIS-001 pendiente de esa evidencia; no equivale a fallo demostrado del algoritmo.

## Matriz de los 35 requisitos

“Verificado” significa respaldado en el alcance probado, no garantía universal. “Parcial” identifica una brecha observable o evidencia limitada. Las comprobaciones físicas y formales pendientes se distinguen de fallos funcionales.

| Requisito | Estado | Evidencia y límite |
|---|---|---|
| REQ-FUNC-001 | Verificado | Carga local, metadatos y vista previa; pruebas AVI y MP4. |
| REQ-FUNC-002 | Verificado | Archivos inexistentes, vacíos, corruptos y truncados rechazados; no inicia análisis. |
| REQ-FUNC-003 | Verificado | Frecuencias, amplificación, escala, resolución, referencia y patrones configurables y validados. |
| REQ-FUNC-004 | Verificado | EVM gaussiana, salida decodificable, selectividad dentro/fuera de banda y control estático. |
| REQ-FUNC-005 | Verificado | Farneback y mismas métricas/resolución/FPS en original y magnificado. |
| REQ-FUNC-006 | Verificado | Mapas temporales y métricas media, percentil 95 y RMS, CSV y gráfico. |
| REQ-FUNC-007 | Verificado con alcance | Cambio de amplitud detectado en datos sintéticos válidos; no diagnóstico mecánico. Si falta referencia suficiente se informa y no se inventan alertas. |
| REQ-FUNC-008 | Verificado con alcance | Mapas/gráfico en ventana y video lado a lado mediante reproductor externo. |
| REQ-FUNC-009 | Verificado con diferencia de diseño | Guarda resultados y configuración; exportación automática unida al análisis. |
| REQ-USAB-001 | Verificado | Carga, configuración, procesamiento y consulta identificables. |
| REQ-USAB-002 | Parcial | Mensajes y progreso presentes; resultados anteriores siguen visibles tras fallo de nueva ejecución. |
| REQ-USAB-003 | Parcial | Posiciones y escala comunes en ventana/textos; faltan leyenda y rótulos dentro de mapas PNG. |
| REQ-REND-001 | Parcial | Tiempo registrado; excluye últimas escrituras/publicación. |
| REQ-REND-002 | Verificado con alcance | Cinco escenarios de referencia procesados; sin extrapolar a cualquier video o resolución. |
| REQ-INT-001 | Verificado con alcance | Formatos documentados; AVI/MP4 comprobados. No se afirma cobertura de todos los códecs. |
| REQ-INT-002 | Verificado | Resultados almacenados localmente. |
| REQ-HUM-001 | Verificado | Flujo por interfaz sin modificar código; registros de pruebas de ventana. |
| REQ-MANT-001 | Verificado | Componentes separados de carga, EVM, movimiento, mapas, patrones, exportación e interfaz. |
| REQ-MANT-002 | Verificado | Versiones fijadas en requirements y registradas en resultados. |
| REQ-CONF-001 | Verificado con observación | Lectura/configuración/exportación fallidas informadas sin nuevo resultado exitoso; véase hallazgo de visualización previa. |
| REQ-CONF-002 | Verificado | Recuperación después de error, incluida salida inválida en nueva prueba de interfaz. |
| REQ-CAL-001 | Verificado con alcance | Análisis, patrones y exportación ejecutados en espacio de red aislado sin interfaces externas; no se desconectó la red del usuario. |
| REQ-CAL-002 | Verificado con alcance | Dos ejecuciones de misma entrada/configuración: comparación exacta de métricas, matrices y patrones. Metadatos de fecha, ruta y duración no se consideran resultados numéricos repetibles. |
| REQ-MOD-001 | Parcial | Operación reflejada mediante mensajes, pero representación completa de estados definida no demostrada. |
| REQ-MOD-002 | Parcial | Recuperación disponible; falta retorno explícito a En espera conforme al modelo. |
| REQ-FIS-001 | Pendiente de evidencia real | Equipo de propósito general operativo; falta ejecución documentada con video capturado por cámara convencional. |
| REQ-FIS-002 | Parcial en verificación física | Procesamiento CPU sin llamadas a GPU; no se realizó ensayo en otro equipo físicamente sin GPU como pide el método de verificación. |
| REQ-AMB-001 | Verificado en simulación | Condiciones de escenarios sintéticos documentadas; las capturas reales futuras requieren iluminación y estabilidad registradas. |
| REQ-AMB-002 | Verificado en simulación | Original/magnificado proceden de misma entrada y preparación; escenarios controlados documentados. |
| REQ-SEG-001 | Verificado | No existe función de control físico de maquinaria. |
| REQ-SEG-002 | Verificado | Advertencias en interfaz, informes y documentación: apoyo a inspección, no diagnóstico certificado. |
| REQ-INF-001 | Verificado | Entrada, SHA-256, configuración y versiones asociados al paquete de salida. |
| REQ-INF-002 | Verificado con alcance | Fallo provocado al publicar exportación: excepción, limpieza y ausencia de salida parcial; GUI informa error de destino. |
| REQ-CV-001 | Parcial | Uso y versiones documentados; instalación limpia incompleta. |
| REQ-CV-002 | Verificado | Registros de pruebas, escenarios, resultados representativos y esta auditoría conservados. |

## Correspondencia con el diseño

La arquitectura local y modular, el uso de CPU, el procesamiento EVM, comparación de movimiento, mapas, métricas y análisis opcional de patrones son coherentes con el diseño. No hay obligación de entrenar una red profunda ni de utilizar TensorFlow/PyTorch: el documento admite técnicas estadísticas/IA según corresponda. El método robusto con Isolation Forest auxiliar no es por sí mismo una desviación.

Las principales diferencias son el flujo de exportación, representación de estados y presentación de mapas. El diseño tampoco convierte los indicadores en diagnóstico automático de daños. No se ha demostrado aceptación de la contraparte ni desempeño industrial.

## Situación respecto del cronograma

- ACT-SW-01 a SW-04: núcleo implementado y probado técnicamente; presentación de mapas necesita cierre. Haber recuperado las funciones no elimina retrasos históricos.
- ACT-PRU-01: referencias sintéticas disponibles; no confundir con captura real validada.
- ACT-SW-05 (12–24 octubre): implementación y evidencia sintética disponibles; aún dentro de su plazo al corte.
- ACT-SW-06 (19–31 octubre): funciones adelantadas, pero pendientes los ajustes de interfaz, comparación y exportación descritos. No declarar cierre completo.
- ACT-PRU-02 (2–7 noviembre), PRU-03 (9–14 noviembre) y PRU-04 (9–16 noviembre): validación formal, desempeño e integración aún futuras. Las pruebas actuales son evidencia anticipada, no sustituto de esos entregables.
- Documentación y presentación final: noviembre. Completar instalación reproducible y evidencia de aceptación antes de la entrega.

## Evidencia y reproducción

Se revisaron los registros existentes de 22 pruebas aprobadas, tres pruebas de interfaz Qt/X11 y cinco escenarios sintéticos. No se presentan como nuevas ejecuciones de esta auditoría.

Pruebas adicionales ejecutadas para esta revisión:

- `auditoria-2026-10-18/comprobar_pipeline.py`: repetición, fallo tardío de publicación, limpieza, recuperación y preservación de entrada. Ejecutado desde la raíz del repositorio con `unshare -Urn env MPLCONFIGDIR=/tmp/daniel-audit-mpl PYTHONPATH=src .venv/bin/python docs/auditoria-2026-10-18/comprobar_pipeline.py`. Resultado en `auditoria-2026-10-18/pipeline.json`.
- `auditoria-2026-10-18/comprobar_interfaz.py`: éxito, error de destino y recuperación; detecta métricas/mapas anteriores visibles. Ejecutado con `QT_QPA_PLATFORM=offscreen MPLCONFIGDIR=/tmp/daniel-audit-mpl PYTHONPATH=src .venv/bin/python docs/auditoria-2026-10-18/comprobar_interfaz.py`. Resultado resumido en `auditoria-2026-10-18/interfaz.json`.

La primera tentativa del ensayo aislado terminó después de dos análisis porque la consulta de interfaces mediante socket no estaba permitida. Se reemplazó solamente esa consulta por lectura de `/proc/net/dev` y se repitió el ensayo completo. No fue un fallo del producto.
