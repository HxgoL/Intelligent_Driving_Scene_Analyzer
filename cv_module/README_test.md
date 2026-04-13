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

Depuis la racine du projet :

```bash
source .venv/bin/activate
```

Puis lancer le test d'inférence :

```bash
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

## Entraînement de deux variantes du modèle

L'issue suivante ajoute un script [train.py](/home/eve/GitHub/Intelligent_Driving_Scene_Analyzer/cv_module/train.py) pour lancer l'entraînement de plusieurs variantes YOLOv8 sur un dataset au format Ultralytics.

Depuis la racine du projet, activer d'abord l'environnement virtuel :

```bash
source .venv/bin/activate
```

Si les splits BDD100K sont dans `data/processed/bdd100k` et les images dans `data/raw/bdd100k/images`, il faut d'abord preparer le dataset YOLO :

```bash
python3 -m cv_module.prepare_bdd100k
```

Cette commande cree un dossier `cv_module/bdd100k_yolo` et un fichier `dataset.yaml` compatible avec YOLO.

Exemple pour comparer `yolov8n` et `yolov8s` :

```bash
python3 -m cv_module.train \
  --data cv_module/bdd100k_yolo/dataset.yaml \
  --models yolov8n yolov8s \
  --epochs 50 \
  --imgsz 640 \
  --batch 16
```

Le script :

- charge chaque variante à partir des poids pré-entraînés Ultralytics
- lance l'entraînement avec des paramètres simples
- sauvegarde les poids `best.pt` et `last.pt`
- affiche les métriques finales principales (`precision`, `recall`, `mAP50`, `mAP50-95`)

## Entraînements réalisés

Les deux modèles ont été entraînés sur le dataset préparé à partir du sous-ensemble BDD100K filtré.

Commandes utilisées :

```bash
python3 -m cv_module.train --data cv_module/bdd100k_yolo/dataset.yaml --models yolov8n --epochs 3 --imgsz 320 --batch 8
python3 -m cv_module.train --data cv_module/bdd100k_yolo/dataset.yaml --models yolov8s --epochs 3 --imgsz 320 --batch 8
```

Résultats obtenus :

- `yolov8n` : precision = 0.9070, recall = 0.0550, mAP50 = 0.0620, mAP50-95 = 0.0312
- `yolov8s` : precision = 0.3775, recall = 0.1855, mAP50 = 0.1781, mAP50-95 = 0.0866

Poids sauvegardés :

- `runs/detect/runs/train/yolov8n_train/weights/best.pt`
- `runs/detect/runs/train/yolov8s_train/weights/best.pt`

## Choix du modèle final

Le modèle retenu pour la suite du projet est `yolov8s`.

Pourquoi :

- son `mAP50` est meilleur que celui de `yolov8n`
- son `mAP50-95` est aussi meilleur
- son recall est plus élevé, donc il détecte plus d'objets pertinents sur le jeu de validation

Même si la précision brute de `yolov8n` est plus haute, `yolov8s` donne de meilleurs résultats globaux pour notre scénario de conduite urbaine.

## Post-traitement des détections

L'inférence a ensuite été améliorée pour rendre les sorties plus cohérentes pour le projet.

Ce qui a été ajouté dans [infer.py](/home/eve/GitHub/Intelligent_Driving_Scene_Analyzer/cv_module/infer.py) :

- un seuil de confiance pour ignorer les détections peu fiables
- un regroupement de certaines classes YOLO, par exemple `bus` vers `truck` et `stop sign` vers `traffic sign`
- un filtrage pour garder surtout les classes utiles au scénario de conduite
- une position relative simple pour chaque objet, par exemple `left-near`, `center-mid` ou `right-far`

La sortie finale d'un objet détecté contient maintenant :

- `label`
- `confidence`
- `bounding_box`
- `relative_position`

## Dataset final du scénario urbain

Pour le scénario final, l'entraînement peut se faire avec les fichiers préparés par Doha :

- train : `data/processed/bdd100k/augmented/labels/train_urban_intersection_augmented.json`
- validation : `data/processed/bdd100k/labels/val_urban_intersection.json`
- test : `data/processed/bdd100k/labels/test_urban_intersection.json`

Si les images augmentées ne sont pas encore présentes localement, on peut les regénérer avec :

```bash
python3 -m data.augmentation
```

Puis preparer le dataset YOLO final :

```bash
python3 -m cv_module.prepare_bdd100k \
  --train-images-dir data/processed/bdd100k/augmented/images/train_urban_intersection \
  --val-images-dir data/raw/bdd100k/images \
  --test-images-dir data/raw/bdd100k/images \
  --train-annotations data/processed/bdd100k/augmented/labels/train_urban_intersection_augmented.json \
  --val-annotations data/processed/bdd100k/labels/val_urban_intersection.json \
  --test-annotations data/processed/bdd100k/labels/test_urban_intersection.json \
  --output-dir cv_module/bdd100k_yolo
```

Le script de préparation nettoie maintenant le dossier `cv_module/bdd100k_yolo` avant de le recréer, ce qui évite de mélanger un ancien dataset avec un nouveau split.

Pour réentraîner `yolov8s` :

```bash
python3 -m cv_module.train --data cv_module/bdd100k_yolo/dataset.yaml --models yolov8s --epochs 5 --imgsz 640 --batch 8
```

Pour évaluer le modèle final :

```bash
python3 -m cv_module.evaluate --data cv_module/bdd100k_yolo/dataset.yaml --model yolov8s --split test --imgsz 640 --conf 0.40 --iou 0.60
```

## Ajustements d'inférence du modèle final

Pour améliorer la précision sur notre scénario urbain, [infer.py](/home/eve/GitHub/Intelligent_Driving_Scene_Analyzer/cv_module/infer.py) applique maintenant :

- un seuil global de confiance à `0.40`
- des seuils plus précis selon la classe détectée
- un filtrage de boîtes trop petites pour éviter certaines fausses détections
- un regroupement limité aux classes cohérentes pour le projet, par exemple `bus` vers `truck` et `stop sign` vers `traffic sign`

Cela permet d'avoir des sorties plus propres dans l'application finale, surtout sur les piétons, les feux et les panneaux.
