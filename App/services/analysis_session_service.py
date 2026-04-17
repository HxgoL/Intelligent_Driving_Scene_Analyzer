"""
Service de gestion de l'etat courant de l'analyse dans Streamlit.

analysis_session_service
initialise les clés de session, 
détecte un nouvel upload,
stocke l’image et le résultat,
puis les restitue quand tu reviens sur la page.

"""

from dataclasses import dataclass

import streamlit as st
from PIL import Image

from pipeline.schema import PipelineOutput


@dataclass(frozen=True)
class StoredAnalysis:
    image: Image.Image | None
    result: PipelineOutput | None


class AnalysisSessionService:
    IMAGE_KEY = "analysis_image"
    RESULT_KEY = "analysis_result"
    FILE_SIGNATURE_KEY = "analysis_file_signature"

    def initialize(self) -> None:
        if self.IMAGE_KEY not in st.session_state:
            st.session_state[self.IMAGE_KEY] = None
        if self.RESULT_KEY not in st.session_state:
            st.session_state[self.RESULT_KEY] = None
        if self.FILE_SIGNATURE_KEY not in st.session_state:
            st.session_state[self.FILE_SIGNATURE_KEY] = None

    def build_file_signature(self, uploaded_file) -> tuple[str | None, int | None]:
        return (
            getattr(uploaded_file, "name", None),
            getattr(uploaded_file, "size", None),
        )

    def has_new_upload(self, uploaded_file) -> bool:
        return st.session_state[self.FILE_SIGNATURE_KEY] != self.build_file_signature(
            uploaded_file
        )

    def store_analysis(self, uploaded_file, image: Image.Image, result: PipelineOutput) -> None:
        st.session_state[self.IMAGE_KEY] = image
        st.session_state[self.RESULT_KEY] = result
        st.session_state[self.FILE_SIGNATURE_KEY] = self.build_file_signature(uploaded_file)

    def get_stored_analysis(self) -> StoredAnalysis:
        return StoredAnalysis(
            image=st.session_state[self.IMAGE_KEY],
            result=st.session_state[self.RESULT_KEY],
        )
