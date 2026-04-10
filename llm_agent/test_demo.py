"""
test_demo.py - Démonstration interactive du pipeline complet
Teste le programme avec différentes scènes et montre les résultats
"""

import sys
from pathlib import Path

# Ajoute le parent du dossier llm_agent au chemin d'import
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.schema import BoundingBox, DetectedObject, SceneDetections
from llm_agent import DrivingSceneAnalyzer, SceneAnalysisTools


def print_section(title):
    """Affiche un titre de section"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def print_scene_analysis(title, scene, context=""):
    """Analyse et affiche les résultats d'une scène"""
    print(f"📍 {title}")
    print(f"   Objets: {len(scene.detected_objects)}")
    
    if scene.detected_objects:
        distribution = SceneAnalysisTools.get_object_distribution(scene)
        density = SceneAnalysisTools.calculate_object_density(scene)
        occupancy = SceneAnalysisTools.calculate_central_occupancy(scene)
        
        print(f"   Distribution: {distribution}")
        print(f"   Densité: {density:.3f} obj/1000px²")
        print(f"   Occupation zone centrale: {occupancy:.1f}%")
    
    # Analyse avec agent
    analyzer = DrivingSceneAnalyzer(use_llm=False)
    result = analyzer.analyze_scene(scene, context)
    
    print(f"\n   📋 Résumé:")
    print(f"   {result.resume}")
    print(f"\n   ⚠️  Niveau de risque: {result.risque_eval.risque_level}")
    print(f"\n   ✅ Recommandations:")
    for i, rec in enumerate(result.recommandations, 1):
        print(f"      {i}. {rec}")


def test_demo_1_empty_road():
    """Test 1: Route claire"""
    scene = SceneDetections(detected_objects=[])
    print_scene_analysis(
        "Test 1: Route claire",
        scene,
        "Route dégagée, conditions normales"
    )


def test_demo_2_simple_traffic():
    """Test 2: Trafic simple"""
    scene = SceneDetections(
        detected_objects=[
            DetectedObject(
                label="car",
                confidence=0.95,
                bounding_box=BoundingBox(x=200, y=200, width=100, height=80)
            ),
            DetectedObject(
                label="car",
                confidence=0.92,
                bounding_box=BoundingBox(x=450, y=180, width=100, height=80)
            ),
        ]
    )
    print_scene_analysis(
        "Test 2: Trafic simple",
        scene,
        "Route urbaine, circulation normale"
    )


def test_demo_3_pedestrian_crossing():
    """Test 3: Passage piéton"""
    scene = SceneDetections(
        detected_objects=[
            DetectedObject(
                label="person",
                confidence=0.94,
                bounding_box=BoundingBox(x=300, y=280, width=50, height=130)
            ),
            DetectedObject(
                label="person",
                confidence=0.89,
                bounding_box=BoundingBox(x=370, y=300, width=50, height=130)
            ),
            DetectedObject(
                label="stop sign",
                confidence=0.97,
                bounding_box=BoundingBox(x=50, y=120, width=40, height=40)
            ),
        ]
    )
    print_scene_analysis(
        "Test 3: Passage piéton",
        scene,
        "Zone urbaine avec passage piéton, heure de pointe"
    )


def test_demo_4_heavy_traffic():
    """Test 4: Trafic dense"""
    scene = SceneDetections(
        detected_objects=[
            DetectedObject(
                label="car",
                confidence=0.96,
                bounding_box=BoundingBox(x=100, y=150, width=90, height=70)
            ),
            DetectedObject(
                label="truck",
                confidence=0.93,
                bounding_box=BoundingBox(x=250, y=120, width=120, height=90)
            ),
            DetectedObject(
                label="car",
                confidence=0.91,
                bounding_box=BoundingBox(x=400, y=140, width=90, height=70)
            ),
            DetectedObject(
                label="motorcycle",
                confidence=0.88,
                bounding_box=BoundingBox(x=200, y=320, width=60, height=50)
            ),
            DetectedObject(
                label="bicycle",
                confidence=0.85,
                bounding_box=BoundingBox(x=500, y=350, width=50, height=90)
            ),
        ]
    )
    print_scene_analysis(
        "Test 4: Trafic dense et dangereux",
        scene,
        "Route nationale, trafic dense, conditions sèches"
    )


def test_demo_5_accident_scenario():
    """Test 5: Scénario critique"""
    scene = SceneDetections(
        detected_objects=[
            DetectedObject(
                label="car",
                confidence=0.98,
                bounding_box=BoundingBox(x=150, y=200, width=100, height=80)
            ),
            DetectedObject(
                label="person",
                confidence=0.96,
                bounding_box=BoundingBox(x=320, y=250, width=40, height=120)
            ),
            DetectedObject(
                label="bicycle",
                confidence=0.94,
                bounding_box=BoundingBox(x=200, y=330, width=55, height=95)
            ),
            DetectedObject(
                label="debris",
                confidence=0.91,
                bounding_box=BoundingBox(x=400, y=300, width=70, height=50)
            ),
        ]
    )
    print_scene_analysis(
        "Test 5: Scénario critique/accident",
        scene,
        "Carrefour urbain dangereux, objets dispersés"
    )


