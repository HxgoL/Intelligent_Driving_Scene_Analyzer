from pathlib import Path

try:
    from data.filter_scenario import (
        build_urban_intersection_subset,
        filter_annotations,
        filter_urban_intersection_scenario,
        load_annotations,
        save_annotations,
    )
    from data.split_dataset import save_split, split_annotations
except ModuleNotFoundError:
    from filter_scenario import (
        build_urban_intersection_subset,
        filter_annotations,
        filter_urban_intersection_scenario,
        load_annotations,
        save_annotations,
    )
    from split_dataset import save_split, split_annotations


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "data" / "processed" / "bdd100k"
LABELS_DIR = OUTPUT_DIR / "labels"


def prepare_dataset() -> dict[str, int]:
    annotations = load_annotations()

    filtered_annotations = filter_annotations(
        annotations,
        required_categories=["car", "truck", "bus", "person", "traffic light", "traffic sign"],
        require_local_image=True,
    )

    filtered_path = LABELS_DIR / "filtered_annotations.json"
    save_annotations(filtered_annotations, filtered_path)

    train_set, val_set, test_set = split_annotations(filtered_annotations)
    save_split("train", train_set, LABELS_DIR)
    save_split("val", val_set, LABELS_DIR)
    save_split("test", test_set, LABELS_DIR)

    return {
        "raw": len(annotations),
        "filtered": len(filtered_annotations),
        "train": len(train_set),
        "val": len(val_set),
        "test": len(test_set),
    }


def prepare_urban_intersection_dataset() -> dict[str, int]:
    annotations = load_annotations()

    strict_filtered_annotations = filter_urban_intersection_scenario(
        annotations,
        require_local_image=True,
    )
    filtered_annotations = build_urban_intersection_subset(
        annotations,
        target_size=200,
        require_local_image=True,
    )

    filtered_path = LABELS_DIR / "filtered_annotations_urban_intersection.json"
    save_annotations(filtered_annotations, filtered_path)

    train_set, val_set, test_set = split_annotations(filtered_annotations)
    save_split("train_urban_intersection", train_set, LABELS_DIR)
    save_split("val_urban_intersection", val_set, LABELS_DIR)
    save_split("test_urban_intersection", test_set, LABELS_DIR)

    return {
        "raw": len(annotations),
        "strict_filtered": len(strict_filtered_annotations),
        "filtered": len(filtered_annotations),
        "train": len(train_set),
        "val": len(val_set),
        "test": len(test_set),
    }


if __name__ == "__main__":
    generic_summary = prepare_dataset()
    urban_summary = prepare_urban_intersection_dataset()

    print("Preparation du dataset terminee.")
    print("--- Dataset generique ---")
    print(f"Annotations de depart : {generic_summary['raw']}")
    print(f"Annotations filtrees : {generic_summary['filtered']}")
    print(f"Train : {generic_summary['train']}")
    print(f"Validation : {generic_summary['val']}")
    print(f"Test : {generic_summary['test']}")
    print("--- Scenario urbain ---")
    print(f"Annotations de depart : {urban_summary['raw']}")
    print(f"Annotations strictement scenario : {urban_summary['strict_filtered']}")
    print(f"Annotations filtrees : {urban_summary['filtered']}")
    print(f"Train : {urban_summary['train']}")
    print(f"Validation : {urban_summary['val']}")
    print(f"Test : {urban_summary['test']}")
    print(f"Dossier de sortie : {OUTPUT_DIR}")
