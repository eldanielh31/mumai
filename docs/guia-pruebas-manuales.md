# Guía para que Daniel pruebe el proyecto completo

Actualizada al **21 de octubre de 2026**. Prueba la implementación de SW-01 a SW-06: entrada, EVM, movimiento, mapas, patrones, comparación y exportación. Los ejemplos son sintéticos; no se presentan como grabaciones reales ni como pruebas formales de noviembre ya realizadas.

## 1. Preparar y abrir

En la terminal, copia estas órdenes:

```bash
cd /home/daniel/Desktop/proyecto-final
.venv/bin/python scripts/create_reference_videos.py
mkdir -p data/output/pruebas-daniel
bash run.sh
```

El generador conserva los videos de referencia que ya existen. La última orden abre la aplicación; deja esa terminal abierta. Si `.venv` falta, consulta la sección de instalación del README antes de seguir. En esta computadora el entorno ya fue preparado y probado.

Los cinco videos están en la carpeta `data/input/referencias` dentro del proyecto. Si el selector lo permite, pega la ruta absoluta:

```text
/home/daniel/Desktop/proyecto-final/data/input/referencias
```

Crea una copia de [la hoja de registro](plantillas/registro-prueba-manual.md) y completa tus resultados. Ningún caso de esa hoja se marca aprobado antes de que tú lo ejecutes.

## 2. Configuración común para las demostraciones

| Campo de la aplicación | Valor |
|---|---:|
| Frecuencia mínima | 0,7 Hz |
| Frecuencia máxima | 1,5 Hz |
| Amplificación | 5 |
| Referencia inicial | 8 segundos |
| Dimensión máxima | 160 píxeles |
| Nivel de reducción espacial | 1 |
| Detectar cambios respecto a la referencia | Activado |
| Condiciones de captura | “Prueba sintética de Daniel; cámara fija simulada; iluminación constante salvo lighting” |

Pulsa **Validar configuración** y después **Analizar**. Los parámetros deben restablecerse a esta tabla antes de cada caso que no indique otra cosa. Los valores numéricos de abajo corresponden a esta configuración y a los archivos generados por el proyecto; no son umbrales universales de maquinaria.

**Guarda antes de cambiar:** los resultados sin exportar son temporales. Cambiar un parámetro retira la vista del resultado anterior; cerrar o reiniciar descarta la sesión. Para conservar una prueba, pulsa **Exportar resultados…** y elige `data/output/pruebas-daniel`. Cada exportación crea una carpeta nueva. Anota su nombre junto al ID de prueba.

## 3. Entrada y preprocesamiento — ACT-SW-01

### M01 — Cargar un video válido

1. Pulsa **Seleccionar video** y abre `subtle.avi`.
2. Espera a que termine la validación.
3. Comprueba **Entrada válida**, vista previa y estos datos: **160 × 120, 20 FPS, 400 fotogramas, duración 20 s**.
4. Aplica la configuración común y pulsa **Validar configuración**.

**Pasa si:** aparece **Configurado**, sin errores y con opción de analizar. No debe comenzar el cálculo antes de pedirlo.

### M02 — Rechazar un archivo que no es video y recuperarse

1. En **Seleccionar video**, cambia el filtro a **Todos los archivos**.
2. Selecciona el `README.md` de la raíz del proyecto. No lo edites ni renombres.
3. Comprueba que aparezca un error de formato y que no permita analizar ese archivo.
4. Vuelve a seleccionar `subtle.avi` y valida los parámetros.

**Pasa si:** el error se muestra sin cerrar la aplicación y puedes volver a **Configurado**. Si el selector no permite elegir otro tipo de archivo, anota “no ejecutado desde selector”; la prueba automática sí cubre formatos inválidos y archivos dañados.

### M03 — Validar parámetros y reducción de tamaño

1. Con `subtle.avi`, cambia frecuencia máxima a **11 Hz** y pulsa **Validar configuración**.
2. Debe rechazarla: con 20 FPS la máxima tiene que ser menor de 10 Hz.
3. Restablece 1,5 Hz. Cambia dimensión máxima a **80** y analiza.
4. Exporta. Abre `informe.json` con un editor de texto y busca `processing_size`: debe mostrar **[80, 60]**. La entrada mantiene 20 FPS; no se modifica el archivo original.
5. Vuelve a dimensión **160** antes de los siguientes casos.

**Pasa si:** el valor inválido no inicia procesamiento y la reducción conserva proporciones. No compares las métricas de esta ejecución reducida con las cifras de referencia de 160 píxeles como si fueran la misma escala.

## 4. Magnificación, movimiento y mapas — SW-02, SW-03 y ACT-SW-04

