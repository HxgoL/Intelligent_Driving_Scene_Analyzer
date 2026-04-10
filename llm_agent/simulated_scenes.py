"""
simulated_scenes.py - Scènes routières simulées pour tester le LLM
"""

from pipeline.schema import SceneDetections, DetectedObject, BoundingBox


class SimulatedDrivingScenes:
    """Collection de scènes routières simulées"""
    
    @staticmethod
    def clear_road() -> SceneDetections:
        """Route complètement dégagée - Risque FAIBLE"""
        return SceneDetections(detected_objects=[])
    
    @staticmethod
    def pedestrian_crossing() -> SceneDetections:
        """Traversée de piétons - Risque ÉLEVÉ"""
        return SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="person",
                    confidence=0.96,
                    bounding_box=BoundingBox(x=250, y=350, width=50, height=120)
                ),
                DetectedObject(
                    label="person",
                    confidence=0.94,
                    bounding_box=BoundingBox(x=320, y=360, width=45, height=115)
                ),
            ]
        )
    
    @staticmethod
    def heavy_traffic() -> SceneDetections:
        """Circulation dense - Risque ÉLEVÉ"""
        return SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="car",
                    confidence=0.97,
                    bounding_box=BoundingBox(x=100, y=120, width=130, height=110)
                ),
                DetectedObject(
                    label="truck",
                    confidence=0.96,
                    bounding_box=BoundingBox(x=280, y=100, width=180, height=140)
                ),
                DetectedObject(
                    label="car",
                    confidence=0.94,
                    bounding_box=BoundingBox(x=500, y=150, width=130, height=110)
                ),
            ]
        )
    
    @staticmethod
    def school_zone() -> SceneDetections:
        """Zone scolaire avec enfants - Risque CRITIQUE"""
        return SceneDetections(
            detected_objects=[
                DetectedObject(
                    label="person",
                    confidence=0.98,
                    bounding_box=BoundingBox(x=200, y=320, width=40, height=100)
                ),
                DetectedObject(
                    label="person",
                    confidence=0.97,
                    bounding_box=BoundingBox(x=300, y=330, width=40, height=100)
                ),
                DetectedObject(
                    label="person",
                    confidence=0.96,
                    bounding_box=BoundingBox(x=380, y=310, width=40, height=100)
                ),
            ]
        )
    
    @staticmethod
    def all_scenes():
        """Toutes les scènes disponibles"""
        return {
            "clear_road": SimulatedDrivingScenes.clear_road(),
            "pedestrian_crossing": SimulatedDrivingScenes.pedestrian_crossing(),
            "heavy_traffic": SimulatedDrivingScenes.heavy_traffic(),
            "school_zone": SimulatedDrivingScenes.school_zone(),
        }
    
    @staticmethod
    def get_scene_by_name(name: str) -> SceneDetections:
        """Retourne une scène par son nom"""
        scenes = SimulatedDrivingScenes.all_scenes()
        if name not in scenes:
            raise ValueError(f"Scène inconnue: {name}. Disponibles: {list(scenes.keys())}")
        return scenes[name]
