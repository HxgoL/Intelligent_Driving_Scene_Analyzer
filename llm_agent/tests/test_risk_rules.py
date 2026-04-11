"""
test_risk_rules.py - Tests du RiskEvaluator
Teste l'évaluation des risques basée sur les objets détectés
"""
import pytest
from llm_agent.risk_rules import RiskEvaluator, RiskLevel
from llm_agent.simulated_scenes import SimulatedDrivingScenes
from pipeline.schema import SceneDetections, DetectedObject, BoundingBox


class TestRiskEvaluatorHazardFactors:
    """Tests des facteurs de risque des objets"""
    
    def test_car_hazard_factor(self):
        """Tester le facteur de risque d'une voiture"""
        factor = RiskEvaluator.get_hazard_factor("car")
        assert factor > 0
    
    def test_person_hazard_factor(self):
        """Tester le facteur de risque d'une personne"""
        factor = RiskEvaluator.get_hazard_factor("person")
        assert factor > 0
    
    def test_traffic_light_no_hazard(self):
        """Tester que les feux tricolores ne sont pas des risques"""
        factor = RiskEvaluator.get_hazard_factor("traffic light")
        assert factor == 0
    
    def test_unknown_object_default_factor(self):
        """Tester le facteur par défaut pour objets inconnus"""
        factor = RiskEvaluator.get_hazard_factor("unknown_object_xyz")
        assert factor >= 0


class TestRiskEvaluatorWeights:
    """Tests des pondérations de risque"""
    
    def test_confidence_weight(self):
        """Tester la pondération selon la confiance"""
        weight_high = RiskEvaluator.calculate_confidence_weight(0.99)
        weight_low = RiskEvaluator.calculate_confidence_weight(0.3)
        
        assert weight_high > weight_low
        assert weight_high >= 0.5
        assert weight_high <= 1.0
    
    def test_proximity_weight_close(self):
        """Tester la pondération pour proximité proche"""
        # Zone proche du centre
        weight = RiskEvaluator.calculate_proximity_weight(320, 336)
        assert weight >= 1.0
    
    def test_proximity_weight_far(self):
        """Tester la pondération pour proximité lointaine"""
        # Zone lointaine (coins de l'image)
        weight = RiskEvaluator.calculate_proximity_weight(50, 50)
        assert weight >= 1.0


class TestRiskEvaluatorDetectionEvaluation:
    """Tests d'évaluation de détections"""
    
    def test_evaluate_empty_scene(self):
        """Tester l'évaluation d'une scène vide"""
        scene = SimulatedDrivingScenes.clear_road()
        risk_score = RiskEvaluator.evaluate_detections(scene)
        
        assert risk_score is not None
        assert risk_score.level == RiskLevel.FAIBLE
        assert risk_score.score == 0
        assert len(risk_score.detected_hazards) == 0
    
    def test_evaluate_pedestrian_scene(self):
        """Tester l'évaluation d'une scène avec piétons"""
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        risk_score = RiskEvaluator.evaluate_detections(scene)
        
        assert risk_score is not None
        assert risk_score.level in [RiskLevel.MOYEN, RiskLevel.ÉLEVÉ, RiskLevel.CRITIQUE]
        assert len(risk_score.detected_hazards) > 0
    
    def test_evaluate_heavy_traffic(self):
        """Tester l'évaluation d'une circulation dense"""
        scene = SimulatedDrivingScenes.heavy_traffic()
        risk_score = RiskEvaluator.evaluate_detections(scene)
        
        assert risk_score is not None
        assert risk_score.score >= 0
        assert len(risk_score.detected_hazards) > 0
    
    def test_evaluate_school_zone_high_risk(self):
        """Tester que une zone scolaire est à risque élevé"""
        scene = SimulatedDrivingScenes.school_zone()
        risk_score = RiskEvaluator.evaluate_detections(scene)
        
        assert risk_score is not None
        assert risk_score.level in [RiskLevel.ÉLEVÉ, RiskLevel.CRITIQUE]


class TestRiskEvaluatorRecommendations:
    """Tests des recommandations générées"""
    
    def test_recommendations_for_low_risk(self):
        """Tester les recommandations pour risque faible"""
        from llm_agent.risk_rules import RiskScore
        
        risk_score = RiskScore(
            level=RiskLevel.FAIBLE,
            score=0,
            detected_hazards=[],
            primary_risks=[]
        )
        
        recs = RiskEvaluator.generate_risk_recommendations(risk_score)
        assert len(recs) > 0
    
    def test_recommendations_for_critical_risk(self):
        """Tester les recommandations pour risque critique"""
        from llm_agent.risk_rules import RiskScore
        
        risk_score = RiskScore(
            level=RiskLevel.CRITIQUE,
            score=80,
            detected_hazards=["person"],
            primary_risks=["personne proche"]
        )
        
        recs = RiskEvaluator.generate_risk_recommendations(risk_score)
        assert len(recs) >= 3  # Au moins 3 recommandations
        assert any("critique" in rec.lower() for rec in recs)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
