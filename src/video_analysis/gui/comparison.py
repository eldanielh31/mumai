"""Revisión sincronizada: ambas vistas pertenecen al mismo fotograma compuesto."""
import math
from pathlib import Path
import cv2
from PySide6.QtCore import Qt, QTimer, QElapsedTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider


class ComparisonPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.capture = None
        self.fps = 0
        self.frame_count = 0
        self.frame_index = 0
        self._pixmap = None
        self._start_index = 0
        self.clock = QElapsedTimer()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.image = QLabel('La comparación aparecerá al terminar el análisis.')
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setMinimumSize(300, 180)
        self.play_button = QPushButton('Reproducir')
        self.play_button.clicked.connect(self.toggle)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.seek)
        self.position = QLabel('Sin video')
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Original a la izquierda · Magnificado a la derecha · Mismo instante'))
        layout.addWidget(self.image, 1)
        controls = QHBoxLayout()
        controls.addWidget(self.play_button)
        controls.addWidget(self.slider, 1)
        controls.addWidget(self.position)
        layout.addLayout(controls)
        self.clear()

    def clear(self):
        self.pause()
        if self.capture is not None:
            self.capture.release()
        self.capture = None
        self._pixmap = None
        self.frame_count = 0
        self.frame_index = 0
        self.image.setText('La comparación aparecerá al terminar el análisis.')
        self.slider.blockSignals(True)
        self.slider.setRange(0, 0)
        self.slider.blockSignals(False)
        self.slider.setEnabled(False)
        self.play_button.setEnabled(False)
        self.position.setText('Sin video')

    def load(self, path):
        self.clear()
        capture = cv2.VideoCapture(str(Path(path)), cv2.CAP_FFMPEG)
        fps = capture.get(cv2.CAP_PROP_FPS)
        count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        if not capture.isOpened() or not math.isfinite(fps) or fps <= 0 or not math.isfinite(count) or count < 1:
            capture.release()
            self.position.setText('No se pudo abrir la comparación.')
            return False
        self.capture, self.fps, self.frame_count = capture, fps, int(count)
        self.slider.setRange(0, self.frame_count - 1)
        self.slider.setEnabled(True)
        self.play_button.setEnabled(True)
        return self.show_frame(0)

    def pause(self):
        self.timer.stop()
        self.play_button.setText('Reproducir')

    def toggle(self):
        if self.capture is None:
            return
        if self.timer.isActive():
            self.pause()
            return
        if self.frame_index >= self.frame_count - 1:
            if not self.show_frame(0):
                return
        self._start_index = self.frame_index
        self.clock.start()
        self.play_button.setText('Pausar')
        self.timer.start(max(1, round(1000 / self.fps)))

    def tick(self):
        target = min(self.frame_count - 1, self._start_index + int(self.clock.elapsed() * self.fps / 1000))
        if target != self.frame_index:
            self.show_frame(target)
        if target >= self.frame_count - 1:
            self.pause()

    def seek(self, frame):
        self.pause()
        if self.capture is not None:
            self.show_frame(frame)

    def show_frame(self, index):
        if self.capture is None:
            return False
        index = max(0, min(int(index), self.frame_count - 1))
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, index)
        ok, frame = self.capture.read()
        if not ok:
            self.clear()
            self.position.setText('No se pudo leer el fotograma. Puedes abrir el video exportado.')
            return False
        self.frame_index = index
        h, w = frame.shape[:2]
        image = QImage(frame.data, w, h, frame.strides[0], QImage.Format.Format_BGR888).copy()
        self._pixmap = QPixmap.fromImage(image)
        self.render_frame()
        self.slider.blockSignals(True)
        self.slider.setValue(index)
        self.slider.blockSignals(False)
        self.position.setText(f'{index / self.fps:.2f} / {(self.frame_count - 1) / self.fps:.2f} s')
        return True

    def render_frame(self):
        if self._pixmap is not None:
            self.image.setPixmap(self._pixmap.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.render_frame()

    def hideEvent(self, event):
        self.pause()
        super().hideEvent(event)
