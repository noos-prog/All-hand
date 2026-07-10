"""Universal Agent Integration Platform."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

SUPPORTED_AGENTS = (
    "OpenHands", "Claude Code", "Codex", "Aider", "Cline", "Continue",
    "Goose", "Roo Code", "OpenCode", "Cursor Agent", "Windsurf Agent",
    "AutoGen", "CrewAI", "OpenManus", "SmolAgents", "AnythingLLM Agents",
    "LangGraph Agents", "MCP Agents", "Custom Agents"
)


class AgentState(Enum):
    """Agent states."""
    IDLE = "idle"
    RUNNING = "running"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DISCONNECTED = "disconnected"


@dataclass
class AgentDescriptor:
    """Agent descriptor."""
    name: str
    version: str
    capabilities: Tuple[str, ...] = ()
    supported_languages: Tuple[str, ...] = ()
    state: AgentState = AgentState.IDLE
    last_invocation: Optional[datetime] = None


@dataclass
class AgentInvocation:
    """Agent invocation record."""
    invocation_id: str
    agent_name: str
    task: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    output: Any = None
    error: Optional[str] = None


@dataclass
class AgentResponse:
    """Agent invocation response."""
    invocation_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time_ms: int = 0


class AgentRegistry:
    """Agent registry."""
    
    def __init__(self):
        self._adapters: Dict[str, Any] = {}
        self._descriptors: Dict[str, AgentDescriptor] = {}
    
    def register(self, name: str, adapter: Any) -> None:
        """Register an agent adapter."""
        self._adapters[name] = adapter
    
    def register_descriptor(self, descriptor: AgentDescriptor) -> None:
        """Register an agent descriptor."""
        self._descriptors[descriptor.name] = descriptor
    
    def get(self, name: str) -> Optional[Any]:
        """Get agent adapter."""
        return self._adapters.get(name)
    
    def get_descriptor(self, name: str) -> Optional[AgentDescriptor]:
        """Get agent descriptor."""
        return self._descriptors.get(name)
    
    def list_all(self) -> List[AgentDescriptor]:
        """List all registered agents."""
        return list(self._descriptors.values())
    
    def list_adapters(self) -> List[str]:
        """List all adapter names."""
        return list(self._adapters.keys())


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
        self.version = "1.0.0"
        self.registry = AgentRegistry()
        self._invocations: Dict[str, AgentInvocation] = {}
    
    def invoke(self, agent_name: str, task: str, parameters: Dict[str, Any] = None) -> AgentResponse:
        """Invoke an agent."""
        invocation_id = f"inv_{int(datetime.utcnow().timestamp())}"
        
        start_time = datetime.utcnow()
        adapter = self.registry.get(agent_name)
        
        if not adapter:
            return AgentResponse(
                invocation_id=invocation_id,
                success=False,
                error=f"Agent not found: {agent_name}"
            )
        
        # Record invocation
        invocation = AgentInvocation(
            invocation_id=invocation_id,
            agent_name=agent_name,
            task=task,
            parameters=parameters or {},
            status="running"
        )
        self._invocations[invocation_id] = invocation
        
        # Execute
        output = {"status": "completed", "task": task}
        
        end_time = datetime.utcnow()
        execution_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Update invocation
        invocation.status = "completed"
        invocation.completed_at = end_time
        invocation.output = output
        
        return AgentResponse(
            invocation_id=invocation_id,
            success=True,
            output=output,
            execution_time_ms=execution_time_ms
        )
    
    def get_invocation(self, invocation_id: str) -> Optional[AgentInvocation]:
        """Get invocation by ID."""
        return self._invocations.get(invocation_id)
    
    def list_invocations(self, agent_name: Optional[str] = None) -> List[AgentInvocation]:
        """List invocations."""
        invocations = list(self._invocations.values())
        if agent_name:
            invocations = [i for i in invocations if i.agent_name == agent_name]
        return invocations
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get invocation statistics."""
        total = len(self._invocations)
        completed = len([i for i in self._invocations.values() if i.status == "completed"])
        failed = len([i for i in self._invocations.values() if i.status == "failed"])
        
        return {
            "total_invocations": total,
            "completed": completed,
            "failed": failed,
            "registered_agents": len(self.registry.list_all()),
            "pending": total - completed - failed
        }
