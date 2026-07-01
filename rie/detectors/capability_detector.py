"""Capability Detector - Detects repository capabilities."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

from rie.detectors import DetectorContext, DetectorResult, IDetector


@dataclass
class CapabilityFeatureSet:
    """Detected capabilities."""
    repository_analysis: float = 0.0  # 0.0 - 1.0 confidence
    code_generation: float = 0.0
    code_review: float = 0.0
    refactoring: float = 0.0
    planning: float = 0.0
    testing: float = 0.0
    deployment: float = 0.0
    documentation: float = 0.0
    debugging: float = 0.0
    git_operations: float = 0.0
    browser_automation: float = 0.0
    filesystem_operations: float = 0.0
    container_operations: float = 0.0
    terminal_operations: float = 0.0
    api_integration: float = 0.0
    
    # Evidence sources
    evidence: Dict[str, List[str]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "capabilities": {
                "repository_analysis": self.repository_analysis,
                "code_generation": self.code_generation,
                "code_review": self.code_review,
                "refactoring": self.refactoring,
                "planning": self.planning,
                "testing": self.testing,
                "deployment": self.deployment,
                "documentation": self.documentation,
                "debugging": self.debugging,
                "git_operations": self.git_operations,
                "browser_automation": self.browser_automation,
                "filesystem_operations": self.filesystem_operations,
                "container_operations": self.container_operations,
                "terminal_operations": self.terminal_operations,
                "api_integration": self.api_integration,
            },
            "evidence": self.evidence
        }


class CapabilityDetector(IDetector):
    """
    Detects repository capabilities.
    
    Rules:
    ✅ Evidence Based
    ✅ Confidence Score
    ✅ Multiple Evidence Sources
    """
    
    # Evidence patterns for capabilities
    EVIDENCE_PATTERNS = {
        "repository_analysis": {
            "files": ["git", "repository", "repo", "clone"],
            "patterns": ["git clone", "git remote", "github api"],
            "weight": 1.0
        },
        "code_generation": {
            "files": ["template", "generator", "scaffold", "boilerplate"],
            "patterns": ["def generate", "class Generator", "template.render"],
            "weight": 1.0
        },
        "code_review": {
            "files": ["lint", "review", "static", "eslint", "prettier"],
            "patterns": ["flake8", "pylint", "eslint", "prettier"],
            "weight": 1.0
        },
        "refactoring": {
            "files": ["refactor", "transform", "rewrite"],
            "patterns": ["AST", "transform", "modify"],
            "weight": 1.0
        },
        "planning": {
            "files": ["planner", "plan", "scheduler"],
            "patterns": ["def plan", "create_plan", "TaskGraph"],
            "weight": 1.0
        },
        "testing": {
            "files": ["test", "spec", "__tests__", "pytest", "unittest"],
            "patterns": ["def test_", "describe(", "it(", "test_", "TestCase"],
            "weight": 1.0
        },
        "deployment": {
            "files": ["docker", "deploy", "ci", "cd", "pipeline", "workflow"],
            "patterns": ["dockerfile", "docker-compose", "kubectl", "helm"],
            "weight": 1.0
        },
        "documentation": {
            "files": ["docs", "readme", "changelog", "contributing"],
            "patterns": ["# Documentation", "docstring", "swagger", "openapi"],
            "weight": 1.0
        },
        "debugging": {
            "files": ["debug", "trace", "log", "pdb", "debugger"],
            "patterns": ["pdb.set_trace", "breakpoint()", "logging.debug"],
            "weight": 1.0
        },
        "git_operations": {
            "files": ["git"],
            "patterns": ["git add", "git commit", "git push", "git pull", "GitPython"],
            "weight": 1.0
        },
        "browser_automation": {
            "files": ["browser", "selenium", "playwright", "puppeteer"],
            "patterns": ["selenium", "playwright", "puppeteer", "webdriver"],
            "weight": 1.0
        },
        "filesystem_operations": {
            "files": [],
            "patterns": ["os.path", "pathlib", "open(", "shutil"],
            "weight": 0.5
        },
        "container_operations": {
            "files": ["docker", "container", "podman"],
            "patterns": ["docker", "container", "FROM", "dockerfile"],
            "weight": 1.0
        },
        "terminal_operations": {
            "files": ["shell", "terminal", "subprocess"],
            "patterns": ["subprocess", "os.system", "shell=True", "pty"],
            "weight": 1.0
        },
        "api_integration": {
            "files": ["api", "client", "sdk", "rest", "graphql"],
            "patterns": ["@app.route", "FastAPI", "Express", "router", "endpoint"],
            "weight": 1.0
        },
    }
    
    @property
    def name(self) -> str:
        return "CapabilityDetector"
    
    @property
    def description(self) -> str:
        return "Detects repository capabilities"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        import time
        start = time.time()
        
        detected = CapabilityFeatureSet()
        
        for capability, patterns in self.EVIDENCE_PATTERNS.items():
            confidence, evidence = self._detect_capability(context, patterns)
            setattr(detected, capability, confidence)
            detected.evidence[capability] = evidence
        
        duration_ms = int((time.time() - start) * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features=detected.to_dict(),
            duration_ms=duration_ms
        )
    
    def _detect_capability(
        self, 
        context: DetectorContext, 
        patterns: Dict
    ) -> tuple:
        """Detect a capability with confidence score."""
        evidence = []
        score = 0.0
        
        # Check file names
        for pattern in patterns.get("files", []):
            for path in context.files.keys():
                if pattern.lower() in path.lower():
                    evidence.append(f"file:{path}")
                    score += 1.0
        
        # Check patterns in file contents
        for pattern in patterns.get("patterns", []):
            for path in context.files.keys():
                if pattern.lower() in path.lower():
                    evidence.append(f"pattern:{path}")
                    score += 1.0
        
        # Normalize score
        weight = patterns.get("weight", 1.0)
        max_score = 5.0
        confidence = min(score / max_score, 1.0) * weight
        
        return confidence, evidence[:10]  # Limit evidence
    
    def get_top_capabilities(self, features: CapabilityFeatureSet, limit: int = 5) -> List[tuple]:
        """Get top capabilities by confidence."""
        capabilities = [
            ("repository_analysis", features.repository_analysis),
            ("code_generation", features.code_generation),
            ("code_review", features.code_review),
            ("refactoring", features.refactoring),
            ("planning", features.planning),
            ("testing", features.testing),
            ("deployment", features.deployment),
            ("documentation", features.documentation),
            ("debugging", features.debugging),
            ("git_operations", features.git_operations),
            ("browser_automation", features.browser_automation),
            ("filesystem_operations", features.filesystem_operations),
            ("container_operations", features.container_operations),
            ("terminal_operations", features.terminal_operations),
            ("api_integration", features.api_integration),
        ]
        
        return sorted(capabilities, key=lambda x: x[1], reverse=True)[:limit]
