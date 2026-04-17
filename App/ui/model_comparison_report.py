"""
Composants d'affichage pour la comparaison pedagogique des modeles.
"""

import streamlit as st

from pipeline.model_catalog_schema import CandidateModel


def _build_table_rows(models: list[CandidateModel]) -> list[dict]:
    rows = []
    for model in models:
        rows.append(
            {
                "Modele": model.name,
                "Famille": model.family,
                "Taille approx.": model.approximate_size,
                "Vitesse relative": model.relative_speed,
                "Precision attendue": model.expected_accuracy,
                "Dans le pipeline": "Oui" if model.used_in_pipeline else "Non",
            }
        )
    return rows


def _render_model_card(model: CandidateModel) -> None:
    with st.container(border=True):
        st.markdown(f"### {model.name}")
        st.caption(f"{model.family} | {model.notes}")

        metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
        with metric_col_1:
            st.metric("Taille", model.approximate_size)
        with metric_col_2:
            st.metric("Vitesse", model.relative_speed)
        with metric_col_3:
            st.metric("Precision", model.expected_accuracy)

        st.markdown("**Cas d'usage**")
        for use_case in model.use_cases:
            st.markdown(f"- {use_case}")

        st.markdown("**Avantages**")
        for strength in model.strengths:
            st.markdown(f"- {strength}")

        st.markdown("**Limites**")
        for limitation in model.limitations:
            st.markdown(f"- {limitation}")

        pipeline_label = "Oui" if model.used_in_pipeline else "Non"
        st.markdown(f"**Utilise dans le pipeline actuel :** {pipeline_label}")


def render_model_comparison_report(models: list[CandidateModel]) -> None:
    st.title("Comparaison des modeles candidats")
    st.markdown(
        "Cette page presente une comparaison pedagogique et descriptive des modeles "
        "candidats, sans dependre d'un dataset d'evaluation."
    )

    if not models:
        st.info("Aucun modele candidat disponible.")
        return

    used_in_pipeline = sum(1 for model in models if model.used_in_pipeline)
    st.markdown("## Vue d'ensemble")
    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
    with metric_col_1:
        st.metric("Modeles presentes", len(models))
    with metric_col_2:
        st.metric("Modeles dans le pipeline", used_in_pipeline)
    with metric_col_3:
        st.metric("Modeles hors pipeline", len(models) - used_in_pipeline)

    st.markdown("## Tableau comparatif")
    st.dataframe(_build_table_rows(models), use_container_width=True)

    st.markdown("## Fiches descriptives")
    for model in models:
        _render_model_card(model)
