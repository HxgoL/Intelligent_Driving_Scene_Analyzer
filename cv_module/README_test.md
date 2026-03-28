# Tests du module Computer Vision

Ce module a été initialisé avec un premier pipeline d'inférence basé sur YOLOv8 pré-entraîné.

## Ce qui a été mis en place

- installation de la bibliothèque `ultralytics`
- création de `model_utils.py` pour charger le modèle YOLO
- création de `infer.py` pour exécuter l'inférence sur une image
- conversion des résultats YOLO dans un format Python simple
- ajout d'un fichier `test_infer.py` pour tester le module sur plusieurs images
- ajout de 5 images de test dans `cv_module/test_images`

## Format de sortie actuel

Chaque détection est retournée sous la forme d'un dictionnaire Python contenant :

- `class` : classe détectée
- `confidence` : score de confiance
- `bbox` : coordonnées de la bounding box au format `[x1, y1, x2, y2]`

Exemple :

```python
{
    "class": "car",
    "confidence": 0.91,
    "bbox": [100.0, 200.0, 300.0, 400.0]
}
```

## Lancement des tests

Depuis la racine du projet, avec l'environnement virtuel activé :

```
python3 -m cv_module.test_infer
```

## Objectif de ce test

Ce test permet de vérifier que :

- le modèle YOLOv8 se charge correctement
- l'inférence fonctionne sur plusieurs images
- les résultats sont bien extraits et structurés dans un format Python clair

## Remarques

Ce test permet de vérifier que :

- le modèle utilisé actuellement est yolov8n.pt, une version pré-entraînée légère
- les détections ne sont pas encore filtrées
- les classes non pertinentes pour le projet peuvent encore apparaître
- l'amélioration de la précision et le post-traitement seront traités dans les prochaines issues
