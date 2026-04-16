"""
Contrats de service pour l'execution du pipeline.
"""

from typing import BinaryIO, Protocol

from pipeline.schema import PipelineOutput


class PipelineRunner(Protocol):
    def run_pipeline(self, uploaded_file: BinaryIO) -> PipelineOutput:
        ...
