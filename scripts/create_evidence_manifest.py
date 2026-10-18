"""Conservar identidad de la versión y evidencia sin incluir videos o entornos locales."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', help='Archivo JSON nuevo para el manifiesto')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    target = Path(args.output).resolve()
    if target.exists():
        parser.error('El manifiesto ya existe; usa otra ruta para conservar el historial.')
    files = [root / name for name in ('README.md', 'requirements.txt', 'requirements.in', 'run.sh')]
    for folder in ('src', 'scripts', 'tests', 'docs'):
        files.extend(p for p in (root / folder).rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts and p.suffix != '.pyc' and p.resolve() != target)
    hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    base = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(),
                                 'base_commit': base, 'scope': 'Archivos del árbol de trabajo al generar este registro; no incluye videos ni entornos.',
                                 'sha256': hashes}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Manifiesto guardado: {target} ({len(hashes)} archivos)')


if __name__ == '__main__':
    main()
