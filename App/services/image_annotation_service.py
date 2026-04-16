"""
Service d'annotation d'image pour la couche UI.
"""

from PIL import Image

from cv_module.infer import draw_detections_on_image
from pipeline.schema import SceneDetections


def annotate_image(image: Image.Image, detections: SceneDetections) -> Image.Image:
    return draw_detections_on_image(image, detections)
