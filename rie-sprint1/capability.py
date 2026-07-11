"""Capability Detection - Detect repository capabilities."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


CAPABILITY_SIGNATURES: Dict[str, List[str]] = {
    "Code Generation": ["code generation", "template", "scaffold", "generator"],
    "Code Analysis": ["lint", "static analysis", "ast", "parser", "analyzer"],
    "Code Review": ["review", "pull request", "pr", "comment"],
    "Repository Analysis": ["repository", "repo", "git", "vcs"],
    "API Development": ["api", "rest", "graphql", "endpoint", "router"],
    "CLI Development": ["cli", "command", "argparse", "click", "typer"],
    "Testing": ["test", "unittest", "pytest", "jest", "mocha", "testing"],
    "Documentation": ["docs", "readme", "docstring", "swagger", "openapi"],
    "Containerization": ["docker", "container", "dockerfile", "containerize"],
    "CI/CD": ["ci", "cd", "pipeline", "github action", "jenkins", "gitlab ci"],
    "Monitoring": ["monitor", "metrics", "dashboard", "grafana", "prometheus"],
    "Security": ["security", "vulnerability", "secret", "auth", "oauth"],
}


@dataclass
class Capability:
    """A detected capability."""
    name: str
    confidence: float
    evidence_count: int = 0


class CapabilityDetector:
    """Detects repository capabilities."""
    
    def detect(self, files: List[Dict[str, Any]], dependencies: List[str] = None) -> List[Capability]:
        """Detect capabilities from files and dependencies."""
        capabilities: List[Capability] = []
        all_text = " ".join([f.get("name", "") + " " + f.get("path", "") for f in files]).lower()
        
        if dependencies:
            all_text += " " + " ".join(dependencies).lower()
        
        for capability_name, signatures in CAPABILITY_SIGNATURES.items():
            count = 0
            for sig in signatures:
                count += all_text.count(sig.lower())
            
            if count > 0:
                confidence = min(1.0, count / 10.0 + 0.5)
                capabilities.append(Capability(
                    name=capability_name,
                    confidence=confidence,
                    evidence_count=count,
                ))
        
        return capabilities


class CapabilityAnalyzer:
    """Analyzes capabilities in detail."""
    
    def __init__(self):
        self.detector = CapabilityDetector()
    
    def analyze(self, files: List[Dict[str, Any]], dependencies: List[str] = None) -> List[Capability]:
        """Analyze capabilities."""
        return self.detector.detect(files, dependencies)
    
    def get_top_capabilities(self, capabilities: List[Capability], limit: int = 5) -> List[Capability]:
        """Get top capabilities by confidence."""
        return sorted(capabilities, key=lambda c: c.confidence, reverse=True)[:limit]
