import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

from video_analysis.gui.main_window import MainWindow

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from create_reference_videos import generate_reference
from create_sample import create_sample


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
                self.assertFalse(window.results_button.isEnabled())
                self.assertTrue(window.export_button.isEnabled())
                self.assertIn("0 ventanas", window.status.text())
                self.assertEqual(window.progress_bar.value(), 100)
                # Un parámetro cambiado invalida la vista anterior y un valor inválido no inicia trabajo.
                window.high.setValue(11)
                window.start_analysis()
                self.assertIsNone(window.worker)
                self.assertIn("FPS/2", window.status.text())
            finally:
                window.cancel()
                self.wait_for_load(window)
                window.close()

    def test_review_export_error_recovery_and_states(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = generate_reference(root / "static.avi", "static", seconds=10, size=(80, 64))
            window = MainWindow()
            window.dimension.setValue(80)
            try:
                self.assertEqual(window.state, "En espera")
                window.load_video(str(path))
                self.wait_for_load(window)
                self.assertEqual(window.state, "Entrada válida")
                window.configure()
                self.assertEqual(window.state, "Configurado")
                window.start_analysis()
                self.assertEqual(window.state, "Procesando")
                self.wait_for_load(window)
                self.assertEqual(window.state, "Resultados disponibles")
                self.assertIsNone(window.exported_path)
                original = window.result_path
                bad = root / "not_directory"
                bad.write_text("test")
                window.start_export(bad)
                self.wait_for_load(window)
                self.assertEqual(window.state, "Error controlado")
                self.assertEqual(window.result_path, original)
                self.assertIn("sigue disponible", window.status.text())
                window.start_export(root / "exported")
                self.wait_for_load(window)
                self.assertEqual(window.state, "Resultados disponibles")
                saved = window.exported_path
                self.assertEqual(
                    (saved / "metricas.csv").read_bytes(), (original / "metricas.csv").read_bytes()
                )
                self.assertTrue(window.results_button.isEnabled())
                with patch(
                    "video_analysis.pipeline.analyze_video",
                    side_effect=ValueError("Fallo controlado de prueba"),
                ):
                    window.start_analysis()
                    self.wait_for_load(window)
                self.assertEqual(window.state, "Error controlado")
                self.assertIsNone(window.result_path)
                self.assertEqual(window.details.text(), "")
                self.assertTrue(window.preview.pixmap().isNull())
                self.assertTrue(window.chart.pixmap().isNull())
                window.reset()
                self.assertEqual(window.state, "En espera")
                self.assertIsNone(window.info)
                self.assertTrue((saved / "informe.json").exists())
                self.assertFalse(original.exists())
            finally:
                window.cancel()
                self.wait_for_load(window)
                window.close()


if __name__ == "__main__":
    unittest.main()
