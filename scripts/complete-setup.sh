#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
bash scripts/install-system.sh
source .venv/bin/activate
python -m pip check
python scripts/verify.py | tee docs/verification.txt
missing=$(ldd .venv/lib/python3.13/site-packages/PySide6/Qt/plugins/platforms/libqxcb.so | sed -n '/not found/p')
if [[ -n "$missing" ]]; then
    echo "$missing"
    exit 1
fi
printf 'Instalación del sistema y verificación completadas.\n'
