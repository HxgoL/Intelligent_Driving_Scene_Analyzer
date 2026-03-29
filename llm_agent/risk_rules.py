"""
risk_rules.py - Implémente la logique d'évaluation des risques basée sur les objets détectés.
Analyse les détections pour calculer un score de risque et des recommandations.
"""


from enum import Enum
from typing import List, Dict, Tuple
from dataclasses import dataclass
from pipeline.schema import SceneDetections, DetectedObject




class RiskLevel(Enum):
   """Niveaux de risque possibles"""
   FAIBLE = "FAIBLE"
   MOYEN = "MOYEN"
   ÉLEVÉ = "ÉLEVÉ"
   CRITIQUE = "CRITIQUE"




@dataclass
class RiskScore:
   """Résultat de l'évaluation des risques"""
   level: RiskLevel
   score: float  # 0 à 100
   detected_hazards: List[str]
   primary_risks: List[str]




class RiskEvaluator:
   """Évalue les risques basés sur les objets détectés dans la scène"""


   # Mapping des labels d'objets à leurs facteurs de risque
   HAZARD_FACTORS = {
       "person": 15,
       "bicycle": 12,
       "car": 20,
       "truck": 25,
       "bus": 22,
       "motorcycle": 18,
       "traffic light": 0,  # Neutre
       "stop sign": 0,      # Neutre
       "speed limit": 0,    # Neutre
       "obstacle": 30,
       "pothole": 25,
       "debris": 20,
       "wet road": 15,
       "construction": 20,
   }


   # Seuils de proximité (en pixels, relatif à l'écran)
   # Les objets détectés près du centre sont plus critiques
   PROXIMITY_THRESHOLD_CLOSE = 0.2  # Dans 20% du centre
   PROXIMITY_THRESHOLD_MEDIUM = 0.5  # Dans 50% du centre


   @staticmethod
   def calculate_confidence_weight(confidence: float) -> float:
       """Pondère le risque selon la confiance de la détection"""
       return confidence * 0.5 + 0.5  # Min 0.5, Max 1.0


   @staticmethod
   def calculate_proximity_weight(
       bbox_center_x: float, bbox_center_y: float,
       image_width: float = 640, image_height: float = 480
   ) -> float:
       """
       Pondère le risque selon la proximité de l'objet au centre (avant du véhicule).
       Plus proche du centre = plus de risque
       """
       center_x = image_width / 2
       center_y = image_height * 0.7  # Considère le bas de l'image comme "devant"


       # Distance relative du centre
       relative_distance = (
           ((bbox_center_x - center_x) ** 2 + (bbox_center_y - center_y) ** 2) ** 0.5
       ) / (image_width / 2)


       # Plus on est loin, moins c'est risqué
       if relative_distance < RiskEvaluator.PROXIMITY_THRESHOLD_CLOSE:
           return 1.5
       elif relative_distance < RiskEvaluator.PROXIMITY_THRESHOLD_MEDIUM:
           return 1.2
       else:
           return 1.0


   @classmethod
   def get_hazard_factor(cls, label: str) -> float:
       """Récupère le facteur de risque pour un label donné"""
       label_lower = label.lower()
       for key, value in cls.HAZARD_FACTORS.items():
           if key in label_lower:
               return value
       return 10  # Facteur par défaut pour objets inconnus


   @classmethod
   def evaluate_detections(cls, detections: SceneDetections) -> RiskScore:
       """
       Évalue le risque global basé sur les détections.
      
       Args:
           detections: Les objets détectés dans la scène
          
       Returns:
           RiskScore avec le niveau, score numérique et hazards détectés
       """
       if not detections.detected_objects:
           return RiskScore(
               level=RiskLevel.FAIBLE,
               score=0,
               detected_hazards=[],
               primary_risks=[]
           )


       total_risk_score = 0
       detected_hazards = []
       hazard_details = []


       for obj in detections.detected_objects:
           # Récupère le facteur de risque de base
           base_factor = cls.get_hazard_factor(obj.label)


           # Calcule les pondérations
           confidence_weight = cls.calculate_confidence_weight(obj.confidence)
           proximity_weight = cls.calculate_proximity_weight(
               bbox_center_x=obj.bounding_box.x + obj.bounding_box.width / 2,
               bbox_center_y=obj.bounding_box.y + obj.bounding_box.height / 2
           )


           # Score pour cet objet
           object_risk = base_factor * confidence_weight * proximity_weight


           if base_factor > 5:  # Ne stocke que les vrais hazards
               detected_hazards.append(obj.label)
               hazard_details.append({
                   "object": obj.label,
                   "confidence": obj.confidence,
                   "risk_score": object_risk
               })


           total_risk_score += object_risk


       # Normalise le score (divise par nombre d'objets pour faire une moyenne)
       if len(detected_hazards) > 0:
           avg_risk_score = total_risk_score / len(detected_hazards)
       else:
           avg_risk_score = total_risk_score


       # Détermine le niveau de risque
       if avg_risk_score < 15:
           risk_level = RiskLevel.FAIBLE
       elif avg_risk_score < 35:
           risk_level = RiskLevel.MOYEN
       elif avg_risk_score < 60:
           risk_level = RiskLevel.ÉLEVÉ
       else:
           risk_level = RiskLevel.CRITIQUE


       # Génère les risques primaires (les 3 détections les plus critiques)
       hazard_details.sort(key=lambda x: x["risk_score"], reverse=True)
       primary_risks = [
           f"{h['object']} (confiance: {h['confidence']:.1%})"
           for h in hazard_details[:3]
       ]


       return RiskScore(
           level=risk_level,
           score=min(100, avg_risk_score),
           detected_hazards=detected_hazards,
           primary_risks=primary_risks
       )


   @classmethod
   def generate_risk_recommendations(cls, risk_score: RiskScore) -> List[str]:
       """Génère des recommandations basées sur le score de risque"""
       recommendations = []


       if risk_score.level == RiskLevel.FAIBLE:
           recommendations.append("Conditions normales. Continuez avec prudence.")


       elif risk_score.level == RiskLevel.MOYEN:
           recommendations.extend([
               "Soyez vigilant. Risques modérés détectés.",
               "Réduisez légèrement votre vitesse.",
               f"Objets à surveiller: {', '.join(risk_score.detected_hazards)}"
           ])


       elif risk_score.level == RiskLevel.ÉLEVÉ:
           recommendations.extend([
               "⚠️ Risque ÉLEVÉ. Réduisez considérablement votre vitesse.",
               f"Principaux risques: {', '.join(risk_score.primary_risks)}",
               "Soyez prêt à freiner ou à manœuvrer d'urgence.",
           ])


       elif risk_score.level == RiskLevel.CRITIQUE:
           recommendations.extend([
               "🚨 RISQUE CRITIQUE. Action immédiate requise!",
               f"Menaces détectées: {', '.join(risk_score.primary_risks)}",
               "Freinez immédiatement ou manœuvrez pour éviter.",
               "Mettez les feux de détresse si arrêt urgent.",
           ])


       return recommendations
