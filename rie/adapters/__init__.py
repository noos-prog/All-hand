"""RIE Adapters - Adapters for AGOS Kernel integration."""
from typing import Any

from application import RepositoryIntelligencePipeline, create_rie_pipeline
from contracts import RepositoryDNA


class RIEKernelAdapter:
    """
    Adapter for AGOS Kernel.
    
    Rules:
    ✅ Kernel communicates only through public interfaces
    ✅ No direct RIE access from Kernel
    """
    
    def __init__(self, pipeline: RepositoryIntelligencePipeline = None):
        self._pipeline = pipeline or create_rie_pipeline()
    
    def analyze_repository(self, url: str, branch: str = "main") -> RepositoryDNA:
        """Analyze repository and return DNA."""
        return self._pipeline.execute(url, branch)
    
    def get_capabilities(self) -> dict:
        """Get RIE capabilities."""
        return {
            "name": "RepositoryIntelligence",
            "version": "1.0.0",
            "description": "Analyzes repositories and generates DNA",
            "skills": ["AnalyzeRepository", "GenerateDNA"]
        }
