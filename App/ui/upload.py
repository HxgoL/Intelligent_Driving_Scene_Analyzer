"""
Gere l'upload et retourne le fichier ainsi que l'image chargee.
"""

from typing import BinaryIO

import streamlit as st
from PIL import Image


def render_uploader() -> tuple[BinaryIO | None, Image.Image | None]:
    uploaded_file = st.file_uploader("Choisir une image (JPG)", type=["jpg"])

    if uploaded_file is None:
        return None, None

    image = Image.open(uploaded_file)
    st.success("Fichier uploade avec succes.")

    return uploaded_file, image
