# Guía para nuevas capturas reales

Uso vigente al **2 de noviembre de 2026**: Daniel ya aportó el video del motor,
confirmó luz de día y completó una ejecución/exportación; su repetibilidad consta en
[PRU-02](pru02-2026-11-02/README.md). Esta guía sirve para futuras capturas y mejores
comparaciones; no significa que siga faltando una primera captura o que deba comprarse
otro equipo para terminar PRU-02. Para repetir el motor usa los parámetros del
[README](../README.md). El procedimiento de recomendaciones del 21/10 sigue abajo.


Fecha: 21 de octubre de 2026. Relación: VAL-001; prepara PRU-02/03 y permite contrastar el prototipo con una cámara convencional. No es necesario comprar una cámara ni una GPU para comenzar.

## Primera grabación recomendada

Graba un **archivo original de 30–60 segundos**, preferentemente **1080p a 30 o 60 FPS**, en MP4. Estas son condiciones iniciales prácticas de prueba, no mínimos obligatorios del documento de requisitos ni garantía de que cualquier vibración pueda medirse.

1. Apoya el celular/cámara en una superficie firme o trípode. Mantén fijo el encuadre; no lo sostengas con la mano durante la grabación.
2. Elige una zona con textura o bordes visibles y movimientos pequeños y repetitivos: por ejemplo, una parte exterior de una estructura o carcasa accesible que vibre. Para comenzar puede servir un montaje de escritorio con movimiento suave; documentaremos que no es maquinaria industrial.
3. Usa luz estable y suficiente, evitando sombras que cambien, reflejos fuertes y cambios automáticos visibles de brillo. Si puedes, bloquea enfoque/exposición. No cambies zoom ni posición.
4. Conserva al menos los primeros **10–15 segundos** con un comportamiento estable como referencia. Si después existe un cambio normal y seguro de operación, anota cuándo sucede. No provoques una avería ni retires protecciones para obtener un ejemplo.
5. Graba a velocidad normal: sin cámara lenta, filtros, edición ni interpolación. Si el teléfono permite FPS constantes, utilízalos. El programa comprueba la regularidad temporal y puede rechazar grabaciones de FPS variables; revisaremos ese caso sin modificar el original.
6. Copia el archivo original a la computadora mediante cable o transferencia de archivo. Evita reenviarlo como video comprimido por una red social o mensajería.

Una toma completamente inmóvil sirve como control, pero no demuestra magnificación de movimiento. Evita que todo el encuadre esté ocupado por aspas rápidas o movimiento grande: pueden ocultar las pequeñas variaciones que se quieren observar. Los 30/60 FPS no bastan para medir cualquier frecuencia mecánica; elegiremos la banda según el video y su referencia. No hay que usar automáticamente los 0,7–1,5 Hz de la demostración.

## Qué información entregar junto al archivo

Puedes completar este texto:

- Ruta del archivo en la computadora:
- Qué objeto o equipo se observa:
- Celular o cámara utilizada:
- Fecha aproximada de grabación:
- Resolución y FPS configurados (si los conoces):
- Cámara fija o en movimiento:
- Iluminación utilizada y cambios observados:
- Qué ocurre al principio y qué cambia después:
- Instante aproximado del cambio:
- Qué comportamiento esperas que se vea:
- ¿Tenemos autorización para usar el video y mostrarlo en el informe?:

No necesitas editarlo ni saber calcular las métricas. Entrega la ruta y estos datos; la validación revisará lectura, duración, regularidad, parámetros y resultados. El original quedará fuera de GitHub salvo autorización explícita.

## Si prefieres buscar uno existente

Debe ser un archivo descargable con permiso de uso, encuadre fijo, duración suficiente, velocidad normal, sin cortes y con información de origen y condiciones. Conserva enlace, autor y licencia o autorización. No basta un video promocional editado o una comparación ya magnificada: necesitamos la entrada original. Una grabación propia controlada facilita documentar estas condiciones.

## Qué queda demostrado y qué no

Un video de cámara convencional permite comprobar el flujo con captura real. Para concluir que una alerta corresponde a una falla o daño hacen falta referencia independiente y revisión del fenómeno. No se inferirá daño únicamente por el color del mapa o por una ventana señalada.

Para una comparación más sólida, consigue después un segundo video de control con misma cámara, posición e iluminación, documentando qué condición cambia. Esto amplía la evidencia; no bloquea la primera prueba.
