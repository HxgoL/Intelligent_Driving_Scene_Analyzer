# 📦 LLM Agent Module

Module d'analyse de scènes routières avec intelligence artificielle. Détecte les risques et génère des recommandations pour le conducteur.

## 📂 Structure du projet

```
llm_agent/
│
├── 🤖 MODULES CORE (API d'utilisation)
├── __init__.py
├── agent.py                      # DrivingSceneAnalyzer - Point d'entrée principal
├── risk_rules.py                 # RiskEvaluator - Scoring et évaluation des risques
├── prompt_builder.py             # PromptBuilder - Construction des prompts pour LLM
├── formatter.py                  # ResponseFormatter - Parsing des réponses LLM
├── tools.py                      # SceneAnalysisTools - Utilitaires d'analyse
├── simulated_scenes.py           # 4 scènes de test (clear_road, pedestrian, traffic, school)
│
├── 📚 DOCUMENTATION
├── README.md                     # Ce fichier
├── README_LLM.md                 # Documentation originale du module
├── STRUCTURE_ORGANISATION.md     # Détails de l'organisation
│
├── 📖 docs/
│   └── GUIDE_INSTALLATION_OPENAI.md  # Guide complet : créer compte → configurer API → tester
│
├── 💡 examples/
│   ├── test_api_quick.py         # Test rapide de la connexion OpenAI
│   └── test_all_scenes.py        # Analyse les 4 scènes simulées
│
├── 🔧 scripts/
│   ├── interactive_tester.py     # Menu interactif pour tester chaque scène
│   ├── batch_analyzer.py         # Analyse automatique avec JSON output
│   └── README.md                 # Guide d'utilisation des scripts
│
└── ✅ tests/                     # Suite complète de tests (85+ tests)
    ├── 📋 TESTS UNITAIRES
    ├── test_agent.py             # Tests DrivingSceneAnalyzer (9 tests)
    ├── test_formatter.py         # Tests ResponseFormatter (10 tests)
    ├── test_risk_rules.py        # Tests RiskEvaluator (11 tests)
    ├── test_tools.py             # Tests SceneAnalysisTools (7 tests)
    │
    ├── 🔗 TESTS API
    ├── test_api_openai.py        # Tests connexion OpenAI (4 tests)
    │
    ├── 🧪 TESTS DÉMONSTRATION
    ├── test_agent_mock.py        # Tests avec données mockées (6 tests)
    ├── test_llm_integration.py   # Tests d'intégration complets (20 tests)
    ├── test_integration.py       # Tests du pipeline (11 tests)
    ├── test_demo.py              # Démonstration interactive (7 tests/démos)
    │
    ├── 🔧 CONFIG
    ├── conftest.py               # Configuration pytest et fixtures
    └── README.md                 # Guide complet des tests
```

## 🚀 Démarrage rapide

### 1️⃣ Installation des dépendances

```bash
# Installer OpenAI
pip install "openai>=1.52.0"

# Ou tous les requirements du projet
pip install -r requirements.txt
```

### 2️⃣ Configuration de l'API

Créer un fichier `.env` à la racine du projet :
```bash
OPEN_API_KEY=sk_proj_xxxxxxxxxxxxx
```

