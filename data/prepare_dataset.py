from pathlib import Path

try:
    from data.filter_scenario import filter_annotations, load_annotations, save_annotations
    from data.split_dataset import save_split, split_annotations
except ModuleNotFoundError:
    from filter_scenario import filter_annotations, load_annotations, save_annotations
    from split_dataset import save_split, split_annotations


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "data" / "processed" / "bdd100k"


def prepare_dataset() -> dict[str, int]:
    annotations = load_annotations()

    filtered_annotations = filter_annotations(
        annotations,
        required_categories=["car", "truck", "bus", "person", "traffic light", "traffic sign"],
        require_local_image=True,
    )

    filtered_path = OUTPUT_DIR / "filtered_annotations.json"
    save_annotations(filtered_annotations, filtered_path)

    train_set, val_set, test_set = split_annotations(filtered_annotations)
    save_split("train", train_set, OUTPUT_DIR)
    save_split("val", val_set, OUTPUT_DIR)
    save_split("test", test_set, OUTPUT_DIR)

    return {
        "raw": len(annotations),
        "filtered": len(filtered_annotations),
        "train": len(train_set),
        "val": len(val_set),
        "test": len(test_set),
    }


if __name__ == "__main__":
    summary = prepare_dataset()

    print("Préparation du dataset terminée.")
    print(f"Annotations de départ : {summary['raw']}")
    print(f"Annotations filtrées : {summary['filtered']}")
    print(f"Train : {summary['train']}")
    print(f"Validation : {summary['val']}")
    print(f"Test : {summary['test']}")
    print(f"Dossier de sortie : {OUTPUT_DIR}")
