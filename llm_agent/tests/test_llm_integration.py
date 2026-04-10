"""
test_llm_integration.py - Tests de l'intégration LLM Agent
Tests unitaires pour vérifier que l'agent fonctionne correctement.
"""

import unittest
import os
from pipeline.schema import (
    BoundingBox,
    DetectedObject,
    SceneDetections
)
from llm_agent.agent import DrivingSceneAnalyzer
from llm_agent.tools import SceneAnalysisTools
from llm_agent.risk_rules import RiskEvaluator, RiskLevel


class TestDrivingSceneAnalyzer(unittest.TestCase):
    """Tests du DrivingSceneAnalyzer en mode sans LLM"""

    def setUp(self):
        """Initialise les données de test"""
        self.analyzer_no_llm = DrivingSceneAnalyzer(use_llm=False)
        
        # Scène simple
        self.simple_scene = SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="car",
                    confidence=0.95,
                    bounding_box=BoundingBox(x=150, y=200, width=100, height=80)
                ),
                DetectedObject(
                    label="person",
                    confidence=0.88,
                    bounding_box=BoundingBox(x=320, y=250, width=50, height=120)
                ),
            ]
        )
        
        # Scène vide
        self.empty_scene = SceneDetections(detected_objects=[])
        
        # Scène complexe
        self.complex_scene = SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="car",
                    confidence=0.95,
                    bounding_box=BoundingBox(x=100, y=150, width=100, height=80)
                ),
                DetectedObject(
                    label="truck",
                    confidence=0.92,
                    bounding_box=BoundingBox(x=400, y=100, width=150, height=100)
                ),
                DetectedObject(
                    label="bicycle",
                    confidence=0.87,
                    bounding_box=BoundingBox(x=250, y=300, width=60, height=100)
                ),
                DetectedObject(
                    label="person",
                    confidence=0.90,
                    bounding_box=BoundingBox(x=200, y=350, width=40, height=120)
                ),
            ]
        )

    def test_analyzer_initialization_no_llm(self):
        """Test l'initialisation de l'analyzer sans LLM"""
        self.assertFalse(self.analyzer_no_llm.use_llm)
        self.assertIsNotNone(self.analyzer_no_llm.risk_evaluator)
        self.assertIsNone(self.analyzer_no_llm.client)

    def test_analyzer_raises_error_on_llm_without_api_key(self):
        """Test que l'analyzer lève une erreur si LLM activé sans clé API"""
        # Retire la clé API s'il y en a une
        original_key = os.environ.pop("OPENAI_API_KEY", None)
        
        try:
            with self.assertRaises((ValueError, ImportError)):
                DrivingSceneAnalyzer(use_llm=True)
        finally:
            # Restaure la clé s'il y avait une
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key

    def test_analyze_empty_scene(self):
        """Test l'analyse d'une scène vide"""
        result = self.analyzer_no_llm.analyze_scene(self.empty_scene)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.risque_eval.risque_level, "FAIBLE")
        self.assertIsNotNone(result.resume)
        self.assertIsInstance(result.recommandations, list)

    def test_analyze_simple_scene(self):
        """Test l'analyse d'une scène simple"""
        result = self.analyzer_no_llm.analyze_scene(self.simple_scene)
        
        self.assertIsNotNone(result)
        self.assertIn(result.risque_eval.risque_level, ["FAIBLE", "MOYEN", "ÉLEVÉ", "CRITIQUE"])
        self.assertGreater(len(result.resume), 0)
        self.assertIsInstance(result.recommandations, list)

    def test_analyze_complex_scene(self):
        """Test l'analyse d'une scène complexe"""
        result = self.analyzer_no_llm.analyze_scene(self.complex_scene)
        
        self.assertIsNotNone(result)
        self.assertIn(result.risque_eval.risque_level, ["FAIBLE", "MOYEN", "ÉLEVÉ", "CRITIQUE"])
        self.assertGreater(len(result.resume), 0)
        self.assertIsInstance(result.recommandations, list)

    def test_analyze_scene_with_context(self):
        """Test l'analyse avec contexte additionnel"""
        result = self.analyzer_no_llm.analyze_scene(
            detections=self.simple_scene,
            scene_context="Route urbaine, heure de pointe, conditions sèches"
        )
        
        self.assertIsNotNone(result)
        self.assertGreater(len(result.resume), 0)

    def test_analyze_with_mock_llm_response(self):
        """Test l'analyse avec une réponse LLM mockée"""
        mock_response = """RÉSUMÉ: Test mock response
RISQUES: Risque 1, Risque 2
RECOMMANDATIONS: Recommandation 1, Recommandation 2"""
        
        result = self.analyzer_no_llm.analyze_scene(
            detections=self.simple_scene,
            mock_llm_response=mock_response
        )
        
        self.assertIsNotNone(result)
        self.assertIn("Test mock", result.resume)


