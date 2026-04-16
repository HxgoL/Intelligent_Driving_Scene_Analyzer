"""
Definit le style general pour les composants Streamlit.
"""

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 2.2rem;
            max-width: 1450px;
        }

        h1, h2, h3 {
            color: #1f4e79;
        }

        [data-testid="stImage"] img {
            border-radius: 14px;
            width: 100%;
            height: auto;
            object-fit: contain;
            border: 1px solid rgba(31, 78, 121, 0.12);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        }

        .report-card {
            padding: 1.2rem 1.25rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #f6fbff 0%, #eef6ff 100%);
            border: 1px solid rgba(31, 78, 121, 0.12);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
        }

        .report-card__header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.75rem;
        }

        .report-card__eyebrow {
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #4b5563;
        }

        .report-card__summary {
            margin: 0;
            color: #0f172a;
            font-size: 1rem;
            line-height: 1.65;
        }

        .risk-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            background: #1f4e79;
            color: white;
            font-size: 0.9rem;
            font-weight: 700;
            white-space: nowrap;
        }

        .recommendation-item {
            display: flex;
            align-items: flex-start;
            gap: 0.65rem;
            padding: 0.65rem 0.8rem;
            margin-bottom: 0.55rem;
            border-radius: 12px;
            background: #fafcff;
            border: 1px solid rgba(31, 78, 121, 0.1);
        }

        .recommendation-bullet {
            color: #1f4e79;
            font-weight: 700;
        }

        .dashboard-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.7rem 0.85rem;
            margin-bottom: 0.45rem;
            border-radius: 12px;
            background: #ffffff;
            border: 1px solid rgba(15, 23, 42, 0.08);
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 16px;
            padding: 0.6rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
