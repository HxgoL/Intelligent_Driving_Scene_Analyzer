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

    # Méthodes d'extraction pour chaque section
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

    # Méthodes d'extraction pour les risques
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

    # Méthode d'extraction pour les recommandations
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

    # Méthode pour inférer le niveau de risque à partir du texte
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

    # Méthode principale pour formater la réponse du LLM en AnalyseResultat
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

    # Méthode de secours pour formater les résultats sans LLM (ex: tests unitaires)
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

    # Méthode pour formater le résultat pour affichage (ex: Streamlit)
   @staticmethod
   def format_for_display(result: AnalyseResultat) -> Dict:
       """Formate le résultat pour affichage lisible (ex: Streamlit)"""
       return {
           "résumé": result.resume,
           "niveau_risque": result.risque_eval.risque_level,
           "recommandations": result.recommandations,
       }
   