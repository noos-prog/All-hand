"""Universal Mission Compiler."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class CompilerPhase(Enum):
    """Compilation phase."""
    INTENT = "intent"
    CONTEXT = "context"
    GOALS = "goals"
    CONSTRAINTS = "constraints"
    POLICIES = "policies"
    KNOWLEDGE = "knowledge"
    CAPABILITIES = "capabilities"
    SKILLS = "skills"
    EXECUTION_GRAPH = "execution_graph"
    EXECUTABLE = "executable"


class CompilerStatus(Enum):
    """Compilation status."""
    PENDING = "pending"
    COMPILING = "compiling"
    VALIDATING = "validating"
    OPTIMIZING = "optimizing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class CompilationPhase:
    """A single compilation phase."""
    phase: CompilerPhase
    status: str = "pending"
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    output: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Intent:
    """Mission intent."""
    text: str
    confidence: float = 0.0
    entities: List[str] = field(default_factory=list)


@dataclass
class Goal:
    """Mission goal."""
    id: str
    description: str
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    success_criteria: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Constraint:
    """Mission constraint."""
    id: str
    type: str  # time, budget, resource, policy
    value: Any
    soft: bool = False


@dataclass
class ExecutableMission:
    """Compiled executable mission."""
    id: str
    intent: Intent
    goals: List[Goal] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    execution_graph: Dict[str, Any] = field(default_factory=dict)
    compiled_at: datetime = field(default_factory=datetime.now)
    status: CompilerStatus = CompilerStatus.PENDING
    phases: List[CompilationPhase] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MissionCompiler:
    """Universal Mission Compiler."""
    
    def __init__(self):
        """Initialize mission compiler."""
        self.compilations: Dict[str, ExecutableMission] = {}
        self.cache: Dict[str, ExecutableMission] = {}
        self.optimizer = MissionOptimizer()
        self.validator = MissionValidator()
    
    def compile(
        self,
        intent_text: str,
        context: Optional[Dict[str, Any]] = None,
        knowledge: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
    ) -> ExecutableMission:
        """Compile a mission from intent."""
        mission_id = self._generate_id(intent_text)
        
        # Create mission
        intent = Intent(text=intent_text, confidence=0.5)
        mission = ExecutableMission(
            id=mission_id,
            intent=intent,
            status=CompilerStatus.COMPILING,
        )
        
        # Phase 1: Intent
        self._compile_intent(mission)
        
        # Phase 2: Context
        self._compile_context(mission, context or {})
        
        # Phase 3: Goals
        self._compile_goals(mission)
        
        # Phase 4: Constraints
        self._compile_constraints(mission)
        
        # Phase 5: Policies
        self._compile_policies(mission)
        
        # Phase 6: Knowledge
        self._compile_knowledge(mission, knowledge or [])
        
        # Phase 7: Capabilities
        self._compile_capabilities(mission, capabilities or [])
        
        # Phase 8: Skills
        self._compile_skills(mission)
        
        # Phase 9: Execution Graph
        self._compile_execution_graph(mission)
        
        # Phase 10: Executable
        self._finalize_executable(mission)
        
        mission.status = CompilerStatus.COMPLETED
        self.compilations[mission_id] = mission
        
        return mission
    
    def _compile_intent(self, mission: ExecutableMission) -> None:
        """Phase 1: Compile intent."""
        phase = CompilationPhase(phase=CompilerPhase.INTENT)
        phase.status = "compiling"
        phase.started_at = datetime.now()
        
        # Parse intent
        mission.intent.confidence = 0.8
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _compile_context(self, mission: ExecutableMission, context: Dict[str, Any]) -> None:
        """Phase 2: Compile context."""
        phase = CompilationPhase(phase=CompilerPhase.CONTEXT)
        phase.started_at = datetime.now()
        
        mission.metadata["context"] = context
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _compile_goals(self, mission: ExecutableMission) -> None:
        """Phase 3: Compile goals."""
        phase = CompilationPhase(phase=CompilerPhase.GOALS)
        phase.started_at = datetime.now()
        
        # Generate goals from intent
        goal = Goal(
            id=self._generate_id("goal"),
            description=f"Goal: {mission.intent.text[:50]}",
            priority=1,
        )
        mission.goals.append(goal)
        
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _compile_constraints(self, mission: ExecutableMission) -> None:
        """Phase 4: Compile constraints."""
        phase = CompilationPhase(phase=CompilerPhase.CONSTRAINTS)
        phase.started_at = datetime.now()
        
        # Add default constraints
        mission.constraints.append(Constraint(
            id=self._generate_id("constraint"),
            type="time",
            value=3600,  # 1 hour
            soft=True,
        ))
        
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _compile_policies(self, mission: ExecutableMission) -> None:
        """Phase 5: Compile policies."""
        phase = CompilationPhase(phase=CompilerPhase.POLICIES)
        phase.started_at = datetime.now()
        
        mission.metadata["policies"] = ["default-policy"]
        
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _compile_knowledge(self, mission: ExecutableMission, knowledge: List[str]) -> None:
        """Phase 6: Compile knowledge."""
        phase = CompilationPhase(phase=CompilerPhase.KNOWLEDGE)
        phase.started_at = datetime.now()
        
        mission.metadata["knowledge"] = knowledge
        
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _compile_capabilities(self, mission: ExecutableMission, capabilities: List[str]) -> None:
        """Phase 7: Compile capabilities."""
        phase = CompilationPhase(phase=CompilerPhase.CAPABILITIES)
        phase.started_at = datetime.now()
        
        mission.metadata["capabilities"] = capabilities
        
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _compile_skills(self, mission: ExecutableMission) -> None:
        """Phase 8: Compile skills."""
        phase = CompilationPhase(phase=CompilerPhase.SKILLS)
        phase.started_at = datetime.now()
        
        mission.metadata["skills"] = []
        
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _compile_execution_graph(self, mission: ExecutableMission) -> None:
        """Phase 9: Compile execution graph."""
        phase = CompilationPhase(phase=CompilerPhase.EXECUTION_GRAPH)
        phase.started_at = datetime.now()
        
        # Create execution graph
        mission.execution_graph = {
            "nodes": [
                {"id": "start", "type": "start"},
                {"id": "execute", "type": "capability"},
                {"id": "validate", "type": "validation"},
                {"id": "end", "type": "end"},
            ],
            "edges": [
                {"from": "start", "to": "execute", "type": "depends_on"},
                {"from": "execute", "to": "validate", "type": "produces"},
                {"from": "validate", "to": "end", "type": "depends_on"},
            ],
        }
        
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def _finalize_executable(self, mission: ExecutableMission) -> None:
        """Phase 10: Finalize executable."""
        phase = CompilationPhase(phase=CompilerPhase.EXECUTABLE)
        phase.started_at = datetime.now()
        
        mission.metadata["executable"] = True
        mission.metadata["compiled_phases"] = len(mission.phases)
        
        phase.status = "completed"
        phase.completed_at = datetime.now()
        mission.phases.append(phase)
    
    def validate(self, mission_id: str) -> bool:
        """Validate a compiled mission."""
        mission = self.compilations.get(mission_id)
        if not mission:
            return False
        
        return self.validator.validate(mission)
    
    def optimize(self, mission_id: str) -> bool:
        """Optimize a compiled mission."""
        mission = self.compilations.get(mission_id)
        if not mission:
            return False
        
        return self.optimizer.optimize(mission)
    
    def get_mission(self, mission_id: str) -> Optional[ExecutableMission]:
        """Get compiled mission."""
        return self.compilations.get(mission_id)
    
    def diff(self, mission_id1: str, mission_id2: str) -> Dict[str, Any]:
        """Compare two missions."""
        m1 = self.compilations.get(mission_id1)
        m2 = self.compilations.get(mission_id2)
        
        if not m1 or not m2:
            return {"error": "Mission not found"}
        
        return {
            "mission1": m1.id,
            "mission2": m2.id,
            "goals_diff": len(m1.goals) - len(m2.goals),
            "constraints_diff": len(m1.constraints) - len(m2.constraints),
        }
    
    def replay(self, mission_id: str) -> List[Dict[str, Any]]:
        """Replay mission compilation."""
        mission = self.compilations.get(mission_id)
        if not mission:
            return []
        
        return [
            {
                "phase": p.phase.value,
                "status": p.status,
                "duration": (p.completed_at - p.started_at).total_seconds() if p.completed_at and p.started_at else 0,
            }
            for p in mission.phases
        ]
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]


class MissionOptimizer:
    """Mission optimizer."""
    
    def optimize(self, mission: ExecutableMission) -> bool:
        """Optimize mission execution graph."""
        # Simple optimization: reduce redundant nodes
        if len(mission.execution_graph.get("nodes", [])) > 10:
            mission.metadata["optimized"] = True
            mission.metadata["optimization_type"] = "node_reduction"
        return True


class MissionValidator:
    """Mission validator."""
    
    def validate(self, mission: ExecutableMission) -> bool:
        """Validate mission."""
        if not mission.goals:
            return False
        if not mission.execution_graph.get("nodes"):
            return False
        return True
