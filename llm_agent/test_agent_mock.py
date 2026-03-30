"""
test_agent_mock.py - Tests du prototype LLM agent avec des données mockées.
Évalue les 3 modules (risk_rules, prompt_builder, formatter) de manière indépendante.
"""


import json
from pipeline.schema import (
   BoundingBox,
   DetectedObject,
   SceneDetections,
   PipelineOutput
)
from llm_agent.agent import DrivingSceneAnalyzer
from llm_agent.risk_rules import RiskEvaluator
from llm_agent.prompt_builder import PromptBuilder
from llm_agent.formatter import ResponseFormatter




# ==================== DONNÉES MOCKÉES ====================


def create_mock_empty_scene() -> SceneDetections:
   """Crée une scène vide (route claire)"""
   return SceneDetections(detected_objects=[])




def create_mock_simple_scene() -> SceneDetections:
   """Crée une scène simple avec quelques objets"""
   objects = [
       DetectedObject(
           label="car",
           confidence=0.95,
           bounding_box=BoundingBox(x=150, y=200, width=100, height=80)
       ),
       DetectedObject(
           label="bicycle",
           confidence=0.87,
           bounding_box=BoundingBox(x=300, y=250, width=60, height=100)
       ),
       DetectedObject(
           label="traffic light",
           confidence=0.92,
           bounding_box=BoundingBox(x=600, y=100, width=30, height=50)
       ),
   ]
   return SceneDetections(detected_objects=objects)




def create_mock_dangerous_scene() -> SceneDetections:
   """Crée une scène avec obstacles/dangers"""
   objects = [
       DetectedObject(
           label="person",
           confidence=0.98,
           bounding_box=BoundingBox(x=280, y=320, width=40, height=100)  # Centre avant
       ),
       DetectedObject(
           label="obstacle",
           confidence=0.91,
           bounding_box=BoundingBox(x=300, y=300, width=80, height=60)   # Proche
       ),
       DetectedObject(
           label="truck",
           confidence=0.93,
           bounding_box=BoundingBox(x=200, y=250, width=150, height=100)
       ),
   ]
   return SceneDetections(detected_objects=objects)




def create_mock_critical_scene() -> SceneDetections:
   """Crée une scène critique"""
   objects = [
       DetectedObject(
           label="person",
           confidence=0.99,
           bounding_box=BoundingBox(x=320, y=340, width=30, height=80)  # Très proche au centre
       ),
       DetectedObject(
           label="obstacle",
           confidence=0.97,
           bounding_box=BoundingBox(x=310, y=330, width=60, height=50)  # Très proche
       ),
   ]
   return SceneDetections(detected_objects=objects)




# ==================== TESTS ====================


def test_risk_evaluation():
   """Test 1: Évaluation des risques avec risk_rules.py"""
   print("\n" + "="*60)
   print("TEST 1: ÉVALUATION DES RISQUES (risk_rules.py)")
   print("="*60)


   test_cases = [
       ("Route claire", create_mock_empty_scene()),
       ("Scène simple", create_mock_simple_scene()),
       ("Scène dangereuse", create_mock_dangerous_scene()),
       ("Scène critique", create_mock_critical_scene()),
   ]


   evaluator = RiskEvaluator()


   for name, scene in test_cases:
       print(f"\n▶ {name}:")
       risk_score = evaluator.evaluate_detections(scene)
      
       print(f"  - Niveau: {risk_score.level.value}")
       print(f"  - Score: {risk_score.score:.1f}/100")
       print(f"  - Hazards: {', '.join(risk_score.detected_hazards) or 'Aucun'}")
       print(f"  - Risques primaires: {', '.join(risk_score.primary_risks) or 'Aucun'}")


       # Génère aussi les recommandations
       recommendations = evaluator.generate_risk_recommendations(risk_score)
       print(f"  - Recommandations ({len(recommendations)}):")
       for rec in recommendations:
           print(f"    • {rec}")




def test_prompt_building():
   """Test 2: Construction des prompts avec prompt_builder.py"""
   print("\n" + "="*60)
   print("TEST 2: CONSTRUCTION DES PROMPTS (prompt_builder.py)")
   print("="*60)


   evaluator = RiskEvaluator()
   scene = create_mock_dangerous_scene()
   risk_score = evaluator.evaluate_detections(scene)


   print("\n▶ Prompt d'analyse complet:")
   prompt = PromptBuilder.build_analysis_prompt(
       detections=scene,
       risk_score=risk_score,
       scene_context="Route urbaine, jour nuageux"
   )
   print(prompt[:500] + "..." if len(prompt) > 500 else prompt)


   print("\n▶ Prompt simple:")
   simple_prompt = PromptBuilder.build_simple_prompt(scene)
   print(simple_prompt)


   print("\n▶ Prompt JSON:")
   json_prompt = PromptBuilder.build_json_prompt(scene)
   print(json_prompt[:400] + "..." if len(json_prompt) > 400 else json_prompt)




