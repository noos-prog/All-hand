"""
Foundation Capabilities
PHASE-02: Foundation Civilization

Foundation Capabilities:
- Repository Analysis
- Architecture Analysis
- Dependency Analysis
- Code Quality Analysis
- Documentation Analysis
- Security Analysis
- Performance Analysis
- Knowledge Extraction
- Repository DNA
- Engineering Reporting
"""

__version__ = "2.0.0"

from agos_kernel.civilization.capabilities.repository_analysis import RepositoryAnalyzer
from agos_kernel.civilization.capabilities.architecture_analysis import ArchitectureAnalyzer
from agos_kernel.civilization.capabilities.dependency_analysis import DependencyAnalyzer
from agos_kernel.civilization.capabilities.code_quality import CodeQualityAnalyzer
from agos_kernel.civilization.capabilities.documentation_analysis import DocAnalyzer
from agos_kernel.civilization.capabilities.security_analysis import SecurityAnalyzer
from agos_kernel.civilization.capabilities.knowledge_extraction import KnowledgeExtractor
from agos_kernel.civilization.capabilities.repository_dna import RepositoryDNA
from agos_kernel.civilization.capabilities.engineering_report import EngineeringReporter

__all__ = [
    'RepositoryAnalyzer',
    'ArchitectureAnalyzer',
    'DependencyAnalyzer',
    'CodeQualityAnalyzer',
    'DocAnalyzer',
    'SecurityAnalyzer',
    'KnowledgeExtractor',
    'RepositoryDNA',
    'EngineeringReporter',
]
