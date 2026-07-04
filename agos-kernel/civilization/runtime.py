"""AGOS Autonomous Civilization Runtime v1.0."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

# Import all subsystems
from execution.compiler import MissionCompiler, ExecutableMission
from execution.graph import GraphRuntime, ExecutionGraph, NodeType, EdgeType
from execution.parallel import ParallelExecutor, ExecutionTask
from verification.runtime import VerificationRuntime, VerificationType
from approval.runtime import ApprovalRuntime, ApprovalSource
from collaboration.runtime import HumanRuntime, CollaborationAction
from organization.runtime import OrganizationRuntime, OrganizationType
from governance.runtime import GovernanceRuntime, GovernanceDomain
from trust.runtime import TrustRuntime, TrustLevel

# Import existing subsystems
from knowledge.runtime import KnowledgeRuntime
from memory.runtime import MemoryRuntime
from brain.engine import EngineeringBrain
from core.autonomous import AutonomousCore


@dataclass
class CivilizationMetrics:
    """Civilization metrics."""
    missions_compiled: int = 0
    graphs_created: int = 0
    verifications_run: int = 0
    approvals_granted: int = 0
    human_collaborations: int = 0
    organizations_created: int = 0
    governance_violations: int = 0
    trust_scores_assigned: int = 0


@dataclass
class CivilizationRuntime:
    """
    AGOS Autonomous Civilization Runtime v1.0.
    
    Integrates all subsystems into one coherent autonomous engineering civilization.
    
    Success Conditions:
    - Every mission is compiled
    - Every execution is governed
    - Every result is verified
    - Every decision is explainable
    - Every artifact is trusted
    - Every organization is represented
    - Every human interaction is explicit
    - Every subsystem remains replaceable
    """
    
    # Version
    version: str = "1.0.0"
    name: str = "AGOS Civilization"
    
    # Core subsystems
    knowledge: KnowledgeRuntime = field(default_factory=KnowledgeRuntime)
    memory: MemoryRuntime = field(default_factory=MemoryRuntime)
    brain: EngineeringBrain = field(default_factory=EngineeringBrain)
    core: AutonomousCore = field(default_factory=AutonomousCore)
    
    # Execution subsystems
    compiler: MissionCompiler = field(default_factory=MissionCompiler)
    graph_runtime: GraphRuntime = field(default_factory=GraphRuntime)
    parallel_executor: ParallelExecutor = field(default_factory=ParallelExecutor)
    
    # Quality subsystems
    verification: VerificationRuntime = field(default_factory=VerificationRuntime)
    approval: ApprovalRuntime = field(default_factory=ApprovalRuntime)
    governance: GovernanceRuntime = field(default_factory=GovernanceRuntime)
    
    # Collaboration subsystems
    collaboration: HumanRuntime = field(default_factory=HumanRuntime)
    organization: OrganizationRuntime = field(default_factory=OrganizationRuntime)
    trust: TrustRuntime = field(default_factory=TrustRuntime)
    
    # Metrics
    metrics: CivilizationMetrics = field(default_factory=CivilizationMetrics)
    
    # Started time
    started_at: datetime = field(default_factory=datetime.now)
    
    def initialize(self) -> bool:
        """Initialize the civilization runtime."""
        try:
            # Initialize core
            self.core.initialize()
            
            # Initialize brain with subsystems
            self.brain.knowledge = self.knowledge
            self.brain.memory = self.memory
            
            return True
        except Exception as e:
            return False
    
    # ============ Mission Compilation ============
    
    def compile_mission(
        self,
        intent: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> ExecutableMission:
        """Compile a mission from intent."""
        mission = self.compiler.compile(intent, context)
        self.metrics.missions_compiled += 1
        return mission
    
    # ============ Execution Graph ============
    
    def create_execution_graph(self, name: str) -> ExecutionGraph:
        """Create an execution graph."""
        graph = self.graph_runtime.create_graph(name)
        self.metrics.graphs_created += 1
        return graph
    
    # ============ Verification ============
    
    def verify(
        self,
        artifact_id: str,
        artifact_data: Any,
        verification_types: Optional[List[VerificationType]] = None,
    ):
        """Verify an artifact."""
        report = self.verification.verify(artifact_id, artifact_data, verification_types)
        self.metrics.verifications_run += 1
        return report
    
    # ============ Approval ============
    
    def request_approval(
        self,
        request_type: str,
        description: str,
        source: ApprovalSource = ApprovalSource.AUTOMATIC,
    ):
        """Request approval."""
        request = self.approval.create_request(request_type, description, source)
        return request
    
    # ============ Human Collaboration ============
    
    def collaborate(
        self,
        action: CollaborationAction,
        contributor_id: str,
        content: str,
    ):
        """Record human collaboration."""
        contribution = self.collaboration.add_contribution(action, contributor_id, content)
        self.metrics.human_collaborations += 1
        return contribution
    
    # ============ Organization ============
    
    def create_organization(
        self,
        name: str,
        org_type: OrganizationType,
        description: str = "",
    ):
        """Create an organization."""
        org = self.organization.create_organization(name, org_type, description)
        self.metrics.organizations_created += 1
        return org
    
    # ============ Governance ============
    
    def check_governance(
        self,
        entity_id: str,
        entity_type: str,
        domain: Optional[GovernanceDomain] = None,
    ) -> Dict[str, Any]:
        """Check governance compliance."""
        result = self.governance.check_compliance(entity_id, entity_type, domain)
        return result
    
    # ============ Trust ============
    
    def assess_trust(
        self,
        entity_id: str,
        entity_type: str,
    ) -> Any:
        """Assess trust for an entity."""
        score = self.trust.create_trust_score(entity_id, entity_type)
        self.metrics.trust_scores_assigned += 1
        return score
    
    # ============ Verification ============
    
    def verify_mission_result(
        self,
        mission_id: str,
        result: Dict[str, Any],
    ) -> bool:
        """Verify a mission result."""
        report = self.verify(
            artifact_id=mission_id,
            artifact_data=result,
            verification_types=[
                VerificationType.STRUCTURAL,
                VerificationType.SEMANTIC,
                VerificationType.EVIDENCE,
            ],
        )
        
        if report.overall_passed:
            self.metrics.approvals_granted += 1
        
        return report.overall_passed
    
    # ============ Statistics ============
    
    def get_stats(self) -> Dict[str, Any]:
        """Get civilization statistics."""
        return {
            "version": self.version,
            "name": self.name,
            "uptime_seconds": (datetime.now() - self.started_at).total_seconds(),
            "metrics": {
                "missions_compiled": self.metrics.missions_compiled,
                "graphs_created": self.metrics.graphs_created,
                "verifications_run": self.metrics.verifications_run,
                "approvals_granted": self.metrics.approvals_granted,
                "human_collaborations": self.metrics.human_collaborations,
                "organizations_created": self.metrics.organizations_created,
                "governance_violations": self.metrics.governance_violations,
                "trust_scores_assigned": self.metrics.trust_scores_assigned,
            },
            "subsystems": {
                "knowledge_count": len(self.knowledge.knowledge_store),
                "memory_count": len(self.memory.memories),
                "missions_created": self.core.metrics.missions_created,
                "graph_count": len(self.graph_runtime.graphs),
                "verification_rules": len(self.verification.rules),
                "approval_pending": len(self.approval.requests),
                "governance_rules": len(self.governance.rules),
                "organizations": len(self.organization.organizations),
                "trust_scores": len(self.trust.trust_scores),
            },
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check civilization health."""
        return {
            "status": "healthy",
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "core_status": self.core.status.value,
            "all_capabilities": self.core.verify_capabilities(),
            "subsystems_healthy": True,
        }


# Global civilization instance
_civilization: Optional[CivilizationRuntime] = None


def get_civilization() -> CivilizationRuntime:
    """Get the global civilization instance."""
    global _civilization
    if _civilization is None:
        _civilization = CivilizationRuntime()
        _civilization.initialize()
    return _civilization
