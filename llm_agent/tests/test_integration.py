"""
test_integration.py - Tests d'intégration complets
Teste le pipeline complète d'analyses de scènes
"""
import pytest
from llm_agent.agent import DrivingSceneAnalyzer
from llm_agent.simulated_scenes import SimulatedDrivingScenes
import os
from dotenv import load_dotenv


class TestIntegrationPipelineWithoutLLM:
    """Tests du pipeline complet sans LLM"""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture : analyzer sans LLM"""
        return DrivingSceneAnalyzer(use_llm=False)
    
    def test_pipeline_empty_scene(self, analyzer):
        """Test pipeline avec route dégagée"""
        scene = SimulatedDrivingScenes.clear_road()
        result = analyzer.analyze_scene(detections=scene)
        
        assert result is not None
        assert result.resume is not None
        assert result.risque_eval is not None
        assert len(result.recommandations) >= 0
    
    def test_pipeline_pedestrian_crossing(self, analyzer):
        """Test pipeline avec traversée piétons"""
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        result = analyzer.analyze_scene(detections=scene)
        
        assert result is not None
        assert result.risque_eval.risque_level in ["FAIBLE", "MOYEN", "ÉLEVÉ", "CRITIQUE"]
        assert len(result.recommandations) >= 0
    
    def test_pipeline_heavy_traffic(self, analyzer):
        """Test pipeline avec circulation dense"""
        scene = SimulatedDrivingScenes.heavy_traffic()
        result = analyzer.analyze_scene(detections=scene)
        
        assert result is not None
        assert result.resume is not None
    
    def test_pipeline_school_zone(self, analyzer):
        """Test pipeline avec zone scolaire"""
        scene = SimulatedDrivingScenes.school_zone()
        result = analyzer.analyze_scene(detections=scene)
        
        assert result is not None
        # Zone scolaire doit être à risque élevé
        assert result.risque_eval.risque_level in ["ÉLEVÉ", "CRITIQUE"]


class TestIntegrationPipelineWithContext:
    """Tests du pipeline avec contexte additionnel"""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture : analyzer sans LLM"""
        return DrivingSceneAnalyzer(use_llm=False)
    
    def test_analysis_with_context_night(self, analyzer):
        """Test analyse avec contexte : nuit"""
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        result = analyzer.analyze_scene(
            detections=scene,
            scene_context="Route la nuit, visibilité réduite"
        )
        
        assert result is not None
    
    def test_analysis_with_context_rain(self, analyzer):
        """Test analyse avec contexte : pluie"""
        scene = SimulatedDrivingScenes.heavy_traffic()
        result = analyzer.analyze_scene(
            detections=scene,
            scene_context="Pluie forte, chaussée mouillée"
        )
        
        assert result is not None
    
    def test_analysis_with_context_construction(self, analyzer):
        """Test analyse avec contexte : zone de construction"""
        scene = SimulatedDrivingScenes.heavy_traffic()
        result = analyzer.analyze_scene(
            detections=scene,
            scene_context="Zone de construction, travaux en cours"
        )
        
        assert result is not None


class TestIntegrationAllScenes:
    """Tests complets avec toutes les scènes"""
    
    def test_all_scenes_analysis(self):
        """Test d'analyse de toutes les scènes"""
        analyzer = DrivingSceneAnalyzer(use_llm=False)
        scenes = SimulatedDrivingScenes.all_scenes()
        
        results = {}
        for scene_name, scene in scenes.items():
            result = analyzer.analyze_scene(detections=scene)
            results[scene_name] = result
            
            assert result is not None
            assert result.resume is not None
            assert result.risque_eval.risque_level is not None
        
        # Vérifier qu'on a les résultats pour toutes les scènes
        assert len(results) == len(scenes)
    
    def test_all_scenes_have_valid_risk_levels(self):
        """Tester que toutes les analyses retournent un niveau de risque valide"""
        analyzer = DrivingSceneAnalyzer(use_llm=False)
        scenes = SimulatedDrivingScenes.all_scenes()
        valid_levels = ["FAIBLE", "MOYEN", "ÉLEVÉ", "CRITIQUE"]
        
        for scene_name, scene in scenes.items():
            result = analyzer.analyze_scene(detections=scene)
            assert result.risque_eval.risque_level in valid_levels


@pytest.mark.slow
class TestIntegrationWithLLM:
    """Tests du pipeline avec LLM réel"""
    
    @pytest.fixture
    def has_api_key(self):
        """Fixture : vérifier qu'on a une clé API"""
        load_dotenv()
        return os.getenv("OPEN_API_KEY") is not None
    
    @pytest.mark.api
    def test_llm_pipeline_pedestrian(self, has_api_key):
        """Test pipeline LLM avec piétons"""
        api_key = os.getenv("OPEN_API_KEY")
        if not api_key:
            pytest.skip("API key not configured")
        
        analyzer = DrivingSceneAnalyzer(use_llm=True, api_key=api_key)
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        result = analyzer.analyze_scene(detections=scene)
        
        assert result is not None
        assert result.resume is not None
    
    @pytest.mark.api
    def test_llm_pipeline_all_scenes(self, has_api_key):
        """Test pipeline LLM avec toutes les scènes"""
        api_key = os.getenv("OPEN_API_KEY")
        if not api_key:
            pytest.skip("API key not configured")
        
        analyzer = DrivingSceneAnalyzer(use_llm=True, api_key=api_key)
        scenes = SimulatedDrivingScenes.all_scenes()
        
        for scene_name, scene in scenes.items():
            result = analyzer.analyze_scene(detections=scene)
            assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
