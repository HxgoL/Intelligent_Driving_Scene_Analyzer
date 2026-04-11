import streamlit as st

from PIL import Image

from pipeline.orchestrator import PipelineOrchestrator


st.title("Hello World.")

#Drag and drop
uploaded_file = st.file_uploader("Choisir une image (JPG)", type=["jpg"])

#Resultats

st.subheader("Résultats de l'analyse de la scène de conduite intelligente")

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    #afficher imazge uploader
    image = Image.open(uploaded_file)
    st.image(image, caption='Image uploadée', use_column_width=True)

    #remetre le curseur au debut de l'image pour la suite du pipeline
    uploaded_file.seek(0)

    orchestrator = PipelineOrchestrator()
    resultat = orchestrator.run_pipeline(uploaded_file)

    st.write("Pipeline execute avec succes")

    # Afficher les résultats de l'analyse (mock pour l'instant)
    st.subheader("Résumé de la scène")
    st.write("Niveau de risque :", resultat.analyse_resultat.risque_eval.risque_level)
    st.write("Résumé :", resultat.analyse_resultat.resume)
    st.write("Recommandations :")
    for reco in resultat.analyse_resultat.recommandations:
        st.write("-", reco)

else:
    st.info("Veuillez uploader une image JPG.")