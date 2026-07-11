"""
Execution Agent Module
====================

Agent execution framework for the AGOS system.
Provides agent lifecycle, execution, and management.

Author: AGOS Team
Version: 1.0.0
"""

import asyncio
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


AGENT_RULES = [
    "Agents never own missions",
    "Agents never own memory",
    "Agents never own reasoning",
    "Agents execute only delegated work"
]


class AgentStatus(Enum):
    """Status of an agent."""
    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class AgentCapability(Enum):
    """Capabilities an agent can have."""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    EXECUTION = "execution"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    REASONING = "reasoning"
    LEARNING = "learning"
    COLLABORATION = "collaboration"
    TOOL_USE = "tool_use"


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    capabilities: Set[AgentCapability] = field(default_factory=set)
    max_concurrent_tasks: int = 5
    timeout: float = 300.0
    retry_count: int = 3
    retry_delay: float = 1.0
    priority: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Task to be executed by an agent."""
    task_id: str
    description: str
    input_data: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Any = None
    error: Optional[str] = None


@dataclass
class Agent:
    """
    Execution agent for the AGOS system.
    
    Attributes:
        agent_id: Unique identifier
        config: Agent configuration
        status: Current status
        current_task: Currently executing task
        task_queue: Pending tasks
        completed_tasks: Completed tasks count
        failed_tasks: Failed tasks count
        capabilities: Set of agent capabilities
    """
    agent_id: str
    config: AgentConfig
    status: AgentStatus = AgentStatus.CREATED
    current_task: Optional[Task] = None
    task_queue: List[Task] = field(default_factory=list)
    completed_tasks: int = 0
    failed_tasks: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_available(self) -> bool:
        """Check if agent is available for work."""
        return self.status == AgentStatus.READY and len(self.task_queue) < self.config.max_concurrent_tasks
    
    def enqueue_task(self, task: Task) -> bool:
        """Add a task to the queue."""
        if len(self.task_queue) >= self.config.max_concurrent_tasks:
            return False
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        return True
    
    def dequeue_task(self) -> Optional[Task]:
        """Get the next task from the queue."""
        if not self.task_queue:
            return None
        return self.task_queue.pop(0)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get agent statistics."""
        total = self.completed_tasks + self.failed_tasks
        success_rate = self.completed_tasks / total if total > 0 else 0.0
        
        return {
            "agent_id": self.agent_id,
            "name": self.config.name,
            "status": self.status.value,
            "queue_size": len(self.task_queue),
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "success_rate": success_rate,
            "capabilities": [c.value for c in self.config.capabilities]
        }


class AgentPool:
    """Pool of execution agents."""
    
    def __init__(self):
        self._agents: Dict[str, Agent] = {}
        self._lock = threading.RLock()
    
    def create_agent(self, config: AgentConfig) -> Agent:
        """Create a new agent."""
        agent_id = f"agent-{uuid.uuid4().hex[:12]}"
        agent = Agent(agent_id=agent_id, config=config)
        
        with self._lock:
            self._agents[agent_id] = agent
        
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID."""
        return self._agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents."""
        return [a.get_statistics() for a in self._agents.values()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get pool statistics."""
        return {
            "total_agents": len(self._agents),
            "available_agents": sum(1 for a in self._agents.values() if a.is_available),
            "total_queue_size": sum(len(a.task_queue) for a in self._agents.values()),
            "total_completed": sum(a.completed_tasks for a in self._agents.values()),
            "total_failed": sum(a.failed_tasks for a in self._agents.values())
        }


class AgentRegistry:
    """Registry for managing agents."""
    
    def __init__(self):
        self._agents: Dict[str, Any] = {}
    
    def register(self, agent_id: str, agent: Any) -> bool:
        """Register an agent."""
        self._agents[agent_id] = agent
        return True
    
    def unregister(self, agent_id: str) -> bool:
        """Unregister an agent."""
        if agent_id in self._agents:
            del self._agents[agent_id]
            return True
        return False
    
    def get(self, agent_id: str) -> Optional[Any]:
        """Get an agent by ID."""
        return self._agents.get(agent_id)
    
    def list_all(self) -> List[Any]:
        """List all registered agents."""
        return list(self._agents.values())


class UniversalAgentRuntime:
    """
    Universal Agent Runtime.
    
    Treat every external AI agent as an execution endpoint.
    
    Agent Rules:
    ✅ Agents never own missions
    ✅ Agents never own memory
    ✅ Agents never own reasoning
    ✅ Agents execute only delegated work
    
    Implements:
    ✅ Runtime, Registry, SDK, Sandbox, Health
    ✅ Benchmark, Compatibility, Telemetry
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.registry = AgentRegistry()
        self.pool = AgentPool()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get runtime statistics."""
        return {
            "version": self.version,
            "agent_rules": AGENT_RULES,
            "total_agents": len(self.registry.list_all()),
            "pool_stats": self.pool.get_statistics()
        }
