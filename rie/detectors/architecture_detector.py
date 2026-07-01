"""Architecture Detector - Detects software architecture patterns."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

from rie.detectors import DetectorContext, DetectorResult, IDetector


@dataclass
class ArchitectureFeatureSet:
    """Detected architecture."""
    # Architecture types
    single_agent: bool = False
    multi_agent: bool = False
    workflow_engine: bool = False
    planner: bool = False
    executor: bool = False
    router: bool = False
    memory: bool = False
    event_bus: bool = False
    plugin_system: bool = False
    
    # Architecture patterns
    microservices: bool = False
    monolith: bool = False
    layered: bool = False
    clean: bool = False
    hexagonal: bool = False
    
    # Confidence
    confidence: float = 0.0
    evidence: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "single_agent": self.single_agent,
            "multi_agent": self.multi_agent,
            "workflow_engine": self.workflow_engine,
            "planner": self.planner,
            "executor": self.executor,
            "router": self.router,
            "memory": self.memory,
            "event_bus": self.event_bus,
            "plugin_system": self.plugin_system,
            "microservices": self.microservices,
            "monolith": self.monolith,
            "layered": self.layered,
            "clean": self.clean,
            "hexagonal": self.hexagonal,
            "confidence": self.confidence,
            "evidence": self.evidence
        }


class ArchitectureDetector(IDetector):
    """
    Detects software architecture patterns.
    
    Rules:
    ❌ Never infer without evidence
    """
    
    # Evidence patterns for architecture
    EVIDENCE_PATTERNS = {
        # Agent patterns
        "single_agent": {
            "patterns": ["agent", "Agent", "agent_loop", "run_agent"],
            "files": ["agent.py", "core/agent.py"],
            "weight": 1.0
        },
        "multi_agent": {
            "patterns": ["multi_agent", "MultiAgent", "agent_team", "crew"],
            "files": [],
            "weight": 1.0
        },
        "workflow_engine": {
            "patterns": ["workflow", "Workflow", "pipeline", "Pipeline", "stage", "TaskGraph"],
            "files": ["workflow.py", "pipeline.py"],
            "weight": 1.0
        },
        "planner": {
            "patterns": ["planner", "Planner", "plan", "planning", "TaskPlanner"],
            "files": ["planner.py", "planning.py"],
            "weight": 1.0
        },
        "executor": {
            "patterns": ["executor", "Executor", "execute", "run_task"],
            "files": ["executor.py"],
            "weight": 1.0
        },
        "router": {
            "patterns": ["router", "Router", "route", "dispatcher"],
            "files": ["router.py"],
            "weight": 1.0
        },
        "memory": {
            "patterns": ["memory", "Memory", "context", "history", "conversation"],
            "files": ["memory.py", "context.py"],
            "weight": 0.8
        },
        "event_bus": {
            "patterns": ["event_bus", "EventBus", "event_dispatcher", "pubsub", "PubSub"],
            "files": ["event.py", "events.py", "pubsub.py"],
            "weight": 1.0
        },
        "plugin_system": {
            "patterns": ["plugin", "Plugin", "extension", "hook", "registry"],
            "files": ["plugin.py", "extension.py", "registry.py"],
            "weight": 1.0
        },
        
        # Architecture patterns
        "microservices": {
            "patterns": ["microservice", "service", "api_gateway"],
            "files": ["docker-compose.yml", "Dockerfile"],
            "weight": 1.0
        },
        "layered": {
            "patterns": ["layer", "service", "repository", "dto"],
            "files": ["services/", "repositories/", "models/", "controllers/"],
            "weight": 0.8
        },
        "clean": {
            "patterns": ["domain", "entity", "usecase", "repository"],
            "files": ["domain/", "usecase/", "entities/"],
            "weight": 0.8
        },
        "hexagonal": {
            "patterns": ["adapter", "port", "domain", "infrastructure"],
            "files": ["adapters/", "ports/", "domain/", "infrastructure/"],
            "weight": 0.8
        },
    }
    
    @property
    def name(self) -> str:
        return "ArchitectureDetector"
    
    @property
    def description(self) -> str:
        return "Detects software architecture patterns"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        import time
        start = time.time()
        
        detected = ArchitectureFeatureSet()
        total_evidence = 0
        
        for arch_type, patterns in self.EVIDENCE_PATTERNS.items():
            has_evidence, evidence_list = self._check_pattern(context, patterns)
            if has_evidence:
                setattr(detected, arch_type, True)
                detected.evidence.extend(evidence_list)
                total_evidence += len(evidence_list)
        
        # Calculate confidence based on evidence
        max_evidence = 20
        detected.confidence = min(total_evidence / max_evidence, 1.0)
        
        # Infer monolith if no clear pattern
        if not (detected.microservices or detected.layered or detected.clean or detected.hexagonal):
            detected.monolith = True
        
        duration_ms = int((time.time() - start) * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features=detected.to_dict(),
            duration_ms=duration_ms
        )
    
    def _check_pattern(self, context: DetectorContext, patterns: Dict) -> tuple:
        """Check if pattern exists in context."""
        evidence = []
        
        # Check file names
        for pattern in patterns.get("files", []):
            for path in context.files.keys():
                if pattern.lower() in path.lower():
                    evidence.append(f"file:{path}")
        
        # Check patterns in file paths
        for pattern in patterns.get("patterns", []):
            for path in context.files.keys():
                if pattern.lower() in path.lower():
                    if f"file:{path}" not in evidence:
                        evidence.append(f"file:{path}")
        
        return len(evidence) > 0, evidence[:5]
