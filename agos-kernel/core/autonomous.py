"""AGOS Autonomous Engineering Core v1.0."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from knowledge.runtime import KnowledgeRuntime
from memory.runtime import MemoryRuntime
from learning.runtime import LearningRuntime
from experience.runtime import ExperienceRuntime
from recommendation.runtime import RecommendationEngine
from benchmark.runtime import BenchmarkPlatform
from optimization.runtime import OptimizationEngine
from brain.engine import EngineeringBrain


class CoreStatus(Enum):
    """Core status."""
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"


class MissionStatus(Enum):
    """Mission status."""
    CREATED = "created"
    PLANNING = "planning"
    REASONING = "reasoning"
    EXECUTING = "executing"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Mission:
    """Mission - the unit of work."""
    id: str
    objective: str
    context: Dict[str, Any] = field(default_factory=dict)
    status: MissionStatus = MissionStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class CoreCapabilities:
    """Core capabilities."""
    understands: bool = True
    plans: bool = True
    reasons: bool = True
    validates: bool = True
    decides: bool = True
    executes: bool = True
    learns: bool = True
    improves: bool = True


@dataclass
class CoreMetrics:
    """Core metrics."""
    missions_created: int = 0
    missions_completed: int = 0
    missions_failed: int = 0
    providers_used: int = 0
    learnings_integrated: int = 0
    optimizations_executed: int = 0


@dataclass
class AutonomousCore:
    """
    AGOS Autonomous Engineering Core v1.0.
    
    Success Conditions:
    - AGOS understands
    - AGOS plans
    - AGOS reasons
    - AGOS validates
    - AGOS decides
    - AGOS executes through external providers
    - AGOS learns from results
    - AGOS improves continuously
    """
    
    # Core name
    name: str = "AGOS"
    version: str = "1.0.0"
    
    # Status
    status: CoreStatus = CoreStatus.INITIALIZING
    
    # Subsystems
    knowledge: KnowledgeRuntime = field(default_factory=KnowledgeRuntime)
    memory: MemoryRuntime = field(default_factory=MemoryRuntime)
    learning: LearningRuntime = field(default_factory=LearningRuntime)
    experience: ExperienceRuntime = field(default_factory=ExperienceRuntime)
    recommendation: RecommendationEngine = field(default_factory=RecommendationEngine)
    benchmark: BenchmarkPlatform = field(default_factory=BenchmarkPlatform)
    optimization: OptimizationEngine = field(default_factory=OptimizationEngine)
    brain: EngineeringBrain = field(default_factory=EngineeringBrain)
    
    # Mission management
    missions: Dict[str, Mission] = field(default_factory=dict)
    active_mission: Optional[str] = None
    
    # Core state
    capabilities: CoreCapabilities = field(default_factory=CoreCapabilities)
    metrics: CoreMetrics = field(default_factory=CoreMetrics)
    
    # Started time
    started_at: datetime = field(default_factory=datetime.now)
    
    def initialize(self) -> bool:
        """Initialize the core."""
        try:
            self.status = CoreStatus.INITIALIZING
            
            # Initialize brain with subsystems
            self.brain.knowledge = self.knowledge
            self.brain.memory = self.memory
            self.brain.learning = self.learning
            self.brain.experience = self.experience
            self.brain.recommendation = self.recommendation
            self.brain.benchmark = self.benchmark
            self.brain.optimization = self.optimization
            
            # Create working memory
            self.memory.create_memory(
                name="core-working",
                memory_type=None,  # Will use WORKING
            )
            
            self.status = CoreStatus.READY
            return True
        except Exception as e:
            self.status = CoreStatus.ERROR
            return False
    
    def create_mission(self, objective: str, context: Optional[Dict[str, Any]] = None) -> Mission:
        """Create a new mission."""
        mission = Mission(
            id=f"mission-{len(self.missions) + 1}",
            objective=objective,
            context=context or {},
        )
        
        self.missions[mission.id] = mission
        self.metrics.missions_created += 1
        
        return mission
    
    def understand(self, mission: Mission) -> bool:
        """Understand the mission objective."""
        mission.status = MissionStatus.PLANNING
        
        # Use brain to understand
        understanding = self.brain.think(mission.objective)
        
        # Store in memory
        self.memory.add_to_memory(
            self.memory.working_memory.id if self.memory.working_memory else "",
            f"Understanding: {mission.objective}",
            importance=0.9,
        )
        
        return True
    
    def plan(self, mission: Mission) -> List[Dict[str, Any]]:
        """Plan the mission execution."""
        # Generate recommendations
        recommendations = self.brain.recommend({"query": mission.objective})
        
        # Create plan from recommendations
        plan = []
        for rec in recommendations[:5]:
            plan.append({
                "step": len(plan) + 1,
                "action": rec.get("type", "unknown"),
                "description": rec.get("description", ""),
                "recommendation_id": rec.get("id", ""),
            })
        
        return plan
    
    def reason(self, mission: Mission) -> Dict[str, Any]:
        """Reason about the mission."""
        mission.status = MissionStatus.REASONING
        
        # Think about the mission
        reasoning = self.brain.think(mission.objective)
        
        # Get relevant knowledge
        relevant = self.knowledge.search_knowledge(mission.objective)
        
        # Get experiences
        experiences = self.experience.search_experiences(mission.objective)
        
        return {
            "reasoning": reasoning,
            "relevant_knowledge_count": len(relevant),
            "relevant_experiences_count": len(experiences),
            "recommendations": recommendations if 'recommendations' in locals() else [],
        }
    
    def validate(self, mission: Mission) -> bool:
        """Validate mission before execution."""
        mission.status = MissionStatus.VALIDATING
        
        # Basic validation
        if not mission.objective:
            mission.errors.append("Empty objective")
            return False
        
        if len(mission.objective) < 5:
            mission.errors.append("Objective too short")
            return False
        
        return True
    
    def execute(self, mission: Mission) -> bool:
        """
        Execute the mission.
        NOTE: Core does not execute directly - it coordinates external providers.
        """
        mission.status = MissionStatus.EXECUTING
        mission.started_at = datetime.now()
        
        self.active_mission = mission.id
        self.status = CoreStatus.RUNNING
        
        # The actual execution is delegated to external providers
        # Core only tracks and monitors
        
        return True
    
    def complete_mission(self, mission_id: str, result: Dict[str, Any]) -> bool:
        """Complete a mission."""
        mission = self.missions.get(mission_id)
        if not mission:
            return False
        
        mission.status = MissionStatus.COMPLETED
        mission.completed_at = datetime.now()
        mission.result = result
        
        self.metrics.missions_completed += 1
        self.active_mission = None
        
        if not self.active_mission:
            self.status = CoreStatus.READY
        
        # Learn from result
        self.brain.learn_from(
            source=None,  # Would use appropriate source
            content=f"Mission {mission_id} completed: {result.get('summary', '')}",
            evidence={"mission": mission_id, "result": result},
        )
        
        return True
    
    def fail_mission(self, mission_id: str, error: str) -> bool:
        """Mark mission as failed."""
        mission = self.missions.get(mission_id)
        if not mission:
            return False
        
        mission.status = MissionStatus.FAILED
        mission.completed_at = datetime.now()
        mission.errors.append(error)
        
        self.metrics.missions_failed += 1
        self.active_mission = None
        
        if not self.active_mission:
            self.status = CoreStatus.READY
        
        # Learn from failure
        self.brain.learn_from(
            source=None,
            content=f"Mission {mission_id} failed: {error}",
            evidence={"mission": mission_id, "error": error},
        )
        
        return True
    
    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Get mission by ID."""
        return self.missions.get(mission_id)
    
    def list_missions(self, status: Optional[MissionStatus] = None) -> List[Mission]:
        """List missions."""
        missions = list(self.missions.values())
        if status:
            missions = [m for m in missions if m.status == status]
        return missions
    
    def get_stats(self) -> Dict[str, Any]:
        """Get core statistics."""
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status.value,
            "metrics": {
                "missions_created": self.metrics.missions_created,
                "missions_completed": self.metrics.missions_completed,
                "missions_failed": self.metrics.missions_failed,
                "success_rate": (
                    self.metrics.missions_completed / self.metrics.missions_created
                    if self.metrics.missions_created > 0 else 0
                ),
                "providers_used": self.metrics.providers_used,
                "learnings_integrated": self.metrics.learnings_integrated,
                "optimizations_executed": self.metrics.optimizations_executed,
            },
            "active_mission": self.active_mission,
            "uptime_seconds": (datetime.now() - self.started_at).total_seconds(),
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check core health."""
        health = self.brain.health_check()
        
        return {
            "status": "healthy" if self.status == CoreStatus.READY else "degraded",
            "core_status": self.status.value,
            "brain_health": health,
            "active_mission": self.active_mission,
            "timestamp": datetime.now().isoformat(),
        }
    
    def verify_capabilities(self) -> Dict[str, bool]:
        """Verify all core capabilities."""
        return {
            "understands": self.capabilities.understands and self.status != CoreStatus.ERROR,
            "plans": self.capabilities.plans and self.status != CoreStatus.ERROR,
            "reasons": self.capabilities.reasons and self.status != CoreStatus.ERROR,
            "validates": self.capabilities.validates and self.status != CoreStatus.ERROR,
            "decides": self.capabilities.decides and self.status != CoreStatus.ERROR,
            "executes": self.capabilities.executes and self.status != CoreStatus.ERROR,
            "learns": self.capabilities.learns and self.status != CoreStatus.ERROR,
            "improves": self.capabilities.improves and self.status != CoreStatus.ERROR,
        }


# Global core instance
_core: Optional[AutonomousCore] = None


def get_core() -> AutonomousCore:
    """Get the global core instance."""
    global _core
    if _core is None:
        _core = AutonomousCore()
        _core.initialize()
    return _core
