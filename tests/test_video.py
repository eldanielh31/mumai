import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from create_sample import create_sample

from video_analysis.__main__ import main
from video_analysis.video import ValidationCancelled, VideoError, inspect_video, iter_frames


class VideoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.video = create_sample(self.root / "prueba con espacios á.avi")

    def test_avi_metadata_and_sequential_frames(self):
        info, first = inspect_video(self.video)
        self.assertEqual((info.width, info.height, info.frame_count), (320, 240, 30))
        self.assertAlmostEqual(info.fps, 10)
        self.assertAlmostEqual(info.duration_seconds, 3)
        frames = list(iter_frames(info))
        self.assertEqual(len(frames), 30)
        np.testing.assert_array_equal(frames[0], first)
        self.assertFalse(np.array_equal(frames[0], frames[-1]))

    def test_mp4(self):
        info, _ = inspect_video(create_sample(self.root / "sample.mp4", codec="mp4v"))
        self.assertEqual(info.frame_count, 30)

    def test_missing_directory_empty_unsupported_and_corrupt(self):
        empty = self.root / "empty.avi"
        empty.touch()
        unsupported = self.root / "file.txt"
        unsupported.write_text("texto")
        corrupt = self.root / "corrupt.mp4"
        corrupt.write_bytes(b"not a video")
        for path, message in [
            (self.root / "missing.avi", "no existe"),
            (self.root, "carpeta"),
            (empty, "vacío"),
            (unsupported, "Formato"),
            (corrupt, "No se pudo abrir"),
        ]:
            with self.subTest(path=path):
                with self.assertRaisesRegex(VideoError, message):
                    inspect_video(path)

    def test_truncated_video(self):
        truncated = self.root / "truncated.avi"
        data = self.video.read_bytes()
        truncated.write_bytes(data[: len(data) // 2])
        with self.assertRaises(VideoError):
            inspect_video(truncated)

    def test_cancel(self):
        with self.assertRaises(ValidationCancelled):
            inspect_video(self.video, cancelled=lambda: True)

    def test_changed_video_after_validation(self):
        info, _ = inspect_video(self.video)
        create_sample(self.video, frames=4)
        with self.assertRaisesRegex(VideoError, "incompleta"):
            list(iter_frames(info))

    def test_cli_json(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main([str(self.video), "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["frame_count"], 30)

    def test_cli_invalid(self):
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            self.assertEqual(main([str(self.root / "missing.mp4")]), 1)
        self.assertIn("no existe", output.getvalue())

    def test_invalid_fps_releases_file(self):
        with patch("video_analysis.video.loader.cv2.VideoCapture") as factory:
            capture = factory.return_value
            capture.get.return_value = float("nan")
            with self.assertRaisesRegex(VideoError, "FPS"):
                inspect_video(self.video)
            capture.release.assert_called_once()


if __name__ == "__main__":
    unittest.main()
