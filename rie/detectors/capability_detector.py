"""Capability Detector - Detect repository capabilities."""
from typing import Dict, List, Set

from ..domain.repository import Repository, FileInfo
from ..domain.evidence import Evidence
from .base_detector import BaseDetector, DetectionResult


CAPABILITY_SIGNATURES: Dict[str, List[str]] = {
    "Code Generation": ["code generation", "code gen", "template", "scaffold"],
    "Code Analysis": ["lint", "static analysis", "ast", "parser"],
    "Code Review": ["review", "pull request", "comment"],
    "Repository Analysis": ["repository", "repo", "git analysis"],
    "Dependency Management": ["dependency", "package", "requirement"],
    "Testing": ["test", "unittest", "pytest", "jest", "mocha"],
    "Documentation": ["docs", "readme", "docstring", "swagger"],
    "API Development": ["api", "rest", "graphql", "endpoint"],
    "CLI Development": ["cli", "command", "argparse", "click"],
    "Containerization": ["docker", "container", "dockerfile"],
    "CI/CD": ["ci", "cd", "pipeline", "github action", "jenkins"],
    "Monitoring": ["monitor", "metrics", "dashboard", "grafana"],
    "Security": ["security", "vulnerability", "sast", "secret"],
}


class CapabilityDetector(BaseDetector):
    """Detects repository capabilities."""
    
    def detect(self, repo: Repository) -> DetectionResult:
        """Detect capabilities by file patterns and dependencies."""
        detected_capabilities: List[Dict[str, any]] = []
        evidence_list: List[Evidence] = []
        
        all_text = " ".join([
            f.name + " " + f.path
            for f in repo.files
        ]).lower()
        
        for capability, signatures in CAPABILITY_SIGNATURES.items():
            for sig in signatures:
                if sig.lower() in all_text:
                    detected_capabilities.append({
                        "name": capability,
                        "confidence": 0.8,
                        "evidence_count": all_text.count(sig.lower()),
                    })
                    evidence_list.append(Evidence(
                        file_path=f"Detected in {len(repo.files)} files",
                        content=f"Signature: {sig}",
                        confidence=0.8,
                    ))
                    break
        
        confidence = 1.0 if len(detected_capabilities) > 0 else 0.0
        
        return DetectionResult(
            detector_name="CapabilityDetector",
            detected=len(detected_capabilities) > 0,
            confidence=confidence,
            data={
                "capabilities": detected_capabilities,
                "count": len(detected_capabilities),
            },
            evidence=evidence_list,
        )
