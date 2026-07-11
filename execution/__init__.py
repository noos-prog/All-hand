"""AGOS Execution Platform - Universal execution for all agents and workflows."""

from .agent import Agent, AgentConfig, AgentStatus, AgentPool
from .adapter import Adapter, AdapterRegistry
from .composition import Composition, CompositionBuilder
from .capability import ExecutionCapability, CapabilityRegistry
from .model import ExecutionModel, ModelFactory
from .provider import ExecutionProvider, ProviderRegistry
from .resolution import ExecutionResolution, Resolver
from .skill import ExecutionSkill, SkillRegistry
from .tool import ExecutionTool, ToolRegistry

__all__ = [
    "Agent", "AgentConfig", "AgentStatus", "AgentPool",
    "Adapter", "AdapterRegistry",
    "Composition", "CompositionBuilder",
    "ExecutionCapability", "CapabilityRegistry",
    "ExecutionModel", "ModelFactory",
    "ExecutionProvider", "ProviderRegistry",
    "ExecutionResolution", "Resolver",
    "ExecutionSkill", "SkillRegistry",
    "ExecutionTool", "ToolRegistry",
]

__version__ = "1.0.0"
