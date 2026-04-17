"""
Composants du rapport textuel.
"""

import streamlit as st

from pipeline.schema import PipelineOutput


def render_report(result: PipelineOutput) -> None:
    risk_level = result.analyse_resultat.risque_eval.risque_level
    summary = result.analyse_resultat.resume
    recommendations = result.analyse_resultat.recommandations

    st.markdown("### Rapport d'analyse")
    st.markdown(
        f"""
        <div class="report-card">
            <div class="report-card__header">
                <span class="report-card__eyebrow">Analyse de scene</span>
                <span class="risk-badge">{risk_level}</span>
            </div>
            <p class="report-card__summary">{summary}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Recommandations")
    for recommendation in recommendations:
        st.markdown(
            f"""
            <div class="recommendation-item">
                <span class="recommendation-bullet">-</span>
                <span>{recommendation}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
