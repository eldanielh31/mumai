# Validación con captura real y equipo de referencia

Estado al 18 de octubre de 2026: **pendiente**. Daniel confirmó en esta sesión que no dispone de un video de prueba real. No hay captura real incorporada a la evidencia actual. Los cinco escenarios del repositorio son sintéticos. No se accedió a una cámara ni se grabó a ninguna persona.

## Material necesario para VAL-001

- Ruta del video y autorización para utilizarlo en el proyecto.
- Cámara utilizada, resolución, FPS, duración, fecha y escenario.
- Iluminación y estabilidad de cámara; indicar movimiento, compresión o edición conocidos.
- Comportamiento de referencia esperado y, cuando exista, medición independiente. Sin ella solo puede comprobarse ejecución/visualización, no exactitud de diagnóstico.

## Procedimiento

1. Registrar condiciones con la plantilla de sesión. Conservar el original sin editar y calcular su SHA-256.
2. Seleccionar frecuencias compatibles con FPS y el fenómeno de interés; justificar amplificación, nivel espacial y resolución. No asumir que los valores de demostración corresponden a cualquier máquina.
3. Reservar tramo inicial representativo de comportamiento normal; comprobar que existen suficientes ventanas útiles después del transitorio y al menos una ventana de evaluación. Si no alcanza, registrar referencia insuficiente.
4. Ejecutar y revisar original, magnificado, mapas con escala común, gráfico, saturación y advertencias. Exportar y guardar configuración y versiones.
5. Repetir misma entrada/configuración. Comparar métricas y eventos; no comparar literalmente fechas, nombres de carpeta ni tiempo de ejecución.
6. Contrastar cambios con referencia externa. Documentar falsos positivos/negativos observados; si no hay etiquetas fiables, no calcular sensibilidad/especificidad como si las hubiera.
7. Registrar defectos nuevos con ID, conservar las salidas y actualizar la matriz indicando exactamente qué quedó comprobado.

## Equipo sin GPU — VAL-002

Documentar equipo, sistema, CPU, memoria, almacenamiento y ausencia de GPU según el método de verificación. Ejecutar el flujo y conservar tiempos y resultados. El código actual utiliza CPU, pero no se marca cerrado este ensayo físico basándose únicamente en esa inspección.

## Rendimiento y aceptación — VAL-003

En las etapas de noviembre medir duración, resolución/FPS, tiempo de análisis, memoria y disco; documentar hardware y condiciones equivalentes. No extrapolar tiempos de los videos pequeños a videos largos o de alta resolución. Registrar aprobación/rechazo y observaciones de la contraparte cuando existan; no anticipar esa aceptación.
