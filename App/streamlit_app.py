import streamlit as st
import pandas as pd
import numpy as np

from PIL import Image

from Intelligent_Driving_Scene_Analyzer.pipeline.orchestrator import PipelineOrchestrator


st.title("Hello World.")

#Drag and drop
uploaded_file = st.file_uploader("Choose a file", type=["jpg"])

#Resultats

st.subheader("Résultats de l'analyse de la scène de conduite intelligente")

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    orchestrator = PipelineOrchestrator()
    resultat = orchestrator.run_pipeline(uploaded_file)

    st.write("Pipeline execute avec succes")

else:
    st.info("Veuillez uploader une image JPG.")