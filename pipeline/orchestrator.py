from PIL import Image

from Intelligent_Driving_Scene_Analyzer.pipeline.schema import PipelineOutput
from Intelligent_Driving_Scene_Analyzer.pipeline.preprocess import preprocess_image
from Intelligent_Driving_Scene_Analyzer.cv_module.infer import run_inference


# Test a enlever apres
from Intelligent_Driving_Scene_Analyzer.pipeline.schema import SceneDetections, DetectedObject, BoundingBox, RisqueEvaluation, AnalyseResultat

class PipelineOrchestrator:

    """
    Coordonne le pipeline en orchestrant les différentes étapes:
    1) image recue de l'interface
    2) pretraitement de l'image preprocess.py
    
    3) détection d'objets avec cv_module/infer.py et le mockDetector
    
    4) adaptation format sortie agent LLM avec adapters.py
    
    (5) context )
    7) rapport final avec ?
    """

    def __init__(self):
        pass

    def run_pipeline(self, uploaded_image) -> PipelineOutput:
        #1) image recue de l'interface
        image = Image.open(uploaded_image)

        #2) pretraitement de l'image preprocess.py
        image_traitée = preprocess_image(image)

        #3) détection de la scene avec cv_module/infer.py 
        scene_detection = run_inference(image_traitée)

        #4) adaptation format sortie agent LLM avec adapters.py (mock)
        # agent_input = adapt_detections_for_llm(scene_detection) avec la classe adapers.py
        # analyse_resultat = run_scene_analysis(agent_input) avec la classe agent.py
        
        risque = RisqueEvaluation(risque_level="Moyen")

        analyse_resultat = AnalyseResultat(
            resume="Scène avec plusieurs véhicules, piétons présents, conditions de visibilité moyennes.",
            recommandations=[
                "Ralentir et rester vigilant aux piétons.",
                "Maintenir une distance de sécurité avec les véhicules devant.",
                "Éviter les changements de voie brusques."
            ],
            risque_eval=risque
        )


        #7) rapport final
        pipeline_output = PipelineOutput(
            scene_detections=scene_detection,
            analyse_resultat=analyse_resultat
        )

        return pipeline_output