📖 [Voir le guide complet d'installation OpenAI](./docs/GUIDE_INSTALLATION_OPENAI.md)

### 3️⃣ Test rapide

```bash
# Test de connexion API
python llm_agent/examples/test_api_quick.py

# Analyse des 4 scènes simulées
python llm_agent/examples/test_all_scenes.py

# Menu interactif
python llm_agent/scripts/interactive_tester.py
```

### 4️⃣ Lancer la suite de tests

```bash
# Tous les tests
pytest llm_agent/tests/ -v

# Un fichier spécifique
pytest llm_agent/tests/test_agent.py -v

# Tests rapides seulement (exclut les tests API lents)
pytest llm_agent/tests/ -v -m "not slow"
```

## � Modules Core

### 🎯 agent.py - DrivingSceneAnalyzer
Point d'entrée principal du module. Orchestre l'analyse complète.

```python
from llm_agent.agent import DrivingSceneAnalyzer

# Sans LLM (rapide, basé sur les règles)
analyzer = DrivingSceneAnalyzer(use_llm=False)

# Avec LLM (nécessite API key)
analyzer = DrivingSceneAnalyzer(use_llm=True)

# Analyser une scène
result = analyzer.analyze_scene(
    detections=scene,
    scene_context="Route urbaine, jour clair"
)

print(f"Risque: {result.risque_eval.risque_level}")
print(f"Résumé: {result.resume}")
print(f"Recommandations: {result.recommandations}")
```

### ⚠️ risk_rules.py - RiskEvaluator
Évalue les risques en fonction des objets détectés.

- **Objets critiques** : piéton, obstacle, collision potentielle
- **Scoring** : zone proximale, confiance, distribution
- **Niveaux** : FAIBLE, MOYEN, ÉLEVÉ, CRITIQUE

### 🎯 prompt_builder.py - PromptBuilder
Construit les prompts JSON pour le LLM.

- Structure standardisée avec contexte
- Inclusion des détections d'objets
- Scoring de risque pré-calculé

### 📝 formatter.py - ResponseFormatter
Parse les réponses du LLM en objets Python.

- Extraction RÉSUMÉ, RISQUES, RECOMMANDATIONS
- Inférence du niveau de risque
- Gestion des réponses malformées

### 🛠️ tools.py - SceneAnalysisTools
Utilitaires pour analyser les scènes.

```python
from llm_agent.tools import SceneAnalysisTools

# Densité d'objets
density = SceneAnalysisTools.calculate_object_density(scene)

# Occupation de la zone centrale (devant le véhicule)
occupancy = SceneAnalysisTools.calculate_central_occupancy(scene)

# Distribution d'objets
dist = SceneAnalysisTools.get_object_distribution(scene)

# Objets critiques
critical = SceneAnalysisTools.identify_critical_objects(scene)
```

## 🔒 Configuration

### Fichier .env (racine du projet)
```bash
OPEN_API_KEY=sk_proj_xxxxxxxxxxxxx
```

⚠️ **Important** : Ne pas committer le fichier `.env` !

## 📊 Scènes simulées

4 scènes de test pour développer sans images réelles :

| Scène | Objets | Risque | Usage |
|-------|--------|--------|-------|
| **Clear Road** | Aucun | ✅ FAIBLE | Route dégagée de base |
| **Pedestrian Crossing** | 2 piétons + feu | ⚠️ MOYEN | Passage piéton urbain |
| **Heavy Traffic** | 5 véhicules + vélo | ⚠️ MOYEN | Trafic dense |
| **School Zone** | Enfants + école | 🔴 CRITIQUE | Zone scolaire dangereuse |

```python
from llm_agent.simulated_scenes import SimulatedDrivingScenes

# Charger toutes les scènes
scenes = SimulatedDrivingScenes.all_scenes()

for name, scene in scenes.items():
    print(f"Scène: {name}")
    print(f"Objets: {len(scene.detected_objects)}")
```

## 📈 Statistiques

- **Modèle LLM** : gpt-4o-mini (rapide, économique)
- **Coût/appel** : ~$0.001 - $0.002 USD
- **Temps de réponse** : <2 secondes
- **Tests** : 85+ tests, 95%+ passing rate
- **Coverage** : Tous les modules couverts

## 🔗 Intégration dans le pipeline

```python
# 1. Recevoir les détections du CV module
from cv_module.infer import detect_objects
detections = detect_objects(image)

# 2. Analyser avec le LLM agent
from llm_agent.agent import DrivingSceneAnalyzer
analyzer = DrivingSceneAnalyzer(use_llm=True)
result = analyzer.analyze_scene(detections)

# 3. Afficher dans Streamlit
# À faire: intégrer dans App/streamlit_app.py
```

## ✅ Vérification rapide

```bash
# Vérifier que tout fonctionne
python3 << 'EOF'
from llm_agent.agent import DrivingSceneAnalyzer
from llm_agent.simulated_scenes import SimulatedDrivingScenes

analyzer = DrivingSceneAnalyzer(use_llm=False)
scenes = SimulatedDrivingScenes.all_scenes()

for name, scene in scenes.items():
    result = analyzer.analyze_scene(scene)
    print(f"✅ {name}: {result.risque_eval.risque_level}")
EOF
```
