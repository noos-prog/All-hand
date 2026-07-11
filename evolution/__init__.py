"""AGOS Evolution Platform - Self-evolving and self-improving system."""

from .runtime import ContinuousEvolutionRuntime, Evolution, EvolutionScheduler, EvolutionPlanner
from .expansion import InfiniteExpansionFramework, UniversalAdapterFactory, UniversalExtensionRuntime
from .knowledge import KnowledgeEvolution, KnowledgeUpdater
from .memory import MemoryEvolution, MemoryOptimizer
from .agent_adapter import AgentEvolution, AgentAdapter
from .pipeline import (
    EvolutionPipeline, PipelineStage, PipelineStageType, StageStatus, EvolutionResult,
    create_evolution_pipeline
)
from .engine import (
    EvolutionEngine, GeneticAlgorithm, Chromosome, Population, SelectionMethod,
    create_evolution_engine
)
from .batch_processing import (
    BatchProcessor, BatchJob, BatchStatus, BatchPriority, BatchProgress,
    BatchMetrics, create_batch_processor
)

__all__ = [
    # Runtime
    "ContinuousEvolutionRuntime", "Evolution", "EvolutionScheduler", "EvolutionPlanner",
    # Expansion
    "InfiniteExpansionFramework", "UniversalAdapterFactory", "UniversalExtensionRuntime",
    # Knowledge
    "KnowledgeEvolution", "KnowledgeUpdater",
    # Memory
    "MemoryEvolution", "MemoryOptimizer",
    # Agent
    "AgentEvolution", "AgentAdapter",
    # Pipeline
    "EvolutionPipeline", "PipelineStage", "PipelineStageType", "StageStatus", "EvolutionResult",
    "create_evolution_pipeline",
    # Engine
    "EvolutionEngine", "GeneticAlgorithm", "Chromosome", "Population", "SelectionMethod",
    "create_evolution_engine",
    # Batch
    "BatchProcessor", "BatchJob", "BatchStatus", "BatchPriority", "BatchProgress",
    "BatchMetrics", "create_batch_processor",
]

__version__ = "1.0.0"
