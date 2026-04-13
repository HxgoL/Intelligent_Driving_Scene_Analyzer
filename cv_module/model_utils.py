from ultralytics import YOLO
from pathlib import Path


MODEL_PATHS = {
    "yolov8n": "yolov8n.pt",
    "yolov8s": "yolov8s.pt",
}
BEST_MODEL_PATHS = {
    "yolov8s": [
        Path("runs/detect/runs/train/best_train/weights/best.pt"),
        Path("runs/detect/runs/train/yolov8s_train/weights/best.pt"),
    ],
    "yolov8n": [
        Path("runs/detect/runs/train/yolov8n_train/weights/best.pt"),
    ],
}


def get_model_path(model_name: str = "yolov8s") -> str:
    # Si on donne un alias connu, on renvoie le bon fichier .pt.
    for best_path in BEST_MODEL_PATHS.get(model_name, []):
        if best_path.exists():
            return str(best_path)
    return MODEL_PATHS.get(model_name, model_name)


def load_model(model_name: str = "yolov8s") -> YOLO:
    # Charge un modèle YOLO à partir d'un alias simple ou d'un chemin de poids.
    model_path = get_model_path(model_name)
    return YOLO(model_path)
