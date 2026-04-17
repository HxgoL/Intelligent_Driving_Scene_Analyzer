"""
Composants d'affichage des images.
"""

import streamlit as st
from PIL import Image

from App.services.image_annotation_service import annotate_image
from pipeline.schema import PipelineOutput

MAX_IMAGE_WIDTH = 900


def _get_display_width(image: Image.Image) -> int:
    return min(image.width, MAX_IMAGE_WIDTH)


def render_centered_image(image: Image.Image, caption: str, width: int | None = None) -> None:
    left_col, center_col, right_col = st.columns([1, 3, 1])
    del left_col, right_col

    with center_col:
        st.image(
            image,
            caption=caption,
            width=width or _get_display_width(image),
        )


def render_image_comparison(image: Image.Image, result: PipelineOutput) -> None:
    annotated_image = annotate_image(image, result.scene_detections)

    st.markdown("### Comparaison visuelle")
    original_col, annotated_col = st.columns(2, gap="large")

    with original_col:
        st.markdown("#### Image source")
        st.image(
            image,
            caption="Image originale",
            use_container_width=True,
        )

    with annotated_col:
        st.markdown("#### Image analysee")
        st.image(
            annotated_image,
            caption="Detections YOLO",
            use_container_width=True,
        )