class TestSceneAnalysisTools(unittest.TestCase):
    """Tests des outils d'analyse de scène"""

    def setUp(self):
        """Initialise les données de test"""
        self.scene = SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="car",
                    confidence=0.95,
                    bounding_box=BoundingBox(x=200, y=200, width=100, height=80)
                ),
                DetectedObject(
                    label="truck",
                    confidence=0.90,
                    bounding_box=BoundingBox(x=400, y=150, width=120, height=100)
                ),
                DetectedObject(
                    label="bicycle",
                    confidence=0.85,
                    bounding_box=BoundingBox(x=100, y=300, width=60, height=100)
                ),
            ]
        )
        
        self.empty_scene = SceneDetections(detected_objects=[])

    def test_calculate_object_density_empty(self):
        """Test le calcul de densité pour une scène vide"""
        density = SceneAnalysisTools.calculate_object_density(self.empty_scene)
        self.assertEqual(density, 0.0)

    def test_calculate_object_density_simple(self):
        """Test le calcul de densité pour une scène simple"""
        density = SceneAnalysisTools.calculate_object_density(self.scene)
        self.assertGreater(density, 0.0)

    def test_calculate_central_occupancy(self):
        """Test le calcul d'occupation centrale"""
        occupancy = SceneAnalysisTools.calculate_central_occupancy(self.scene)
        self.assertGreaterEqual(occupancy, 0)
        self.assertLessEqual(occupancy, 100)

    def test_get_object_distribution(self):
        """Test la distribution d'objets"""
        distribution = SceneAnalysisTools.get_object_distribution(self.scene)
        
        self.assertEqual(len(distribution), 3)
        self.assertIn("car", distribution)
        self.assertEqual(distribution["car"], 1)
        self.assertEqual(distribution["truck"], 1)
        self.assertEqual(distribution["bicycle"], 1)

    def test_get_average_confidence(self):
        """Test la confiance moyenne"""
        avg_conf = SceneAnalysisTools.get_average_confidence(self.scene)
        
        self.assertGreater(avg_conf, 0.8)
        self.assertLess(avg_conf, 1.0)

    def test_identify_critical_objects(self):
        """Test l'identification d'objets critiques"""
        critical = SceneAnalysisTools.identify_critical_objects(self.scene)
        
        self.assertIsInstance(critical, list)

    def test_build_scene_context(self):
        """Test la construction du contexte de scène"""
        context = SceneAnalysisTools.build_scene_context(self.scene)
        
        self.assertIsInstance(context, str)
        self.assertGreater(len(context), 0)
        self.assertIn("3 objets", context)

    def test_get_risk_factors_summary(self):
        """Test le résumé des facteurs de risque"""
        summary = SceneAnalysisTools.get_risk_factors_summary(self.scene)
        
        self.assertIsInstance(summary, dict)
        self.assertIn("total_objects", summary)
        self.assertEqual(summary["total_objects"], 3)


class TestRiskEvaluator(unittest.TestCase):
    """Tests de l'évaluateur de risque"""

    def setUp(self):
        """Initialise les données de test"""
        self.evaluator = RiskEvaluator()

    def test_evaluate_empty_scene(self):
        """Test l'évaluation d'une scène vide"""
        empty_scene = SceneDetections(detected_objects=[])
        risk_score = self.evaluator.evaluate_detections(empty_scene)
        
        self.assertEqual(risk_score.level, RiskLevel.FAIBLE)
        self.assertEqual(risk_score.score, 0)
        self.assertEqual(len(risk_score.detected_hazards), 0)

    def test_evaluate_simple_scene(self):
        """Test l'évaluation d'une scène simple"""
        simple_scene = SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="car",
                    confidence=0.95,
                    bounding_box=BoundingBox(x=200, y=200, width=100, height=80)
                )
            ]
        )
        risk_score = self.evaluator.evaluate_detections(simple_scene)
        
        self.assertIn(risk_score.level, [RiskLevel.FAIBLE, RiskLevel.MOYEN])
        self.assertGreater(risk_score.score, 0)

    def test_risk_recommendations(self):
        """Test la génération de recommandations"""
        simple_scene = SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="person",
                    confidence=0.95,
                    bounding_box=BoundingBox(x=200, y=200, width=50, height=120)
                )
            ]
        )
        risk_score = self.evaluator.evaluate_detections(simple_scene)
        recommendations = self.evaluator.generate_risk_recommendations(risk_score)
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)


class TestIntegration(unittest.TestCase):
    """Tests d'intégration complets"""

    def test_full_pipeline_no_llm(self):
        """Test le pipeline complet sans LLM"""
        analyzer = DrivingSceneAnalyzer(use_llm=False)
        
        scene = SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="car",
                    confidence=0.95,
                    bounding_box=BoundingBox(x=150, y=200, width=100, height=80)
                ),
                DetectedObject(
                    label="person",
                    confidence=0.88,
                    bounding_box=BoundingBox(x=320, y=250, width=50, height=120)
                ),
            ]
        )
        
        # Analyse
        result = analyzer.analyze_scene(scene)
        
        # Vérifications
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.resume)
        self.assertIsNotNone(result.risque_eval)
        self.assertIsInstance(result.recommandations, list)

    def test_pipeline_with_pipeline_output(self):
        """Test le pipeline complet avec PipelineOutput"""
        analyzer = DrivingSceneAnalyzer(use_llm=False)
        
        scene = SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="car",
                    confidence=0.95,
                    bounding_box=BoundingBox(x=150, y=200, width=100, height=80)
                )
            ]
        )
        
        # Analyse avec pipeline output
        pipeline_output = analyzer.analyze_with_pipeline_output(scene)
        
        # Vérifications
        self.assertIsNotNone(pipeline_output)
        self.assertIsNotNone(pipeline_output.scene_detections)
        self.assertIsNotNone(pipeline_output.analyse_resultat)


if __name__ == "__main__":
    print("=" * 60)
    print("Tests LLM Agent Integration")
    print("=" * 60)
    unittest.main(verbosity=2)
