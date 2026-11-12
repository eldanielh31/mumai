# Notas de coherencia de los documentos del proyecto

Corte del 2 de noviembre de 2026. Estas notas distinguen el alcance definido del
estado de cada informe. Se conservan los originales fechados y no se modifican horas,
aprobaciones o fechas históricas sin evidencia. La definición del producto está en
el plan, los requisitos y el diseño; los informes muestran lo que se declaró en su corte.

## Alcance y selección técnica

- El plan especifica software local, EVM, una medida compartida de movimiento,
  mapas/métricas, patrones opcionales, comparación y exportación. El diseño selecciona
  el enfoque híbrido tras comparar procesamiento clásico e IA centrada.
- La ficha menciona TensorFlow/PyTorch como plataformas posibles. El plan y los
  requisitos los condicionan al método seleccionado. No es necesario incorporarlos
  para reemplazar el criterio robusto e Isolation Forest auxiliar ya utilizados.
- La ficha propone diciembre como plazo probable; el plan establece la línea base
  concreta hasta el 21/11/2026. Las fechas de seguimiento y pendientes usan el plan.
- La mención a Ubuntu 22.04 en el Informe 1 corresponde a un entorno previsto entonces.
  El entorno Ubuntu 24.04/WSL actual sigue cumpliendo Linux como plataforma principal.

## Discrepancias de presentación

La presentación intermedia y su guion no reflejan las alternativas del Diseño §11 y
contienen expresiones como «daño visible» o «sin atrasos importantes». Se corrige su
lectura vigente en la [fe de erratas](../Presentacion/Fe_de_erratas_alcance_2026-11-02.md).
No usar esas diapositivas como una especificación alternativa ni como prueba de
puntualidad general. El guion de referencia incluido en la fe de erratas es el texto
alineado para explicar hoy la solución.

## Fechas y esfuerzo reportados

El Informe 1, al 11/10, declara que falta evidencia de un módulo funcional de carga;
el registro `docs/avance-2026-10-06.md` describe un módulo y once pruebas al 6/10.
Existe una diferencia entre fuentes: con esta revisión no se determina cuál refleja
la fecha efectiva. La evidencia posterior demuestra disponibilidad actual, pero no
resuelve por sí sola esa cronología. No se reescribe un informe como si hubiera
incluido pruebas que no cita.

El Informe 2 reporta AC acumulado de 141 h y cierres hasta el 30/10. Esos valores
se conservan como declarados en el documento aportado. El registro operativo
`docs/registro-horas.csv` no tiene filas de horas reales; no se utiliza el tiempo de
procesamiento ni una estimación para reconstruirlo. Tampoco se certifican esas horas
por haber verificado hoy las funciones. Los datos para el próximo informe deberán
proceder de registros reales o confirmación expresa, manteniendo esa procedencia.

## Estado vigente y límites

PRU-02 tiene evidencia técnica nueva del 2/11; PRU-03/04, documento final y presentación
conservan el calendario del plan. No se exige añadir un modelo diagnóstico, sensores,
servicios remotos o una campaña con fallas etiquetadas como entregables nuevos.
La ausencia de ese conjunto limita lo que se puede concluir sobre daños; no anula
las pruebas funcionales del prototipo.

La luz de día y el método de prueba funcional con CPU fueron confirmados por Daniel
el 2/11. No se presentan como decisiones del profesor. La constancia de aprobación
académica no se fabrica; las notas sobre versiones internas y sus nombres se resuelven
citando archivo, fecha y huella, sin renombrar retroactivamente la línea base.

La política actual del repositorio, confirmada por Daniel, permite el remoto público
con videos del motor y exige petición explícita para commit o push. Las referencias
anteriores a privacidad y publicación automática son históricas y no prevalecen sobre
esa instrucción.
