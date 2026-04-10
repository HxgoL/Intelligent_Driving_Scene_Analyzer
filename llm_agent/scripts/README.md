# 🛠️ Scripts et Outils LLM Agent

Ce dossier contient des utilitaires et scripts pratiques pour tester et analyser des scènes routières avec le LLM Agent.

## 📂 Structure

```
scripts/
├── __init__.py                 # Initialisation du package
├── interactive_tester.py       # Testeur interactif du LLM
└── batch_analyzer.py           # Analyseur batch des scènes
```

## 🎮 Outils disponibles

### 1. `interactive_tester.py` - Testeur interactif

Permet de tester le LLM interactivement en sélectionnant des scènes une par une.

**Utilisation :**
```bash
python llm_agent/scripts/interactive_tester.py
```

**Fonctionnalités :**
- ✅ Menu interactif avec toutes les scènes
- ✅ Analyse individuelles ou batch
- ✅ Affichage des résultats en temps réel
- ✅ Support LLM et mode sans-LLM

**Exemple de menu :**
```
======================================================================
🚗 TESTEUR INTERACTIF LLM
======================================================================

Scènes disponibles :

  1. clear_road
  2. pedestrian_crossing
  3. heavy_traffic
  4. school_zone

  5. Analyser TOUTES les scènes
  6. Quitter

======================================================================
Entrez votre choix (numéro ou 'q' pour quitter) : 
```

**Navigation :**
- Entrez le **numéro** d'une scène pour l'analyser
- Entrez **5** pour analyser toutes les scènes
- Entrez **q** pour quitter

### 2. `batch_analyzer.py` - Analyseur batch

Analyse automatiquement toutes les scènes et sauvegarde les résultats en JSON.

**Utilisation :**
```bash
python llm_agent/tools/batch_analyzer.py
```

**Fonctionnalités :**
- ✅ Analyse automatique de toutes les scènes
- ✅ Sauvegarde des résultats en JSON
- ✅ Résumé statistique
- ✅ Gestion intelligente des erreurs

**Output attendu :**
```
======================================================================
🚀 ANALYSE BATCH DE TOUTES LES SCÈNES
======================================================================
Mode LLM : ✅ ACTIF
Nombre de scènes : 4
======================================================================

[1/4] Analyse de 'clear_road'...
      Contexte : Route dégagée, jour clair, bonne visibilité
      Objets : 0
      ✅ Risque : FAIBLE

[2/4] Analyse de 'pedestrian_crossing'...
      Contexte : Zone piétonne, heures d'affluence, jour clair
      Objets : 2
      ✅ Risque : ÉLEVÉ

...

======================================================================
📊 RÉSUMÉ
======================================================================
✅ Analyses réussies   : 4/4
❌ Analyses échouées   : 0/4
📈 Taux de réussite    : 100.0%

📋 Distribution des niveaux de risque :
   • FAIBLE     : 1 scènes
   • MOYEN      : 0 scènes
   • ÉLEVÉ      : 3 scènes
   • CRITIQUE   : 0 scènes

======================================================================

💾 Résultats sauvegardés dans : llm_batch_results_20260410_143052.json
```

**Fichier JSON généré :**
```json
{
  "timestamp": "2026-04-10T14:30:52.123456",
  "total_scenes": 4,
  "successful": 4,
  "failed": 0,
  "use_llm": true,
  "results": [
    {
      "scene_name": "clear_road",
      "status": "✅ SUCCÈS",
      "num_objects": 0,
      "scene_context": "Route dégagée, jour clair, bonne visibilité",
      "resume": "Route complètement dégagée...",
      "risk_level": "FAIBLE",
      "recommendations": [...]
    },
    ...
  ],
  "errors": []
}
```

## 📊 Scènes disponibles

| Nom | Description | Objets | Risque |
|-----|-------------|--------|--------|
| `clear_road` | Route dégagée | 0 | 🟢 FAIBLE |
| `pedestrian_crossing` | Traversée de piétons | 2 | 🔴 ÉLEVÉ |
| `heavy_traffic` | Circulation dense | 3 | 🟡 MOYEN |
| `school_zone` | Zone scolaire | 3 | 🔴 ÉLEVÉ |

## 🚀 Cas d'utilisation

### Développement et débogage
```bash
# Tester une scène spécifique
python llm_agent/tools/interactive_tester.py
# → Choisir scène 1
```

### Tests de performance
```bash
# Tester toutes les scènes avec statistiques
python llm_agent/tools/batch_analyzer.py
# → Analyse complète + sauvegarde JSON
```

### Pipeline d'intégration continue
```bash
# Dans un script CI/CD
python llm_agent/tools/batch_analyzer.py > logs/batch_results.log
```

### Comparaison mode LLM vs sans-LLM
```bash
# Avec LLM (export OPEN_API_KEY=sk_xxx)
python llm_agent/tools/batch_analyzer.py

# Sans LLM (supprimer la variable d'env)
unset OPEN_API_KEY
python llm_agent/tools/batch_analyzer.py
```

## 🔧 Configuration

### Clé API OpenAI
Les outils utilisent **automatiquement** la clé API du fichier `.env` :

```bash
# Dans .env à la racine du projet
OPEN_API_KEY=sk_proj_xxxxxxxxxxxxx
```

Si la clé n'est pas trouvée → Mode sans-LLM automatique

## 📝 Exemples avancés

### Tester une scène personnalisée
```python
# Créer un script Python
from llm_agent.agent import DrivingSceneAnalyzer
from pipeline.schema import SceneDetections, DetectedObject, BoundingBox

analyzer = DrivingSceneAnalyzer(use_llm=True)

scene = SceneDetections(
    detected_objects=[
        DetectedObject(
            label="car",
            confidence=0.95,
            bounding_box=BoundingBox(x=150, y=200, width=100, height=80)
        ),
    ]
)

result = analyzer.analyze_scene(detections=scene)
print(result.resume)
```

### Intégrer dans une pipeline CI/CD
```bash
#!/bin/bash
# test_llm.sh

cd /path/to/project
python llm_agent/tools/batch_analyzer.py

# Vérifier qu'il n'y a pas d'erreurs
if grep -q '"failed": 0' llm_batch_results_*.json; then
    echo "✅ Tests LLM OK"
    exit 0
else
    echo "❌ Tests LLM ÉCHOUÉS"
    exit 1
fi
```

## 📚 Voir aussi

- [Tests unitaires](./tests/README.md)
- [README du LLM Agent](../README_LLM.md)
- [Module simulated_scenes](../simulated_scenes.py)
