import argparse
import json
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description="Carga y validación local de videos")
    parser.add_argument("video", nargs="?", help="Video que se validará sin abrir la interfaz")
    parser.add_argument("--json", action="store_true", help="Mostrar los datos en JSON (requiere video)")
    args = parser.parse_args(argv)
    if args.json and not args.video:
        parser.error("--json requiere la ruta de un video")
    if args.video:
        from video_analysis.video import VideoError, inspect_video
        try:
            info, _ = inspect_video(args.video)
        except (VideoError, OSError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(info.as_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"Video válido: {info.path.name}\n"
                  f"Resolución: {info.width} × {info.height}\n"
                  f"FPS: {info.fps:.3f}\nFotogramas: {info.frame_count}\n"
                  f"Duración estimada: {info.duration_seconds:.2f} s")
        return 0
    from PySide6.QtWidgets import QApplication
    from video_analysis.gui.main_window import MainWindow
    app = QApplication([sys.argv[0]])
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
