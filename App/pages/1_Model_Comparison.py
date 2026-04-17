import sys
from pathlib import Path

# Les pages Streamlit sont exécutées comme des scripts séparés.
# On ajoute explicitement la racine du projet pour rendre `import App` fiable.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from App.ui.model_comparison_page import render_model_comparison_page


render_model_comparison_page()
