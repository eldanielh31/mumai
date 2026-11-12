# Procedimiento de medición e integración

Las mediciones se ejecutan en serie, con GNU time, en Ubuntu 24.04 sobre WSL.
Cada análisis se inicia en un proceso nuevo con OpenCL desactivado.
Se conservan tiempo de pared, máximo RSS, bytes de los archivos del paquete,
configuración, métricas, origen y firmas SHA-256 de CSV, NPY y patrones.
El tiempo interno del informe se conserva como una medida adicional.

| Conjunto | Repeticiones por archivo | Dimensión máxima | Alpha | Referencia |
|---|---:|---:|---:|---:|
| Cinco AVI sintéticos de referencia | 3 | 160 | 5 | 8 s |
| Motor regularizado a 30 FPS | 2 | 480 | 2 | 10 s |

Banda de 0,7 a 1,5 Hz, nivel espacial 1 y detección de patrones activada.
Los archivos sintéticos conservan las condiciones del escenario controlado.
Para el motor se registran luz de día, soporte independiente y banda exploratoria.
Las comparaciones original y magnificado se hacen dentro de una misma ejecución.
La campaña mide el flujo completo por consola en cada resolución de procesamiento.

Ejemplo de reproducción desde la raíz con un directorio nuevo por repetición.

```bash
OPENCV_OPENCL_RUNTIME=disabled /usr/bin/time -f '%e %M' \
  bash run.sh data/input/referencias/subtle.avi --analyze \
  --low 0.7 --high 1.5 --alpha 5 --baseline 8 --spatial-level 1 \
  --max-dimension 160 --capture-notes 'Escenario sintético controlado' \
  --output data/output/mi-medicion/subtle-1 --json
```

Tras medir se ejecutan unittest, pip check, los 15 casos funcionales Qt en modo
offscreen, la suite de referencias y git diff --check. La comprobación de
integridad decodifica los videos completos, verifica los paquetes exportados
por Qt, recalcula las métricas del CSV y revisa los enlaces del resumen.
