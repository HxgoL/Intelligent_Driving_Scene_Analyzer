"""
Schemas pour la comparaison pedagogique des modeles candidats.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateModel:
    name: str
    family: str
    approximate_size: str
    relative_speed: str
    expected_accuracy: str
    use_cases: list[str]
    strengths: list[str]
    limitations: list[str]
    used_in_pipeline: bool
    notes: str = ""
