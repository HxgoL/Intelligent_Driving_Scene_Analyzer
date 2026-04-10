#!/usr/bin/env python3
"""
batch_analyzer.py - Analyse batch de toutes les scènes simulées
Teste le LLM sur toutes les scènes et sauvegarde les résultats
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

from llm_agent.agent import DrivingSceneAnalyzer
from llm_agent.simulated_scenes import SimulatedDrivingScenes


class BatchAnalyzer:
    """Analyseur batch pour tester le LLM"""
    
    def __init__(self, use_llm: bool = True, api_key: str = None):
        """
        Initialiser le batch analyzer
        
        Args:
            use_llm: Utiliser l'API OpenAI réelle
            api_key: Clé API OpenAI
        """
        self.use_llm = use_llm
        self.results = []
        self.errors = []
        
        try:
            self.analyzer = DrivingSceneAnalyzer(use_llm=use_llm, api_key=api_key)
        except Exception as e:
            print(f"❌ Erreur d'initialisation : {e}")
            sys.exit(1)
    
    def analyze_scene(self, scene_name: str, scene_context: str = "Route générale, jour clair"):
        """Analyser une scène"""
        try:
            scene = SimulatedDrivingScenes.get_scene_by_name(scene_name)
            
            result = self.analyzer.analyze_scene(
                detections=scene,
                scene_context=scene_context
            )
            
            analysis = {
                "scene_name": scene_name,
                "status": "✅ SUCCÈS",
                "num_objects": len(scene.detected_objects),
                "scene_context": scene_context,
                "resume": result.resume,
                "risk_level": result.risque_eval.risque_level,
                "recommendations": result.recommandations,
            }
            
            self.results.append(analysis)
            return analysis
            
        except Exception as e:
            error_info = {
                "scene_name": scene_name,
                "status": "❌ ERREUR",
                "error": str(e)
            }
            self.errors.append(error_info)
            return error_info
    
    def run_all_scenes(self):
        """Analyser toutes les scènes"""
        scenes = SimulatedDrivingScenes.all_scenes()
        
        print("\n" + "=" * 70)
        print("🚀 ANALYSE BATCH DE TOUTES LES SCÈNES")
        print("=" * 70)
        print(f"Mode LLM : {'✅ ACTIF' if self.use_llm else '⏸️  DÉSACTIVÉ'}")
        print(f"Nombre de scènes : {len(scenes)}")
        print("=" * 70)
        
        contexts = {
            "clear_road": "Route dégagée, jour clair, bonne visibilité",
            "pedestrian_crossing": "Zone piétonne, heures d'affluence, jour clair",
            "heavy_traffic": "Route urbaine, heure de pointe, visibilité bonne",
            "school_zone": "Zone scolaire, heures de sortie, visibilité excellente",
        }
        
        for i, (scene_name, scene) in enumerate(scenes.items(), 1):
            context = contexts.get(scene_name, "Route générale, jour clair")
            
            print(f"\n[{i}/{len(scenes)}] Analyse de '{scene_name}'...")
            print(f"      Contexte : {context}")
            print(f"      Objets : {len(scene.detected_objects)}")
            
            result = self.analyze_scene(scene_name, context)
            
            if result["status"] == "✅ SUCCÈS":
                print(f"      ✅ Risque : {result['risk_level']}")
            else:
                print(f"      ❌ ERREUR : {result['error']}")
    
    def save_results(self, filename: str = None):
        """Sauvegarder les résultats en JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"llm_batch_results_{timestamp}.json"
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_scenes": len(self.results) + len(self.errors),
            "successful": len(self.results),
            "failed": len(self.errors),
            "use_llm": self.use_llm,
            "results": self.results,
            "errors": self.errors
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def print_summary(self):
        """Imprimer un résumé"""
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ")
        print("=" * 70)
        
        total = len(self.results) + len(self.errors)
        success_rate = (len(self.results) / total * 100) if total > 0 else 0
        
        print(f"✅ Analyses réussies   : {len(self.results)}/{total}")
        print(f"❌ Analyses échouées   : {len(self.errors)}/{total}")
        print(f"📈 Taux de réussite    : {success_rate:.1f}%")
        
        # Distribution des risques
        if self.results:
            risk_levels = {}
            for result in self.results:
                level = result.get("risk_level", "INCONNU")
                risk_levels[level] = risk_levels.get(level, 0) + 1
            
            print("\n📋 Distribution des niveaux de risque :")
            for level, count in sorted(risk_levels.items()):
                print(f"   • {level:12} : {count} scènes")
        
        # Erreurs
        if self.errors:
            print("\n⚠️  Erreurs rencontrées :")
            for error in self.errors:
                print(f"   • {error['scene_name']} : {error['error']}")
        
        print("\n" + "=" * 70)


def main():
    """Fonction principale"""
    
    # Charger les variables d'env
    load_dotenv()
    api_key = os.getenv("OPEN_API_KEY")
    
    use_real_llm = bool(api_key)
    
    if not use_real_llm:
        print("\n⚠️  OPEN_API_KEY non trouvée !")
        print("   Mode TEST activé (sans appels réels à l'API)\n")
    
    # Initialiser et lancer l'analyse
    analyzer = BatchAnalyzer(use_llm=use_real_llm, api_key=api_key)
    analyzer.run_all_scenes()
    analyzer.print_summary()
    
    # Sauvegarder
    output_file = analyzer.save_results()
    print(f"\n💾 Résultats sauvegardés dans : {output_file}")
    
    return 0 if len(analyzer.errors) == 0 else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Arrêt par l'utilisateur")
        sys.exit(1)
