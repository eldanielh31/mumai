# Cierre técnico semanal: 26 de octubre–1 de noviembre de 2026

Corte: **1 de noviembre de 2026**, Costa Rica. Versión de aplicación verificada: `83b02c3`. Esta sesión añadió un protocolo ejecutable; no modificó los algoritmos ni el código de la aplicación.

## Dictamen

**La implementación prevista hasta el 31 de octubre está completa en el alcance del prototipo.** SW-06 dispone de visualización, comparación sincronizada, métricas, revisión antes de exportar, almacenamiento local y recuperación. Sus dependencias SW-01, SW-04 y SW-05 están disponibles y verificadas. No se identificó una función pendiente de implementación respecto del plan y diseño.

Las comprobaciones nuevas se ejecutaron el **1 de noviembre**, no se retrofechan al 31/10. El Informe de Avance 2 declara cierre al 30/10; se conserva como documento aportado, sin atribuirle evidencia posterior. El cierre técnico de implementación no significa terminar las etapas de pruebas y entrega final de noviembre, ni certificar daños mecánicos.

## Entregables de esta sesión

- [Conciliación de las 19 actividades y ocho entregables](cronograma-y-entregables.md).
- [Matriz actualizada de los 35 requisitos](../matriz-requisitos-2026-11-01.md).
- [Protocolo funcional PRU-02 para el 2–7 de noviembre](protocolo-pru02.md), con casos, criterios y comandos.
- [Condiciones de captura confirmadas](condiciones-captura.json).
- [Distribución de esfuerzo estimado](esfuerzo-estimado.md), separada de horas reales.
- Nuevo script `scripts/validate_real_workflow.py`: repite la configuración de un reporte previo por la interfaz, verifica identidad de entrada, resultados, reproducción, exportación y reinicio; rechaza sobrescribir evidencia.

## Resultados de verificación

| Verificación | Resultado | Evidencia |
|---|---|---|
| Suite automática completa | 32/32 aprobadas, 8,631 s | pruebas.txt |
| Comparación/exportación Qt/X11 en escritorio | 7/7 aprobadas, 1,746 s | interfaz-nativa.txt |
| Referencias sintéticas | Cinco escenarios; 7/7 criterios aprobados | referencias.json y .txt |
| Flujo real y repetibilidad | 18/18 comprobaciones aprobadas | motor-flujo-repetibilidad.json y .txt |
| Preservación de evidencia | Ruta existente rechazada y huella intacta | proteccion-evidencia.json |
| Calidad de código | Reglas F/I sin errores; 32 archivos con formato correcto | calidad-codigo.txt |
| Dependencias | Sin incompatibilidades detectadas | dependencias.txt |

Las siete pruebas nativas son un subconjunto de la suite, no siete requisitos adicionales. Un porcentaje de pruebas aprobadas no es porcentaje de avance. Los nombres de salida con fecha UTC 2/11 corresponden a la tarde del 1/11 en Costa Rica.

### Referencias controladas

Estático: movimiento cero y sin alertas. Vibración sutil de 1 Hz: razón de movimiento 2,438 y sin alertas estables. Fuera de banda de 5 Hz: razón 1,000. Cambio de amplitud: 14 ventanas posteriores al cambio, sin alertas prematuras según criterios. Iluminación: residuo absoluto pequeño, sin alertas; su razón elevada tiene un denominador muy pequeño y no se interpreta como desplazamiento físico.

### Captura real

Daniel confirmó: **Samsung Galaxy S25 Ultra**, grabación el **28/10/2026**, soporte independiente del vehículo y tramos al ralentí y acelerados. No se conocen intervalos exactos de aceleración, RPM, bloqueo de exposición ni fuente de iluminación; no se inventan.

La copia analizada tiene 848×478, 30 FPS, 1644 fotogramas y 54,8 s. Se conserva el MP4 original; la copia FFV1 regulariza tiempos sin agregar información física. Configuración: banda exploratoria 0,7–1,5 Hz, alpha 2, nivel 1, referencia 10 s, dimensión máxima 480. Procesamiento 480×270 y tiempo **129.88 s**.

La repetición produjo exactamente el mismo CSV, ambas matrices NPY, patrones y métricas que el análisis previo. Se comprobó búsqueda y reproducción del comparativo, recibo íntegro por hashes y tamaños, fuente intacta y exportación conservada después de reiniciar. Razón de movimiento medio 1,127; saturación 0,922 %. Ventanas señaladas: 42,5–43,0 y 51,0–51,5 s. Pueden corresponder a cambios de régimen; no son etiquetas de fallas. El tramo inicial tampoco se certifica como ralentí estable.

