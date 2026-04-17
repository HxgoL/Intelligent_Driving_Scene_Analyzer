"""
Service applicatif pour la comparaison des modeles candidats.
"""

from App.repositories.model_catalog_repository import get_candidate_models
from pipeline.model_catalog_schema import CandidateModel


def list_candidate_models() -> list[CandidateModel]:
    return get_candidate_models()


def get_models_used_in_pipeline(models: list[CandidateModel]) -> list[CandidateModel]:
    return [model for model in models if model.used_in_pipeline]
