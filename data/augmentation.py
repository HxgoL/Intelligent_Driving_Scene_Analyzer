import argparse
import copy
import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_IMAGES_DIR = ROOT_DIR / "data" / "raw" / "bdd100k" / "images"
DEFAULT_ANNOTATIONS_PATH = (
    ROOT_DIR / "data" / "processed" / "bdd100k" / "labels" / "train_urban_intersection.json"
)
DEFAULT_OUTPUT_IMAGES_DIR = (
    ROOT_DIR / "data" / "processed" / "bdd100k" / "augmented" / "images" / "train_urban_intersection"
)
DEFAULT_OUTPUT_ANNOTATIONS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "bdd100k"
    / "augmented"
    / "labels"
    / "train_urban_intersection_augmented.json"
)
DEFAULT_SUMMARY_PATH = (
    ROOT_DIR / "data" / "processed" / "bdd100k" / "augmented" / "labels" / "augmentation_summary.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cree des variantes d'images pour enrichir le jeu d'entrainement."
    )
    parser.add_argument(
        "--images-dir",
        default=str(DEFAULT_IMAGES_DIR),
        help="Dossier contenant les images source.",
    )
    parser.add_argument(
        "--annotations",
        default=str(DEFAULT_ANNOTATIONS_PATH),
        help="Fichier JSON contenant les annotations du split train.",
    )
    parser.add_argument(
        "--output-images-dir",
        default=str(DEFAULT_OUTPUT_IMAGES_DIR),
        help="Dossier de sortie des images augmentées.",
    )
    parser.add_argument(
        "--output-annotations",
        default=str(DEFAULT_OUTPUT_ANNOTATIONS_PATH),
        help="Fichier JSON de sortie pour les annotations augmentées.",
    )
    parser.add_argument(
        "--summary-path",
        default=str(DEFAULT_SUMMARY_PATH),
        help="Fichier JSON de synthese des augmentations appliquees.",
    )
    return parser.parse_args()


def load_annotations(annotations_path: Path) -> list[dict]:
    with annotations_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data: object, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def apply_darker(image: Image.Image) -> Image.Image:
    return ImageEnhance.Brightness(image).enhance(0.7)


def apply_higher_contrast(image: Image.Image) -> Image.Image:
    return ImageEnhance.Contrast(image).enhance(1.25)


def apply_slight_blur(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.GaussianBlur(radius=1.0))


def get_augmentation_operations() -> dict[str, callable]:
    return {
        "darker": apply_darker,
        "higher_contrast": apply_higher_contrast,
        "slight_blur": apply_slight_blur,
    }


def build_augmented_name(image_name: str, suffix: str) -> str:
    image_path = Path(image_name)
    return f"{image_path.stem}_{suffix}{image_path.suffix}"


def augment_training_split(
    annotations: list[dict],
    images_dir: Path,
    output_images_dir: Path,
) -> tuple[list[dict], dict[str, int]]:
    output_images_dir.mkdir(parents=True, exist_ok=True)

    operations = get_augmentation_operations()
    augmented_annotations: list[dict] = []
    summary = {
        "original_images_kept": 0,
        "augmented_images_created": 0,
        "missing_source_images": 0,
    }
    for operation_name in operations:
        summary[f"augmentation_{operation_name}"] = 0

    for annotation in annotations:
        image_name = annotation["name"]
        source_image_path = images_dir / image_name

        if not source_image_path.exists():
            summary["missing_source_images"] += 1
            continue

        with Image.open(source_image_path) as image:
            image = image.convert("RGB")

            # On recopie aussi l'image originale dans le dossier d'entrainement augmente.
            original_output_path = output_images_dir / image_name
            original_output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(original_output_path)

            original_annotation = copy.deepcopy(annotation)
            original_annotation["name"] = image_name
            augmented_annotations.append(original_annotation)
            summary["original_images_kept"] += 1

            # Les transformations choisies ne modifient pas la geometrie,
            # donc les annotations de boites restent valides.
            for operation_name, operation in operations.items():
                augmented_image = operation(image.copy())
                augmented_name = build_augmented_name(image_name, operation_name)
                augmented_output_path = output_images_dir / augmented_name
                augmented_image.save(augmented_output_path)

                augmented_annotation = copy.deepcopy(annotation)
                augmented_annotation["name"] = augmented_name
                augmented_annotations.append(augmented_annotation)

                summary["augmented_images_created"] += 1
                summary[f"augmentation_{operation_name}"] += 1

    return augmented_annotations, summary


def main() -> None:
    args = parse_args()

    images_dir = Path(args.images_dir)
    annotations_path = Path(args.annotations)
    output_images_dir = Path(args.output_images_dir)
    output_annotations_path = Path(args.output_annotations)
    summary_path = Path(args.summary_path)

    annotations = load_annotations(annotations_path)
    augmented_annotations, summary = augment_training_split(
        annotations=annotations,
        images_dir=images_dir,
        output_images_dir=output_images_dir,
    )

    summary["source_annotations"] = len(annotations)
    summary["output_annotations"] = len(augmented_annotations)
    summary["source_annotations_path"] = str(annotations_path)
    summary["output_annotations_path"] = str(output_annotations_path)
    summary["output_images_dir"] = str(output_images_dir)

    save_json(augmented_annotations, output_annotations_path)
    save_json(summary, summary_path)

    print("Augmentation terminee.")
    print(f"Annotations source : {len(annotations)}")
    print(f"Annotations de sortie : {len(augmented_annotations)}")
    print(f"Images originales conservees : {summary['original_images_kept']}")
    print(f"Images augmentees creees : {summary['augmented_images_created']}")
    print(f"Images source manquantes : {summary['missing_source_images']}")
    print(f"Fichier annotations : {output_annotations_path}")
    print(f"Dossier images : {output_images_dir}")
    print(f"Resume : {summary_path}")


if __name__ == "__main__":
    main()
