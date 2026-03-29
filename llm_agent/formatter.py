def format_report(risk, detections):
    analysis = []
    recommendations = []

    for obj in detections["objects"]:
        if obj["label"] == "pedestrian":
            analysis.append("Présence de piéton")
            recommendations.append("Ralentir et surveiller")

        if obj["label"] == "car":
            analysis.append("Véhicule à proximité")

    return {
        "risk": risk,
        "analysis": ", ".join(analysis),
        "recommendations": ", ".join(recommendations)
    }