### M04 — Control estático

1. Carga `static.avi` y usa la configuración común.
2. Analiza y revisa **Resumen numérico**, mapas y **Métricas en el tiempo**.

**Pasa si:** las métricas son cero o prácticamente cero; para esta referencia, movimiento medio magnificado **menor de 0,001 px/fotograma**. Debe indicar **0 ventanas** de cambios. La escena no debe interpretarse como movimiento por tener un mapa con escala mínima artificialmente pequeña.

### M05 — Movimiento sutil dentro de la banda

1. Carga `subtle.avi` y analiza con la configuración común.
2. En **Video comparativo**, reproduce, pausa y desplaza la barra para revisar el mismo instante en ambas mitades.
3. Consulta **Resumen numérico**, mapas y gráfico.

**Esperado en esta computadora:** media original aproximadamente **0,02054** y magnificada **0,05007 px/fotograma**, razón aproximada **2,44**. Las pequeñas diferencias por plataforma no son necesariamente un defecto; un criterio funcional de esta referencia es razón **mayor de 1,5**.

**Pasa si:** aumenta el movimiento medido dentro de banda, hay títulos Original/Magnificado y ambos mapas usan la misma escala. El gráfico identifica las dos series y unidades. Debe haber **0 ventanas de cambio**: movimiento estable amplificado no significa anomalía.

### M06 — Movimiento fuera de banda

1. Carga `out_of_band.avi`, manteniendo la banda 0,7–1,5 Hz.
2. Analiza y exporta.

**Esperado:** medias original y magnificada próximas a **0,09540 px/fotograma**, razón próxima a **1** y sin alertas en esta referencia. Su movimiento de 5 Hz está fuera de la banda seleccionada.

**Pasa si:** no aumenta como el caso anterior. La comparación automatizada exige que la ganancia de `subtle` supere la de este caso por un factor mayor de 1,5. No es un requisito que EVM elimine todo movimiento fuera de banda: conserva el original.

### M07 — Amplificación cero

1. Carga `subtle.avi`, cambia amplificación a **0** y analiza.
2. Compara las métricas, ambos mapas y las mitades del video.

**Pasa si:** original y magnificado coinciden numéricamente (salvo redondeo visible); razón próxima a **1**. En el gráfico las líneas pueden superponerse. Restablece amplificación **5**.

## 5. Análisis de patrones — ACT-SW-05

### M08 — Cambio conocido de amplitud

1. Carga `amplitude_change.avi` y usa la configuración común completa, referencia **8 s** y patrones activados.
2. Analiza y revisa el gráfico temporal.
3. Exporta y abre `patrones.json` con un editor de texto si quieres consultar los intervalos exactos.

**Esperado:** **14 ventanas de medio segundo** señaladas entre **13 y 20 s**, sin alertas anteriores en esta referencia. El gráfico muestra los intervalos posteriores al cambio. Son 14 ventanas consecutivas de un cambio, no 14 averías distintas.

**Pasa si:** detecta el cambio introducido sin señalar la parte estable previa. Para el criterio automático se exige al menos un intervalo a partir de 13 s y ninguno anterior a 12,5 s.

### M09 — Patrones desactivados

1. En el mismo video, desmarca **Detectar cambios respecto al tramo inicial de referencia**.
2. Analiza de nuevo.

**Pasa si:** siguen disponibles magnificación, mapas y métricas, pero se informa **Análisis de patrones desactivado**. En `patrones.json`, `status` es `disabled`. No debe presentarse “desactivado” como “evaluado y sin anomalías”. Reactiva la opción al terminar.

### M10 — Referencia insuficiente

1. Con patrones activados y `amplitude_change.avi`, cambia referencia inicial a **1 segundo**.
2. Analiza.

**Pasa si:** se informa **Referencia insuficiente** y se conservan las otras salidas. No debe inventar un resultado de detección. En `patrones.json`, `status` es `insufficient_reference`.

Esto es un resultado controlado previsto: el filtro excluye un transitorio y el método requiere al menos ocho ventanas completas de referencia. Restablece **8 segundos**.

### M11 — Iluminación variable, límite del método

1. Carga `lighting.avi` y usa la configuración común.
2. Consulta métricas y video.

**Esperado:** movimiento residual pequeño, aproximadamente **0,0000834** original y **0,0006746 px/fotograma** magnificado, y **0 ventanas** señaladas en esta referencia. Aunque la razón sea grande, las magnitudes absolutas son pequeñas.

**Pasa si:** el análisis termina y se conservan las advertencias sobre iluminación. No concluyas que un cambio de brillo representa un daño mecánico ni que esta prueba elimina todo posible falso positivo con luz real.

