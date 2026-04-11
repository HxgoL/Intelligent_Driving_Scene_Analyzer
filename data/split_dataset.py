import json
import random
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
LABELS_DIR = ROOT_DIR / "data" / "processed" / "bdd100k" / "labels"
FILTERED_ANNOTATIONS_PATH = LABELS_DIR / "filtered_annotations.json"
OUTPUT_DIR = LABELS_DIR


def load_annotations(annotations_path: Path = FILTERED_ANNOTATIONS_PATH) -> list[dict]:
    with annotations_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def split_annotations(
    annotations: list[dict],
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
) -> tuple[list[dict], list[dict], list[dict]]:
    total_ratio = train_ratio + val_ratio + test_ratio
    if round(total_ratio, 6) != 1.0:
        raise ValueError("Les ratios train/val/test doivent totaliser 1.0")

    shuffled_annotations = annotations[:]
    random.Random(seed).shuffle(shuffled_annotations)

    train_end = int(len(shuffled_annotations) * train_ratio)
    val_end = train_end + int(len(shuffled_annotations) * val_ratio)

    train_set = shuffled_annotations[:train_end]
    val_set = shuffled_annotations[train_end:val_end]
    test_set = shuffled_annotations[val_end:]

    return train_set, val_set, test_set


def save_split(split_name: str, annotations: list[dict], output_dir: Path = OUTPUT_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{split_name}.json"
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(annotations, file, indent=2)
    return output_path


if __name__ == "__main__":
    annotations = load_annotations()
    train_set, val_set, test_set = split_annotations(annotations)

    train_path = save_split("train", train_set)
    val_path = save_split("val", val_set)
    test_path = save_split("test", test_set)

    print(f"Nombre total d'annotations : {len(annotations)}")
    print(f"Train : {len(train_set)} -> {train_path}")
    print(f"Validation : {len(val_set)} -> {val_path}")
    print(f"Test : {len(test_set)} -> {test_path}")
