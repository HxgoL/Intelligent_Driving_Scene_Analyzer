"""
Couche de service

intermediaire entre ui et pipeline metier


TODO: gestion d'erreurs, cache, logs, mesures de tmemps, choix de pipelines

"""

from typing import BinaryIO

from pipeline.orchestrator import PipelineOrchestrator
from pipeline.schema import PipelineOutput
from App.services.pipeline_contracts import PipelineRunner


def get_default_runner() -> PipelineRunner:
    return PipelineOrchestrator()


def run_analysis(
    uploaded_file: BinaryIO,
    runner: PipelineRunner | None = None,
) -> PipelineOutput:
    uploaded_file.seek(0)
    pipeline_runner = runner or get_default_runner()
    return pipeline_runner.run_pipeline(uploaded_file)

