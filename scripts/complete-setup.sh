#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
# --skip-system permite preparar/verificar Python sin modificar paquetes del equipo.
case "${1:-}" in
    --skip-system|'') ;;
    *) echo 'Uso: bash scripts/complete-setup.sh [--skip-system]' >&2; exit 2 ;;
esac
setup_env="${PROJECT_VENV:-.venv}"
setup_python="${PROJECT_PYTHON:-python3.13}"
# Comprobar el intérprete antes de pedir sudo o cambiar paquetes del sistema.
if [[ -x "$setup_env/bin/python" ]]; then
    setup_python="$setup_env/bin/python"
elif ! command -v "$setup_python" >/dev/null; then
    echo 'Se necesita Python 3.13. Define PROJECT_PYTHON con la ruta a ese intérprete; consulta README.md.' >&2
    exit 1
fi
"$setup_python" -c 'import sys; assert sys.version_info[:2] == (3, 13), "La versión verificada es Python 3.13"'
if [[ "${1:-}" != --skip-system ]]; then
    bash scripts/install-system.sh
fi
if [[ ! -x "$setup_env/bin/python" ]]; then
    "$setup_python" -m venv "$setup_env"
fi
"$setup_env/bin/python" -m pip install -r requirements.txt
"$setup_env/bin/python" -m pip check
mkdir -p docs
"$setup_env/bin/python" scripts/verify.py | tee docs/verification-install-latest.txt
setup_plugin=$("$setup_env/bin/python" -c 'from PySide6.QtCore import QLibraryInfo; print(QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath) + "/platforms/libqxcb.so")')
setup_missing=$(ldd "$setup_plugin" | sed -n '/not found/p')
if [[ -n "$setup_missing" ]]; then
    echo "$setup_missing" >&2
    exit 1
fi
printf 'Entorno creado, dependencias instaladas y verificadas.\n'
