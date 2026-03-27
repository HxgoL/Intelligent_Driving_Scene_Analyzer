from cv_module.model_utils import load_model
from pipeline.schema import BoundingBox, DetectedObject, SceneDetections


# Cette méthode exécute YOLO sur une image et retourne les détections dans le schéma commun du pipeline.

def run_inference(image_path: str) -> SceneDetections:
    # Charge le modèle YOLO puis lance l'inférence sur l'image fournie.
    model = load_model()
    results = model(image_path)
    detected_objects = []

    for result in results:
        # Récupère les noms de classes et les boîtes détectées pour ce résultat.
        names = result.names
        boxes = result.boxes

        # Passe au résultat suivant si aucun objet n'a été détecté.
        if boxes is None:
            continue

        # Convertit les détections YOLO dans les objets partagés du pipeline.
        for box in boxes:
            cls_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            x1, y1, x2, y2 = [float(x) for x in box.xyxy[0].tolist()]

            bounding_box = BoundingBox(
                x=x1,
                y=y1,
                width=x2 - x1,
                height=y2 - y1,
            )

            detected_objects.append(
                DetectedObject(
                    label=names[cls_id],
                    confidence=confidence,
                    bounding_box=bounding_box,
                )
            )

    return SceneDetections(detected_objects=detected_objects)
