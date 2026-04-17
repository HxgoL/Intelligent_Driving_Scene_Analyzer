"""
Calcule les metriques affichees dans le dashboard.
"""

from collections import Counter
from dataclasses import dataclass

from pipeline.schema import SceneDetections


@dataclass(frozen=True)
class DashboardMetrics:
    total_objects: int
    people_count: int
    vehicle_count: int
    near_objects: int
    average_confidence: float
    top_label: str
    label_counts: Counter


def compute_dashboard_metrics(detections: SceneDetections) -> DashboardMetrics:
    detected_objects = detections.detected_objects
    label_counts = Counter(obj.label for obj in detected_objects)
    confidences = [obj.confidence for obj in detected_objects]
    near_objects = [
        obj for obj in detected_objects if (obj.relative_position or "").endswith("near")
    ]
    people_count = label_counts.get("person", 0)
    vehicle_count = label_counts.get("car", 0) + label_counts.get("truck", 0)

    top_label = "Aucun"
    if label_counts:
        top_label = label_counts.most_common(1)[0][0]

    average_confidence = 0.0
    if confidences:
        average_confidence = sum(confidences) / len(confidences)

    return DashboardMetrics(
        total_objects=len(detected_objects),
        people_count=people_count,
        vehicle_count=vehicle_count,
        near_objects=len(near_objects),
        average_confidence=average_confidence,
        top_label=top_label,
        label_counts=label_counts,
    )
