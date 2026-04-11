"""
tools.py - Fonctions auxiliaires pour l'analyse de scènes routières.
Fournit des utilitaires pour calculer la densité d'objets, le contexte, etc.
"""

from typing import List, Dict, Tuple
from pipeline.schema import SceneDetections, DetectedObject


class SceneAnalysisTools:
    """Outils pour analyser les scènes routières en détail"""

    @staticmethod
    def calculate_object_density(detections: SceneDetections, image_width: float = 640, image_height: float = 480) -> float:
        """
        Calcule la densité d'objets dans la scène.
        Densité = nombre d'objets / surface de l'image
        
        Args:
            detections: Les objets détectés
            image_width: Largeur de l'image (pixels)
            image_height: Hauteur de l'image (pixels)
            
        Returns:
            Densité d'objets (objets par 1000 pixels²)
        """
        if not detections.detected_objects:
            return 0.0
        
        image_area = image_width * image_height
        num_objects = len(detections.detected_objects)
        
        density = (num_objects / image_area) * 1000  # Normalisé pour 1000 pixels²
        return round(density, 3)

    @staticmethod
    def calculate_central_occupancy(detections: SceneDetections, image_width: float = 640, image_height: float = 480, center_zone_ratio: float = 0.3) -> float:
        """
        Calcule le pourcentage de la zone centrale occupée par des objets.
        La zone centrale est la partie "devant" du véhicule.
        
        Args:
            detections: Les objets détectés
            image_width: Largeur de l'image
            image_height: Hauteur de l'image
            center_zone_ratio: Ratio de la zone centrale (0.3 = 30% au centre)
            
        Returns:
            Pourcentage de la zone centrale occupée
        """
        if not detections.detected_objects:
            return 0.0
        
        center_x = image_width / 2
        center_y = image_height * 0.7  # Zone devant (70% vers le bas)
        
        zone_width = image_width * center_zone_ratio
        zone_height = image_height * center_zone_ratio
        
        total_central_area = 0.0
        
        for obj in detections.detected_objects:
            bbox_center_x = obj.bounding_box.x + obj.bounding_box.width / 2
            bbox_center_y = obj.bounding_box.y + obj.bounding_box.height / 2
            
            # Vérifier si l'objet est dans la zone centrale
            if (abs(bbox_center_x - center_x) < zone_width / 2 and 
                abs(bbox_center_y - center_y) < zone_height / 2):
                total_central_area += obj.bounding_box.width * obj.bounding_box.height
        
        zone_area = zone_width * zone_height
        occupancy = (total_central_area / zone_area) * 100 if zone_area > 0 else 0
        
        return round(occupancy, 2)

    @staticmethod
    def get_object_distribution(detections: SceneDetections) -> Dict[str, int]:
        """
        Calcule la distribution des objets par type.
        
        Args:
            detections: Les objets détectés
            
        Returns:
            Dictionnaire {label: count}
        """
        distribution = {}
        for obj in detections.detected_objects:
            label = obj.label.lower()
            distribution[label] = distribution.get(label, 0) + 1
        
        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))

    @staticmethod
    def get_average_confidence(detections: SceneDetections) -> float:
        """
        Calcule la confiance moyenne des détections.
        
        Args:
            detections: Les objets détectés
            
        Returns:
            Confiance moyenne (0-1)
        """
        if not detections.detected_objects:
            return 0.0
        
        total_confidence = sum(obj.confidence for obj in detections.detected_objects)
        avg = total_confidence / len(detections.detected_objects)
        return round(avg, 3)

    @staticmethod
    def identify_critical_objects(detections: SceneDetections, confidence_threshold: float = 0.8) -> List[DetectedObject]:
        """
        Identifie les objets critiques (haute confiance, proche du centre).
        
        Args:
            detections: Les objets détectés
            confidence_threshold: Seuil minimum de confiance
            
        Returns:
            Liste des objets critiques
        """
        critical_objects = []
        image_width, image_height = 640, 480
        center_x = image_width / 2
        center_y = image_height * 0.7
        
        for obj in detections.detected_objects:
            if obj.confidence >= confidence_threshold:
                bbox_center_x = obj.bounding_box.x + obj.bounding_box.width / 2
                bbox_center_y = obj.bounding_box.y + obj.bounding_box.height / 2
                
                # Distance du centre (normalisée)
                distance_ratio = (
                    ((bbox_center_x - center_x) ** 2 + (bbox_center_y - center_y) ** 2) ** 0.5
                ) / (image_width / 2)
                
                # Si proche du centre et haute confiance -> critique
                if distance_ratio < 0.5:
                    critical_objects.append(obj)
        
        return critical_objects

    @staticmethod
    def build_scene_context(detections: SceneDetections) -> str:
        """
        Construit une description textuelle du contexte de la scène.
        Utile pour enrichir le prompt du LLM.
        
        Args:
            detections: Les objets détectés
            
        Returns:
            Description textuelle du contexte
        """
        if not detections.detected_objects:
            return "Route claire, aucun obstacle détecté"
        
        distribution = SceneAnalysisTools.get_object_distribution(detections)
        density = SceneAnalysisTools.calculate_object_density(detections)
        occupancy = SceneAnalysisTools.calculate_central_occupancy(detections)
        
        parts = []
        
        # Description du nombre d'objets
        num_objects = len(detections.detected_objects)
        if num_objects == 1:
            parts.append(f"1 objet détecté")
        elif num_objects <= 3:
            parts.append(f"{num_objects} objets détectés")
        else:
            parts.append(f"{num_objects} objets détectés (forte densité)")
        
        # Description de la distribution
        top_objects = list(distribution.items())[:3]
        object_desc = ", ".join([f"{count} {label}" if count > 1 else label 
                                for label, count in top_objects])
        parts.append(f"Composition: {object_desc}")
        
        # Description de la centralité
        if occupancy > 50:
            parts.append("Nombreux obstacles en zone centrale")
        elif occupancy > 20:
            parts.append("Obstacles modérés en zone centrale")
        
        return " | ".join(parts)

    @staticmethod
    def get_risk_factors_summary(detections: SceneDetections) -> Dict[str, any]:
        """
        Résume les principaux facteurs de risque détectés.
        
        Args:
            detections: Les objets détectés
            
        Returns:
            Dictionnaire avec résumé des facteurs
        """
        critical_objects = SceneAnalysisTools.identify_critical_objects(detections)
        distribution = SceneAnalysisTools.get_object_distribution(detections)
        
        high_risk_labels = ["person", "bicycle", "motorcycle", "obstacle", "debris"]
        high_risk_count = sum(
            count for label, count in distribution.items() 
            if any(risk_label in label.lower() for risk_label in high_risk_labels)
        )
        
        return {
            "total_objects": len(detections.detected_objects),
            "critical_objects_count": len(critical_objects),
            "high_risk_count": high_risk_count,
            "object_distribution": distribution,
            "average_confidence": SceneAnalysisTools.get_average_confidence(detections),
            "central_occupancy_percent": SceneAnalysisTools.calculate_central_occupancy(detections),
        }
