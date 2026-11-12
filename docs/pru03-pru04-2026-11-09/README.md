# Evidencia de PRU-03 y PRU-04

Corte del 9 de noviembre de 2026, Guatemala.

- [Reporte de desempeño e integración](../../Proyecto/Informes/Reporte_Desempeno_Integracion_PRU03_PRU04_2026-11-09.md).
- [Procedimiento](procedimiento.md) y [entorno](entorno.json).
- [Mediciones completas](mediciones.jsonl) y [resumen](resumen.json).
- [Regresión automática](regresion.txt), [dependencias](dependencias.txt) y [estados](regresion-estados.jsonl).
- [Casos Qt](funcionales/casos.json), [referencias](referencias.json) e [integridad](integridad.json).
- [Matriz vigente](../matriz-requisitos-2026-11-09.md) y [manifiesto](manifiesto.json).

Los paquetes medidos están en data/output/pru03-2026-11-09. Las rutas de las
exportaciones Qt constan en funcionales/casos.json. Las imágenes de esa carpeta
documentan pruebas con entradas sintéticas. Base Git be0cbf8bcd83372de0bb974ab4840d9b6530a3cb, con identidad
del árbol de trabajo registrada en el manifiesto.

Los casos M01–M15 reutilizan el verificador de PRU-02 como regresión de PRU-04.
