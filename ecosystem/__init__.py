"""
AGOS Ecosystem Platform
======================

Universal ecosystem for agent orchestration and inter-operation.
Manages the complete lifecycle of agents, capabilities, and resources.

Author: AGOS Team
Version: 1.0.0
"""

from .registry import EcosystemRegistry, ComponentEntry, EntryType, get_registry
from .federation import Federation, NodeInfo, ConnectionStatus, create_federation
from .automation import AutomationEngine, WorkflowStep, StepResult, Automator
from .global_ import GlobalContext, ContextScope, get_global_context
from .sdk import EcosystemSDK, ClientConfig, create_client

__all__ = [
    "EcosystemRegistry",
    "ComponentEntry", 
    "EntryType",
    "get_registry",
    "Federation",
    "NodeInfo",
    "ConnectionStatus",
    "create_federation",
    "AutomationEngine",
    "WorkflowStep",
    "StepResult",
    "Automator",
    "GlobalContext",
    "ContextScope",
    "get_global_context",
    "EcosystemSDK",
    "ClientConfig",
    "create_client",
]

__version__ = "1.0.0"
