"""La preparación no instala paquetes si el intérprete falta o es incompatible."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


@unittest.skipUnless(os.name == "posix" and shutil.which("bash"), "Preparación para Linux")
class SetupTests(unittest.TestCase):
    def check_rejected_before_system_changes(self, interpreter):
        source = Path(__file__).resolve().parents[1] / "scripts/complete-setup.sh"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "scripts"
            scripts.mkdir()
            shutil.copy2(source, scripts / "complete-setup.sh")
            marker = root / "system-install-invoked"
            (scripts / "install-system.sh").write_text('touch "' + str(marker) + '"\n')
            if interpreter == "incompatible":
                python = root / "incompatible-python"
                python.write_text("#!/bin/sh\nexit 1\n")
                python.chmod(0o700)
            else:
                python = root / "missing-python"
            process = subprocess.run(
                ["bash", str(scripts / "complete-setup.sh")],
                env=dict(os.environ, PROJECT_PYTHON=str(python), PROJECT_VENV=str(root / "venv")),
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(process.returncode, 0)
            self.assertFalse(marker.exists(), "No debe instalar paquetes sin Python válido")
            self.assertFalse((root / "venv").exists())

    def test_missing_python_does_not_install_system_packages(self):
        self.check_rejected_before_system_changes("missing")

    def test_incompatible_python_does_not_install_system_packages(self):
        self.check_rejected_before_system_changes("incompatible")


if __name__ == "__main__":
    unittest.main()
