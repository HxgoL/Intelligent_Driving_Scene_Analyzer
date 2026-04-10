import json
from pathlib import Path
from typing import Iterable, Optional


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_LABELS_PATH = ROOT_DIR / "data" / "raw" / "bdd100k" / "labels" / "subset_car_300.json"
RAW_IMAGES_DIR = ROOT_DIR / "data" / "raw" / "bdd100k" / "images"


def load_annotations(labels_path: Path = RAW_LABELS_PATH) -> list[dict]:
    with labels_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _normalize_values(values: Optional[Iterable[str]]) -> Optional[set[str]]:
    if not values:
        return None
    return {value.strip().lower() for value in values if value.strip()}


def filter_annotations(
    annotations: list[dict],
    required_categories: Optional[Iterable[str]] = None,
    weather: Optional[Iterable[str]] = None,
    scenes: Optional[Iterable[str]] = None,
    times_of_day: Optional[Iterable[str]] = None,
    images_dir: Optional[Path] = RAW_IMAGES_DIR,
    require_local_image: bool = True,
) -> list[dict]:
    categories_filter = _normalize_values(required_categories)
    weather_filter = _normalize_values(weather)
    scene_filter = _normalize_values(scenes)
    time_filter = _normalize_values(times_of_day)

    filtered_annotations: list[dict] = []

    for item in annotations:
        attributes = item.get("attributes", {})
        labels = item.get("labels", [])
        label_categories = {label.get("category", "").lower() for label in labels}

        if categories_filter and not categories_filter.intersection(label_categories):
            continue

        if weather_filter and attributes.get("weather", "").lower() not in weather_filter:
            continue

        if scene_filter and attributes.get("scene", "").lower() not in scene_filter:
            continue

        if time_filter and attributes.get("timeofday", "").lower() not in time_filter:
            continue

        if require_local_image and images_dir is not None:
            image_path = images_dir / item["name"]
            if not image_path.exists():
                continue

        filtered_annotations.append(item)

    return filtered_annotations


def save_annotations(annotations: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(annotations, file, indent=2)


if __name__ == "__main__":
    annotations = load_annotations()
    filtered = filter_annotations(
        annotations,
        required_categories=["car", "truck", "bus", "person", "traffic light", "traffic sign"],
        require_local_image=True,
    )

    output_path = ROOT_DIR / "data" / "processed" / "bdd100k" / "filtered_annotations.json"
    save_annotations(filtered, output_path)

    print(f"Annotations chargées : {len(annotations)}")
    print(f"Annotations filtrées : {len(filtered)}")
    print(f"Fichier enregistré : {output_path}")
