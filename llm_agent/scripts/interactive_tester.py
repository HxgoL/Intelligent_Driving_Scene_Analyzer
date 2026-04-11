#!/usr/bin/env python3
"""
interactive_tester.py - Testeur interactif du LLM
Permet de tester rapidement des scènes spécifiques avec menu interactif
"""

import os
import sys
from dotenv import load_dotenv
from llm_agent.agent import DrivingSceneAnalyzer
from llm_agent.simulated_scenes import SimulatedDrivingScenes


def print_menu():
    """Affiche le menu principal"""
    scenes = SimulatedDrivingScenes.all_scenes()
    
    print("\n" + "=" * 70)
    print("🚗 TESTEUR INTERACTIF LLM")
    print("=" * 70)
    print("\nScènes disponibles :\n")
    
    for i, scene_name in enumerate(scenes.keys(), 1):
        print(f"  {i}. {scene_name}")
    
    print(f"\n  {len(scenes)+1}. Analyser TOUTES les scènes")
    print(f"  {len(scenes)+2}. Quitter")
    print("\n" + "=" * 70)


def analyze_single_scene(analyzer: DrivingSceneAnalyzer, scene_name: str):
    """Analyse une scène unique"""
    contexts = {
        "clear_road": "Route dégagée, jour clair, bonne visibilité",
        "pedestrian_crossing": "Zone piétonne, heures d'affluence, jour clair",
        "heavy_traffic": "Route urbaine, heure de pointe, visibilité bonne",
        "school_zone": "Zone scolaire, heures de sortie, visibilité excellente",
    }
    
    try:
        scene = SimulatedDrivingScenes.get_scene_by_name(scene_name)
        context = contexts.get(scene_name, "Route générale, jour clair")
        
        print(f"\n{'=' * 70}")
        print(f"🔍 Analyse de la scène : {scene_name}")
        print(f"{'=' * 70}")
        print(f"Contexte : {context}")
        print(f"Objets détectés : {len(scene.detected_objects)}")
        
        if scene.detected_objects:
            print("\nDétections :")
            for obj in scene.detected_objects:
                print(f"  • {obj.label:15} (confiance: {obj.confidence:.0%})")
        
        print("\n⏳ Analyse en cours...")
        
        result = analyzer.analyze_scene(
            detections=scene,
            scene_context=context
        )
        
        print(f"\n✅ Analyse complète !")
        print(f"\n{'─' * 70}")
        print(f"Résumé : {result.resume}")
        print(f"{'─' * 70}")
        print(f"Niveau de risque : {result.risque_eval.risque_level}")
        print(f"\nRecommandations :")
        if result.recommandations:
            for i, rec in enumerate(result.recommandations, 1):
                print(f"  {i}. {rec}")
        else:
            print("  (Aucune recommandation spécifique)")
        print(f"{'=' * 70}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}\n")
        return False


def main():
    """Fonction principale"""
    
    # Charger les variables d'env
    load_dotenv()
    api_key = os.getenv("OPEN_API_KEY")
    
    if not api_key:
        print("\n⚠️  OPEN_API_KEY non trouvée !")
        print("   Mode TEST activé (mode sans LLM avec règles prédéfini)\n")
        use_llm = False
    else:
        print("\n✅ Clé API trouvée !")
        print("   Mode LLM activé (utilisation de gpt-4o-mini)\n")
        use_llm = True
    
    # Initialise l'analyzer
    try:
        analyzer = DrivingSceneAnalyzer(use_llm=use_llm, api_key=api_key)
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        sys.exit(1)
    
    scenes = list(SimulatedDrivingScenes.all_scenes().keys())
    
    while True:
        print_menu()
        
        try:
            choice = input("Entrez votre choix (numéro ou 'q' pour quitter) : ").strip().lower()
            
            if choice == 'q':
                print("\n👋 Au revoir !\n")
                break
            
            choice = int(choice)
            
            if choice == len(scenes) + 1:
                # Analyser toutes les scènes
                print("\n🚀 Analyse de TOUTES les scènes...")
                for scene_name in scenes:
                    analyze_single_scene(analyzer, scene_name)
                
            elif choice == len(scenes) + 2:
                print("\n👋 Au revoir !\n")
                break
            
            elif 1 <= choice <= len(scenes):
                scene_name = scenes[choice - 1]
                analyze_single_scene(analyzer, scene_name)
            
            else:
                print("❌ Choix invalide. Veuillez réessayer.")
        
        except ValueError:
            print("❌ Entrée invalide. Veuillez entrer un numéro ou 'q'.")
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt par l'utilisateur !\n")
            break
        except Exception as e:
            print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erreur critique : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
