from ultralytics import YOLO


MODEL_PATHS = {
    "yolov8n": "yolov8n.pt",
    "yolov8s": "yolov8s.pt",
}


def get_model_path(model_name: str = "yolov8n") -> str:
    # Si on donne un alias connu, on renvoie le bon fichier .pt.
    return MODEL_PATHS.get(model_name, model_name)


def load_model(model_name: str = "yolov8n") -> YOLO:
    # Charge un modèle YOLO à partir d'un alias simple ou d'un chemin de poids.
    model_path = get_model_path(model_name)
    return YOLO(model_path)
