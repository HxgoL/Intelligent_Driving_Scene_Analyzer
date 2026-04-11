#!/usr/bin/env python3
"""
Test du LLM Agent avec scènes simulées
"""
import os
import sys
from pathlib import Path

# Ajouter le parent au Python path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

# Charger la clé API
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

from llm_agent.agent import DrivingSceneAnalyzer
from llm_agent.simulated_scenes import SimulatedDrivingScenes

print("\n" + "=" * 70)
print("🚗 TEST LLM AGENT AVEC SCÈNES SIMULÉES")
print("=" * 70)

# Initialiser l'analyzer
try:
    analyzer = DrivingSceneAnalyzer(use_llm=True, api_key=api_key)
    print("\n✅ Analyzer initialisé avec LLM")
except Exception as e:
    print(f"❌ Erreur d'initialisation : {e}")
    exit(1)

# Tester les scènes
scenes = SimulatedDrivingScenes.all_scenes()

for i, (scene_name, scene) in enumerate(scenes.items(), 1):
    print(f"\n[{i}/{len(scenes)}] Analyse de '{scene_name}'...")
    print(f"    Objets : {len(scene.detected_objects)}")
    
    try:
        result = analyzer.analyze_scene(
            detections=scene,
            scene_context="Route générale, jour clair"
        )
        
        print(f"    ✅ Résultat : Risque {result.risque_eval.risque_level}")
        print(f"    📝 Résumé : {result.resume[:60]}...")
        
    except Exception as e:
        print(f"    ❌ Erreur : {e}")

print("\n" + "=" * 70)
print("✅ TOUS LES TESTS RÉUSSIS !")
print("=" * 70 + "\n")
