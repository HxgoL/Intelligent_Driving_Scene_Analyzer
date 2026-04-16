"""
Couche de service

intermediaire entre ui et pipeline metier


TODO: gestion d'erreurs, cache, logs, mesures de tmemps, choix de pipelines

"""

from pipeline.orchestrator import PipelineOrchestrator
from pipeline.schema import PipelineOutput

def run_analysis(uploaded_file) -> PipelineOutput:
    uploaded_file.seek(0)
    orchestrator = PipelineOrchestrator()
    return orchestrator.run_pipeline(uploaded_file)

