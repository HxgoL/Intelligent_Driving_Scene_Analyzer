"""
conftest.py - Configuration de pytest pour les tests du LLM agent
Définit les fixtures communes de pytest
"""
import pytest
from llm_agent.simulated_scenes import SimulatedDrivingScenes
from llm_agent.agent import DrivingSceneAnalyzer


@pytest.fixture
def simulated_scenes():
    """Fixture : toutes les scènes simulées"""
    return SimulatedDrivingScenes.all_scenes()


@pytest.fixture
def analyzer_no_llm():
    """Fixture : analyzer sans LLM"""
    return DrivingSceneAnalyzer(use_llm=False)


@pytest.fixture
def clear_road_scene():
    """Fixture : scène route dégagée"""
    return SimulatedDrivingScenes.clear_road()


@pytest.fixture
def pedestrian_crossing_scene():
    """Fixture : scène traversée piétons"""
    return SimulatedDrivingScenes.pedestrian_crossing()


@pytest.fixture
def heavy_traffic_scene():
    """Fixture : scène circulation dense"""
    return SimulatedDrivingScenes.heavy_traffic()


@pytest.fixture
def school_zone_scene():
    """Fixture : scène zone scolaire"""
    return SimulatedDrivingScenes.school_zone()


def pytest_configure(config):
    """Configuration de pytest"""
    config.addinivalue_line(
        "markers", "slow: marque les tests qui font des appels API réels"
    )
