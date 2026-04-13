import argparse
import json
import shutil
from pathlib import Path


CLASS_NAMES = ["car", "truck", "person", "traffic sign", "traffic light"]
CLASS_TO_ID = {name: index for index, name in enumerate(CLASS_NAMES)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare un dataset YOLO a partir des splits BDD100K filtres."
    )
    parser.add_argument(
        "--train-images-dir",
        default="data/raw/bdd100k/images",
        help="Dossier contenant les images du split train.",
    )
    parser.add_argument(
        "--val-images-dir",
        default="data/raw/bdd100k/images",
        help="Dossier contenant les images du split val.",
    )
    parser.add_argument(
        "--test-images-dir",
        default="data/raw/bdd100k/images",
        help="Dossier contenant les images du split test.",
    )
    parser.add_argument(
        "--train-annotations",
        default="data/processed/bdd100k/labels/train.json",
        help="Fichier JSON contenant les annotations train.",
    )
    parser.add_argument(
        "--val-annotations",
        default="data/processed/bdd100k/labels/val.json",
        help="Fichier JSON contenant les annotations val.",
    )
    parser.add_argument(
        "--test-annotations",
        default="data/processed/bdd100k/labels/test.json",
        help="Fichier JSON contenant les annotations test.",
    )
    parser.add_argument(
        "--output-dir",
        default="cv_module/bdd100k_yolo",
        help="Dossier de sortie du dataset YOLO.",
    )
    return parser.parse_args()


def convert_box(width: int, height: int, box2d: dict) -> str | None:
    x1 = box2d.get("x1")
    y1 = box2d.get("y1")
    x2 = box2d.get("x2")
    y2 = box2d.get("y2")
    if None in (x1, y1, x2, y2):
        return None
    if x2 <= x1 or y2 <= y1:
        return None

    x_center = ((x1 + x2) / 2) / width
    y_center = ((y1 + y2) / 2) / height
    box_width = (x2 - x1) / width
    box_height = (y2 - y1) / height
    return f"{x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"


def annotation_to_yolo_lines(annotation: dict) -> list[str]:
    lines = []
    for label in annotation.get("labels", []):
        class_name = label.get("category")
        if class_name not in CLASS_TO_ID:
            continue
        box = convert_box(1280, 720, label.get("box2d", {}))
        if box is None:
            continue
        lines.append(f"{CLASS_TO_ID[class_name]} {box}")
    return lines


def prepare_split(
    split_name: str,
    images_dir: Path,
    annotations_path: Path,
    output_dir: Path,
) -> int:
    annotations = json.loads(annotations_path.read_text(encoding="utf-8"))

    images_out = output_dir / "images" / split_name
    labels_out = output_dir / "labels" / split_name
    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    kept = 0
    for item in annotations:
        image_name = item["name"]
        image_path = images_dir / image_name
        if not image_path.exists():
            continue

        yolo_lines = annotation_to_yolo_lines(item)
        if not yolo_lines:
            continue

        shutil.copy2(image_path, images_out / image_name)
        label_path = labels_out / f"{Path(image_name).stem}.txt"
        label_path.write_text("\n".join(yolo_lines) + "\n", encoding="utf-8")
        kept += 1

    return kept


def write_yaml(output_dir: Path) -> Path:
    yaml_path = output_dir / "dataset.yaml"
    yaml_lines = [
        f"path: {output_dir.resolve()}",
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "",
        "names:",
    ]
    for index, name in enumerate(CLASS_NAMES):
        yaml_lines.append(f"  {index}: {name}")
    yaml_path.write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")
    return yaml_path


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    train_images_dir = Path(args.train_images_dir)
    val_images_dir = Path(args.val_images_dir)
    test_images_dir = Path(args.test_images_dir)
    train_annotations = Path(args.train_annotations)
    val_annotations = Path(args.val_annotations)
    test_annotations = Path(args.test_annotations)

    if output_dir.exists():
        shutil.rmtree(output_dir)

    train_count = prepare_split("train", train_images_dir, train_annotations, output_dir)
    val_count = prepare_split("val", val_images_dir, val_annotations, output_dir)
    test_count = prepare_split("test", test_images_dir, test_annotations, output_dir)
    yaml_path = write_yaml(output_dir)

    print(f"Train prepare : {train_count}")
    print(f"Val prepare : {val_count}")
    print(f"Test prepare : {test_count}")
    print(f"YAML : {yaml_path}")


if __name__ == "__main__":
    main()
