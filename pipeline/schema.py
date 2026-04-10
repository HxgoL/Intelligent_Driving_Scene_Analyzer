# idée: api interne
# pipeline/schema.py définit les objets métier partagés du projet.
# Chaque module peut avoir son format interne, mais sa sortie publique doit respecter ce schéma commun afin de garantir l’intégration entre vision, agent LLM et interface.


from dataclasses import dataclass
from typing import List, Optional

#Pour cv_module
# On a infer.py qui renvoie la detection de l'image (classification, bounding box, etc)

#Je crée une classe bounding box pour stocker les coordonnées de la boîte englobante
#objet qui represente une boite
@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

#Je crée une classe pour stocker les informations sur les objets détectés
#objet qui represente un objet detecté
@dataclass
class DetectedObject:
    label: str
    confidence: float
    bounding_box: BoundingBox
    relative_position: Optional[str] = None

#Objet qui represente la sortie brute du cv
@dataclass
class SceneDetections:
    detected_objects: List[DetectedObject]
    #On peut ajouter d'autres informations sur la scène, comme les conditions météorologiques, l'heure de la journée, etc.

#Pour l'agent

#Objet qui represente le risque evalué
@dataclass
class RisqueEvaluation:
    risque_level: str

#objet qui represente la sortie textuelle finale
@dataclass
class AnalyseResultat:
    resume: str
    recommandations: List[str]
    risque_eval: RisqueEvaluation

#Objet qui represente la sortie pour streamlit
@dataclass
class PipelineOutput:
    scene_detections: SceneDetections
    analyse_resultat: AnalyseResultat
