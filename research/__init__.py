"""AGOS Research - Research platform for AGOS evolution."""
from .genome import AgentGenome, GenomeEngine, GenomeAnalyzer
from .simulation import Simulation, SimulationEngine, SimulationResult
from .platform import ResearchPlatform, Experiment, ExperimentResult
from .future import FutureRoadmap, TechnologyPrediction, FutureEngine

__all__ = [
    "AgentGenome", "GenomeEngine", "GenomeAnalyzer",
    "Simulation", "SimulationEngine", "SimulationResult",
    "ResearchPlatform", "Experiment", "ExperimentResult",
    "FutureRoadmap", "TechnologyPrediction", "FutureEngine",
]

__version__ = "1.0.0"
