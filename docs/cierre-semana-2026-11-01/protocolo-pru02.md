# Protocolo preparado: ACT-PRU-02, 2–7 de noviembre de 2026

Presupuesto del plan: 12 horas, no horas reales. Objetivo: verificar funciones principales y trazabilidad antes de desempeño e integración final. Preparado el 1 de noviembre; sin resultados fechados en el futuro.

## Preparación

1. Identificar commit, entorno y versión de dependencias. Conservar el manifiesto y abrir un directorio nuevo de evidencia para cada sesión.
2. Generar las cinco referencias con `scripts/create_reference_videos.py`; conservar entrada y JSON de etiquetas. No sobrescribir las capturas reales.
3. Consultar `docs/guia-pruebas-manuales.md` y su hoja de resultados. Registrar ejecutor, fecha, entrada, configuración, resultado observado y evidencia.
4. Usar el video real adaptado del motor para la prueba de compatibilidad; consultar `condiciones-captura.json`. No usar cambios de aceleración como etiquetas de daños.

## Casos y criterios de decisión

| Grupo | Casos | Criterio / evidencia |
|---|---|---|
| Entrada | M01–M03: video válido, archivo ilegible, parámetros y reducción | Metadatos correctos, rechazo controlado sin resultados falsos, dimensiones esperadas; vincular REQ-FUNC-001/002/003 e INT-001. |
| Procesamiento | M04–M07: estático, vibración en banda, fuera de banda y alpha cero | Estático <0,001 px/fotograma, ganancia en banda >1,5 en referencia sintética, ganancia fuera de banda inferior; alpha cero coincide. |
| Patrones | M08–M11: cambio, desactivación, referencia insuficiente, iluminación | Cambio tras 13 s y sin anticipación; estados correctos; no convertir iluminación en diagnóstico. |
| Consulta | M12: cuatro pestañas, pausa, búsqueda y reinicio de reproducción | Ambas mitades del mismo instante, métricas identificadas, mapas con unidades y escala común. |
| Persistencia | M13: cancelar selector, exportar, repetir exportación, reiniciar | Cancelar selector conserva revisión; copias íntegras; nombres nuevos; exportación persiste tras reiniciar. |
| Recuperación | M14–M15: invalidar configuración, error, cancelación | Sin visualización obsoleta ni publicación parcial; nueva ejecución posible. Si termina antes de cancelar, registrar “no ejecutado a tiempo” y repetir; no marcar aprobado automáticamente. |
| Captura real | Repetir configuración exacta del análisis previo por interfaz | CSV, NPY, patrones y métricas reproducibles; copia verificada y fuente intacta. Ejecutar `scripts/validate_real_workflow.py --help` para parámetros. |
| Sin red | Ejecutar en entorno de proceso sin interfaces externas | Carga, análisis y exportación completas sin conexiones. Registrar aislamiento; no desconectar la red del usuario. |
| GPU opcional | Funciones con dispositivos GPU inaccesibles | Evidencia técnica de CPU. El método literal de requisitos pide equipo sin GPU: si se exige ese ensayo físico, documentar equipo o aprobación de equivalencia; no inferirlo de un proceso aislado. |
| Entrega | Revisar instalación, versiones, estructura, configuración y huellas | Los 35 requisitos quedan vinculados a evidencia o pendientes explícitos. |

## Herramientas reproducibles

Desde `/home/daniel/Desktop/proyecto-final`:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/validate_reference_suite.py --evidence docs/NUEVA_SESION/referencias.json
QT_QPA_PLATFORM=xcb PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -p test_sw06.py -v
.venv/bin/python scripts/validate_sw06.py --evidence docs/NUEVA_SESION/flujo
.venv/bin/python scripts/create_evidence_manifest.py docs/NUEVA_SESION/manifiesto.json
```

Sustituir `NUEVA_SESION` por una ruta nueva real. La prueba nativa necesita una sesión de escritorio disponible; no confundir un error de acceso al display con falta de dependencias. Los tiempos de las órdenes son mediciones de ejecución, nunca horas de ingeniería.

## Cierre de la etapa

Revisar todos los casos, corregir fallos reproducibles y ejecutar su regresión. Registrar por separado las comprobaciones automáticas y la revisión de Daniel; no rellenar su hoja como si él hubiera ejecutado los casos. Documentar desviaciones, videos y parámetros. Revisar con la contraparte las limitaciones y los pendientes. Una captura sin referencia externa permite comprobar el flujo, pero no calcular sensibilidad/especificidad de diagnóstico.

## Preparación de etapas posteriores

Para PRU-03 registrar equipo, duración/resolución/FPS, tiempo total, RAM máxima y tamaño de salida para un conjunto definido y varias repeticiones; no imponer un límite de rendimiento no existente en requisitos. PRU-04 consolidará correcciones y regresión. DOC-01 y PRE-01 usarán evidencias reales y resultados aprobados, no proyecciones presentadas como mediciones.