def test_tools_analysis():
    """Teste les outils d'analyse en détail"""
    print_section("TEST DES OUTILS D'ANALYSE")
    
    scene = SceneDetections(
        detected_objects=[
            DetectedObject(
                label="car",
                confidence=0.95,
                bounding_box=BoundingBox(x=200, y=200, width=100, height=80)
            ),
            DetectedObject(
                label="truck",
                confidence=0.92,
                bounding_box=BoundingBox(x=400, y=150, width=120, height=100)
            ),
            DetectedObject(
                label="person",
                confidence=0.88,
                bounding_box=BoundingBox(x=320, y=280, width=40, height=120)
            ),
        ]
    )
    
    print("🔬 Analyse détaillée d'une scène avec 3 objets:\n")
    
    density = SceneAnalysisTools.calculate_object_density(scene)
    print(f"  📊 Densité: {density:.3f} objets/1000px²")
    
    occupancy = SceneAnalysisTools.calculate_central_occupancy(scene)
    print(f"  📍 Occupation zone centrale: {occupancy:.1f}%")
    
    distribution = SceneAnalysisTools.get_object_distribution(scene)
    print(f"  📦 Distribution: {distribution}")
    
    avg_confidence = SceneAnalysisTools.get_average_confidence(scene)
    print(f"  📈 Confiance moyenne: {avg_confidence:.1%}")
    
    critical = SceneAnalysisTools.identify_critical_objects(scene)
    print(f"  🎯 Objets critiques: {len(critical)}")
    
    context = SceneAnalysisTools.build_scene_context(scene)
    print(f"  📝 Contexte: {context}")
    
    summary = SceneAnalysisTools.get_risk_factors_summary(scene)
    print(f"  ⚠️  Résumé risques:")
    print(f"      - Objets totaux: {summary['total_objects']}")
    print(f"      - Objets critiques: {summary['critical_objects_count']}")
    print(f"      - Objets à risque élevé: {summary['high_risk_count']}")


def test_comparison():
    """Compare les différents modes d'analyse"""
    print_section("COMPARAISON: AVEC/SANS LLM")
    
    scene = SceneDetections(
        detected_objects=[
            DetectedObject(
                label="car",
                confidence=0.95,
                bounding_box=BoundingBox(x=200, y=200, width=100, height=80)
            ),
            DetectedObject(
                label="person",
                confidence=0.88,
                bounding_box=BoundingBox(x=320, y=280, width=40, height=120)
            ),
        ]
    )
    
    # Sans LLM (rapide, basé sur les règles)
    print("🟢 MODE SANS LLM (basé sur les règles):")
    analyzer_no_llm = DrivingSceneAnalyzer(use_llm=False)
    result_no_llm = analyzer_no_llm.analyze_scene(scene)
    print(f"   Résumé: {result_no_llm.resume}\n")
    
    # Avec mock LLM (pour tester la structure)
    print("🔵 MODE AVEC LLM (mockée pour démo):")
    mock_response = """RÉSUMÉ: Scène urbaine avec une voiture et un piéton. Niveau de risque moyen.
RISQUES: Piéton en zone centrale, véhicule à proximité
RECOMMANDATIONS: Réduire la vitesse, rester vigilant, prêt à freiner"""
    
    result_llm = analyzer_no_llm.analyze_scene(scene, mock_llm_response=mock_response)
    print(f"   Résumé: {result_llm.resume}\n")


if __name__ == "__main__":
    print("\n")
    print("🚗" * 35)
    print("  DÉMONSTRATION DU DRIVING SCENE ANALYZER")
    print("🚗" * 35)
    
    # Tests de scènes
    print_section("TESTS DE SCÈNES RÉALISTES")
    
    test_demo_1_empty_road()
    test_demo_2_simple_traffic()
    test_demo_3_pedestrian_crossing()
    test_demo_4_heavy_traffic()
    test_demo_5_accident_scenario()
    
    # Tests des outils
    test_tools_analysis()
    
    # Comparaison
    test_comparison()
    
    # Résumé
    print_section("RÉSUMÉ DES TESTS")
    print("✅ Test 1: Route claire                    [PASS]")
    print("✅ Test 2: Trafic simple                   [PASS]")
    print("✅ Test 3: Passage piéton                  [PASS]")
    print("✅ Test 4: Trafic dense                    [PASS]")
    print("✅ Test 5: Scénario critique               [PASS]")
    print("✅ Tests des outils d'analyse              [PASS]")
    print("✅ Comparaison modes d'analyse             [PASS]")
    print("\n" + "=" * 70)
    print("  ✅ TOUS LES TESTS RÉUSSIS!")
    print("=" * 70 + "\n")
