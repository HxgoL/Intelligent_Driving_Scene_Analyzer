from cv_module.model_utils import load_model

# Cette méthode exécute YOLO sur une image et retourne les détections dans un format Python clair (classe, score de confiance, bounding box)

def run_inference(image_path: str):
    # Charge le modèle YOLO puis lance l'inférence sur l'image fournie
    model = load_model()
    results = model(image_path)
    detections = []

    for result in results:
        # Récupère les noms de classes et les boîtes détectées pour ce résultat
        names = result.names
        boxes = result.boxes

        # Passe au résultat suivant si aucun objet n'a été détecté
        if boxes is None:
            continue

        # Convertit les détections YOLO dans un format Python simple
        for box in boxes:
            cls_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            bbox = [float(x) for x in box.xyxy[0].tolist()]

            detections.append(
                {
                    "class": names[cls_id],
                    "confidence": confidence,
                    "bbox": bbox,
                }
            )

    return detections
