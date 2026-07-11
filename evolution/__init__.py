"""AGOS Evolution Platform - Self-evolving and self-improving system."""

from .pipeline import EvolutionPipeline, PipelineStage, PipelineStageType, StageStatus, EvolutionResult
from .engine import EvolutionEngine, GeneticAlgorithm, Chromosome, Population, SelectionMethod
from .batch_processing import BatchProcessor, BatchJob, BatchStatus

__all__ = [
    "EvolutionPipeline", "PipelineStage", "PipelineStageType", "StageStatus", "EvolutionResult",
    "EvolutionEngine", "GeneticAlgorithm", "Chromosome", "Population", "SelectionMethod",
    "BatchProcessor", "BatchJob", "BatchStatus",
]

__version__ = "1.0.0"
