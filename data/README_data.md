# Documentation Donnees

## Role de ce dossier

Le dossier `data/` contient tout le travail de preparation des donnees pour le projet.
L'objectif est de partir d'un sous-ensemble exploitable de BDD100K, puis de produire des fichiers simples a utiliser pour l'entrainement et l'evaluation.

## Organisation

- `raw/`
  Contient les donnees source conservees localement.
  On y trouve :
  - les images du subset de travail
  - le fichier d'annotations source `subset_car_300.json`

- `processed/`
  Contient les sorties preparees a partir des donnees source.
  Ce dossier est organise en :
  - `labels/` pour les fichiers JSON de filtrage et de split
  - `augmented/labels/` pour les annotations du train augmente
  - `augmented/images/` pour les images augmentees generees localement

## Dataset source retenu

Le travail est base sur un subset local de `300` images annotees provenant de BDD100K.
Ce subset sert de base commune pour les experimentations du projet.

Fichier source :
- `data/raw/bdd100k/labels/subset_car_300.json`

Images source :
- `data/raw/bdd100k/images/`

## Scenario du groupe

Le scenario retenu pour le projet est :

- conduite urbaine
- intersections
- presence de pietons
- presence de feux
- forte densite d'objets
- situations avec priorites complexes

## Strategie de filtrage

Deux niveaux de preparation sont conserves :

### 1. Version generique

Une version generique du subset est conservee pour garder une base simple et reutilisable.

Fichiers :
- `data/processed/bdd100k/labels/filtered_annotations.json`
- `data/processed/bdd100k/labels/train.json`
- `data/processed/bdd100k/labels/val.json`
- `data/processed/bdd100k/labels/test.json`

Cette version contient :
- `300` annotations filtrees
- `210` images pour train
- `45` images pour val
- `45` images pour test

### 2. Version scenario urbain

Une version plus ciblee a ete creee pour correspondre au scenario final du groupe.

Le filtrage privilegie :
- les scenes `city street`
- la presence de `person` et/ou `traffic light`
- une densite minimale d'objets dans l'image

Le filtrage strict renvoyait `184` images.
Pour obtenir un sous-ensemble de travail plus confortable, le dataset a ete complete
jusqu'a `200` images avec des images issues du subset initial de `300`, en gardant en
priorite les plus pertinentes pour le scenario.

Fichiers :
- `data/processed/bdd100k/labels/filtered_annotations_urban_intersection.json`
- `data/processed/bdd100k/labels/train_urban_intersection.json`
- `data/processed/bdd100k/labels/val_urban_intersection.json`
- `data/processed/bdd100k/labels/test_urban_intersection.json`

Cette version contient :
- `200` annotations filtrees
- `140` images pour train
- `30` images pour val
- `30` images pour test

## Augmentation de donnees

L'augmentation est appliquee uniquement au fichier :
- `train_urban_intersection.json`

Elle n'est pas appliquee a `val` ni `test` afin de garder une evaluation propre.

Transformations retenues :
- assombrissement (`darker`)
- contraste renforce (`higher_contrast`)
- leger flou (`slight_blur`)

Ces transformations ont ete choisies car elles modifient les conditions visuelles sans
changer la geometrie de l'image. Les bounding boxes restent donc valides sans avoir a
recalculer les annotations.

Sorties generees :
- `data/processed/bdd100k/augmented/labels/train_urban_intersection_augmented.json`
- `data/processed/bdd100k/augmented/labels/augmentation_summary.json`
- `data/processed/bdd100k/augmented/images/train_urban_intersection/`

Resultat :
- `140` images d'origine conservees
- `420` images augmentees creees
- `560` annotations/images au total pour le train augmente

## Scripts utilises

- `data/filter_scenario.py`
  Charge les annotations et applique les criteres de filtrage.

- `data/split_dataset.py`
  Cree les splits `train / val / test`.

- `data/prepare_dataset.py`
  Orchestre la preparation complete des JSON generiques et du scenario urbain.

- `data/augmentation.py`
  Cree les variantes d'images pour enrichir le train du scenario urbain.

## Ce qui est versionne dans Git

Sont conserves dans Git :
- les scripts Python
- les JSON de `processed/labels`
- les JSON de `processed/augmented/labels`

Ne sont pas conserves dans Git :
- `data/raw/`
- `data/processed/bdd100k/augmented/images/`

Les images brutes et augmentees sont partagees a l'equipe en dehors de Git
(par exemple via Drive) pour eviter d'alourdir le depot.

## Version a utiliser

Pour l'entrainement du scenario final, la version conseillee est :

- train :
  `data/processed/bdd100k/augmented/labels/train_urban_intersection_augmented.json`

- validation :
  `data/processed/bdd100k/labels/val_urban_intersection.json`

- test :
  `data/processed/bdd100k/labels/test_urban_intersection.json`

La version generique est conservee comme base de reference, mais pour le scenario final
du groupe il faut privilegier la version `urban_intersection`.
