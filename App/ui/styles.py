"""
Definit le style general pour les composants Streamlit.
"""

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --app-accent: #1f4e79;
            --app-accent-soft: rgba(31, 78, 121, 0.12);
            --app-border: rgba(128, 128, 128, 0.22);
            --app-surface: color-mix(in srgb, var(--secondary-background-color) 82%, transparent);
            --app-surface-strong: color-mix(in srgb, var(--background-color) 76%, var(--app-accent) 24%);
        }

        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 2.2rem;
            max-width: 1450px;
        }

        h1, h2, h3 {
            color: var(--text-color);
        }

        [data-testid="stImage"] img {
            display: block;
            max-width: 100%;
            border-radius: 14px;
            border: 1px solid var(--app-accent-soft);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        }

        .report-card {
            padding: 1.5rem 1.6rem;
            border-radius: 18px;
            background: var(--app-surface-strong);
            border: 1px solid var(--app-accent-soft);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
            color: var(--text-color);
            min-height: 220px;
        }

        .report-card__header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .report-card__eyebrow {
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-color);
            opacity: 0.75;
        }

        .report-card__summary {
            margin: 0;
            color: var(--text-color);
            font-size: 1.08rem;
            line-height: 1.9;
            white-space: pre-wrap;
        }

        .risk-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            background: var(--app-accent);
            color: #ffffff;
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
            background: var(--app-surface);
            border: 1px solid var(--app-accent-soft);
            color: var(--text-color);
        }

        .recommendation-bullet {
            color: var(--app-accent);
            font-weight: 700;
        }

        .dashboard-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.7rem 0.85rem;
            margin-bottom: 0.45rem;
            border-radius: 12px;
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            color: var(--text-color);
        }

        [data-testid="stMetric"] {
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: 16px;
            padding: 0.6rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stCaptionContainer"] {
            color: var(--text-color);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
