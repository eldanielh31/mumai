"""Exportación explícita de un análisis revisado, sin sobrescribir otras ejecuciones."""
from pathlib import Path
import os
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
        for item in source.iterdir():
            if cancelled():
                raise ValidationCancelled('Exportación cancelada. El análisis sigue disponible.')
            if item.is_file():
                shutil.copy2(item, staging / item.name)
        if cancelled():
            raise ValidationCancelled('Exportación cancelada. El análisis sigue disponible.')
        os.rename(staging, final)
        return final
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
