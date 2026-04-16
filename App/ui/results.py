"""
Affiche les resultats de l'analyse avec une mise en page plus lisible.
"""

from collections import Counter

import streamlit as st
from PIL import Image

from cv_module.infer import draw_detections_on_image
from pipeline.schema import PipelineOutput, SceneDetections


def _compute_dashboard_metrics(detections: SceneDetections) -> dict:
    detected_objects = detections.detected_objects
    label_counts = Counter(obj.label for obj in detected_objects)
    confidences = [obj.confidence for obj in detected_objects]
    near_objects = [
        obj for obj in detected_objects if (obj.relative_position or "").endswith("near")
    ]
    people_count = label_counts.get("person", 0)
    vehicle_count = label_counts.get("car", 0) + label_counts.get("truck", 0)

    most_common_label = "Aucun"
    if label_counts:
        most_common_label = label_counts.most_common(1)[0][0]

    average_confidence = 0.0
    if confidences:
        average_confidence = sum(confidences) / len(confidences)

    return {
        "total_objects": len(detected_objects),
        "people_count": people_count,
        "vehicle_count": vehicle_count,
        "near_objects": len(near_objects),
        "average_confidence": average_confidence,
        "top_label": most_common_label,
        "label_counts": label_counts,
    }


def _render_report(result: PipelineOutput) -> None:
    risk_level = result.analyse_resultat.risque_eval.risque_level
    summary = result.analyse_resultat.resume
    recommendations = result.analyse_resultat.recommandations

    st.markdown("### Rapport d'analyse")
    st.markdown(
        f"""
        <div class="report-card">
            <div class="report-card__header">
                <span class="report-card__eyebrow">Analyse de scene</span>
                <span class="risk-badge">{risk_level}</span>
            </div>
            <p class="report-card__summary">{summary}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Recommandations")
    for recommendation in recommendations:
        st.markdown(
            f"""
            <div class="recommendation-item">
                <span class="recommendation-bullet">-</span>
                <span>{recommendation}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_images(image: Image.Image, result: PipelineOutput) -> None:
    annotated_image = draw_detections_on_image(image, result.scene_detections)

    st.markdown("### Comparaison visuelle")
    original_col, annotated_col = st.columns(2, gap="large")

    with original_col:
        st.markdown("#### Image source")
        st.image(image, caption="Image originale", use_container_width=True)

    with annotated_col:
        st.markdown("#### Image analysee")
        st.image(
            annotated_image,
            caption="Detections YOLO",
            use_container_width=True,
        )


def _render_dashboard(detections: SceneDetections) -> None:
    metrics = _compute_dashboard_metrics(detections)

    st.markdown("### Dashboard")

    metric_col_1, metric_col_2 = st.columns(2)
    with metric_col_1:
        st.metric("Objets detectes", metrics["total_objects"])
        st.metric("Vehicules", metrics["vehicle_count"])
        st.metric("Pres du vehicule", metrics["near_objects"])

    with metric_col_2:
        st.metric("Pietons", metrics["people_count"])
        st.metric("Classe dominante", metrics["top_label"])
        st.metric("Confiance moyenne", f"{metrics['average_confidence']:.2f}")

    st.markdown("#### Repartition des detections")
    if metrics["label_counts"]:
        for label, count in metrics["label_counts"].most_common():
            st.markdown(
                f"""
                <div class="dashboard-row">
                    <span>{label}</span>
                    <span>{count}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Aucun objet detecte sur cette image.")

    st.markdown("#### Donnees utiles disponibles")
    st.caption(
        "Actuellement, le dashboard peut s'appuyer sur le nombre d'objets, les classes "
        "detectees, la confiance des detections et la position relative left/center/right + "
        "near/mid/far."
    )


def render_results(image: Image.Image, result: PipelineOutput) -> None:
    st.success("Pipeline execute avec succes.")

    content_col, dashboard_col = st.columns([1.7, 1], gap="large")

    with content_col:
        _render_report(result)
        st.markdown("---")
        _render_images(image, result)

    with dashboard_col:
        _render_dashboard(result.scene_detections)
