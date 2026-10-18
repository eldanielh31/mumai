import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import sys, subprocess, importlib, tempfile
from pathlib import Path
for name in ("numpy", "scipy", "cv2", "matplotlib", "PySide6", "sklearn"):
    module = importlib.import_module(name)
    print(name, module.__version__)
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import QLibraryInfo
if "cv2/qt" in os.environ.get("QT_QPA_PLATFORM_PLUGIN_PATH", ""):
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
app = QApplication([])
label = QLabel("Verificación")
label.show()
app.processEvents()
print(f"Qt: ventana creada correctamente ({app.platformName()})")
import cv2, numpy as np
with tempfile.TemporaryDirectory() as folder:
    path = str(Path(folder) / "test.avi")
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"MJPG"), 10, (64,64))
    assert writer.isOpened(), "No se pudo abrir el codificador"
    for i in range(10):
        writer.write(np.full((64,64,3), i*20, dtype=np.uint8))
    writer.release()
    capture = cv2.VideoCapture(path)
    ok, frame = capture.read()
    capture.release()
    assert ok and frame.shape == (64,64,3)
print("OpenCV: escritura y lectura de video correctas")
print("Python", sys.version)
failed = False
for command in (["git", "--version"], ["ffmpeg", "-version"]):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        lines = (result.stdout or result.stderr).splitlines()
        print(command[0], result.returncode, lines[0] if lines else "Sin salida")
        failed = failed or result.returncode != 0
    except FileNotFoundError:
        print(command[0], "PENDIENTE: no instalado")
        failed = True
    except subprocess.TimeoutExpired:
        print(command[0], "ERROR: excedió el tiempo de verificación")
        failed = True
raise SystemExit(1 if failed else 0)
