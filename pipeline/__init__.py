"""
pipeline - Module de schéma commun pour l'intégration du projet.

Exports principaux:
- BoundingBox: Coordonnées d'une boîte englobante
- DetectedObject: Objet détecté (label, confidence, bbox)
- SceneDetections: Résultat des détections CV
- AnalyseResultat: Résultat de l'analyse LLM
- RisqueEvaluation: Évaluation du risque
- PipelineOutput: Sortie complète du pipeline
"""

from pipeline.schema import (
    BoundingBox,
    DetectedObject,
    SceneDetections,
    AnalyseResultat,
    RisqueEvaluation,
    PipelineOutput,
)

__all__ = [
    "BoundingBox",
    "DetectedObject",
    "SceneDetections",
    "AnalyseResultat",
    "RisqueEvaluation",
    "PipelineOutput",
]
