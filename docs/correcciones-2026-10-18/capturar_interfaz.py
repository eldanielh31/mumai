"""Captura reproducible de una ejecución sintética; ejecutar desde la raíz del proyecto."""
import shutil
import time
from pathlib import Path
from PySide6.QtWidgets import QApplication
from video_analysis.gui.main_window import MainWindow

app = QApplication([])
root = Path.cwd()
out = root / 'docs/correcciones-2026-10-18'
window = MainWindow()

def wait():
    deadline = time.monotonic() + 60
    while window.worker is not None and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(.01)
    if window.worker is not None:
        window.cancel()
        window.worker.wait()
        app.processEvents()
        raise RuntimeError('La operación excedió 60 segundos.')

try:
    window.notes.setText('Escenario sintético de cambio de amplitud; cámara fija; iluminación constante.')
    window.dimension.setValue(160)
    window.show()
    window.load_video(str(root / 'data/input/referencias/amplitude_change.avi'))
    wait()
    window.configure()
    window.start_analysis()
    wait()
    if window.result_path is None:
        raise RuntimeError(window.status.text())
    app.processEvents()
    window.grab().save(str(out / 'interfaz.png'))
    for name in ('mapas_comparados.png', 'mapa_original.png', 'informe.json', 'patrones.json'):
        shutil.copyfile(window.result_path / name, out / name)
finally:
    window.close()
