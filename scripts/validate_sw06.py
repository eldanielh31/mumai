"""Evidencia reproducible del flujo interactivo ACT-SW-06 con datos sintéticos."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from PySide6.QtWidgets import QApplication
from video_analysis.gui.main_window import MainWindow
from create_reference_videos import generate_reference


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', required=True, help='Directorio de evidencia nueva')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    evidence = Path(args.evidence).resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    if (evidence / 'flujo.json').exists() or (evidence / 'ejemplo').exists():
        parser.error('La evidencia ya existe; selecciona una carpeta nueva para conservar el historial.')
    video = root / 'data/input/referencias/amplitude_change.avi'
    if not video.exists():
        generate_reference(video, 'amplitude_change')
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    checks = {}

    def wait():
        deadline = time.monotonic() + 90
        while window.worker is not None and time.monotonic() < deadline:
            app.processEvents(); time.sleep(.01)
        if window.worker is not None:
            raise RuntimeError('La operación excedió 90 segundos.')

    try:
        window.dimension.setValue(160)
        window.notes.setText('Simulación controlada: cambio de amplitud a los 13 s; cámara fija e iluminación constante.')
        window.show()
        window.load_video(str(video)); wait()
        checks['entrada_valida'] = window.state == 'Entrada válida'
        window.configure()
        checks['configurado'] = window.state == 'Configurado'
        window.start_analysis(); wait()
        checks['resultados_antes_de_exportar'] = window.result_path is not None and window.exported_path is None
        if window.result_path is None:
            raise RuntimeError(window.status.text())
        checks['cuatro_metricas_comparadas'] = window.metrics_table.rowCount() == 4
        window.tabs.setCurrentWidget(window.player)
        window.player.seek(280)
        app.processEvents()
        window.grab().save(str(evidence / 'comparacion-interfaz.png'))
        checks['consulta_instante_14s'] = window.player.frame_index == 280
        window.tabs.setCurrentWidget(window.metrics_table)
        app.processEvents()
        window.grab().save(str(evidence / 'metricas-interfaz.png'))
        window.start_export(root / 'data/output/sw06'); wait()
        if window.exported_path is None:
            raise RuntimeError(window.status.text())
        exported = window.exported_path
        receipt = json.loads((exported / 'exportacion.json').read_text())
        checks['copias_integras'] = all(hashlib.sha256((exported / name).read_bytes()).hexdigest() == item['sha256']
                                      for name, item in receipt['files'].items())
        checks['resumen_local'] = (exported / 'resumen.html').is_file()
        checks['estado_exportacion'] = window.state == 'Resultados disponibles'
        window.reset()
        checks['reinicio_conserva_exportacion'] = window.state == 'En espera' and (exported / 'informe.json').exists()
        shutil.copytree(exported, evidence / 'ejemplo')
        result = {'fecha_corte': '2026-10-21', 'actividad': 'ACT-SW-06', 'tipo': 'Simulación; no captura real',
                  'exportacion_local': str(exported.relative_to(root)), 'qt_platform': app.platformName(), 'checks': checks}
        (evidence / 'flujo.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not all(checks.values()):
            raise RuntimeError('Hay criterios que no se cumplieron.')
    finally:
        if window.worker is not None:
            window.cancel()
            window.worker.wait()
            app.processEvents()
        window.close()


if __name__ == '__main__':
    main()
