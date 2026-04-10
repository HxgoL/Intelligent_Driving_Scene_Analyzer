# 🧪 Tests du Module LLM Agent

Ce dossier contient l'ensemble des tests unitaires et d'intégration pour le module `llm_agent`.

## 📂 Structure

```
tests/
├── __init__.py                 # Initialisation du package
├── conftest.py                 # Configuration pytest et fixtures
├── test_api_openai.py          # Tests de connexion à l'API OpenAI
├── test_agent.py               # Tests du DrivingSceneAnalyzer
├── test_formatter.py           # Tests du ResponseFormatter
├── test_risk_rules.py          # Tests du RiskEvaluator
├── test_tools.py               # Tests des outils d'analyse
└── test_integration.py         # Tests d'intégration complets
```

## 🧪 Tests disponibles

### 1. `test_api_openai.py` - Connexion OpenAI
Tests de base pour vérifier que l'API OpenAI est configurée et fonctionnelle.

```bash
pytest tests/test_api_openai.py -v
```

**Contient :**
- ✅ Vérification de la clé API
- ✅ Import de la librairie openai
- ✅ Initialisation du client
- ✅ Appel API réel (marqué comme `@pytest.mark.slow`)

### 2. `test_agent.py` - DrivingSceneAnalyzer
Tests de l'orchestrateur principal de l'analyse de scènes.

```bash
pytest tests/test_agent.py -v
```

**Contient :**
- ✅ Initialisation avec/sans LLM
- ✅ Analyse de scènes vides
- ✅ Analyse de scènes avec objets
- ✅ Tests de niveau de risque
- ✅ Tests avec LLM réel

### 3. `test_formatter.py` - ResponseFormatter
Tests du parsing et formatage des réponses LLM.

```bash
pytest tests/test_formatter.py -v
```

**Contient :**
- ✅ Extraction du résumé
- ✅ Extraction des risques
- ✅ Extraction des recommandations
- ✅ Inférence du niveau de risque
- ✅ Formatage pour affichage

### 4. `test_risk_rules.py` - RiskEvaluator
Tests de l'évaluation des risques basée sur les objets détectés.

```bash
pytest tests/test_risk_rules.py -v
```

**Contient :**
- ✅ Facteurs de risque des objets
- ✅ Pondérations de risque (confiance, proximité)
- ✅ Évaluation de détections
- ✅ Recommandations générées

### 5. `test_tools.py` - SceneAnalysisTools
Tests des outils d'analyse de scène.

```bash
pytest tests/test_tools.py -v
```

**Contient :**
- ✅ Densité d'objets
- ✅ Occupation de zone centrale
- ✅ Distribution d'objets
- ✅ Confiance moyenne

### 6. `test_integration.py` - Tests d'intégration
Tests complets du pipeline d'analyse de scènes.

```bash
pytest tests/test_integration.py -v
```

**Contient :**
- ✅ Pipeline sans LLM
- ✅ Pipeline avec contexte additionnel
- ✅ Analyse de toutes les scènes
- ✅ Pipeline avec LLM réel (marqué comme `@pytest.mark.slow`)

## 🚀 Comment exécuter les tests

### Tous les tests
```bash
pytest tests/ -v
```

### Tests rapides uniquement (exclut les appels API)
```bash
pytest tests/ -v -m "not slow"
```

### Tests API uniquement
```bash
pytest tests/test_api_openai.py -v -m slow
```

### Tests d'un fichier spécifique
```bash
pytest tests/test_agent.py -v
```

### Tests d'une classe spécifique
```bash
pytest tests/test_agent.py::TestDrivingSceneAnalyzerInitialization -v
```

### Tests d'une méthode spécifique
```bash
pytest tests/test_agent.py::TestDrivingSceneAnalyzerInitialization::test_initialization_without_llm -v
```

## 📊 Couverture de tests

Les tests couvrent :

| Module | Fichier | Classes | Méthodes |
|--------|---------|---------|----------|
| **API OpenAI** | test_api_openai.py | 1 | 4 |
| **Agent** | test_agent.py | 3 | 8 |
| **Formatter** | test_formatter.py | 3 | 10 |
| **Risk Rules** | test_risk_rules.py | 4 | 11 |
| **Tools** | test_tools.py | 4 | 7 |
| **Intégration** | test_integration.py | 3 | 11 |
| **TOTAL** | - | 18 | 51 |

## 🔧 Installation des dépendances de test

```bash
# Installer pytest
pip install pytest pytest-cov

# Ou via requirements (si présent)
pip install -r requirements-dev.txt
```

## 📝 Exemples de sortie

### Exécution réussie
```
tests/test_agent.py::TestDrivingSceneAnalyzerInitialization::test_initialization_without_llm PASSED
tests/test_agent.py::TestDrivingSceneAnalyzerAnalysis::test_analysis_empty_scene PASSED
tests/test_formatter.py::TestResponseFormatterExtraction::test_extract_resume PASSED
=============================== 51 passed in 2.34s ===============================
```

### Avec tests lents (API)
```
tests/test_api_openai.py::TestOpenAIConnection::test_openai_api_call PASSED
tests/test_integration.py::TestIntegrationWithLLM::test_llm_pipeline_pedestrian PASSED
=============================== 61 passed in 15.32s ===============================
```

## 🐛 Débogage et développement

### Avec output détaillé
```bash
pytest tests/ -vv -s
```

### Avec traceback complet
```bash
pytest tests/ -vv --tb=long
```

### Avec logs
```bash
pytest tests/ -v --log-cli-level=DEBUG
```

### Coverage (couverture)
```bash
pytest tests/ --cov=llm_agent --cov-report=html
```

## ✅ Checklist avant commit

- [ ] `pytest tests/ -m "not slow"` passe
- [ ] Aucun warning ou erreur
- [ ] Coverage > 80%
- [ ] Code propre et lisible

## 📚 Voir aussi

- [README du LLM Agent](../README_LLM.md)
- [Tools et Utilitaires](../tools/)
- [Simulated Scenes](../simulated_scenes.py)