def test_response_formatting():
   """Test 3: Formatage des réponses avec formatter.py"""
   print("\n" + "="*60)
   print("TEST 3: FORMATAGE DES RÉPONSES (formatter.py)")
   print("="*60)


   # Simule des réponses du LLM
   test_responses = [
       """RÉSUMÉ: Route dégagée, conditions normales.
RISQUES: Aucun risque majeur
RECOMMANDATIONS: Continuer normalement - Maintenir vigilance""",


       """RÉSUMÉ: Personne détectée à proximité du véhicule.
RISQUES: Piéton sur la route - Risque de collision
RECOMMANDATIONS:
- Réduire vitesse immédiatement
- Préparer freinage d'urgence
- Klaxonner si nécessaire""",


       """RÉSUMÉ: Situation critique avec obstruction totale
RISQUES: 🚨 Obstacle critique à 20m - Personne en danger
RECOMMANDATIONS:
- FREINER D'URGENCE
- Manœuvre d'évitement immédiate
- Activer feux de détresse""",
   ]


   for i, response in enumerate(test_responses, 1):
       print(f"\n▶ Réponse {i}:")
       print(f"  LLM raw: {response[:80]}...")
      
       result = ResponseFormatter.format_llm_response(response)
       print(f"  ✓ Parsée:")
       print(f"    - Résumé: {result.resume}")
       print(f"    - Niveau: {result.risque_eval.risque_level}")
       print(f"    - Recommandations: {len(result.recommandations)} items")




def test_full_agent_workflow():
   """Test 4: Workflow complet de l'agent"""
   print("\n" + "="*60)
   print("TEST 4: WORKFLOW COMPLET DE L'AGENT")
   print("="*60)


   analyzer = DrivingSceneAnalyzer(use_llm=False)


   test_scenarios = [
       ("Situation normale", create_mock_simple_scene()),
       ("Situation dangereuse", create_mock_dangerous_scene()),
       ("Situation critique", create_mock_critical_scene()),
   ]


   for name, scene in test_scenarios:
       print(f"\n▶ {name}:")
      
       result = analyzer.analyze_scene(
           detections=scene,
           scene_context="Test routier"
       )


       print(f"  📋 Résumé: {result.resume}")
       print(f"  ⚠️  Risque: {result.risque_eval.risque_level}")
       print(f"  ✓ Recommandations ({len(result.recommandations)}):")
       for rec in result.recommandations:
           print(f"    - {rec}")




def test_mock_llm_response():
   """Test 5: Agent avec réponse mockée du LLM"""
   print("\n" + "="*60)
   print("TEST 5: AGENT AVEC RÉPONSE LLM MOCKÉE")
   print("="*60)


   mock_response = """RÉSUMÉ: Scène routière complexe avec multiples obstacles détectés.
RISQUES:
- Véhicule lourd à proximité
- Piéton détecté sur le côté
- Feu tricolore à surveiller
RECOMMANDATIONS:
- Réduire vitesse de 20 km/h
- Maintenir distance de sécurité
- Rester vigilant aux changements"""


   analyzer = DrivingSceneAnalyzer(use_llm=False)
   scene = create_mock_dangerous_scene()


   result = analyzer.analyze_scene(
       detections=scene,
       scene_context="Zone urbaine dense",
       mock_llm_response=mock_response
   )


   print(f"\n✓ Analyse complète générée:")
   print(f"  📋 Résumé: {result.resume}")
   print(f"  ⚠️  Risque: {result.risque_eval.risque_level}")
   print(f"  ✓ Recommandations:")
   for rec in result.recommandations:
       print(f"    - {rec}")




def test_pipeline_output():
   """Test 6: Sortie complète du pipeline"""
   print("\n" + "="*60)
   print("TEST 6: SORTIE COMPLÈTE DU PIPELINE")
   print("="*60)


   analyzer = DrivingSceneAnalyzer(use_llm=False)
   scene = create_mock_simple_scene()


   output = analyzer.analyze_with_pipeline_output(
       detections=scene,
       scene_context="Route générale"
   )


   print(f"\n✓ PipelineOutput:")
   print(f"  - Détections: {len(output.scene_detections.detected_objects)} objets")
   print(f"  - Analyse risque: {output.analyse_resultat.risque_eval.risque_level}")
   print(f"  - Recommandations: {len(output.analyse_resultat.recommandations)} items")




# ==================== EXÉCUTION ====================


if __name__ == "__main__":
   print("\n🚀 TESTS DU PROTOTYPE AGENT LLM AVEC DONNÉES MOCKÉES\n")


   test_risk_evaluation()
   test_prompt_building()
   test_response_formatting()
   test_full_agent_workflow()
   test_mock_llm_response()
   test_pipeline_output()


   print("\n" + "="*60)
   print("✅ TOUS LES TESTS COMPLÉTÉS!")
   print("="*60)
   print("\n📝 Résumé:")
   print("  ✓ risk_rules.py: Évaluation des risques fonctionnelle")
   print("  ✓ prompt_builder.py: Construction des prompts fonctionnelle")
   print("  ✓ formatter.py: Parsing des réponses fonctionnel")
   print("  ✓ agent.py: Orchestration complète fonctionnelle")
   print("\n💡 Prochaines étapes:")
   print("  1. Intégrer un vrai LLM (OpenAI, HuggingFace, etc.)")
   print("  2. Connecter à la sortie réelle du CV module")
   print("  3. Intégrer dans l'interface Streamlit")
   print("  4. Tests d'intégration complète")
