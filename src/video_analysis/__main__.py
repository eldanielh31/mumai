import argparse
import json
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description="Carga y validación local de videos")
    parser.add_argument("video", nargs="?", help="Video que se validará sin abrir la interfaz")
    parser.add_argument(
        "--json", action="store_true", help="Mostrar los datos en JSON (requiere video)"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Ejecutar magnificación, movimiento, mapas y patrones",
    )
    parser.add_argument(
        "--output", default="data/output", help="Carpeta donde crear una ejecución nueva"
    )
    parser.add_argument("--low", type=float, default=0.7, help="Frecuencia mínima en Hz")
    parser.add_argument("--high", type=float, default=1.5, help="Frecuencia máxima en Hz")
    parser.add_argument("--alpha", type=float, default=5, help="Factor de amplificación temporal")
    parser.add_argument("--spatial-level", type=int, default=1, help="Reducciones gaussianas (0–4)")
    parser.add_argument(
        "--baseline", type=float, default=8, help="Fin del tramo inicial de referencia, en segundos"
    )
    parser.add_argument("--max-dimension", type=int, default=480)
    parser.add_argument("--no-patterns", action="store_true")
    parser.add_argument(
        "--capture-notes", default="Condiciones de captura no documentadas por el usuario."
    )
    args = parser.parse_args(argv)
    if (args.json or args.analyze) and not args.video:
        parser.error("--json y --analyze requieren la ruta de un video")
    if args.video:
        from video_analysis.video import inspect_video

        try:
            if args.analyze:
                from video_analysis.pipeline import AnalysisConfig, analyze_video

                config = AnalysisConfig(
                    low_hz=args.low,
                    high_hz=args.high,
                    alpha=args.alpha,
                    spatial_level=args.spatial_level,
                    baseline_seconds=args.baseline,
                    max_dimension=args.max_dimension,
                    patterns_enabled=not args.no_patterns,
                    capture_notes=args.capture_notes,
                )
                result = analyze_video(args.video, args.output, config)
                print(
                    json.dumps({"output": str(result)}, ensure_ascii=False)
                    if args.json
                    else f"Resultados: {result}"
                )
                return 0
            info, _ = inspect_video(args.video)
        except (ValueError, OSError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(info.as_dict(), ensure_ascii=False, indent=2))
        else:
            print(
                f"Video válido: {info.path.name}\n"
                f"Resolución: {info.width} × {info.height}\n"
                f"FPS: {info.fps:.3f}\nFotogramas: {info.frame_count}\n"
                f"Duración estimada: {info.duration_seconds:.2f} s"
            )
        return 0
    from PySide6.QtWidgets import QApplication

    from video_analysis.gui.main_window import MainWindow

    app = QApplication([sys.argv[0]])
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
