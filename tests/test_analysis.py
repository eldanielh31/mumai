import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from create_reference_videos import generate_reference
from video_analysis.magnification.eulerian import EulerianMagnifier
from video_analysis.motion.optical_flow import MotionAnalyzer
from video_analysis.heatmaps.maps import render_pair
from video_analysis.anomalies.patterns import detect_patterns
from video_analysis.pipeline import AnalysisConfig, analyze_video
from video_analysis.video import ValidationCancelled, VideoInfo, VideoError, iter_frames


class AlgorithmTests(unittest.TestCase):
    def temporal_gain(self, frequency):
        evm = EulerianMagnifier(20, .7, 1.5, 5, 1)
        inputs, outputs = [], []
        for i in range(400):
            value = round(128 + 5 * np.sin(2 * np.pi * frequency * i / 20))
            frame = np.full((32, 32, 3), value, np.uint8)
            result = evm.process(frame)
            if i >= 100:
                inputs.append(value)
                outputs.append(result[16, 16, 0])
        return np.std(outputs) / np.std(inputs)

    def test_frequency_selectivity(self):
        inside, outside = self.temporal_gain(1), self.temporal_gain(5)
        self.assertGreater(inside, 3)
        self.assertLess(outside, 1.5)

    def test_static_and_zero_amplification(self):
        for alpha in (0, 5):
            evm = EulerianMagnifier(20, alpha=alpha)
            image = np.full((32, 32, 3), 120, np.uint8)
            for _ in range(40):
                np.testing.assert_array_equal(evm.process(image), image)

    def test_reject_bad_parameters(self):
        for kwargs in ({"low_hz": 2, "high_hz": 1}, {"high_hz": 10},
                       {"alpha": float("nan")}, {"alpha": -1}, {"level": 8}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                EulerianMagnifier(20, **kwargs)

    def test_flow_known_translation(self):
        rng = np.random.default_rng(5)
        gray = rng.integers(0, 256, (96, 96), dtype=np.uint8)
        frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        moved = cv2.warpAffine(frame, np.float32([[1, 0, 1], [0, 1, 0]]), (96, 96))
        flow = MotionAnalyzer()
        self.assertIsNone(flow.process(frame))
        magnitude = flow.process(moved)
        self.assertAlmostEqual(float(np.median(magnitude[20:-20, 20:-20])), 1, delta=.15)

    def test_heatmaps_shared_scale(self):
        original, amplified, maximum = render_pair(np.ones((8, 8)), np.ones((8, 8)) * 2)
        self.assertEqual(maximum, 2)
        self.assertFalse(np.array_equal(original, amplified))

    def test_patterns_no_future_leakage(self):
        windows = [{"start_seconds": i * .5, "end_seconds": (i + 1) * .5,
                    "original_rms": .1 if i < 12 else 1.,
                    "original_p95": .2 if i < 12 else 2.} for i in range(20)]
        result = detect_patterns(windows, 6)
        self.assertEqual(result["reference_windows"], 12)
        self.assertEqual(len(result["events"]), 8)
        np.testing.assert_allclose(result["median"], [.1, .2])
        stable = [dict(w, original_rms=.1, original_p95=.2) for w in windows]
        self.assertEqual(detect_patterns(stable, 6)["events"], [])
        self.assertEqual(detect_patterns(windows[:4], 6)["status"], "insufficient_reference")

    def test_variable_timing_rejected(self):
        with patch("video_analysis.video.loader._open") as opened:
            capture = opened.return_value[1]
            opened.return_value = (Path("test.avi"), capture)
            capture.read.side_effect = [(True, np.zeros((32, 32, 3), np.uint8))] * 3
            capture.get.side_effect = [0, 50, 130]
            info = VideoInfo(Path("test.avi"), 20, 32, 32, 3)
            with self.assertRaisesRegex(VideoError, "variable"):
                list(iter_frames(info, require_constant_fps=True))
            capture.release.assert_called_once()


class PipelineTests(unittest.TestCase):
    def test_complete_export_and_static_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            video = generate_reference(root / "static.avi", "static", seconds=10, size=(80, 64))
            result = analyze_video(video, root / "results", AnalysisConfig(max_dimension=80))
            report = json.loads((result / "informe.json").read_text())
            self.assertLess(report["original"]["mean_px_frame"], 1e-4)
            self.assertLess(report["magnified"]["mean_px_frame"], 1e-4)
            self.assertEqual(report["patterns_status"], "evaluated")
            self.assertEqual(report["flagged_windows"], 0)
            self.assertTrue((result / "comparacion.avi").is_file())
            self.assertEqual(len(report["input_sha256"]), 64)
            self.assertFalse(list((root / "results").glob(".processing-*")))

    def test_cancel_leaves_no_published_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            video = generate_reference(root / "test.avi", seconds=5, size=(80, 64))
            state = {"cancel": False}
            with self.assertRaises(ValidationCancelled):
                analyze_video(video, root / "results", cancelled=lambda: state["cancel"],
                              progress=lambda _: state.update(cancel=True))
            self.assertEqual(list((root / "results").iterdir()), [])
            self.assertTrue(video.exists())

    def test_short_video_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            video = generate_reference(Path(tmp) / "short.avi", seconds=1)
            with self.assertRaisesRegex(ValueError, "corto"):
                analyze_video(video, Path(tmp) / "results")


if __name__ == "__main__":
    unittest.main()
