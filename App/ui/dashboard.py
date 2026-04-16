"""
Composants du dashboard lateral.
"""

import streamlit as st

from App.services.dashboard_metrics import compute_dashboard_metrics
from pipeline.schema import SceneDetections


def render_dashboard(detections: SceneDetections) -> None:
    metrics = compute_dashboard_metrics(detections)

    st.markdown("### Dashboard")

    metric_col_1, metric_col_2 = st.columns(2)
    with metric_col_1:
        st.metric("Objets detectes", metrics.total_objects)
        st.metric("Vehicules", metrics.vehicle_count)
        st.metric("Objets proches", metrics.near_objects)

    with metric_col_2:
        st.metric("Pietons", metrics.people_count)
        st.metric("Classe dominante", metrics.top_label)
        st.metric("Confiance moyenne", f"{metrics.average_confidence:.2f}")

    st.markdown("#### Repartition des detections")
    if metrics.label_counts:
        for label, count in metrics.label_counts.most_common():
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

    st.markdown("#### Donnees disponibles")
    st.caption(
        "Nombre d'objets, classes detectees, confiance des detections et position relative "
        "left/center/right + near/mid/far."
    )