Se mantuvieron las notas del análisis previo para repetir su configuración exacta. Los datos nuevos del teléfono y régimen quedan en condiciones-captura.json, sin reescribir informes anteriores.

Salida real local: `/home/daniel/Desktop/proyecto-final/data/output/cierre-semana-2026-11-01/analisis-20261102T001500Z-e9828f93-export-e674992b`. Videos, imágenes reales y resultados voluminosos no se publican en GitHub; la evidencia textual conserva su identidad y ubicación.

### Red y GPU

El flujo real completo se ejecutó con Bubblewrap: namespace de red separado, `/dev` privado, OpenCL desactivado y Qt offscreen. `/proc/net/dev` muestra solo loopback y no hay dispositivos GPU accesibles al proceso. El campo `network_interfaces` del JSON proviene del sysfs del host y puede enumerar interfaces de la computadora; no representa acceso a esas interfaces desde el proceso aislado. No se modificó la conexión ni el hardware del usuario.

Equipo observado: Intel Core i7-1165G7, Python 3.13.16, Linux y memoria total reportada 16068908 kB. No se midió RAM máxima de proceso en esta sesión. La prueba nativa de escritorio se ejecutó por separado con referencias sintéticas.

## Riesgos y límites pendientes

| Elemento | Situación y acción |
|---|---|
| R-INS-01, videos disponibles | Mitigado para compatibilidad: captura real disponible. Falta conjunto representativo etiquetado para evaluar diagnóstico. |
| R-INS-02 / R-PRO-01, captura y artefactos | Soporte confirmado, aceleración presente e iluminación parcialmente documentada. Alpha reducido a 2; interpretar cambios sin atribuirlos a fallas. |
| R-PRO-02, capacidad discriminante | Comprobada en referencias sintéticas; sin validación de daños reales. |
| R-HER-01, dependencias | Versiones fijadas y verificadas. Poppler empaquetado falló por GLIBC; se usó /usr/bin/pdftoppm para leer el cronograma, sin cambios al producto. |
| R-HER-02, recursos | Captura real completada; campaña de rendimiento y RAM sigue programada para PRU-03. |
| VAL-001 | Captura, condiciones básicas, ejecución y repetibilidad resueltas. Faltan tiempos/RPM y referencia externa para atribuir causas o evaluar diagnóstico. |
| VAL-002 | Funcionamiento sin acceso a GPU comprobado; ensayo literal en computadora físicamente sin GPU no realizado. Requiere ese ensayo o aceptación de equivalencia. |
| VAL-003 | Etapas formales de noviembre y entrega final conservan calendario. Daniel confirmó que funciona; no se le atribuyen los 15 casos manuales completos. |
| REP-001 | Resuelto: repositorio privado conectado; este cierre se publica en el mismo remoto. |
| Aprobación | Daniel confirma aprobación del plan. El PDF no contiene la captura de aprobación; no se fabrica firma ni evidencia del supervisor. |
| Esfuerzo | Las cifras del Informe 2 se conservan como reportadas. La distribución nueva es estimada y no se incorpora como AC ni horas reales. |

## Reproducción

Desde `/home/daniel/Desktop/proyecto-final`, con la entrada y análisis previos disponibles localmente:

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/python scripts/validate_real_workflow.py \
  data/output/motor-validacion-2026-11-01/analisis-20261101T201740Z-96f59e0b \
  --output data/output/nueva-repeticion \
  --evidence docs/NUEVA_SESION/motor.json
```

Usar una ruta nueva para la evidencia. Un clon de GitHub no contiene el video del carro ni los resultados locales. El aislamiento de esta sesión utilizó raíz de solo lectura, proyecto con escritura, `/dev` privado, `/proc` del namespace, `/tmp` temporal, `--unshare-net`, `QT_QPA_PLATFORM=offscreen` y `OPENCV_OPENCL_RUNTIME=disabled`; no es necesario para el uso normal.

## Próxima etapa

PRU-02 comienza el 2/11 y finaliza el 7/11; su protocolo está preparado y puede reutilizar esta evidencia identificada. PRU-03 y PRU-04 comienzan el 9/11, documentación final el 16/11 y presentación el 18/11. No se declaran esas actividades terminadas antes de ejecutar su alcance y resolver los pendientes aplicables.
