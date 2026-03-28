from ultralytics import YOLO

def load_model(model_name: str = "yolov8n.pt"):
    # Charge un modèle YOLO
    return YOLO(model_name)
