"""Universal Skill Engine - Every capability executes only through Skills."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type


class SkillInput:
    """Base class for skill inputs."""
    pass


class SkillOutput:
    """Base class for skill outputs."""
    pass


@dataclass
class SkillContext:
    """Context for skill execution."""
    mission_id: str
    skill_name: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


class SkillStatus(Enum):
    """Skill execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SkillResult:
    """Result of skill execution."""
    skill_name: str
    status: SkillStatus
    started_at: datetime
    output: Optional[Any] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None
    duration_ms: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_name": self.skill_name,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata
        }


class ISkill(ABC):
    """
    Skill interface.
    All skills must implement this interface.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Skill name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Skill description."""
        pass
    
    @property
    def input_type(self) -> Type[SkillInput]:
        """Input type for this skill."""
        return SkillInput
    
    @property
    def output_type(self) -> Type[SkillOutput]:
        """Output type for this skill."""
        return SkillOutput
    
    @abstractmethod
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute the skill."""
        pass


class Skill(ABC):
    """
    Base class for skills.
    Skills are atomic, stateless, and reusable.
    """
    
    @property
    def name(self) -> str:
        """Skill name from class name."""
        return self.__class__.__name__
    
    @property
    def description(self) -> str:
        """Default description."""
        return f"Skill: {self.name}"
    
    def execute(self, context: SkillContext) -> SkillResult:
        """
        Execute the skill.
        Override this in subclasses.
        """
        raise NotImplementedError("Skills must implement execute()")


class SkillRunner:
    """
    Executes skills.
    Only SkillRunner may execute Skills.
    Skills cannot call each other directly.
    """
    
    def __init__(self):
        self._skills: Dict[str, Skill] = {}
    
    def register(self, skill: Skill) -> None:
        """Register a skill."""
        self._skills[skill.name] = skill
    
    def unregister(self, skill_name: str) -> None:
        """Unregister a skill."""
        if skill_name in self._skills:
            del self._skills[skill_name]
    
    def get(self, skill_name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self._skills.get(skill_name)
    
    def list_all(self) -> List[Skill]:
        """List all registered skills."""
        return list(self._skills.values())
    
    def run(self, skill_name: str, context: SkillContext) -> SkillResult:
        """
        Run a skill.
        Only this method may execute skills.
        """
        skill = self.get(skill_name)
        
        if skill is None:
            return SkillResult(
                skill_name=skill_name,
                status=SkillStatus.FAILED,
                error=f"Skill not found: {skill_name}",
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
                duration_ms=0
            )
        
        started_at = datetime.utcnow()
        
        try:
            result = skill.execute(context)
            result.status = SkillStatus.COMPLETED
            result.completed_at = datetime.utcnow()
            result.duration_ms = int((result.completed_at - started_at).total_seconds() * 1000)
            return result
            
        except Exception as e:
            return SkillResult(
                skill_name=skill_name,
                status=SkillStatus.FAILED,
                error=str(e),
                started_at=started_at,
                completed_at=datetime.utcnow(),
                duration_ms=int((datetime.utcnow() - started_at).total_seconds() * 1000)
            )


class SkillPipeline:
    """
    Executes multiple skills in sequence.
    Skills are executed through SkillRunner only.
    """
    
    def __init__(self, skill_runner: SkillRunner):
        self.skill_runner = skill_runner
    
    def execute(self, skill_names: List[str], context: SkillContext) -> List[SkillResult]:
        """Execute multiple skills in sequence."""
        results = []
        
        for skill_name in skill_names:
            result = self.skill_runner.run(skill_name, context)
            results.append(result)
            
            # Stop on failure
            if result.status == SkillStatus.FAILED:
                break
        
        return results
