"""
agent.py - Orchestrateur principal de l'agent LLM.
Coordonne l'évaluation des risques, la construction de prompts et le formatage des réponses.
"""

import os
import logging
from typing import Optional, Dict

# Importations des schémas de données et des modules internes
from pipeline.schema import (
   SceneDetections,
   AnalyseResultat,
   RisqueEvaluation,
   BoundingBox,
   DetectedObject,
   PipelineOutput
)
from llm_agent.risk_rules import RiskEvaluator, RiskLevel
from llm_agent.prompt_builder import PromptBuilder
from llm_agent.formatter import ResponseFormatter
from llm_agent.tools import SceneAnalysisTools

# Importation du client OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("openai package not installed. Install with: pip install openai")

# Configure les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _resolve_openai_api_key(explicit_api_key: Optional[str] = None) -> Optional[str]:
   """Retourne la clé API depuis le paramètre explicite ou l'environnement."""
   return explicit_api_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_API_KEY")


#Classe principale de l'agent d'analyse de scènes routières
class DrivingSceneAnalyzer: 
   """
   Agent d'analyse de scènes routières.
  
   Prend en entrée les détections CV (SceneDetections) et produit
   une analyse complète (AnalyseResultat) avec évaluation des risques.
   """

   def __init__(self, use_llm: bool = False, api_key: Optional[str] = None):
       """
       Initialise l'analyseur.
      
       Args:
           use_llm: Si False, utilise une analyse basée sur des règles uniquement.
                   Si True, utalisera l'API OpenAI.
           api_key: Clé API OpenAI. Si None, utilise OPENAI_API_KEY depuis l'environnement.
       """
       self.use_llm = use_llm
       self.risk_evaluator = RiskEvaluator()
       self.client = None
       self.model = "gpt-4o-mini"  # Modèle utilisé (gpt-4-turbo ou gpt-4o-mini pour économiser)
       
       # Initialise le client OpenAI si nécessaire
       if self.use_llm:
           if not OPENAI_AVAILABLE:
               raise ImportError(
                   "openai est requis pour utiliser le LLM. "
                   "Installez avec: pip install openai"
               )
           
           # Récupère la clé API
           api_key = _resolve_openai_api_key(api_key)
           if not api_key:
               raise ValueError(
                   "Clé API OpenAI non trouvée. "
                   "Configurez OPENAI_API_KEY (ou OPEN_API_KEY) en variable d'environnement ou passez-la en paramètre."
               )
           
           self.client = OpenAI(api_key=api_key)
           logger.info(f"Client OpenAI initialisé avec le modèle: {self.model}")

   def analyze_scene(
       self,
       detections: SceneDetections,
       scene_context: str = "scene_context a definir",
       mock_llm_response: Optional[str] = None
   ) -> AnalyseResultat:
       """
       Analyse une scène routière complètement.
      
       Workflow:
       1. Évalue le risque basé sur les détections (règles)
       2. Construit un prompt pour le LLM
       3. (Optionnel) Appelle le LLM pour analyse enrichie
       4. Formate le résultat final
      
       Args:
           detections: Les objets détectés dans la scène
           scene_context: Contexte additionnel (météo, heure, etc.)
           mock_llm_response: (Test) Réponse mockée du LLM
          
       Returns:
           AnalyseResultat contenant résumé, risques et recommandations
       """
       # Phase 1: Évalue le risque basé sur les règles
       risk_score = self.risk_evaluator.evaluate_detections(detections)

       # Phase 2: Génère les recommandations de base
       base_recommendations = self.risk_evaluator.generate_risk_recommendations(risk_score)

       # Phase 3: Construit le prompt pour le LLM
       prompt = PromptBuilder.build_analysis_prompt(
           detections=detections,
           risk_score=risk_score,
           scene_context=scene_context
       )

       # Phase 4: Appelle le LLM ou utilise données mockées
       if mock_llm_response:
           # Mode test avec données mockées
           llm_response = mock_llm_response
       elif self.use_llm:
           # TODO: Appeler le vrai LLM ici (API OpenAI, HuggingFace, etc.)
           llm_response = self._call_llm(prompt)
       else:
           # Utilise une réponse par défaut basée sur les règles
           llm_response = self._generate_default_response(risk_score)

       # Phase 5: Formate la réponse du LLM
       analysis_result = ResponseFormatter.format_llm_response(
           llm_response,
           risk_score=risk_score.score
       )

       # Phase 6: Enrichit avec les recommandations basées sur les règles si pertinent
       if not analysis_result.recommandations:
           analysis_result.recommandations = base_recommendations

       return analysis_result

   def analyze_with_pipeline_output(
       self,
       detections: SceneDetections,
       scene_context: str = "Route générale"
   ) -> PipelineOutput:
       """
       Analyse la scène et retourne une sortie complète du pipeline.
      
       Args:
           detections: Les détections CV
           scene_context: Contexte additionnel
          
       Returns:
           PipelineOutput complet (détections + analyse)
       """
       analysis = self.analyze_scene(detections, scene_context)
       return PipelineOutput(
           scene_detections=detections,
           analyse_resultat=analysis
       )

   def _generate_default_response(self, risk_score) -> str:
       """Génère une réponse par défaut basée sur les règles"""
       if not risk_score.detected_hazards:
           response = """RÉSUMÉ: Route claire, aucun obstacles détectés. Continuez votre route.
RISQUES: Aucun risque majeur identifié.
RECOMMANDATIONS: Maintenir une vigilance constante et respecter les limitations de vitesse."""
       else:
           response = f"""RÉSUMÉ: Scène routière avec {len(risk_score.detected_hazards)} objets détectés. Niveau de risque: {risk_score.level.value}.
RISQUES: {', '.join(risk_score.primary_risks)}
RECOMMANDATIONS: {chr(10).join(['- ' + r for r in risk_score.primary_risks[:3]])}"""
      
       return response

   def _call_llm(self, prompt: str) -> str:
       """
       Appelle l'API OpenAI avec le prompt.
      
       Args:
           prompt: Le prompt pour le LLM
          
       Returns:
           La réponse du LLM
           
       Raises:
           RuntimeError: Si le client n'est pas initialisé
       """
       if not self.client:
           raise RuntimeError(
               "Client OpenAI non initialisé. "
               "Initialisez l'agent avec use_llm=True et une clé API valide."
           )
       
       try:
           logger.info(f"Appel API OpenAI avec le modèle {self.model}...")
           
           response = self.client.chat.completions.create(
               model=self.model,
               messages=[
                   {
                       "role": "system",
                       "content": PromptBuilder.SYSTEM_PROMPT
                   },
                   {
                       "role": "user",
                       "content": prompt
                   }
               ],
               temperature=0.7,
               max_tokens=500,
               top_p=0.9
           )
           
           llm_response = response.choices[0].message.content
           logger.info("Réponse LLM reçue avec succès")
           
           return llm_response
           
       except Exception as e:
           logger.error(f"Erreur lors de l'appel API OpenAI: {str(e)}")
           raise RuntimeError(f"Erreur OpenAI: {str(e)}") from e
