import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path
import sys
import tempfile
import time
import unittest

from PySide6.QtWidgets import QApplication
from video_analysis.gui.main_window import MainWindow

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from create_sample import create_sample
from create_reference_videos import generate_reference


class GuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def wait_for_load(self, window):
        deadline = time.monotonic() + 10
        while window.worker is not None and time.monotonic() < deadline:
            self.app.processEvents()
            time.sleep(0.01)
        self.assertIsNone(window.worker, "La validación no terminó")

    def test_load_preview_and_error_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            window = MainWindow()
            try:
                window.show()
                self.app.processEvents()
                path = create_sample(Path(directory) / "sample.avi")
                window.load_video(str(path))
                self.wait_for_load(window)
                self.assertEqual(window.info.frame_count, 30)
                self.assertFalse(window.preview.pixmap().isNull())
                self.assertIn("320 × 240", window.details.text())
                window.load_video(str(Path(directory) / "missing.mp4"))
                self.wait_for_load(window)
                self.assertIsNone(window.info)
                self.assertIn("no existe", window.status.text())
                self.assertTrue(window.open_button.isEnabled())
                self.assertEqual(window.details.text(), "")
                window.load_video(str(path))
                self.wait_for_load(window)
                self.assertIsNotNone(window.info)
            finally:
                window.cancel()
                self.wait_for_load(window)
                window.close()

    def test_close_during_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            window = MainWindow()
            window.show()
            window.load_video(str(create_sample(Path(directory) / "sample.avi")))
            window.close()
            self.wait_for_load(window)
            self.assertFalse(window.isVisible())

    def test_analysis_from_window(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = generate_reference(root / "static.avi", "static", seconds=10, size=(80, 64))
            window = MainWindow()
            window.output_root = root / "results"
            window.dimension.setValue(80)
            try:
                window.load_video(str(path))
                self.wait_for_load(window)
                window.start_analysis()
                self.wait_for_load(window)
                self.assertIsNotNone(window.result_path, window.status.text())
                self.assertTrue((window.result_path / "informe.json").exists())
                self.assertTrue(window.results_button.isEnabled())
                self.assertIn("0 ventanas", window.status.text())
                self.assertEqual(window.progress_bar.value(), 100)
                # Un parámetro inválido no inicia un trabajo ni borra el resultado previo.
                window.high.setValue(11)
                window.start_analysis()
                self.assertIsNone(window.worker)
                self.assertIn("FPS/2", window.status.text())
            finally:
                window.cancel()
                self.wait_for_load(window)
                window.close()


if __name__ == "__main__":
    unittest.main()
