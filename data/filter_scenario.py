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


def filter_urban_intersection_scenario(
    annotations: list[dict],
    images_dir: Optional[Path] = RAW_IMAGES_DIR,
    require_local_image: bool = True,
    min_objects: int = 6,
) -> list[dict]:
    """
    Filtre les annotations pour le scenario du groupe :
    conduite urbaine avec forte densite d'objets, pietons et feux.
    """
    filtered_annotations: list[dict] = []

    for item in annotations:
        attributes = item.get("attributes", {})
        labels = item.get("labels", [])
        categories = [label.get("category", "").lower() for label in labels]
        category_set = set(categories)

        if attributes.get("scene", "").lower() != "city street":
            continue

        has_person = "person" in category_set
        has_traffic_light = "traffic light" in category_set
        has_intersection_context = has_person or has_traffic_light
        has_high_density = len(labels) >= min_objects

        if not has_intersection_context:
            continue

        if not has_high_density:
            continue

        if require_local_image and images_dir is not None:
            image_path = images_dir / item["name"]
            if not image_path.exists():
                continue

        filtered_annotations.append(item)

    return filtered_annotations


def build_urban_intersection_subset(
    annotations: list[dict],
    target_size: int = 200,
    images_dir: Optional[Path] = RAW_IMAGES_DIR,
    require_local_image: bool = True,
    min_objects: int = 6,
) -> list[dict]:
    """
    Construit un sous-ensemble de taille fixe pour le scenario urbain.
    On prend d'abord les images les plus pertinentes, puis on complete
    avec le subset existant si on n'atteint pas target_size.
    """
    primary_subset = filter_urban_intersection_scenario(
        annotations,
        images_dir=images_dir,
        require_local_image=require_local_image,
        min_objects=min_objects,
    )

    if len(primary_subset) >= target_size:
        return primary_subset[:target_size]

    selected_names = {item["name"] for item in primary_subset}
    completed_subset = primary_subset[:]

    fallback_subset = filter_annotations(
        annotations,
        required_categories=["car", "truck", "bus", "person", "traffic light", "traffic sign"],
        images_dir=images_dir,
        require_local_image=require_local_image,
    )

    for item in fallback_subset:
        if item["name"] in selected_names:
            continue
        completed_subset.append(item)
        selected_names.add(item["name"])
        if len(completed_subset) >= target_size:
            break

    return completed_subset


def save_annotations(annotations: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(annotations, file, indent=2)


if __name__ == "__main__":
    annotations = load_annotations()
    generic_filtered = filter_annotations(
        annotations,
        required_categories=["car", "truck", "bus", "person", "traffic light", "traffic sign"],
        require_local_image=True,
    )
    urban_filtered = build_urban_intersection_subset(
        annotations,
        target_size=200,
        require_local_image=True,
    )

    generic_output_path = ROOT_DIR / "data" / "processed" / "bdd100k" / "filtered_annotations.json"
    urban_output_path = (
        ROOT_DIR / "data" / "processed" / "bdd100k" / "filtered_annotations_urban_intersection.json"
    )

    save_annotations(generic_filtered, generic_output_path)
    save_annotations(urban_filtered, urban_output_path)

    print(f"Annotations chargees : {len(annotations)}")
    print(f"Annotations filtrees (generique) : {len(generic_filtered)}")
    print(f"Annotations filtrees (scenario urbain) : {len(urban_filtered)}")
    print(f"Fichier genere : {generic_output_path}")
    print(f"Fichier genere : {urban_output_path}")
