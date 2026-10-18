import json, tempfile, socket, hashlib
from pathlib import Path
from unittest.mock import patch
from video_analysis.pipeline import analyze_video, AnalysisConfig
root=Path.cwd()
source=root/'data/input/referencias/subtle.avi'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=digest(source)
with tempfile.TemporaryDirectory(prefix='daniel-audit-') as tmp:
    tmp=Path(tmp)
    a=analyze_video(source,tmp/'repeat')
    b=analyze_video(source,tmp/'repeat')
    names=['metricas.csv','movimiento_original.npy','movimiento_magnificado.npy','patrones.json']
    results={'network_interfaces':Path('/proc/net/dev').read_text(),'repeat_identical':{n:digest(a/n)==digest(b/n) for n in names}}
    with patch('video_analysis.pipeline.os.rename',side_effect=PermissionError('Fallo de exportación provocado por auditoría')):
        try:
            analyze_video(source,tmp/'failed')
            results['export_error_raised']=False
        except PermissionError as e:
            results['export_error_raised']=True
            results['error']=str(e)
    results['no_partial_export']=not list((tmp/'failed').iterdir())
    c=analyze_video(source,tmp/'recovery')
    results['recovery_success']=(c/'informe.json').exists()
    results['input_unchanged']=digest(source)==before
print(json.dumps(results,ensure_ascii=False,indent=2))
