"""
prompt_builder.py - Construit les prompts pour le LLM basés sur les détections.
Transforme les données brutes en prompts structurés et contextualisés.
"""


from typing import List, Dict
import json
from pipeline.schema import SceneDetections, DetectedObject
from llm_agent.risk_rules import RiskScore, RiskLevel




class PromptBuilder:
   """Construit les prompts pour communication avec le LLM"""


   SYSTEM_PROMPT = """Tu es un expert en sécurité routière et en analyse de scènes de conduite.
Tu analyzes les objets détectés dans une scène routière et tu fournis:
1. Un résumé de la situation
2. Les risques identifiés
3. Des recommandations de sécurité


Sois concis, clair et actionnable. Priorité à la sécurité."""


   @staticmethod
   def format_detection_for_llm(detection: DetectedObject) -> Dict:
       """Formate une détection pour le LLM"""
       return {
           "type": detection.label,
           "confiance": f"{detection.confidence:.1%}",
           "position": {
               "x": f"{detection.bounding_box.x:.0f}px",
               "y": f"{detection.bounding_box.y:.0f}px",
               "largeur": f"{detection.bounding_box.width:.0f}px",
               "hauteur": f"{detection.bounding_box.height:.0f}px",
           }
       }


   @classmethod
   def build_analysis_prompt(
       cls,
       detections: SceneDetections,
       risk_score: RiskScore,
       scene_context: str = "Route généraleuse, jour clair"
   ) -> str:
       """
       Construit un prompt complet pour analyser la scène.
      
       Args:
           detections: Les objets détectés
           risk_score: Le score de risque calculé
           scene_context: Contexte additionnel (météo, heure, etc.)
          
       Returns:
           Le prompt structuré pour le LLM
       """
       # Formate les détections
       formatted_detections = [
           cls.format_detection_for_llm(obj)
           for obj in detections.detected_objects
       ]


       prompt = f"""ANALYSE DE SCÈNE ROUTIÈRE


Contexte:
- Conditions: {scene_context}
- Nombre d'objets détectés: {len(detections.detected_objects)}
- Niveau de risque préliminaire: {risk_score.level.value}
- Score de risque: {risk_score.score:.1f}/100


Objets détectés:
"""
      
       if formatted_detections:
           prompt += json.dumps(formatted_detections, ensure_ascii=False, indent=2)
       else:
           prompt += "Aucun objet détecté - Route claire"


       prompt += f"""


Risques identifiés:
- Hazards: {', '.join(risk_score.detected_hazards) if risk_score.detected_hazards else 'Aucun'}
- Risques primaires: {', '.join(risk_score.primary_risks) if risk_score.primary_risks else 'Aucun'}


Tâche:
1. Fournis un résumé (2-3 lignes) de la situation
2. Liste les principaux risques
3. Donne 2-3 recommandations d'action


Format réponse:
RÉSUMÉ: [ton résumé]
RISQUES: [liste des risques]
RECOMMANDATIONS: [liste d'actions]
"""
       return prompt


   @classmethod
   def build_simple_prompt(
       cls,
       detections: SceneDetections
   ) -> str:
       """
       Construit un prompt simple pour les tests avec données mockées.
       """
       objects_summary = []
       for obj in detections.detected_objects:
           objects_summary.append(
               f"- {obj.label} (confiance: {obj.confidence:.0%})"
           )


       prompt = f"""Scène routière détectée avec {len(detections.detected_objects)} objets:


{chr(10).join(objects_summary) if objects_summary else 'Aucun objet détecté'}


Analysez brièvement les risques et proposez des recommandations."""
      
       return prompt


   @staticmethod
   def build_json_prompt(detections: SceneDetections) -> str:
       """
       Construit un prompt JSON pour communication structurée.
       Utile pour les LLMs qui comprennent JSON.
       """
       detections_dict = {
           "scene": {
               "nombre_objets": len(detections.detected_objects),
               "objets": [
                   {
                       "label": obj.label,
                       "confidence": obj.confidence,
                       "bbox": {
                           "x": obj.bounding_box.x,
                           "y": obj.bounding_box.y,
                           "width": obj.bounding_box.width,
                           "height": obj.bounding_box.height,
                       }
                   }
                   for obj in detections.detected_objects
               ]
           }
       }
       return json.dumps(detections_dict, ensure_ascii=False, indent=2)
