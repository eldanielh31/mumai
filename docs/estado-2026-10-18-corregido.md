# Estado del proyecto después de corregir los hallazgos

Fecha de corte: **18 de octubre de 2026**. Este documento describe la versión posterior a la auditoría. El historial anterior permanece disponible y no se reescribe retroactivamente.

## Resultado

Se corrigieron los seis hallazgos de software/documentación que podían resolverse con los recursos disponibles: resultados obsoletos, estados, mapas sin leyenda, exportación unida al análisis, instalación incompleta y alcance del tiempo medido. Se documentaron problemas, causas, soluciones, decisiones y pruebas. No se declara cumplimiento total del proyecto: faltan captura real, ensayo físico específico sin GPU, evaluación formal y aceptación.

## Cambios visibles

- Acciones separadas: Seleccionar video → Validar configuración → Analizar → revisar → Exportar resultados.
- Indicador de los seis estados y opción para volver a En espera.
- Cambio de parámetros o nuevo análisis retira la visualización anterior. Un fallo de cálculo ya no deja mapas previos en pantalla.
- Mapas exportados identifican Original/Magnificado e incluyen barra y unidades.
- Si falla la exportación, se conserva el análisis revisable y se permite reintentar. Los paquetes incompletos se retiran y exportaciones anteriores no se sobrescriben.
- Las instrucciones crean un entorno Python nuevo e instalan dependencias fijadas.
- Tiempo registrado hasta publicación de resultados, con alcance de medición declarado.

**Uso importante:** el análisis de la interfaz es temporal hasta exportarlo. Se descarta al cerrar/reiniciar; las exportaciones permanecen. La consola sigue guardando en la carpeta indicada por `--output`.

## Verificación

- 25 pruebas automáticas aprobadas, incluyendo nuevos casos de estados, vista obsoleta, error/reintento de exportación, cancelación/no sobrescritura y medición de tiempo.
- Cuatro pruebas de interfaz también aprobadas en Qt/X11 del escritorio; el primer intento aislado no tuvo acceso al display y se conservó ese registro.
- Cinco escenarios sintéticos y siete criterios de referencia aprobados después de los cambios.
- Instalación de versiones exactas en entorno Python nuevo y dos pruebas integradas allí. Se reutilizaron intérprete y bibliotecas del sistema existentes; no se ensayó instalación completa de Ubuntu.
- Análisis repetido sin red: mismas métricas, matrices y patrones; error tardío de publicación recuperable y video original intacto.
- Inspección visual de mapas exportados y ventana.

Los registros están en [correcciones-2026-10-18](correcciones-2026-10-18/README.md). Las pruebas sintéticas no demuestran sensibilidad/especificidad sobre maquinaria real.

## Seguimiento del plan

SW-01 a SW-04 tienen núcleo técnico implementado; la presentación de mapas se corrigió. SW-05 (12–24 octubre) mantiene evidencia sintética de detección. SW-06 (19–31 octubre) cuenta por adelantado con revisión/exportación y los ajustes descritos; conserva necesidad de evaluación de uso y pruebas formales. PRU-02/03/04 permanecen en noviembre, al igual que documentación y presentación final. La documentación se prepara desde ahora para facilitar esas entregas.

El avance técnico recuperado no elimina retrasos históricos ni demuestra horas reales. El registro de horas debe completarse con información real. No se calcula valor ganado nuevo ni se presume aceptación de la contraparte.

## Pendientes

| ID | Pendiente | Dependencia | Criterio para cerrar |
|---|---|---|---|
| VAL-001 | Cámara convencional y condiciones reales | Daniel confirmó que no dispone de video real | Captura documentada, ejecución, exportación y revisión; referencia independiente para evaluar exactitud. |
| VAL-002 | Método de verificación en equipo sin GPU | Equipo/documentación de hardware | Ejecutar funciones principales y conservar evidencia física y resultados. |
| VAL-003 | Evaluación formal y aprobación | Etapas del cronograma y revisión de contraparte | Protocolos completados, resultados y aceptación explícita. |

El protocolo y las plantillas están preparados. No se sustituyen pendientes reales con simulaciones presentadas como si fueran capturas.
