# Revisión de código y preparación de GitHub

Fecha: 1 de noviembre de 2026 (Costa Rica). Base: `a400830`.

## Alcance

Revisión manual de todos los módulos de `src/video_analysis`, scripts de soporte y pruebas: carga y temporización, preprocesamiento, EVM, flujo óptico, mapas, patrones, integración, cancelación, interfaz, reproductor y exportación. Ruff 0.14.3 revisó importaciones, símbolos sin uso y formato en 31 archivos Python. Esto no es una garantía de ausencia de defectos ni sustituye las fases formales del plan.

## Hallazgos y cambios

- **INC-013, integridad de reexportación:** al exportar una carpeta que ya contenía `exportacion.json`, se incluía el recibo antiguo entre los archivos verificados y luego se reemplazaba. La nueva prueba reprodujo el fallo; ahora se genera un recibo nuevo sin intentar incluirse a sí mismo. Se comprobó igualdad entre archivos, hashes y recibo. La exportación habitual desde la interfaz no dependía de reexportar paquetes previamente exportados.
- **INC-014, fecha del script SW-06:** `validate_sw06.py` mantenía fija la fecha del 21 de octubre. Ahora usa la fecha de Costa Rica o `--date`; el nuevo flujo registra 2026-11-01. No se alteraron evidencias históricas.
- Se eliminaron importaciones sin uso de `VideoError` en la consola y `cv2` en una prueba. Se ordenaron importaciones, se separaron instrucciones encadenadas y se aplicó formato uniforme. Los comentarios que justifican decisiones, límites y liberación de recursos se conservaron; no se detectó una colección de funciones muertas que justificara borrar módulos o utilidades utilizadas por las pruebas.
- Comparación estructural de Python antes/después: excluyendo importaciones, solo cambiaron `export/package.py`, `create_evidence_manifest.py`, `validate_sw06.py` y la nueva prueba de reexportación. Los algoritmos y umbrales permanecen iguales.
- El generador de manifiestos ahora incluye `Proyecto/` y `ruff.toml`. El README corrige una referencia obsoleta al reproductor externo.

## Documentos

Se incorporaron los **26 documentos** aportados por Daniel. `Presentaicon` se corrigió a `Presentacion`; los documentos sueltos se agruparon en `Ficha`, `Riesgos` y `Actividades`. Se conservaron Plan, Requerimientos, Diseño e Informes. `Proyecto/README.md` enlaza todos los archivos. Se verificó SHA-256 antes/después: ningún documento perdió ni cambió contenido. No se editaron los PDF, Word ni diapositivas, ni se borraron evidencias históricas por considerarlas duplicadas.

## Verificación

- 32 pruebas automáticas aprobadas (6,819 s), incluida regresión de reexportación.
- Nueve comprobaciones de interfaz y exportación aprobadas con Qt offscreen. En esta sesión no se afirma una prueba nativa de escritorio.
- Ruff: sin errores en las reglas F e I; 31 archivos con formato correcto.
- Dependencias: `pip check` sin incompatibilidades.
- Escaneo acotado de archivos versionados: sin patrones de clave privada ni token GitHub. No equivale a una auditoría exhaustiva de secretos.
- El ejemplo del flujo es sintético; las grabaciones reales del automóvil y sus resultados se conservan locales, fuera de Git.

Daniel indicó que la prueba del motor funciona correctamente. Se registra su observación sin atribuirle la ejecución de los 15 casos manuales ni aceptación global del proyecto. Continúan los límites de validación mecánica y los pendientes descritos en el registro de captura real.

## Evidencia

`pruebas.txt`, `analisis-estatico.txt`, `dependencias.txt`, `flujo.txt`, `flujo/flujo.json`, `documentos.json`, `reexportacion-antes.txt` y el manifiesto de versión. La publicación se verifica comparando el commit local y el remoto; su URL y estado están en `../repositorio.md`.
