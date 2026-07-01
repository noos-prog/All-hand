"""Universal Mission Engine - All missions execute through this engine."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from mission import Mission, MissionStatus


class MissionState(Enum):
    """Mission lifecycle states."""
    CREATED = "created"
    VALIDATED = "validated"
    PLANNED = "planned"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class MissionValidationResult:
    """Result of mission validation."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class MissionPlan:
    """Execution plan for a mission."""
    mission_id: str
    steps: List[str] = field(default_factory=list)
    estimated_duration_ms: int = 0
    required_capabilities: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)


@dataclass
class MissionExecutionResult:
    """Result of mission execution."""
    mission_id: str
    state: MissionState
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: int = 0
    result: Optional[Any] = None
    error: Optional[str] = None
    events: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "state": self.state.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": self.duration_ms,
            "result": self.result,
            "error": self.error,
            "events": self.events,
            "metrics": self.metrics
        }


class MissionParser:
    """Parses raw input into Mission objects."""
    
    @staticmethod
    def parse(input_data: Any) -> Mission:
        """Parse input into Mission."""
        if isinstance(input_data, Mission):
            return input_data
        
        if isinstance(input_data, dict):
            return Mission(
                id=input_data.get("id", ""),
                name=input_data.get("name", ""),
                description=input_data.get("description", ""),
                capability=input_data.get("capability", ""),
                parameters=input_data.get("parameters", {}),
            )
        
        raise ValueError(f"Cannot parse input of type: {type(input_data)}")


class MissionValidator:
    """Validates missions before execution."""
    
    def validate(self, mission: Mission) -> MissionValidationResult:
        """Validate mission."""
        errors = []
        warnings = []
        
        # Required fields
        if not mission.name:
            errors.append("Mission name is required")
        
        if not mission.capability:
            errors.append("Mission capability is required")
        
        # Capability format
        if mission.capability and not mission.capability[0].isupper():
            warnings.append("Capability name should start with uppercase")
        
        # Parameters
        if not mission.parameters:
            warnings.append("No parameters provided")
        
        return MissionValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


class MissionPlanner:
    """Creates execution plans for missions."""
    
    def plan(self, mission: Mission) -> MissionPlan:
        """Create execution plan."""
        steps = [
            "resolve_capability",
            "resolve_provider",
            "create_context",
            "execute_skills",
            "collect_results",
            "generate_output"
        ]
        
        return MissionPlan(
            mission_id=mission.id,
            steps=steps,
            estimated_duration_ms=5000,
            required_capabilities=[mission.capability],
            required_skills=[]
        )


class MissionExecutor:
    """Executes missions using the pipeline."""
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
    
    def execute(self, mission: Mission) -> MissionExecutionResult:
        """Execute mission and return structured result."""
        result = MissionExecutionResult(
            mission_id=mission.id,
            state=MissionState.EXECUTING,
            started_at=datetime.utcnow()
        )
        
        try:
            # Execute through pipeline
            pipeline_result = self.pipeline.execute(mission)
            
            if pipeline_result.status.value == "completed":
                result.state = MissionState.COMPLETED
                result.result = pipeline_result.result
                result.events = [{"step": s.name, "status": s.status.value} for s in pipeline_result.steps]
            else:
                result.state = MissionState.FAILED
                result.error = pipeline_result.error
            
            result.completed_at = datetime.utcnow()
            result.duration_ms = int((result.completed_at - result.started_at).total_seconds() * 1000)
            
        except Exception as e:
            result.state = MissionState.FAILED
            result.error = str(e)
            result.completed_at = datetime.utcnow()
            result.duration_ms = int((result.completed_at - result.started_at).total_seconds() * 1000)
        
        return result


class MissionResultBuilder:
    """Builds mission execution results."""
    
    @staticmethod
    def build(
        mission: Mission,
        state: MissionState,
        started_at: datetime,
        completed_at: Optional[datetime],
        result: Any = None,
        error: Optional[str] = None
    ) -> MissionExecutionResult:
        """Build mission execution result."""
        duration_ms = 0
        if completed_at:
            duration_ms = int((completed_at - started_at).total_seconds() * 1000)
        
        return MissionExecutionResult(
            mission_id=mission.id,
            state=state,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            result=result,
            error=error
        )


class MissionEngine:
    """
    Universal Mission Engine.
    All missions execute through this engine.
    """
    
    def __init__(self, pipeline):
        self.parser = MissionParser()
        self.validator = MissionValidator()
        self.planner = MissionPlanner()
        self.executor = MissionExecutor(pipeline)
        self.result_builder = MissionResultBuilder()
    
    def run(self, input_data: Any) -> MissionExecutionResult:
        """
        Run mission through complete lifecycle:
        Created → Validated → Planned → Executing → Completed/Failed
        """
        # 1. Parse
        mission = self.parser.parse(input_data)
        
        # 2. Validate
        validation = self.validator.validate(mission)
        if not validation.valid:
            return MissionExecutionResult(
                mission_id=mission.id,
                state=MissionState.FAILED,
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
                error="; ".join(validation.errors)
            )
        
        # 3. Plan
        plan = self.planner.plan(mission)
        
        # 4. Execute
        result = self.executor.execute(mission)
        
        # 5. Return result
        return result
