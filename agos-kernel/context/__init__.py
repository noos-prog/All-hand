"""Execution Context."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from mission import Mission


@dataclass
class ExecutionContext:
    """
    Context passed through the execution pipeline.
    Contains everything needed to execute a mission.
    """
    mission: Mission
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # Selected components
    selected_capability: Optional[str] = None
    selected_provider: Optional[str] = None
    selected_skills: List[str] = field(default_factory=list)
    
    # Execution state
    current_skill: Optional[str] = None
    skill_results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_skill_result(self, skill_name: str, result: Any) -> None:
        """Add a skill execution result."""
        self.skill_results[skill_name] = result
    
    def get_skill_result(self, skill_name: str) -> Optional[Any]:
        """Get a skill execution result."""
        return self.skill_results.get(skill_name)
    
    def add_error(self, error: str) -> None:
        """Add an error."""
        self.errors.append(error)
    
    @property
    def has_errors(self) -> bool:
        """Check if there are errors."""
        return len(self.errors) > 0


class ContextBuilder:
    """
    Builds execution context from mission.
    """
    
    def build(self, mission: Mission) -> ExecutionContext:
        """Build context from mission."""
        return ExecutionContext(
            mission=mission,
            selected_capability=mission.capability,
            selected_skills=[]  # Will be filled by Decision Engine
        )
