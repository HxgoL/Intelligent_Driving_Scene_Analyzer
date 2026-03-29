"""
formatter.py - Parse et formate les réponses du LLM en structures exploitables.
Transforme le texte brut du LLM en objets AnalyseResultat structurés.
"""

import re
from typing import List, Tuple, Optional, Dict
from pipeline.schema import AnalyseResultat, RisqueEvaluation


class ResponseFormatter:
   """Parse les réponses du LLM et les formate en structures exploitables"""

   # Pattern pour extraire les sections du prompt
   RESUME_PATTERN = r"(?:RÉSUMÉ|RESUME)\s*:\s*(.+?)(?=(?:RISQUES|RECOMMANDATIONS|$))"
   RISQUES_PATTERN = r"(?:RISQUES|MENACES)\s*:\s*(.+?)(?=RECOMMANDATIONS|$)"
   RECOMMANDATIONS_PATTERN = r"RECOMMANDATIONS?\s*:\s*(.+?)$"

   @staticmethod
   def extract_resume(text: str) -> str:
       """Extrait le résumé du texte de réponse"""
       match = re.search(ResponseFormatter.RESUME_PATTERN, text, re.IGNORECASE | re.DOTALL)
       if match:
           resume = match.group(1).strip()
           # Limite à ~200 caractères pour la concision
           if len(resume) > 200:
               resume = resume[:197] + "..."
           return resume
       return "Analyse non disponible"

   @staticmethod
   def extract_risks(text: str) -> List[str]:
       """Extrait la liste des risques du texte"""
       match = re.search(ResponseFormatter.RISQUES_PATTERN, text, re.IGNORECASE | re.DOTALL)
       if match:
           risks_text = match.group(1).strip()
           # Split par tirets, numéros ou retours à la ligne
           risks = re.split(r'[-•\n]+', risks_text)
           # Nettoie et filtre les risques vides
           risks = [r.strip() for r in risks if r.strip()]
           return risks[:5]  # Limite à 5 risques
       return []

   @staticmethod
   def extract_recommendations(text: str) -> List[str]:
       """Extrait les recommandations du texte"""
       match = re.search(ResponseFormatter.RECOMMANDATIONS_PATTERN, text, re.IGNORECASE | re.DOTALL)
       if match:
           rec_text = match.group(1).strip()
           # Split par tirets, numéros ou retours à la ligne
           recommendations = re.split(r'[-•\n]+', rec_text)
           # Nettoie et filtre les recommandations vides
           recommendations = [r.strip() for r in recommendations if r.strip()]
           return recommendations[:5]  # Limite à 5 recommandations
       return []

   @staticmethod
   def infer_risk_level(text: str, risk_score: float = 50) -> str:
       """Infère le niveau de risque basé sur le contenu du texte"""
       text_lower = text.lower()


       # Cherche les mots clés indiquant le niveau de risque
       if any(word in text_lower for word in ["critique", "immédiat", "danger", "🚨"]):
           return "CRITIQUE"
       elif any(word in text_lower for word in ["élevé", "urgent", "réduisez vitesse", "attention"]):
           return "ÉLEVÉ"
       elif any(word in text_lower for word in ["moyen", "vigilant", "prudence", "attention"]):
           return "MOYEN"
       else:
           return "FAIBLE"

   @classmethod
   def format_llm_response(
       cls,
       llm_response: str,
       risk_score: Optional[float] = None
   ) -> AnalyseResultat:
       """
       Formate la réponse brute du LLM en objet AnalyseResultat structuré.
      
       Args:
           llm_response: La réponse textuelle du LLM
           risk_score: Score numérique optionnel (0-100) pour refiner le niveau de risque
          
       Returns:
           AnalyseResultat structuré et prêt à utiliser
       """
       # Extrait les composants
       resume = cls.extract_resume(llm_response)
       risks = cls.extract_risks(llm_response)
       recommendations = cls.extract_recommendations(llm_response)


       # Infère le niveau de risque
       risk_level = cls.infer_risk_level(llm_response, risk_score or 50)


       # Crée l'objet de résultat
       return AnalyseResultat(
           resume=resume,
           recommandations=recommendations,
           risque_eval=RisqueEvaluation(risque_level=risk_level)
       )

   @staticmethod
   def fallback_format(
       resume: str,
       risks: List[str],
       recommendations: List[str],
       risk_level: str = "MOYEN"
   ) -> AnalyseResultat:
       """
       Formate les données en utilisant les valeurs fournies directement.
       Utile pour les tests ou quand on n'aparse pas le LLM.
       """
       return AnalyseResultat(
           resume=resume,
           recommandations=recommendations,
           risque_eval=RisqueEvaluation(risque_level=risk_level)
       )

   @staticmethod
   def format_for_display(result: AnalyseResultat) -> Dict:
       """Formate le résultat pour affichage lisible (ex: Streamlit)"""
       return {
           "résumé": result.resume,
           "niveau_risque": result.risque_eval.risque_level,
           "recommandations": result.recommandations,
       }
    detections = payload.get("detections", [])
    labels = {str(det.get('label', '')).lower() for det in detections}

    recommendations: List[str] = []

    if risk_level in {"ÉLEVÉ", "CRITIQUE"}:
        recommendations.append("Réduire immédiatement la vitesse et renforcer la vigilance.")
    elif risk_level == "MOYEN":
        recommendations.append("Adapter la vitesse aux conditions de circulation.")

    if "pedestrian" in labels or "person" in labels:
        recommendations.append("Surveiller attentivement les piétons à proximité.")

    if "truck" in labels or "bus" in labels:
        recommendations.append("Augmenter la distance de sécurité avec les gros véhicules.")

    weather = str(payload.get("scene_context", {}).get("weather", "")).lower()
    if weather in {"rain", "fog", "storm"}:
        recommendations.append("Anticiper un freinage plus long à cause des conditions météo.")

    if not recommendations:
        recommendations.append("Poursuivre la conduite avec vigilance normale.")

    return recommendations[:3]

def format_report(
    payload: Dict[str, Any],
    risk_result: Dict[str, Any],
) -> str:
    """
    Produit un rapport texte simple pour semaine 1.
    Pas encore de vrai appel LLM ici : c'est un prototype déterministe.
    """
    scene_text = _scene_summary(payload)
    risk_level = risk_result.get("risk_level", "INCONNU")
    score = risk_result.get("score", 0)
    reasoning = risk_result.get("reasoning", [])
    recommendations = _recommendations(payload, risk_level)

    reasoning_text = ""
    if reasoning:
        reasoning_text = "\n".join(f"- {reason}" for reason in reasoning[:6])
    else:
        reasoning_text = "- Aucune justification disponible."

    recommendations_text = "\n".join(f"- {rec}" for rec in recommendations)

    return (
        "=== RAPPORT D'ANALYSE DE SCÈNE ===\n\n"
        f"Résumé de la scène :\n{scene_text}\n\n"
        f"Niveau de risque : {risk_level}\n"
        f"Score de risque : {score}\n\n"
        "Justification :\n"
        f"{reasoning_text}\n\n"
        "Recommandations :\n"
        f"{recommendations_text}\n"
    )
