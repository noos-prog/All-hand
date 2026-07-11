"""Repository Intelligence Engine (RIE) - Analyze repositories and generate Repository DNA."""
from .domain.repository_dna import RepositoryDNA, DNASection
from .domain.repository import Repository
from .domain.scores import QualityScores, ProductionReadiness
from .application.pipeline import RIEPipeline
from .application.dna_generator import DNAGenerator
from .application.scoring import ScoringEngine
from .detectors.base_detector import BaseDetector
from .detectors.language_detector import LanguageDetector
from .detectors.framework_detector import FrameworkDetector
from .detectors.ai_detector import AIStackDetector
from .detectors.capability_detector import CapabilityDetector
from .detectors.architecture_detector import ArchitectureDetector

__all__ = [
    "RepositoryDNA", "DNASection",
    "Repository",
    "QualityScores", "ProductionReadiness",
    "RIEPipeline",
    "DNAGenerator",
    "ScoringEngine",
    "BaseDetector",
    "LanguageDetector",
    "FrameworkDetector",
    "AIStackDetector",
    "CapabilityDetector",
    "ArchitectureDetector",
]

__version__ = "2.0.0"