## 6. Comparación y exportación — ACT-SW-06

### M12 — Revisar las cuatro pestañas

Con un análisis exitoso de `amplitude_change.avi`:

1. **Vista previa / mapas:** identifica cada mapa y la barra de escala.
2. **Métricas en el tiempo:** identifica las dos series, el transitorio y las ventanas señaladas.
3. **Video comparativo:** reproduce, pausa, busca **14 s**, ve al final y vuelve a reproducir. Las mitades deben moverse juntas y reiniciar desde el principio.
4. **Resumen numérico:** comprueba cuatro filas, columnas Original/Magnificado y unidades.

**Pasa si:** puedes consultar todos los resultados sin exportar primero ni depender de un reproductor externo. Si el equipo no mantiene todos los fotogramas durante reproducción, revisa pausado; esa limitación de visualización no modifica las métricas calculadas.

### M13 — Exportar y conservar

1. Pulsa **Exportar resultados…**, cancela el selector y comprueba que el análisis siga disponible.
2. Vuelve a exportar y selecciona `data/output/pruebas-daniel`.
3. Espera el mensaje **Exportación completada** y abre la carpeta desde el botón.
4. Abre `resumen.html` en el navegador: debe mostrar las métricas, imágenes, configuración y advertencias sin requerir internet.
5. Comprueba la presencia de videos, mapas, gráfico, CSV, matrices NPY, `informe.json`, `patrones.json`, `LEEME.txt` y `exportacion.json`.
6. Exporta de nuevo: debe crear otra carpeta sin sobrescribir la primera.
7. Pulsa **Volver a En espera**. Las dos exportaciones deben seguir en disco.

**Pasa si:** la información es legible, corresponde a tu configuración y las copias permanecen tras reiniciar. `exportacion.json` registra las huellas de los archivos; no necesitas calcularlas manualmente para esta comprobación. Los fallos de copia y corrupción están cubiertos por pruebas automáticas; no cambies permisos del sistema para provocarlos.

### M14 — No confundir datos anteriores

1. Completa y exporta un análisis.
2. Cambia amplificación u otro parámetro.
3. Comprueba que mapas, gráfico, reproductor y tabla anteriores se retiren de la vista.
4. Introduce un parámetro inválido, valida, corrígelo y ejecuta otra vez.

**Pasa si:** el error no muestra el resultado anterior como si perteneciera a la configuración nueva, y puedes recuperarte. La exportación previa permanece en su carpeta.

### M15 — Cancelar y volver a empezar

1. Carga un video de referencia y pulsa **Analizar**.
2. Pulsa **Cancelar** inmediatamente, mientras todavía se procesa.
3. Espera a que termine la cancelación; vuelve a En espera y carga otro video válido.

**Pasa si:** informa la cancelación, no presenta un nuevo análisis como exitoso y permite continuar. Si el análisis ya había finalizado al pulsar, anota “no ejecutado a tiempo” y repite; eso no demuestra un fallo. Guarda primero cualquier resultado que quieras conservar.

## 7. Pruebas automáticas opcionales

Desde la misma carpeta del proyecto, con la aplicación cerrada:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/validate_reference_suite.py
```

La primera debe terminar con **31 pruebas y OK** en esta versión. La segunda procesa cinco referencias, verifica siete criterios y crea un JSON con fecha de Costa Rica y nombre nuevo; no sobrescribe la evidencia anterior. Ambas usan datos sintéticos.

Para elegir la carpeta de evidencia de una ejecución concreta, utiliza una ruta nueva:

```bash
.venv/bin/python scripts/validate_reference_suite.py --evidence docs/mi-prueba-daniel/referencias.json
```

Si esa ruta ya existe, el script lo rechaza para protegerla; elige otra para repetir. Guarda la salida de la terminal si necesitas compartir un error. Avisos del decodificador durante las pruebas de archivos dañados pueden ser esperados: el resultado de aprobación es `OK`, no la ausencia de mensajes.

## 8. Qué enviarme si algo falla

Indica **M01…M15**, nombre/ruta del video, parámetros, qué esperabas, qué ocurrió, texto exacto del error y una captura si ayuda. Conserva la exportación si existe. No cambies el video ni borres los resultados antes de registrar el problema. Si no sabes interpretar un valor, márcalo **inconcluso**, no aprobado por suposición.

## 9. Qué no quedará validado con esta guía sintética

La captura de cámara convencional, el ensayo físico específico sin GPU y la aceptación formal siguen pendientes. Para el primer caso usa [la guía de video real](guia-video-real.md). Las pruebas manuales de Daniel son evidencia de revisión de uso cuando se registren; este documento por sí solo no significa que ya las haya ejecutado.
