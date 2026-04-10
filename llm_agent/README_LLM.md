"""
CONFIGURATION ET UTILISATION DU LLM AGENT
=========================================

Le module LLM Agent utilise OpenAI pour générer des analyses contextées des scènes de conduite.

## Installation

1. Installez les dépendances :
   pip install -r requirements.txt

   Ou directement :
   pip install openai>=1.52.0

2. Obtenez une clé API OpenAI :
   - Allez sur https://platform.openai.com/api-keys
   - Créez une nouvelle clé API
   - Copiez-la (elle ne s'affichera qu'une fois)


## Configuration

La clé API peut être définie de deux façons :

### Option 1 : Variable d'environnement (recommandé)
Définissez la variable d'environnement OPENAI_API_KEY :

# macOS/Linux
export OPENAI_API_KEY="sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

Puis utilisez l'agent :
```python
from llm_agent.agent import DrivingSceneAnalyzer

analyzer = DrivingSceneAnalyzer(use_llm=True)
result = analyzer.analyze_scene(detections)
```

### Option 2 : Passage direct du paramètre
```python
from llm_agent.agent import DrivingSceneAnalyzer

analyzer = DrivingSceneAnalyzer(
    use_llm=True,
    api_key="sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)
result = analyzer.analyze_scene(detections)
```


## Utilisation

### Exemple simple
```python
from pipeline.schema import SceneDetections, DetectedObject, BoundingBox
from llm_agent.agent import DrivingSceneAnalyzer

# Créez une scène avec des objets détectés
scene = SceneDetections(
    detected_objects=[
        DetectedObject(
            label="car",
            confidence=0.95,
            bounding_box=BoundingBox(x=150, y=200, width=100, height=80)
        ),
        DetectedObject(
            label="person",
            confidence=0.88,
            bounding_box=BoundingBox(x=320, y=250, width=50, height=120)
        ),
    ]
)

# Analysez-la avec le LLM
analyzer = DrivingSceneAnalyzer(use_llm=True)
result = analyzer.analyze_scene(
    detections=scene,
    scene_context="Route urbaine, heure de pointe"
)

# Affichez les résultats
print(f"Résumé: {result.resume}")
print(f"Risques: {result.risque_eval.risques}")
print(f"Recommandations: {result.recommandations}")
print(f"Niveau: {result.risque_eval.risque_level}")
```

### Utilisation des outils d'analyse
```python
from llm_agent.tools import SceneAnalysisTools

# Calculer la densité d'objets
density = SceneAnalysisTools.calculate_object_density(scene)

# Calculer l'occupation de la zone centrale
occupancy = SceneAnalysisTools.calculate_central_occupancy(scene)

# Obtenir la distribution des objets
distribution = SceneAnalysisTools.get_object_distribution(scene)

# Identifier les objets critiques
critical_objects = SceneAnalysisTools.identify_critical_objects(scene)

# Construire un contexte pour le LLM
context = SceneAnalysisTools.build_scene_context(scene)

# Résumé des facteurs de risque
risk_summary = SceneAnalysisTools.get_risk_factors_summary(scene)
```

### Mode sans LLM (analyse par règles)
```python
analyzer = DrivingSceneAnalyzer(use_llm=False)
result = analyzer.analyze_scene(detections)
# Utilise des règles prédéfinies au lieu du LLM
```


## Modèles disponibles

Par défaut, le module utilise **gpt-4o-mini** pour optimiser les coûts.
Vous pouvez changer le modèle en modifiant `agent.py` :

```python
self.model = "gpt-4-turbo"  # Plus puissant, plus cher
# ou
self.model = "gpt-4o"       # Version complète GPT-4o
# ou
self.model = "gpt-4o-mini"  # Par défaut, moins cher ✓
```


## Coûts et limitations

- **Coût** : gpt-4o-mini est ~10x moins cher que gpt-4-turbo
- **Latence** : Chaque analyse prend quelques secondes (appel API)
- **Limite de taux** : Vérifiez vos limites sur https://platform.openai.com/account/rate-limits
- **Contexte** : Le modèle digère ~500 tokens max par analyse

Pour les tests intensifs, utilisez le mode sans LLM :
```python
analyzer = DrivingSceneAnalyzer(use_llm=False)
```


## Dépannage

### Erreur "Clé API non trouvée"
```
ValueError: Clé API OpenAI non trouvée. Configurez OPENAI_API_KEY en variable d'environnement
```
→ Définissez la variable OPENAI_API_KEY ou passez-la en paramètre

### Erreur "openai package not installed"
```
ImportError: openai est requis pour utiliser le LLM. Installez avec: pip install openai
```
→ Exécutez : `pip install openai>=1.52.0`

### Erreur "Rate limit exceeded"
→ Vous avez dépassé votre quota d'API. Attendez ou vérifiez votre plan.

### Erreur "Invalid API key"
→ Vérifiez que votre clé commence par `sk_` et est valide sur https://platform.openai.com/api-keys


## Voir aussi

- [agent.py](agent.py) - Code principal de l'agent
- [tools.py](tools.py) - Outils d'analyse de scène
- [test_agent_mock.py](test_agent_mock.py) - Tests avec données mockées
- [test_llm_integration.py](test_llm_integration.py) - Suite de tests (20 tests)
"""
