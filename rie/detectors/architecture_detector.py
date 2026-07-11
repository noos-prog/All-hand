"""Architecture Detector - Detect architecture patterns."""
from typing import Dict, List, Set

from ..domain.repository import Repository, DirectoryInfo
from ..domain.evidence import Evidence
from .base_detector import BaseDetector, DetectionResult


ARCHITECTURE_PATTERNS: Dict[str, Dict[str, any]] = {
    "Microservices": {
        "directories": ["services", "microservices", "apis"],
        "confidence_boost": 0.3,
    },
    "Monolithic": {
        "directories": ["app", "src", "lib"],
        "confidence_boost": 0.2,
    },
    "Layered": {
        "directories": ["layers", "tiers", "domain", "presentation", "infrastructure"],
        "confidence_boost": 0.3,
    },
    "Modular": {
        "directories": ["modules", "components", "packages", "plugins"],
        "confidence_boost": 0.3,
    },
    "Event-Driven": {
        "directories": ["events", "handlers", "listeners", "queues"],
        "confidence_boost": 0.3,
    },
    "Clean Architecture": {
        "directories": ["entities", "usecases", "interfaces", "adapters"],
        "confidence_boost": 0.4,
    },
    "Hexagonal": {
        "directories": ["ports", "adapters", "core", "application"],
        "confidence_boost": 0.4,
    },
    "MVC": {
        "directories": ["models", "views", "controllers"],
        "confidence_boost": 0.3,
    },
    "MVVM": {
        "directories": ["models", "views", "viewmodels"],
        "confidence_boost": 0.3,
    },
    "DDD": {
        "directories": ["domain", "application", "infrastructure", "bounded"],
        "confidence_boost": 0.4,
    },
}


class ArchitectureDetector(BaseDetector):
    """Detects architecture patterns."""
    
    def detect(self, repo: Repository) -> DetectionResult:
        """Detect architecture by directory structure."""
        detected_patterns: List[Dict[str, any]] = []
        evidence_list: List[Evidence] = []
        
        dir_names = set(d.name.lower() for d in repo.directories)
        
        for pattern_name, pattern_info in ARCHITECTURE_PATTERNS.items():
            matches = 0
            for dir_pattern in pattern_info["directories"]:
                if any(dir_pattern in d for d in dir_names):
                    matches += 1
            
            if matches > 0:
                confidence = min(1.0, (matches / len(pattern_info["directories"])) + pattern_info["confidence_boost"])
                detected_patterns.append({
                    "pattern": pattern_name,
                    "confidence": confidence,
                    "matches": matches,
                })
                evidence_list.append(Evidence(
                    file_path=f"Directory structure",
                    content=f"Matched {matches}/{len(pattern_info['directories'])} patterns",
                    confidence=confidence,
                ))
        
        confidence = 1.0 if len(detected_patterns) > 0 else 0.0
        
        return DetectionResult(
            detector_name="ArchitectureDetector",
            detected=len(detected_patterns) > 0,
            confidence=confidence,
            data={
                "patterns": detected_patterns,
                "count": len(detected_patterns),
            },
            evidence=evidence_list,
        )
