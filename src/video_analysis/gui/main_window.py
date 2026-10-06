"""Interfaz mínima del primer módulo: selección, validación y vista previa."""

import os
from PySide6.QtCore import Qt, QThread, Signal, QLibraryInfo
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QFileDialog, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget,
)

from video_analysis.video import VideoError, inspect_video

# OpenCV puede dirigir Qt hacia sus propios plugins. La ventana usa Qt de PySide6.
if "cv2/qt" in os.environ.get("QT_QPA_PLATFORM_PLUGIN_PATH", ""):
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)


class VideoWorker(QThread):
    loaded = Signal(object, object)
    failed = Signal(str)

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path

    def run(self):
        try:
            info, frame = inspect_video(self.path, self.isInterruptionRequested)
            self.loaded.emit(info, frame)
        except (VideoError, OSError) as exc:
            self.failed.emit(str(exc))
        except Exception:
            self.failed.emit("No se pudo completar la lectura del video.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.info = None
        self._closing = False
        self.setWindowTitle("Proyecto Final — Carga de video")
        self.resize(900, 650)
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.open_button = QPushButton("Seleccionar video")
        self.open_button.clicked.connect(self.choose_video)
        self.cancel_button = QPushButton("Cancelar validación")
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setEnabled(False)
        self.status = QLabel("Selecciona un video para comprobar su lectura.")
        self.status.setWordWrap(True)
        self.details = QLabel()
        self.details.setTextFormat(Qt.TextFormat.PlainText)
        self.details.setWordWrap(True)
        self.preview = QLabel("Vista previa del primer fotograma")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for widget in (self.open_button, self.cancel_button, self.status, self.details, self.preview):
            layout.addWidget(widget)
        self.setCentralWidget(panel)

    def choose_video(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar video", "",
            "Videos (*.mp4 *.avi *.mov *.mkv *.m4v *.webm);;Todos los archivos (*)",
        )
        if path:
            self.load_video(path)

    def load_video(self, path):
        if self.worker is not None:
            return
        self.info = None
        self.details.clear()
        self.preview.clear()
        self.open_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.status.setText("Validando todos los fotogramas. Esto puede tardar según la duración del video…")
        self.worker = VideoWorker(path, self)
        self.worker.loaded.connect(self.show_video)
        self.worker.failed.connect(self.status.setText)
        self.worker.finished.connect(self.finished)
        self.worker.start()

    def show_video(self, info, frame):
        self.info = info
        self.status.setText("Video validado. Listo para la siguiente etapa de procesamiento.")
        self.details.setText(
            f"Archivo: {info.path.name}\n"
            f"Resolución: {info.width} × {info.height} píxeles\n"
            f"FPS: {info.fps:.3f}\nFotogramas leídos: {info.frame_count}\n"
            f"Duración estimada: {info.duration_seconds:.2f} segundos"
        )
        image = QImage(frame.data, info.width, info.height, frame.strides[0], QImage.Format.Format_BGR888).copy()
        self.preview.setPixmap(QPixmap.fromImage(image).scaled(
            800, 420, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation,
        ))

    def cancel(self):
        if self.worker is not None:
            self.worker.requestInterruption()

    def finished(self):
        self.worker.deleteLater()
        self.worker = None
        self.open_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        if self._closing:
            self.close()

    def closeEvent(self, event):
        if self.worker is not None:
            self._closing = True
            self.cancel()
            event.ignore()
        else:
            event.accept()
