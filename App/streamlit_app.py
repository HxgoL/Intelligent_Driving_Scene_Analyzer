""" Idée de streamlit_app.py:
Point d'entrée de l'application, orchestre le flux et delegue les taches au classes appropriées, 
voici les etapes:

1) configurer la page
2) appliquer le style
3) afficher l’en-tête
4) demander une image à l’utilisateur
5) lancer l’analyse
6) afficher les résultats

"""

import streamlit as st

from App.services.pipeline_runner import run_analysis
from App.ui.page import configure_page, render_header
from App.ui.results import render_results
from App.ui.styles import apply_styles
from App.ui.upload import render_uploader

def main() -> None:
    configure_page()
    apply_styles()
    render_header()

    uploaded_file, image = render_uploader()

    if uploaded_file is None or image is None:
        st.info("Veuillez uploader une image JPG")
        return
    
    result = run_analysis(uploaded_file)
    render_results(image, result)

if __name__ == "__main__":
    main()

