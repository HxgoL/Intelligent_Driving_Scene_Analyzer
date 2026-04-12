import argparse
from pathlib import Path

from cv_module.infer import CONFIDENCE_THRESHOLD
from cv_module.model_utils import get_model_path, load_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evalue un modele YOLO sur un dataset et affiche les metriques principales."
    )
    parser.add_argument(
        "--data",
        required=True,
        help="Chemin vers le fichier dataset YAML.",
    )
    parser.add_argument(
        "--model",
        default="yolov8s",
        help="Modele a evaluer.",
    )
    parser.add_argument(
        "--split",
        default="test",
        choices=["train", "val", "test"],
        help="Split utilise pour l'evaluation.",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Taille des images pour l'evaluation.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=CONFIDENCE_THRESHOLD,
        help="Seuil de confiance applique pendant l'evaluation.",
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.60,
        help="Seuil d'IoU pour le NMS pendant l'evaluation.",
    )
    return parser.parse_args()


def _safe_value(results_dict: dict, key: str) -> float | None:
    value = results_dict.get(key)
    if value is None:
        return None
    return float(value)


def evaluate_model(
    model_name: str,
    data_path: str,
    split: str,
    imgsz: int,
    conf: float,
    iou: float,
) -> dict:
    model = load_model(model_name)
    results = model.val(
        data=data_path,
        split=split,
        imgsz=imgsz,
        conf=conf,
        iou=iou,
    )
    return {
        "model": get_model_path(model_name),
        "split": split,
        "confidence_threshold": conf,
        "iou_threshold": iou,
        "precision": _safe_value(results.results_dict, "metrics/precision(B)"),
        "recall": _safe_value(results.results_dict, "metrics/recall(B)"),
        "mAP50": _safe_value(results.results_dict, "metrics/mAP50(B)"),
        "mAP50-95": _safe_value(results.results_dict, "metrics/mAP50-95(B)"),
        "save_dir": str(results.save_dir) if hasattr(results, "save_dir") else None,
    }


def main() -> None:
    args = parse_args()
    summary = evaluate_model(
        model_name=args.model,
        data_path=args.data,
        split=args.split,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
    )
    print("Modele :", summary["model"])
    print("Split :", summary["split"])
    print("Seuil confiance :", summary["confidence_threshold"])
    print("Seuil IoU :", summary["iou_threshold"])
    print("Precision :", summary["precision"])
    print("Recall :", summary["recall"])
    print("mAP50 :", summary["mAP50"])
    print("mAP50-95 :", summary["mAP50-95"])
    if summary["save_dir"]:
        print("Dossier :", summary["save_dir"])


if __name__ == "__main__":
    main()
