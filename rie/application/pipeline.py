"""RIE Pipeline - Main analysis pipeline."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from ..domain.repository import Repository
from ..domain.repository_dna import RepositoryDNA, DNAVersion
from ..detectors.base_detector import BaseDetector, DetectionResult
from ..detectors.language_detector import LanguageDetector
from ..detectors.framework_detector import FrameworkDetector
from ..detectors.ai_detector import AIStackDetector
from ..detectors.capability_detector import CapabilityDetector
from ..detectors.architecture_detector import ArchitectureDetector


class PipelineStage:
    """A stage in the pipeline."""
    
    def __init__(self, name: str, detector: BaseDetector):
        self.name = name
        self.detector = detector
        self.result: Optional[DetectionResult] = None
    
    def run(self, repo: Repository) -> DetectionResult:
        self.result = self.detector.run(repo)
        return self.result


@dataclass
class PipelineResult:
    """Result of running the pipeline."""
    pipeline_id: str
    repo_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    stages: List[Dict[str, Any]] = field(default_factory=list)
    dna: Optional[RepositoryDNA] = None
    success: bool = True
    error: Optional[str] = None


class RIEPipeline:
    """
    Repository Intelligence Engine Pipeline.
    
    Pipeline Steps:
    1. Fetch - Clone repository
    2. Normalize - Convert to universal format
    3. Discover - Find files and directories
    4. Detect - Run all detectors
    5. Extract - Extract features
    6. Analyze - Aggregate features
    7. Score - Calculate scores
    8. Generate - Create RepositoryDNA v2
    """
    
    def __init__(self):
        self.pipeline_id = str(uuid.uuid4())
        self.stages: List[PipelineStage] = []
        self._setup_stages()
    
    def _setup_stages(self) -> None:
        """Set up pipeline stages with detectors."""
        self.stages = [
            PipelineStage("Language Detection", LanguageDetector()),
            PipelineStage("Framework Detection", FrameworkDetector()),
            PipelineStage("AI Stack Detection", AIStackDetector()),
            PipelineStage("Capability Detection", CapabilityDetector()),
            PipelineStage("Architecture Detection", ArchitectureDetector()),
        ]
    
    def run(self, repo: Repository) -> PipelineResult:
        """Run the full pipeline."""
        started_at = datetime.utcnow()
        
        result = PipelineResult(
            pipeline_id=str(uuid.uuid4()),
            repo_id=repo.repo_id,
            started_at=started_at,
        )
        
        try:
            for stage in self.stages:
                stage_result = stage.run(repo)
                result.stages.append({
                    "stage_name": stage.name,
                    "detected": stage_result.detected,
                    "confidence": stage_result.confidence,
                    "data": stage_result.data,
                })
            
            result.completed_at = datetime.utcnow()
            result.success = True
        
        except Exception as e:
            result.completed_at = datetime.utcnow()
            result.success = False
            result.error = str(e)
        
        return result
    
    def get_detectors(self) -> List[BaseDetector]:
        """Get all detectors in the pipeline."""
        return [stage.detector for stage in self.stages]
