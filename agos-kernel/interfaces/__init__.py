"""Interfaces for AGOS Kernel."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type

from shared import SkillInput, SkillOutput


class IProvider(ABC):
    """Provider interface."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        pass
    
    @abstractmethod
    def execute(self, skill_name: str, input_data: SkillInput) -> SkillOutput:
        """Execute a skill."""
        pass
    
    @abstractmethod
    def supports_skill(self, skill_name: str) -> bool:
        """Check if provider supports a skill."""
        pass


class ICapability(ABC):
    """Capability interface."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Capability name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Capability description."""
        pass
    
    @property
    @abstractmethod
    def skills(self) -> List[str]:
        """List of skills this capability requires."""
        pass
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute the capability."""
        pass


class ISkill(ABC):
    """Skill interface."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Skill name."""
        pass
    
    @property
    @abstractmethod
    def input_type(self) -> Type[SkillInput]:
        """Input type for this skill."""
        pass
    
    @property
    @abstractmethod
    def output_type(self) -> Type[SkillOutput]:
        """Output type for this skill."""
        pass
    
    @abstractmethod
    def execute(self, input_data: SkillInput) -> SkillOutput:
        """Execute the skill."""
        pass
