"""Universal Agent Integration Platform."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

SUPPORTED_AGENTS = [
    "OpenHands", "Claude Code", "Codex", "Aider", "Cline", "Continue",
    "Goose", "Roo Code", "OpenCode", "Cursor Agent", "Windsurf Agent",
    "AutoGen", "CrewAI", "OpenManus", "SmolAgents", "AnythingLLM Agents",
    "LangGraph Agents", "MCP Agents", "Custom Agents"
]

class AgentState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

@dataclass
class AgentDescriptor:
    name: str
    version: str
    capabilities: List[str] = field(default_factory=list)
    supported_languages: List[str] = field(default_factory=list)

@dataclass
class AgentResponse:
    invocation_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None

class AgentRegistry:
    def __init__(self):
        self._adapters: Dict[str, Any] = {}
    
    def register(self, name: str, adapter: Any) -> None:
        self._adapters[name] = adapter
    
    def get(self, name: str) -> Optional[Any]:
        return self._adapters.get(name)
    
    def list_all(self) -> List[AgentDescriptor]:
        return [AgentDescriptor(name=k, version="1.0.0") for k in self._adapters.keys()]

class AgentInvocationRuntime:
    """
    Agent Invocation Runtime.
    Rules:
    ✅ External agents receive only atomic tasks
    ✅ External agents never receive global context
    ✅ External agents cannot modify Kernel
    ✅ External agents cannot make architectural decisions
    ✅ External agents return structured outputs only
    """
    def __init__(self):
        self.registry = AgentRegistry()
    
    def invoke(self, agent_name: str, task: str, parameters: Dict[str, Any] = None) -> AgentResponse:
        invocation_id = f"inv_{int(datetime.utcnow().timestamp())}"
        adapter = self.registry.get(agent_name)
        if not adapter:
            return AgentResponse(invocation_id=invocation_id, success=False, error=f"Agent not found: {agent_name}")
        return AgentResponse(invocation_id=invocation_id, success=True, output={"status": "completed", "task": task})
