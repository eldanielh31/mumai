# Proyecto Final: análisis de video

Primer módulo funcional de la aplicación local: carga, validación completa de lectura,
metadatos y acceso secuencial a fotogramas. Incluye una interfaz mínima con selección
de archivo, cancelación y vista previa, además de una opción de consola.

## Uso

Desde esta carpeta, abre la aplicación:

```bash
bash run.sh
```

Pulsa **Seleccionar video**. La aplicación lee el archivo completo en segundo plano
y muestra resolución, FPS, cantidad real de fotogramas leídos, duración estimada y
el primer fotograma. Los videos largos tardarán más en validarse. Puedes cancelar.

Para validar desde la consola:

```bash
bash run.sh "/ruta/al/video.mp4"
bash run.sh "/ruta/al/video.mp4" --json
```

El resultado correcto devuelve código 0; una entrada inválida devuelve código 1 y
un mensaje de error. No modifica el video original.

## Video de demostración

```bash
.venv/bin/python scripts/create_sample.py
bash run.sh data/input/prueba_movimiento.avi --json
```

El ejemplo sintético tiene 30 fotogramas, 320 × 240 píxeles, 10 FPS y 3 segundos.
Sirve para comprobar el módulo; no representa una prueba de diagnóstico de maquinaria.
El generador conserva el archivo si ya existe.

## Validación y límites

- Contenedores admitidos: MP4, AVI, MOV, MKV, M4V y WebM; el códec debe ser legible
  por el FFmpeg de OpenCV. AVI/MJPEG y MP4/MPEG-4 están cubiertos por pruebas.
- Se rechazan rutas inexistentes, carpetas, archivos vacíos, formatos no admitidos,
  archivos sin fotogramas legibles, FPS inválidos y cambios de resolución.
- Se decodifica todo el archivo sin acumularlo en memoria. Si se leen menos
  fotogramas que los declarados en el contenedor, se informa lectura incompleta.
  Un índice incorrecto del contenedor también puede provocar este rechazo.
- OpenCV puede tolerar algunos daños y no siempre diferencia error de lectura de
  fin de archivo: la validación no certifica la integridad absoluta del video.
- La duración se estima como fotogramas/FPS. Para análisis temporal posterior se
  deben usar videos de tasa constante; esta versión no certifica esa condición.
- `inspect_video(path)` devuelve `VideoInfo` y el primer fotograma BGR.
  `iter_frames(info)` entrega fotogramas BGR en orden para el siguiente módulo.
  Si se detiene antes del final, debe cerrarse el generador con `close()`.

## Pruebas

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

Las pruebas de interfaz usan una pantalla virtual por defecto. Para comprobar una
ventana real en una sesión de escritorio Ubuntu con X11/XWayland:

```bash
QT_QPA_PLATFORM=xcb PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p test_gui.py -v
```

## Entorno

Python 3.13 está instalado en `.python` y `.venv`, sin reemplazar el Python de Ubuntu.
Las dependencias exactas están en `requirements.txt`. PySide6 usa una versión anterior
a 6.10 elegida para este Ubuntu 22.04. VS Code está configurado para usar `.venv`.

Para activar el entorno en una terminal:

```bash
source .venv/bin/activate
```

Las dependencias de escritorio y FFmpeg fueron verificadas el 6 de octubre de 2026.
En otra instalación de Ubuntu, `bash scripts/complete-setup.sh` instala los paquetes
del sistema y verifica el entorno; necesita contraseña de administrador.
Para reinstalar las librerías: `.venv/bin/python -m pip install -r requirements.txt`.

## Estado y estructura

`src/video_analysis/video/` contiene el módulo de entrada; `gui/`, su interfaz mínima.
Los módulos `magnification`, `motion`, `heatmaps`, `anomalies` y `export` siguen pendientes
para etapas posteriores. La interfaz actual no reproduce ni procesa el video.

`data/input/` y `data/output/` guardan archivos locales excluidos de Git.
`tests/` contiene las pruebas; `scripts/`, las herramientas de verificación y muestras;
`docs/`, el registro de avance y resultados.
