"""
test_agent.py - Tests du DrivingSceneAnalyzer
Teste l'orchestration principal de l'analyse de scènes
"""
import pytest
from llm_agent.agent import DrivingSceneAnalyzer
from llm_agent.simulated_scenes import SimulatedDrivingScenes
from pipeline.schema import SceneDetections, DetectedObject, BoundingBox


class TestDrivingSceneAnalyzerInitialization:
    """Tests d'initialisation du DrivingSceneAnalyzer"""
    
    def test_initialization_without_llm(self):
        """Tester l'initialisation sans LLM"""
        analyzer = DrivingSceneAnalyzer(use_llm=False)
        
        assert analyzer is not None
        assert analyzer.use_llm is False
        assert analyzer.client is None
        assert analyzer.risk_evaluator is not None
    
    def test_initialization_with_invalid_api_key(self):
        """Tester que l'init échoue avec une clé API invalide"""
        with pytest.raises(ValueError):
            DrivingSceneAnalyzer(use_llm=True, api_key="invalid_key")
    
    def test_initialization_with_valid_api_key(self):
        """Tester l'init avec une clé API valide"""
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("OPEN_API_KEY")
        
        if api_key:
            analyzer = DrivingSceneAnalyzer(use_llm=True, api_key=api_key)
            assert analyzer.use_llm is True
            assert analyzer.client is not None


class TestDrivingSceneAnalyzerAnalysis:
    """Tests d'analyse de scènes"""
    
    @pytest.fixture
    def analyzer_no_llm(self):
        """Fixture : analyzer sans LLM"""
        return DrivingSceneAnalyzer(use_llm=False)
    
    def test_analysis_empty_scene(self, analyzer_no_llm):
        """Tester l'analyse d'une route dégagée"""
        scene = SimulatedDrivingScenes.clear_road()
        result = analyzer_no_llm.analyze_scene(detections=scene)
        
        assert result is not None
        assert result.resume is not None
        assert result.risque_eval is not None
        assert result.recommandations is not None
    
    def test_analysis_with_objects(self, analyzer_no_llm):
        """Tester l'analyse d'une scène avec objets"""
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        result = analyzer_no_llm.analyze_scene(detections=scene)
        
        assert result is not None
        assert len(scene.detected_objects) > 0
        assert result.risque_eval.risque_level in ["FAIBLE", "MOYEN", "ÉLEVÉ", "CRITIQUE"]
    
    def test_analysis_school_zone_critical(self, analyzer_no_llm):
        """Tester que zone scolaire retourne un risque élevé"""
        scene = SimulatedDrivingScenes.school_zone()
        result = analyzer_no_llm.analyze_scene(detections=scene)
        
        # Zone scolaire doit avoir un risque élevé ou critique
        assert result.risque_eval.risque_level in ["ÉLEVÉ", "CRITIQUE"]
    
    def test_analysis_returns_recommendations(self, analyzer_no_llm):
        """Vérifier que l'analyse retourne des recommandations"""
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        result = analyzer_no_llm.analyze_scene(detections=scene)
        
        assert result.recommandations is not None
        assert len(result.recommandations) >= 0
    
    @pytest.mark.slow
    def test_analysis_with_llm(self):
        """Test d'analyse avec LLM réel"""
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("OPEN_API_KEY")
        
        if api_key:
            analyzer = DrivingSceneAnalyzer(use_llm=True, api_key=api_key)
            scene = SimulatedDrivingScenes.pedestrian_crossing()
            result = analyzer.analyze_scene(detections=scene)
            
            assert result is not None
            assert result.resume is not None
            assert result.risque_eval.risque_level in ["FAIBLE", "MOYEN", "ÉLEVÉ", "CRITIQUE"]


class TestDrivingSceneAnalyzerWithCustomScenes:
    """Tests avec des scènes personnalisées"""
    
    def test_custom_scene(self):
        """Tester une scène personnalisée"""
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
        
        result = analyzer.analyze_scene(detections=scene)
        
        assert result is not None
        assert result.risque_eval.risque_level is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
