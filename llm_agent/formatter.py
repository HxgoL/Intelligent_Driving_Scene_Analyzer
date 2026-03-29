# llm_agent/formatter.py

from __future__ import annotations

from typing import Any, Dict, List


def _scene_summary(payload: Dict[str, Any]) -> str:
    detections = payload.get("detections", [])
    scene_context = payload.get("scene_context", {})

    weather = scene_context.get("weather", "inconnu")
    time_of_day = scene_context.get("time_of_day", "inconnu")
    location_type = scene_context.get("location_type", "inconnu")

    if not detections:
        return (
            f"Scène {location_type}, moment: {time_of_day}, météo: {weather}. "
            "Aucun objet significatif détecté."
        )

    counts: Dict[str, int] = {}
    for det in detections:
        label = str(det.get("label", "unknown"))
        counts[label] = counts.get(label, 0) + 1

    parts = [f"{count} {label}" for label, count in counts.items()]
    objects_text = ", ".join(parts)

    return (
        f"Scène {location_type}, moment: {time_of_day}, météo: {weather}. "
        f"Objets détectés : {objects_text}."
    )


def _recommendations(payload: Dict[str, Any], risk_level: str) -> List[str]:
    detections = payload.get("detections", [])
    labels = {str(det.get('label', '')).lower() for det in detections}

    recommendations: List[str] = []

    if risk_level in {"ÉLEVÉ", "CRITIQUE"}:
        recommendations.append("Réduire immédiatement la vitesse et renforcer la vigilance.")
    elif risk_level == "MOYEN":
        recommendations.append("Adapter la vitesse aux conditions de circulation.")

    if "pedestrian" in labels or "person" in labels:
        recommendations.append("Surveiller attentivement les piétons à proximité.")

    if "truck" in labels or "bus" in labels:
        recommendations.append("Augmenter la distance de sécurité avec les gros véhicules.")

    weather = str(payload.get("scene_context", {}).get("weather", "")).lower()
    if weather in {"rain", "fog", "storm"}:
        recommendations.append("Anticiper un freinage plus long à cause des conditions météo.")

    if not recommendations:
        recommendations.append("Poursuivre la conduite avec vigilance normale.")

    return recommendations[:3]


def format_report(
    payload: Dict[str, Any],
    risk_result: Dict[str, Any],
) -> str:
    """
    Produit un rapport texte simple pour semaine 1.
    Pas encore de vrai appel LLM ici : c'est un prototype déterministe.
    """
    scene_text = _scene_summary(payload)
    risk_level = risk_result.get("risk_level", "INCONNU")
    score = risk_result.get("score", 0)
    reasoning = risk_result.get("reasoning", [])
    recommendations = _recommendations(payload, risk_level)

    reasoning_text = ""
    if reasoning:
        reasoning_text = "\n".join(f"- {reason}" for reason in reasoning[:6])
    else:
        reasoning_text = "- Aucune justification disponible."

    recommendations_text = "\n".join(f"- {rec}" for rec in recommendations)

    return (
        "=== RAPPORT D'ANALYSE DE SCÈNE ===\n\n"
        f"Résumé de la scène :\n{scene_text}\n\n"
        f"Niveau de risque : {risk_level}\n"
        f"Score de risque : {score}\n\n"
        "Justification :\n"
        f"{reasoning_text}\n\n"
        "Recommandations :\n"
        f"{recommendations_text}\n"
    )
