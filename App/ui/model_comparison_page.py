"""
Page Streamlit de comparaison des modeles candidats.
"""

import streamlit as st

from App.services.model_catalog_service import list_candidate_models
from App.ui.model_comparison_report import render_model_comparison_report


def render_model_comparison_page() -> None:
    st.set_page_config(page_title="Model Comparison", layout="wide")
    st.sidebar.markdown("## Navigation")
    st.sidebar.caption("Utilisez le menu natif Streamlit pour changer de page.")
    models = list_candidate_models()
    render_model_comparison_report(models)
