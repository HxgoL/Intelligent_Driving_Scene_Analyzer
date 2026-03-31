import argparse
from pathlib import Path

from cv_module.model_utils import get_model_path, load_model


DEFAULT_MODELS = ("yolov8n", "yolov8s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Entraine une ou plusieurs variantes YOLOv8 pour le module CV."
    )
    parser.add_argument(
        "--data",
        required=True,
        help="Chemin vers le fichier dataset YAML Ultralytics.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=list(DEFAULT_MODELS),
        help=(
            "Variantes a comparer. Accepte des alias (yolov8n, yolov8s) "
            "ou un chemin vers des poids."
        ),
    )
    parser.add_argument("--epochs", type=int, default=50, help="Nombre d'epochs.")
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Taille des images redimensionnees par YOLO pendant l'entrainement.",
    )
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument(
        "--project",
        default="runs/train",
        help="Dossier parent pour les runs d'entrainement.",
    )
    return parser.parse_args()


def train_variant(
    model_name: str,
    data_path: str,
    epochs: int,
    imgsz: int,
    batch: int,
    project: str,
) -> dict:
    # Nom simple du run pour retrouver facilement les essais.
    run_name = f"{Path(get_model_path(model_name)).stem}_train"
    model = load_model(model_name)
    # Lance l'entrainement YOLO avec les parametres choisis.
    results = model.train(
        data=data_path,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project,
        name=run_name,
        exist_ok=True,
    )

    # On garde seulement les infos utiles pour comparer les essais.
    summary = {
        "model": model_name,
        "run_name": run_name,
        "save_dir": str(results.save_dir),
        "best_weights": str(Path(results.save_dir) / "weights" / "best.pt"),
        "last_weights": str(Path(results.save_dir) / "weights" / "last.pt"),
        "metrics": {
            "precision": _safe_metric_value(results.results_dict, "metrics/precision(B)"),
            "recall": _safe_metric_value(results.results_dict, "metrics/recall(B)"),
            "mAP50": _safe_metric_value(results.results_dict, "metrics/mAP50(B)"),
            "mAP50-95": _safe_metric_value(results.results_dict, "metrics/mAP50-95(B)"),
            "fitness": _safe_metric_value(results.results_dict, "fitness"),
        },
    }
    return summary


def _safe_metric_value(results_dict: dict, key: str) -> float | None:
    # Evite une erreur si une metrique n'est pas presente dans les resultats.
    value = results_dict.get(key)
    if value is None:
        return None
    return float(value)


def main() -> None:
    args = parse_args()

    # Boucle sur les variantes demandees pour lancer les deux entrainements.
    for model_name in args.models:
        print(f"\n=== Entrainement de {model_name} ===")
        run_summary = train_variant(
            model_name=model_name,
            data_path=args.data,
            epochs=args.epochs,
            imgsz=args.imgsz,
            batch=args.batch,
            project=args.project,
        )
        print("Run :", run_summary["run_name"])
        print("Dossier :", run_summary["save_dir"])
        print("Best weights :", run_summary["best_weights"])
        print("Precision :", run_summary["metrics"]["precision"])
        print("Recall :", run_summary["metrics"]["recall"])
        print("mAP50 :", run_summary["metrics"]["mAP50"])
        print("mAP50-95 :", run_summary["metrics"]["mAP50-95"])


if __name__ == "__main__":
    main()
