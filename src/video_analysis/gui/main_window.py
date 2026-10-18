"""Interfaz mínima del primer módulo: selección, validación y vista previa."""

import os
import json
from pathlib import Path
from PySide6.QtCore import Qt, QThread, Signal, QLibraryInfo, QUrl
from PySide6.QtGui import QImage, QPixmap, QDesktopServices
from PySide6.QtWidgets import (
    QFileDialog, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QDoubleSpinBox, QSpinBox, QCheckBox, QFormLayout, QGroupBox, QHBoxLayout,
    QProgressBar, QLineEdit, QTabWidget,
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


class AnalysisWorker(QThread):
    completed = Signal(object)
    failed = Signal(str)
    progress = Signal(int)

    def __init__(self, path, output, config, parent=None):
        super().__init__(parent)
        self.path, self.output, self.config = path, output, config

    def run(self):
        from video_analysis.pipeline import analyze_video
        try:
            result = analyze_video(self.path, self.output, self.config,
                                   self.isInterruptionRequested, self.progress.emit)
            self.completed.emit(result)
        except (ValueError, OSError) as exc:
            self.failed.emit(str(exc))
        except Exception as exc:
            self.failed.emit(f"El análisis no pudo completarse: {exc}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.info = None
        self._closing = False
        self.result_path = None
        self.output_root = Path(__file__).resolve().parents[3] / "data/output"
        self.setWindowTitle("Proyecto Final — Magnificación y análisis de video")
        self.resize(1000, 850)
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.open_button = QPushButton("Seleccionar video")
        self.open_button.clicked.connect(self.choose_video)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setEnabled(False)
        self.status = QLabel("Selecciona un video para comprobar su lectura.")
        self.status.setWordWrap(True)
        self.details = QLabel()
        self.details.setTextFormat(Qt.TextFormat.PlainText)
        self.details.setWordWrap(True)
        self.preview = QLabel("Vista previa del primer fotograma")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart = QLabel("El gráfico aparecerá después del análisis")
        self.chart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tabs = QTabWidget()
        self.tabs.addTab(self.preview, "Vista previa / mapas")
        self.tabs.addTab(self.chart, "Métricas en el tiempo")
        self.settings = QGroupBox("Configuración del análisis")
        form = QFormLayout(self.settings)
        self.low = QDoubleSpinBox()
        self.low.setRange(.05, 1000)
        self.low.setValue(.7)
        self.high = QDoubleSpinBox()
        self.high.setRange(.1, 1000)
        self.high.setValue(1.5)
        self.alpha = QDoubleSpinBox()
        self.alpha.setRange(0, 30)
        self.alpha.setValue(5)
        self.baseline = QDoubleSpinBox()
        self.baseline.setRange(1, 36000)
        self.baseline.setValue(8)
        self.dimension = QSpinBox()
        self.dimension.setRange(64, 1280)
        self.dimension.setValue(480)
        self.spatial_level = QSpinBox()
        self.spatial_level.setRange(0, 4)
        self.spatial_level.setValue(1)
        self.patterns = QCheckBox("Detectar cambios respecto al tramo inicial de referencia")
        self.patterns.setChecked(True)
        self.notes = QLineEdit()
        self.notes.setPlaceholderText("Describe iluminación, estabilidad de cámara y escenario")
        band = QHBoxLayout()
        for label, control in (("Mínima (Hz)", self.low), ("Máxima (Hz)", self.high), ("Amplificación", self.alpha)):
            band.addWidget(QLabel(label))
            band.addWidget(control)
        form.addRow(band)
        form.addRow("Referencia inicial (segundos)", self.baseline)
        form.addRow("Dimensión máxima (píxeles)", self.dimension)
        form.addRow("Nivel de reducción espacial", self.spatial_level)
        form.addRow(self.patterns)
        form.addRow("Condiciones de captura", self.notes)
        self.analyze_button = QPushButton("Analizar y guardar resultados")
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.start_analysis)
        self.results_button = QPushButton("Abrir carpeta de resultados")
        self.results_button.setEnabled(False)
        self.results_button.clicked.connect(self.open_results)
        self.comparison_button = QPushButton("Abrir video comparativo")
        self.comparison_button.setEnabled(False)
        self.comparison_button.clicked.connect(self.open_comparison)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        for widget in (self.open_button, self.settings, self.analyze_button, self.cancel_button,
                       self.progress_bar, self.status, self.details, self.tabs, self.results_button, self.comparison_button):
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
        self.result_path = None
        self.results_button.setEnabled(False)
        self.comparison_button.setEnabled(False)
        self.chart.clear()
        self.analyze_button.setEnabled(False)
        self.settings.setEnabled(False)
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
            800, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation,
        ))

    def start_analysis(self):
        if self.worker is not None or self.info is None:
            return
        from video_analysis.pipeline import AnalysisConfig
        config = AnalysisConfig(low_hz=self.low.value(), high_hz=self.high.value(),
                                alpha=self.alpha.value(), baseline_seconds=self.baseline.value(),
                                max_dimension=self.dimension.value(), patterns_enabled=self.patterns.isChecked(),
                                spatial_level=self.spatial_level.value(),
                                capture_notes=self.notes.text() or "Condiciones no documentadas.")
        try:
            config.validate(self.info.fps)
        except ValueError as exc:
            self.status.setText(str(exc))
            return
        self.result_path = None
        self.results_button.setEnabled(False)
        self.comparison_button.setEnabled(False)
        self.open_button.setEnabled(False)
        self.analyze_button.setEnabled(False)
        self.settings.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status.setText("Procesando video y preparando resultados…")
        self.worker = AnalysisWorker(self.info.path, self.output_root, config, self)
        self.worker.completed.connect(self.show_results)
        self.worker.failed.connect(self.status.setText)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.finished)
        self.worker.start()

    def show_results(self, path):
        self.result_path = Path(path)
        report = json.loads((self.result_path / "informe.json").read_text())
        state = {"evaluated": f"{report['flagged_windows']} ventanas con cambios respecto a la referencia",
                 "disabled": "Análisis de patrones desactivado",
                 "insufficient_reference": "Referencia insuficiente para evaluar patrones; consulta el informe"}[report["patterns_status"]]
        self.status.setText(f"Análisis guardado. {state}. Los resultados no constituyen un diagnóstico de daños.")
        self.details.setText(
            f"Movimiento medio: original {report['original']['mean_px_frame']:.5f} / "
            f"magnificado {report['magnified']['mean_px_frame']:.5f} px/fotograma\n"
            f"Mapas: original a la izquierda y magnificado a la derecha; escala común 0–{report['heatmap_scale']['max']:.5f} px/fotograma.\n"
            f"Resultados: {path}"
        )
        self.preview.setPixmap(QPixmap(str(self.result_path / "mapas_comparados.png")).scaled(
            800, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.results_button.setEnabled(True)
        self.comparison_button.setEnabled(True)
        self.chart.setPixmap(QPixmap(str(self.result_path / "movimiento.png")).scaled(
            800, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def open_results(self):
        if self.result_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.result_path)))

    def open_comparison(self):
        if self.result_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.result_path / "comparacion.avi")))

    def cancel(self):
        if self.worker is not None:
            self.worker.requestInterruption()

    def finished(self):
        self.worker.deleteLater()
        self.worker = None
        self.open_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.settings.setEnabled(True)
        self.analyze_button.setEnabled(self.info is not None)
        if self._closing:
            self.close()

    def closeEvent(self, event):
        if self.worker is not None:
            self._closing = True
            self.cancel()
            event.ignore()
        else:
            event.accept()
