"""Exportación explícita de un análisis revisado, sin sobrescribir otras ejecuciones."""
from pathlib import Path
import os
import json
import hashlib
from datetime import datetime, timezone
import shutil
import tempfile
import uuid
from video_analysis.video import ValidationCancelled


def export_results(source, destination, cancelled=lambda: False):
    source, destination = Path(source).resolve(), Path(destination).expanduser().resolve()
    if not (source / 'informe.json').is_file():
        raise ValueError('No hay un análisis completo para exportar.')
    if destination == source or source in destination.parents:
        raise ValueError('Selecciona una carpeta fuera del resultado temporal.')
    destination.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.export-', dir=destination))
    final = destination / f'{source.name}-export-{uuid.uuid4().hex[:8]}'
    try:
        files = {}
        def digest(path):
            sha = hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    if cancelled():
                        raise ValidationCancelled('Exportación cancelada. El análisis sigue disponible.')
                    sha.update(block)
            return sha.hexdigest()
        for item in source.iterdir():
            if cancelled():
                raise ValidationCancelled('Exportación cancelada. El análisis sigue disponible.')
            if item.is_file():
                shutil.copy2(item, staging / item.name)
                copied = digest(staging / item.name)
                if copied != digest(item):
                    raise OSError(f'La copia de {item.name} no coincide con el análisis original.')
                files[item.name] = {'sha256': copied, 'bytes': item.stat().st_size}
        if cancelled():
            raise ValidationCancelled('Exportación cancelada. El análisis sigue disponible.')
        receipt = {'schema_version': 1, 'exported_utc': datetime.now(timezone.utc).isoformat(),
                   'files': files, 'purpose': 'Integridad de los archivos copiados; no certifica exactitud del análisis.'}
        (staging / 'exportacion.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
        if cancelled():
            raise ValidationCancelled('Exportación cancelada. El análisis sigue disponible.')
        os.rename(staging, final)
        return final
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
