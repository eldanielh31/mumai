"""Interfaz de análisis, revisión y exportación con estados explícitos."""

import os
import json
import tempfile
from pathlib import Path
from PySide6.QtCore import Qt, QThread, Signal, QLibraryInfo, QUrl
from PySide6.QtGui import QImage, QPixmap, QDesktopServices
from PySide6.QtWidgets import (
    QFileDialog, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QDoubleSpinBox, QSpinBox, QCheckBox, QFormLayout, QGroupBox, QHBoxLayout,
    QProgressBar, QLineEdit, QTabWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView,
)

from video_analysis.video import VideoError, inspect_video
from video_analysis.gui.comparison import ComparisonPlayer

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
        try:
            from video_analysis.pipeline import analyze_video
            result = analyze_video(self.path, self.output, self.config,
                                   self.isInterruptionRequested, self.progress.emit)
            self.completed.emit(result)
        except (ValueError, OSError) as exc:
            self.failed.emit(str(exc))
        except Exception as exc:
            self.failed.emit(f"El análisis no pudo completarse: {exc}")


class ExportWorker(QThread):
    completed = Signal(object)
    failed = Signal(str)

    def __init__(self, source, destination, parent=None):
        super().__init__(parent)
        self.source, self.destination = source, destination

    def run(self):
        try:
            from video_analysis.export.package import export_results
            self.completed.emit(export_results(self.source, self.destination, self.isInterruptionRequested))
        except Exception as exc:
            self.failed.emit(f"No se exportaron los resultados: {exc}. El análisis sigue disponible para revisar o reintentar.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.info = None
        self._closing = False
        self.result_path = None
        self.exported_path = None
        self._session = tempfile.TemporaryDirectory(prefix="video-analysis-")
        self.output_root = Path(__file__).resolve().parents[3] / "data/output"
        self.setWindowTitle("Proyecto Final — Magnificación y análisis de video")
        self.resize(1000, 800)
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.open_button = QPushButton("Seleccionar video")
        self.open_button.clicked.connect(self.choose_video)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setEnabled(False)
        self.state_label = QLabel("Estado: En espera")
        self.state = "En espera"
        self.status = QLabel("Selecciona un video para comprobar su lectura.")
        self.reset_button = QPushButton("Volver a En espera (descartar análisis sin exportar)")
        self.reset_button.clicked.connect(self.reset)
        self.configure_button = QPushButton("Validar configuración")
        self.configure_button.clicked.connect(self.configure)
        self.configure_button.setEnabled(False)
        self.export_button = QPushButton("Exportar resultados…")
        self.export_button.clicked.connect(self.choose_export)
        self.export_button.setEnabled(False)
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
        self.player = ComparisonPlayer()
        self.tabs.addTab(self.player, "Video comparativo")
        self.metrics_table = QTableWidget(0, 3)
        self.metrics_table.setHorizontalHeaderLabels(["Indicador", "Original", "Magnificado"])
        self.metrics_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.metrics_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabs.addTab(self.metrics_table, "Resumen numérico")
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
        self.analyze_button = QPushButton("Analizar")
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
        layout.addWidget(self.open_button)
        layout.addWidget(self.settings)
        actions = QHBoxLayout()
        for widget in (self.configure_button, self.analyze_button, self.cancel_button):
            actions.addWidget(widget)
        layout.addLayout(actions)
        for widget in (self.state_label, self.progress_bar, self.status, self.details, self.tabs):
            layout.addWidget(widget)
        outputs = QHBoxLayout()
        for widget in (self.export_button, self.results_button, self.comparison_button):
            outputs.addWidget(widget)
        layout.addLayout(outputs)
        layout.addWidget(self.reset_button)
        self.setCentralWidget(panel)
        for control in (self.low, self.high, self.alpha, self.baseline, self.dimension, self.spatial_level):
            control.valueChanged.connect(self.configuration_changed)
        self.patterns.toggled.connect(self.configuration_changed)
        self.notes.textChanged.connect(self.configuration_changed)

    def set_state(self, state, message):
        self.state = state
        self.state_label.setText(f"Estado: {state}")
        self.status.setText(message)

    def show_error(self, message):
        self.set_state("Error controlado", message)

    def clear_results(self):
        self.result_path = None
        self.exported_path = None
        self.results_button.setEnabled(False)
        self.comparison_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.details.clear()
        self.preview.clear()
        self.chart.clear()
        self.player.clear()
        self.metrics_table.setRowCount(0)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

    def reset(self):
        if self.worker is not None:
            return
        self.clear_results()
        self.info = None
        self._session.cleanup()
        self._session = tempfile.TemporaryDirectory(prefix="video-analysis-")
        self.progress_bar.setValue(0)
        self.analyze_button.setEnabled(False)
        self.configure_button.setEnabled(False)
        self.set_state("En espera", "Selecciona un video. Los análisis sin exportar se han descartado.")

    def configuration_changed(self, *_):
        if self.info is not None and self.worker is None:
            self.clear_results()
            self.set_state("Entrada válida", "Configuración modificada. Valídala antes de analizar.")

    def configure(self):
        if self.info is None or self.worker is not None:
            return None
        from video_analysis.pipeline import AnalysisConfig
        config = AnalysisConfig(low_hz=self.low.value(), high_hz=self.high.value(),
                                alpha=self.alpha.value(), baseline_seconds=self.baseline.value(),
                                max_dimension=self.dimension.value(), patterns_enabled=self.patterns.isChecked(),
                                spatial_level=self.spatial_level.value(),
                                capture_notes=self.notes.text() or "Condiciones no documentadas.")
        try:
            config.validate(self.info.fps)
        except ValueError as exc:
            self.clear_results()
            self.show_error(str(exc))
            return None
        self.set_state("Configurado", "Parámetros válidos. Puedes iniciar el análisis.")
        return config

    def choose_export(self):
        if self.result_path is None or self.worker is not None:
            return
        destination = QFileDialog.getExistingDirectory(self, "Exportar resultados", str(self.output_root))
        if destination:
            self.start_export(destination)

    def start_export(self, destination):
        if self.result_path is None or self.worker is not None:
            return
        selected = Path(destination).expanduser().resolve()
        temporary = Path(self._session.name).resolve()
        if selected == temporary or temporary in selected.parents:
            self.show_error("Elige una carpeta permanente fuera de la sesión temporal para conservar la exportación.")
            return
        self.set_busy()
        self.progress_bar.setRange(0, 0)
        self.set_state("Procesando", "Exportando y verificando los resultados revisados…")
        self.worker = ExportWorker(self.result_path, destination, self)
        self.worker.completed.connect(self.export_completed)
        self.worker.failed.connect(self.show_error)
        self.worker.finished.connect(self.finished)
        self.worker.start()

    def export_completed(self, path):
        self.exported_path = Path(path)
        self.details.setText(self.details.text().rsplit("\n", 1)[0] + f"\nExportado en: {path}")
        self.set_state("Resultados disponibles", f"Exportación completada: {path}")

    def set_busy(self):
        for widget in (self.open_button, self.analyze_button, self.configure_button, self.settings,
                       self.reset_button, self.export_button, self.results_button, self.comparison_button):
            widget.setEnabled(False)
        self.cancel_button.setEnabled(True)

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
        self.clear_results()
        self.set_busy()
        self.set_state("En espera", "Validando todos los fotogramas antes de aceptar la entrada…")
        self.worker = VideoWorker(path, self)
        self.worker.loaded.connect(self.show_video)
        self.worker.failed.connect(self.show_error)
        self.worker.finished.connect(self.finished)
        self.worker.start()

    def show_video(self, info, frame):
        self.info = info
        self.set_state("Entrada válida", "Video validado. Revisa y valida la configuración.")
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
        config = self.configure()
        if config is None:
            return
        self.clear_results()
        self.set_busy()
        self.progress_bar.setValue(0)
        self.set_state("Procesando", "Procesando video. Después podrás revisar y exportar los resultados.")
        self.worker = AnalysisWorker(self.info.path, self._session.name, config, self)
        self.worker.completed.connect(self.show_results)
        self.worker.failed.connect(self.show_error)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.finished)
        self.worker.start()

    def show_results(self, path):
        self.result_path = Path(path)
        self.player.load(self.result_path / "comparacion.avi")
        report = json.loads((self.result_path / "informe.json").read_text())
        state = {"evaluated": f"{report['flagged_windows']} ventanas con cambios respecto a la referencia",
                 "disabled": "Análisis de patrones desactivado",
                 "insufficient_reference": "Referencia insuficiente para evaluar patrones; consulta el informe"}[report["patterns_status"]]
        self.set_state("Resultados disponibles", f"{state}. Revisa y exporta antes de cerrar o reiniciar. No constituye un diagnóstico de daños.")
        self.details.setText(
            f"Movimiento medio: original {report['original']['mean_px_frame']:.5f} / "
            f"magnificado {report['magnified']['mean_px_frame']:.5f} px/fotograma\n"
            f"Mapas: original a la izquierda y magnificado a la derecha; escala común 0–{report['heatmap_scale']['max']:.5f} px/fotograma.\n"
            "Análisis temporal pendiente de exportación."
        )
        self.preview.setPixmap(QPixmap(str(self.result_path / "mapas_comparados.png")).scaled(
            800, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        indicators = [("Media (px/fotograma)", "mean_px_frame"), ("Percentil 95 medio (px/fotograma)", "p95_px_frame"),
                      ("RMS medio (px/fotograma)", "rms_px_frame"), ("Media (px/s)", "mean_px_second")]
        self.metrics_table.setRowCount(len(indicators))
        for row, (label, key) in enumerate(indicators):
            for column, value in enumerate((label, f"{report['original'][key]:.6g}", f"{report['magnified'][key]:.6g}")):
                self.metrics_table.setItem(row, column, QTableWidgetItem(value))
        self.export_button.setEnabled(True)
        self.comparison_button.setEnabled(True)
        self.chart.setPixmap(QPixmap(str(self.result_path / "movimiento.png")).scaled(
            800, 280, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def open_results(self):
        if self.exported_path and not QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.exported_path))):
            self.show_error(f"No se pudo abrir la carpeta. Los resultados están guardados en: {self.exported_path}")

    def open_comparison(self):
        if self.result_path and not QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.result_path / "comparacion.avi"))):
            self.show_error("No se pudo abrir el reproductor externo. Usa la pestaña Video comparativo; el análisis sigue disponible.")

    def cancel(self):
        if self.worker is not None:
            self.worker.requestInterruption()

    def finished(self):
        self.worker.deleteLater()
        self.worker = None
        self.progress_bar.setRange(0, 100)
        self.open_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.settings.setEnabled(True)
        self.analyze_button.setEnabled(self.info is not None)
        self.configure_button.setEnabled(self.info is not None)
        self.reset_button.setEnabled(True)
        self.export_button.setEnabled(self.result_path is not None)
        self.comparison_button.setEnabled(self.result_path is not None)
        self.results_button.setEnabled(self.exported_path is not None)
        if self._closing:
            self.close()

    def closeEvent(self, event):
        if self.worker is not None:
            self._closing = True
            self.cancel()
            event.ignore()
        else:
            self.player.clear()
            self._session.cleanup()
            event.accept()
