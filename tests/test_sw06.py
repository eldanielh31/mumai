"""Aceptación técnica de visualización/comparación/exportación (ACT-SW-06)."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import hashlib
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication
from video_analysis.gui.main_window import MainWindow
from video_analysis.gui.comparison import ComparisonPlayer
from video_analysis.export.package import export_results
from video_analysis.export.summary import save_summary
from video_analysis.pipeline import analyze_video, AnalysisConfig
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from create_reference_videos import generate_reference


class SW06Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.folder = tempfile.TemporaryDirectory()
        cls.root = Path(cls.folder.name)
        cls.video = generate_reference(cls.root / 'static.avi', 'static', seconds=10, size=(80, 64))
        cls.analysis = analyze_video(cls.video, cls.root / 'analysis', AnalysisConfig(max_dimension=80))

    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def test_player_seek_play_pause_and_clear(self):
        player = ComparisonPlayer()
        try:
            self.assertTrue(player.load(self.analysis / 'comparacion.avi'))
            self.assertEqual(player.frame_index, 0)
            self.assertEqual(player.frame_count, 200)
            player.slider.setValue(100)
            self.assertEqual(player.frame_index, 100)
            self.assertIn('5.00', player.position.text())
            player.toggle()
            deadline = time.monotonic() + 1
            while player.frame_index <= 100 and time.monotonic() < deadline:
                self.app.processEvents(); time.sleep(.01)
            self.assertGreater(player.frame_index, 100)
            player.pause()
            self.assertFalse(player.timer.isActive())
            player.seek(199); player.toggle()
            self.assertEqual(player.frame_index, 0)
            player.clear()
            self.assertIsNone(player.capture)
            self.assertFalse(player.play_button.isEnabled())
        finally:
            player.clear(); player.close()

    def test_invalid_video_player_recovers(self):
        player = ComparisonPlayer()
        try:
            self.assertFalse(player.load(self.root / 'missing.avi'))
            self.assertTrue(player.load(self.analysis / 'comparacion.avi'))
        finally:
            player.clear(); player.close()

    def test_summary_is_local_escaped_and_complete(self):
        report = json.loads((self.analysis / 'informe.json').read_text())
        report['config']['capture_notes'] = '<script>alert("test")</script>'
        report['patterns_status'] = 'insufficient_reference'
        target = self.root / 'escaped.html'
        save_summary(report, target)
        html = target.read_text()
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('Referencia insuficiente', html)
        self.assertIn(report['input_sha256'], html)
        self.assertNotIn('https://', html)
        for file in ('mapas_comparados.png', 'movimiento.png', 'metricas.csv', 'informe.json', 'patrones.json', 'comparacion.avi'):
            self.assertIn(file, html)
            self.assertTrue((self.analysis / file).is_file())

    def test_export_receipt_matches_all_files(self):
        result = export_results(self.analysis, self.root / 'exports')
        receipt = json.loads((result / 'exportacion.json').read_text())
        for name, details in receipt['files'].items():
            self.assertEqual(hashlib.sha256((result / name).read_bytes()).hexdigest(), details['sha256'])
            self.assertEqual((result / name).stat().st_size, details['bytes'])
        self.assertIn('resumen.html', receipt['files'])
        self.assertIn('informe.json', receipt['files'])

    def test_corrupt_copy_not_published(self):
        def corrupt(source, target):
            Path(target).write_bytes(b'corrupted')
        destination = self.root / 'failed-copy'
        with patch('video_analysis.export.package.shutil.copy2', side_effect=corrupt):
            with self.assertRaisesRegex(OSError, 'no coincide'):
                export_results(self.analysis, destination)
        self.assertEqual(list(destination.iterdir()), [])
        self.assertTrue((self.analysis / 'informe.json').is_file())

    def test_metrics_and_fallback_preserve_result(self):
        window = MainWindow()
        try:
            window.show_results(self.analysis)
            self.assertEqual(window.metrics_table.rowCount(), 4)
            self.assertEqual(window.metrics_table.item(0, 1).text(), '0')
            self.assertIsNotNone(window.player.capture)
            with patch('video_analysis.gui.main_window.QDesktopServices.openUrl', return_value=False):
                window.open_comparison()
            self.assertIn('Video comparativo', window.status.text())
            self.assertEqual(window.result_path, self.analysis)
            window.start_export(window._session.name)
            self.assertIsNone(window.worker)
            self.assertIn('permanente', window.status.text())
            window.export_completed(self.root / 'first-export')
            window.export_completed(self.root / 'second-export')
            self.assertIn('second-export', window.details.text())
            self.assertNotIn('first-export', window.details.text())
            window.clear_results()
            self.assertEqual(window.metrics_table.rowCount(), 0)
            self.assertIsNone(window.player.capture)
        finally:
            window.close()


if __name__ == '__main__':
    unittest.main()
