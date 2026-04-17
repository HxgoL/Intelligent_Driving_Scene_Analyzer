"""
Repository statique des modeles candidats.
"""

from pipeline.model_catalog_schema import CandidateModel


def get_candidate_models() -> list[CandidateModel]:
    return [
        CandidateModel(
            name="YOLOv8n",
            family="YOLOv8",
            approximate_size="Tres petit",
            relative_speed="Tres rapide",
            expected_accuracy="Correcte a moderee",
            use_cases=[
                "Prototype temps reel",
                "Machines peu puissantes",
                "Iteration rapide",
            ],
            strengths=[
                "Tres faible cout de calcul",
                "Inference rapide",
                "Facile a deployer",
            ],
            limitations=[
                "Moins precis sur scenes chargees",
                "Peut manquer de robustesse sur petits objets",
            ],
            used_in_pipeline=False,
            notes="Bon candidat pour les tests rapides et les machines contraintes.",
        ),
        CandidateModel(
            name="YOLOv8s",
            family="YOLOv8",
            approximate_size="Petit",
            relative_speed="Rapide",
            expected_accuracy="Bonne",
            use_cases=[
                "Inference temps reel equilibree",
                "Projet principal de detection",
                "Bon compromis precision/vitesse",
            ],
            strengths=[
                "Compromis solide entre vitesse et precision",
                "Plus robuste que YOLOv8n",
                "Adapté a un pipeline applicatif",
            ],
            limitations=[
                "Plus lourd que YOLOv8n",
                "Peut rester insuffisant face a des modeles plus grands sur scenes complexes",
            ],
            used_in_pipeline=True,
            notes="Modele actuellement le plus coherent pour le pipeline du projet.",
        ),
        CandidateModel(
            name="Modele futur",
            family="A definir",
            approximate_size="A renseigner",
            relative_speed="A renseigner",
            expected_accuracy="A renseigner",
            use_cases=[
                "Comparaison future",
                "Scenario a definir",
            ],
            strengths=[
                "Emplacement reserve pour un futur modele",
            ],
            limitations=[
                "Caracteristiques non encore evaluees",
            ],
            used_in_pipeline=False,
            notes="Peut etre remplace plus tard par YOLOv8m, RT-DETR ou un modele custom.",
        ),
    ]
