import json,time,tempfile
from pathlib import Path
from PySide6.QtWidgets import QApplication
from video_analysis.gui.main_window import MainWindow
app=QApplication([])
w=MainWindow()
def wait():
    deadline=time.monotonic()+60
    while w.worker is not None and time.monotonic()<deadline:
        app.processEvents();time.sleep(.01)
    assert w.worker is None
with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    w.output_root=root/'good'
    w.load_video(str(Path.cwd()/'data/input/referencias/subtle.avi'));wait()
    w.start_analysis();wait()
    assert w.result_path is not None
    details=w.details.text(); preview=w.preview.pixmap().cacheKey()
    bad=root/'not_directory';bad.write_text('audit')
    w.output_root=bad
    w.start_analysis();wait()
    result={'error_status':w.status.text(),'result_path_cleared':w.result_path is None,'old_details_still_visible':w.details.text()==details,'old_preview_still_visible':w.preview.pixmap().cacheKey()==preview,'results_button_disabled':not w.results_button.isEnabled()}
    w.output_root=root/'recovered';w.start_analysis();wait()
    result['gui_recovery_success']=w.result_path is not None
    w.close()
print(json.dumps(result,ensure_ascii=False,indent=2))
