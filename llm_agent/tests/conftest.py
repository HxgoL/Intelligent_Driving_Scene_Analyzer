"""
conftest.py - Configuration de pytest pour les tests du LLM agent
Définit les fixtures communes de pytest
"""
import os
import pytest

# NOTE: We don't load .env here! This allows CI/CD to override environment.
# Only load .env if explicitly requested by tests or in specific contexts.
from dotenv import load_dotenv

from llm_agent.simulated_scenes import SimulatedDrivingScenes
from llm_agent.agent import DrivingSceneAnalyzer

# Vérifie la disponibilité de la clé API (ne pas charger .env ici!)
HAS_API_KEY = bool(os.getenv("OPEN_API_KEY") or os.getenv("OPENAI_API_KEY"))


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
        "markers", "api: test qui nécessite une clé API OpenAI"
    )
    config.addinivalue_line(
        "markers", "slow: marque les tests qui font des appels API réels"
    )


def pytest_collection_modifyitems(config, items):
    """Skip les tests marqués 'api' s'il n'y a pas de clé API"""
    # Re-check for API key at collection time
    has_key = bool(os.getenv("OPEN_API_KEY") or os.getenv("OPENAI_API_KEY"))
    
    if not has_key:
        skip_api = pytest.mark.skip(reason="API key not configured")
        for item in items:
            # Check all markers on the item
            if item.get_closest_marker("api"):
                item.add_marker(skip_api)
