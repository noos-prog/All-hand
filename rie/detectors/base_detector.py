"""Base Detector - Abstract base for all detectors."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid

from ..domain.evidence import Evidence
from ..domain.repository import Repository


@dataclass
class DetectionResult:
    """Result of a detection."""
    detector_name: str
    detected: bool
    confidence: float = 0.0
    data: Dict[str, Any] = field(default_factory=dict)
    evidence: List[Evidence] = field(default_factory=list)
    
    def is_confident(self, threshold: float = 0.7) -> bool:
        return self.detected and self.confidence >= threshold


class BaseDetector(ABC):
    """Abstract base class for all detectors."""
    
    def __init__(self):
        self.detector_id = str(uuid.uuid4())
        self.detector_name = self.__class__.__name__
    
    @abstractmethod
    def detect(self, repo: Repository) -> DetectionResult:
        """Detect patterns in the repository."""
        pass
    
    def run(self, repo: Repository) -> DetectionResult:
        """Run the detector with error handling."""
        try:
            return self.detect(repo)
        except Exception as e:
            return DetectionResult(
                detector_name=self.detector_name,
                detected=False,
                confidence=0.0,
                data={"error": str(e)},
            )
    
    def get_metadata(self) -> Dict[str, Any]:
        return {
            "detector_id": self.detector_id,
            "detector_name": self.detector_name,
            "detector_class": self.__class__.__name__,
        }
