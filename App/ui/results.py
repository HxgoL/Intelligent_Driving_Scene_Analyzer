"""
Orchestre l'affichage global des resultats.
"""

import streamlit as st
from PIL import Image

from App.ui.dashboard import render_dashboard
from App.ui.image_panels import render_image_comparison
from App.ui.report import render_report
from pipeline.schema import PipelineOutput


def render_results(image: Image.Image, result: PipelineOutput) -> None:
    st.success("Pipeline execute avec succes.")

    content_col, dashboard_col = st.columns([2.3, 0.9], gap="large")

    with content_col:
        render_image_comparison(image, result)
        st.markdown("---")
        render_report(result)

    with dashboard_col:
        render_dashboard(result.scene_detections)
