from cv_module.model_utils import load_model
from pipeline.schema import BoundingBox, DetectedObject, SceneDetections

# Cette méthode exécute YOLO sur une image et retourne les détections dans le schéma commun du pipeline.

CONFIDENCE_THRESHOLD = 0.40
CLASS_CONFIDENCE_THRESHOLDS = {
    "car": 0.45,
    "truck": 0.45,
    "person": 0.55,
    "traffic light": 0.30,
    "traffic sign": 0.35,
}
CLASS_MAPPING = {
    "bus": "truck",
    "stop sign": "traffic sign",
}
ALLOWED_LABELS = {
    "car",
    "truck",
    "person",
    "traffic light",
    "traffic sign",
}


def normalize_label(label: str) -> str | None:
    normalized_label = CLASS_MAPPING.get(label.lower(), label.lower())
    if normalized_label in ALLOWED_LABELS:
        return normalized_label
    return None


def is_box_reliable(label: str, width: float, height: float) -> bool:
    if width < 12 or height < 12:
        return False
    if label in {"car", "truck"} and width < 24:
        return False
    return True


def get_relative_position(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    image_width: float,
    image_height: float,
) -> str:
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    if center_x < image_width / 3:
        horizontal_position = "left"
    elif center_x < (2 * image_width) / 3:
        horizontal_position = "center"
    else:
        horizontal_position = "right"

    if center_y > image_height * 0.72:
        depth_position = "near"
    elif center_y > image_height * 0.45:
        depth_position = "mid"
    else:
        depth_position = "far"

    return f"{horizontal_position}-{depth_position}"


def run_inference(image_path: str, confidence_threshold: float = CONFIDENCE_THRESHOLD) -> SceneDetections:
    # Charge le modèle YOLO puis lance l'inférence sur l'image fournie.
    model = load_model()
    results = model(image_path)
    detected_objects = []

    for result in results:
        # Récupère les noms de classes et les boîtes détectées pour ce résultat.
        names = result.names
        boxes = result.boxes
        image_height, image_width = result.orig_shape

        # Passe au résultat suivant si aucun objet n'a été détecté.
        if boxes is None:
            continue

        # Convertit les détections YOLO dans les objets partagés du pipeline.
        for box in boxes:
            cls_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            x1, y1, x2, y2 = [float(x) for x in box.xyxy[0].tolist()]
            label = normalize_label(names[cls_id])
            box_width = x2 - x1
            box_height = y2 - y1

            if label is None:
                continue
            if confidence < max(confidence_threshold, CLASS_CONFIDENCE_THRESHOLDS.get(label, confidence_threshold)):
                continue
            if not is_box_reliable(label, box_width, box_height):
                continue

            bounding_box = BoundingBox(
                x=x1,
                y=y1,
                width=box_width,
                height=box_height,
            )
            relative_position = get_relative_position(
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                image_width=float(image_width),
                image_height=float(image_height),
            )

            detected_objects.append(
                DetectedObject(
                    label=label,
                    confidence=confidence,
                    bounding_box=bounding_box,
                    relative_position=relative_position,
                )
            )

    return SceneDetections(detected_objects=detected_objects)
