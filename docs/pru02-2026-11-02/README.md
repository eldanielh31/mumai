# Evidencia funcional del 2 de noviembre de 2026

La campaña técnica de ACT-PRU-02 está ejecutada. Consulta el
[reporte de pruebas funcionales](../../Proyecto/Informes/Reporte_Pruebas_Funcionales_PRU02_2026-11-02.md)
y la [matriz de los 35 requisitos](../matriz-requisitos-2026-11-02.md).

- Regresión final: [35 pruebas](regresion-final.txt).
- Funciones por escritorio Qt: [15 casos](funcionales/casos.json), [log](funcionales.txt) y cuatro capturas sintéticas en funcionales/.
- Referencias: [cinco escenarios y siete criterios](referencias.json).
- Captura real: [18 comprobaciones de repetibilidad y exportación sin red](motor-sin-red.json).
- CPU sin acceso a GPU ni red: [33 pruebas](cpu-sin-red.txt); los dos casos nuevos de preparación se ejecutaron en la suite final normal.
- Integridad: [cuatro exportaciones y entradas intactas](integridad.json), [verificador](comprobar_integridad.py).
- Entorno inicial: [identidad y huellas](entorno.json).
- Preparación: [Python faltante/incompatible](preparacion.json); calidad: [reglas](calidad.txt), [formato](formato.txt), [dependencias](dependencias.txt).
- Identidad final de archivos: [manifiesto](manifiesto.json).
- Remoto público autorizado y política sin commit/push automático: [remoto](remoto.json) y [confirmaciones de Daniel](confirmaciones-daniel.json).

Las entradas y exportaciones previas se conservaron. Los resultados reales nuevos
permanecen en data/output/. Las pruebas fueron automatizadas por Codex; no se
atribuyen a Daniel ni certifican daños o aceptación externa. Las fechas UTC 3/11
del nombre de algunas salidas corresponden al 2/11 en America/Guatemala.

Para repetir los casos en otro directorio nuevo:

```bash
cd ~/mumai
QT_QPA_PLATFORM=xcb .venv/bin/python scripts/validate_functional_week.py --evidence docs/NUEVA_SESION/funcionales
```

No reutilices rutas de evidencia existentes. La comprobación de integridad de esta
sesión se ejecutó antes de cerrar el manifiesto y rechaza reemplazar su JSON.
