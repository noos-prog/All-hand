"""RIE Domain - Core domain models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Repository:
    """Repository domain object."""
    url: str
    name: str = ""
    owner: str = ""
    branch: str = "main"
    commit: str = ""
    local_path: str = ""


@dataclass
class FileNode:
    """File or directory node."""
    path: str
    is_dir: bool
    size: int = 0
    content: Optional[str] = None
    extension: str = ""


@dataclass
class DetectionResult:
    """Result from a detector."""
    detector_name: str
    detected: bool
    confidence: float = 1.0
    data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


@dataclass
class Feature:
    """A detected feature."""
    name: str
    category: str
    value: Any
    confidence: float = 1.0
    source: str = ""


@dataclass
class AnalysisContext:
    """Context for analysis."""
    repository: Repository
    files: List[FileNode] = field(default_factory=list)
    features: List[Feature] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    def add_feature(self, feature: Feature) -> None:
        """Add a feature."""
        self.features.append(feature)
    
    def get_features_by_category(self, category: str) -> List[Feature]:
        """Get features by category."""
        return [f for f in self.features if f.category == category]
