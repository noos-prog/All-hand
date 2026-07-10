"""
AGOS Research Infrastructure (ARI)
==================================

The World's Largest Automated Research Laboratory.

ARI provides:
- Research Data Lake: Repositories, Benchmarks, Providers
- Evaluation Engines: Benchmark, Sandbox, Judge, Evidence
- Discovery Layer: Repository Universe, Capability Library, Golden Tasks
- Analytics: Leaderboards, Reports, Dashboards

Core Principle: "ARI is the source of truth for Core Brain."
"""

from .data_lake.repository import (
    Repository, RepositoryMetrics,
    RepositoryDiscovery, RepositoryAnalyzer
)
from .data_lake.provider import (
    Provider, ProviderMetrics,
    ProviderRegistry, CapabilityMapping
)
from .data_lake.benchmark import (
    Benchmark, BenchmarkResult, BenchmarkSuite,
    BenchmarkRunner, BenchmarkCollector
)
from .data_lake.model import (
    Model, ModelMetrics,
    ModelRegistry, ModelComparison
)
from .evaluation.engine import (
    EvaluationEngine, EvaluationTask, EvaluationResult,
    TaskGenerator, ResultAggregator
)
from .evaluation.sandbox import (
    Sandbox, SandboxFactory, SandboxEnvironment,
    ExecutionResult, SecurityPolicy
)
from .evaluation.judge import (
    JudgeEngine, Judgement, JudgementCriteria,
    JudgeConfig, JudgeResult
)
from .evaluation.genome import (
    GenomeEngine, Genome, Gene,
    GenomeAnalyzer, GenomeMutator
)
from .analytics.leaderboard import (
    Leaderboard, LeaderboardEntry,
    RankingCriteria, RankingEngine
)
from .analytics.reports import (
    Report, ReportGenerator,
    ReportTemplate, ReportPublisher
)

__all__ = [
    # Data Lake
    "Repository",
    "RepositoryMetrics",
    "RepositoryDiscovery",
    "Provider",
    "ProviderMetrics",
    "ProviderRegistry",
    "Benchmark",
    "BenchmarkResult",
    "BenchmarkRunner",
    "Model",
    "ModelRegistry",
    # Evaluation
    "EvaluationEngine",
    "EvaluationTask",
    "EvaluationResult",
    "Sandbox",
    "SandboxFactory",
    "JudgeEngine",
    "Judgement",
    "GenomeEngine",
    "Genome",
    # Analytics
    "Leaderboard",
    "LeaderboardEntry",
    "Report",
    "ReportGenerator",
]

__version__ = "1.0.0"
