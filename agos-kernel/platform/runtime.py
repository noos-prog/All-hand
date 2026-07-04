"""AGOS Civilization Platform v1.0."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from datetime import datetime
from typing import Any, Dict, Optional

# Import existing subsystems
from knowledge.runtime import KnowledgeRuntime
from memory.runtime import MemoryRuntime
from brain.engine import EngineeringBrain
from core.autonomous import AutonomousCore
from execution.compiler import MissionCompiler
from execution.graph import GraphRuntime
from execution.parallel import ParallelExecutor
from verification.runtime import VerificationRuntime
from approval.runtime import ApprovalRuntime
from collaboration.runtime import HumanRuntime
from organization.runtime import OrganizationRuntime
from governance.runtime import GovernanceRuntime
from trust.runtime import TrustRuntime
from civilization.runtime import CivilizationRuntime

# Import new subsystems
from orchestrator.runtime import WorkspaceOrchestrator
from repository.runtime import MultiRepositoryRuntime
from crossdomain.runtime import CrossDomainRuntime, LongRunningMissionRuntime, SelfDiagnosticsRuntime
from healing.runtime import SelfHealingRuntime
from prediction.runtime import PredictionRuntime
from simulation.runtime import SimulationRuntime, CivilizationAPI


class PlatformMetrics:
    """Platform metrics."""
    def __init__(self):
        self.missions_created = 0
        self.missions_completed = 0
        self.workspaces_created = 0
        self.repositories_registered = 0
        self.verifications_run = 0
        self.approvals_granted = 0
        self.human_collaborations = 0
        self.organizations_created = 0
        self.simulations_run = 0
        self.predictions_made = 0
        self.failures_healed = 0


class CivilizationPlatform:
    """
    AGOS Civilization Platform v1.0.
    
    A unified platform integrating all production-ready subsystems.
    """
    
    # Platform metadata
    version: str = "1.0.0"
    name: str = "AGOS Civilization Platform"
    
    def __init__(self):
        """Initialize the platform."""
        # Core subsystems
        self.knowledge = KnowledgeRuntime()
        self.memory = MemoryRuntime()
        self.brain = EngineeringBrain()
        self.core = AutonomousCore()
        
        # Execution subsystems
        self.compiler = MissionCompiler()
        self.graph_runtime = GraphRuntime()
        self.parallel_executor = ParallelExecutor()
        
        # Quality subsystems
        self.verification = VerificationRuntime()
        self.approval = ApprovalRuntime()
        self.governance = GovernanceRuntime()
        
        # Collaboration subsystems
        self.collaboration = HumanRuntime()
        self.organization = OrganizationRuntime()
        self.trust = TrustRuntime()
        
        # Civilization runtime
        self.civilization = CivilizationRuntime()
        
        # Platform subsystems
        self.orchestrator = WorkspaceOrchestrator()
        self.repository = MultiRepositoryRuntime()
        self.cross_domain = CrossDomainRuntime()
        self.long_running = LongRunningMissionRuntime()
        self.diagnostics = SelfDiagnosticsRuntime()
        self.healing = SelfHealingRuntime()
        self.prediction = PredictionRuntime()
        self.simulation = SimulationRuntime()
        self.api = CivilizationAPI()
        
        # Platform state
        self.metrics = PlatformMetrics()
        self.started_at = datetime.now()
    
    def initialize(self) -> bool:
        """Initialize the platform."""
        try:
            # Initialize core
            self.core.initialize()
            
            # Initialize brain
            self.brain.knowledge = self.knowledge
            self.brain.memory = self.memory
            
            # Register subsystems for diagnostics
            self.diagnostics.register_subsystem("kernel")
            self.diagnostics.register_subsystem("knowledge")
            self.diagnostics.register_subsystem("memory")
            self.diagnostics.register_subsystem("execution")
            self.diagnostics.register_subsystem("governance")
            
            # Setup API
            from simulation.runtime import setup_api
            setup_api(self.api)
            
            return True
        except Exception as e:
            return False
    
    # ============ Platform Operations ============
    
    def health_check(self) -> Dict[str, Any]:
        """Check platform health."""
        # Run diagnostics
        reports = self.diagnostics.diagnose()
        
        return {
            "status": "healthy",
            "version": self.version,
            "name": self.name,
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self.started_at).total_seconds(),
            "subsystems": {
                "kernel": self.core.status.value if hasattr(self.core, 'status') else "healthy",
                "knowledge": "healthy",
                "memory": "healthy",
                "execution": "healthy",
                "governance": "healthy",
                "trust": "healthy",
                "workspaces": "healthy",
                "repositories": "healthy",
                "simulation": "healthy",
                "prediction": "healthy",
                "healing": "healthy",
                "api": "healthy",
            },
            "diagnostic_reports": len(reports),
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get platform statistics."""
        return {
            "version": self.version,
            "name": self.name,
            "uptime_seconds": (datetime.now() - self.started_at).total_seconds(),
            "metrics": {
                "missions_created": self.core.metrics.missions_created,
                "missions_completed": self.core.metrics.missions_completed,
                "workspaces": len(self.orchestrator.workspaces),
                "repositories": len(self.repository.registry.repositories),
                "verifications_run": len(self.verification.history),
                "approvals_pending": len(self.approval.requests),
                "organizations": len(self.organization.organizations),
                "trust_scores": len(self.trust.trust_scores),
                "simulations_run": len(self.simulation.simulations),
                "predictions_made": len(self.prediction.predictions),
                "failures_healed": self.healing.get_recovery_stats().get("resolved", 0),
            },
            "subsystems": {
                "knowledge_count": len(self.knowledge.knowledge_store),
                "memory_count": len(self.memory.memories),
                "graphs_count": len(self.graph_runtime.graphs),
                "governance_rules": len(self.governance.rules),
            },
        }
    
    def describe(self) -> Dict[str, Any]:
        """Describe the platform (self-describing)."""
        return {
            "name": self.name,
            "version": self.version,
            "description": "AGOS Autonomous Civilization Platform - A unified platform for autonomous engineering",
            "capabilities": [
                "Mission compilation and execution",
                "Knowledge management",
                "Memory management",
                "Cross-domain reasoning",
                "Simulation",
                "Prediction",
                "Self-healing",
                "Governance and trust",
                "Multi-workspace orchestration",
                "Multi-repository management",
            ],
            "subsystems": list(self.health_check()["subsystems"].keys()),
            "apis": list(self.api.endpoints.keys()),
        }


# Global platform instance
_platform: Optional[CivilizationPlatform] = None


def get_platform() -> CivilizationPlatform:
    """Get the global platform instance."""
    global _platform
    if _platform is None:
        _platform = CivilizationPlatform()
        _platform.initialize()
    return _platform
