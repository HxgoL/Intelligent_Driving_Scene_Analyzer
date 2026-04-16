"""
Definit la page, les titres et les sous-titres.

TODO:
Ajouter une sidebar, la navigation, du multi-pages et un header dynamique.
"""

import streamlit as st


def configure_page() -> None:
    st.set_page_config(
        page_title="Intelligent Driving Scene Analyzer",
        layout="wide",
    )


def render_header() -> None:
    st.title("Intelligent Driving Scene Analyzer")
    st.subheader("Résultats de l'analyse de la scène de conduite intelligente")
