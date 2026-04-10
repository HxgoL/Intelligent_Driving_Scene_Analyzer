"""
test_tools.py - Tests des outils d'analyse de scène
Teste les fonctions utilitaires de calcul d'analyse
"""
import pytest
from llm_agent.tools import SceneAnalysisTools
from llm_agent.simulated_scenes import SimulatedDrivingScenes


class TestSceneAnalysisToolsDensity:
    """Tests du calcul de densité d'objets"""
    
    def test_density_empty_scene(self):
        """Tester la densité d'une scène vide"""
        scene = SimulatedDrivingScenes.clear_road()
        density = SceneAnalysisTools.calculate_object_density(scene)
        
        assert density == 0.0
    
    def test_density_with_objects(self):
        """Tester la densité avec objets"""
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        density = SceneAnalysisTools.calculate_object_density(scene)
        
        assert density > 0


class TestSceneAnalysisToolsOccupancy:
    """Tests du calcul d'occupation de zone centrale"""
    
    def test_occupancy_empty_scene(self):
        """Tester l'occupation d'une scène vide"""
        scene = SimulatedDrivingScenes.clear_road()
        occupancy = SceneAnalysisTools.calculate_central_occupancy(scene)
        
        assert occupancy == 0.0
    
    def test_occupancy_with_objects(self):
        """Tester l'occupation avec objets"""
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        occupancy = SceneAnalysisTools.calculate_central_occupancy(scene)
        
        assert occupancy >= 0


class TestSceneAnalysisToolsDistribution:
    """Tests du calcul de distribution d'objets"""
    
    def test_distribution_empty_scene(self):
        """Tester la distribution d'une scène vide"""
        scene = SimulatedDrivingScenes.clear_road()
        dist = SceneAnalysisTools.get_object_distribution(scene)
        
        assert len(dist) == 0
    
    def test_distribution_with_objects(self):
        """Tester la distribution avec objets"""
        scene = SimulatedDrivingScenes.heavy_traffic()
        dist = SceneAnalysisTools.get_object_distribution(scene)
        
        assert len(dist) > 0
        assert sum(dist.values()) == len(scene.detected_objects)
    
    def test_distribution_sorted(self):
        """Tester que la distribution est triée"""
        scene = SimulatedDrivingScenes.heavy_traffic()
        dist = SceneAnalysisTools.get_object_distribution(scene)
        
        # Vérifier que c'est trié par count décroissant
        counts = list(dist.values())
        assert counts == sorted(counts, reverse=True)


class TestSceneAnalysisToolsConfidence:
    """Tests du calcul de confiance moyenne"""
    
    def test_average_confidence_empty_scene(self):
        """Tester la confiance d'une scène vide"""
        scene = SimulatedDrivingScenes.clear_road()
        conf = SceneAnalysisTools.get_average_confidence(scene)
        
        assert conf == 0.0
    
    def test_average_confidence_with_objects(self):
        """Tester la confiance avec objets"""
        scene = SimulatedDrivingScenes.pedestrian_crossing()
        conf = SceneAnalysisTools.get_average_confidence(scene)
        
        assert conf > 0
        assert conf <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
