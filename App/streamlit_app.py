"""
Point d'entree de l'application Streamlit.
"""

import streamlit as st

from App.services.analysis_session_service import AnalysisSessionService
from App.services.pipeline_runner import run_analysis
from App.ui.page import configure_page, render_header
from App.ui.results import render_results
from App.ui.styles import apply_styles
from App.ui.upload import render_uploader


def main() -> None:
    session_service = AnalysisSessionService()

    configure_page()
    apply_styles()
    st.sidebar.markdown("## Navigation")
    st.sidebar.caption("Utilisez le menu natif Streamlit pour changer de page.")
    render_header()
    session_service.initialize()

    uploaded_file, image = render_uploader()

    if uploaded_file is not None and image is not None:
        if session_service.has_new_upload(uploaded_file):
            result = run_analysis(uploaded_file)
            session_service.store_analysis(uploaded_file, image, result)

    stored_analysis = session_service.get_stored_analysis()

    if stored_analysis.image is not None and stored_analysis.result is not None:
        render_results(stored_analysis.image, stored_analysis.result)
        return

    st.info("Veuillez uploader une image JPG.")


if __name__ == "__main__":
    main()
