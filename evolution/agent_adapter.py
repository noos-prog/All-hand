"""
Agent Adapter Module
=================

Universal adapter framework for integrating external agents.
Enables AGOS to coordinate with any autonomous agent system.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

TARGET_AGENTS = [
    "GitHub Coding Agent", "MCP Agent", "CLI Agent", "IDE Agent",
    "Cloud Agent", "Browser Agent", "Future Agent Protocol"
]


class AgentType(Enum):
    """Types of agents that can be adapted."""
    GITHUB_CODING = "github_coding"
    MCP = "mcp"
    CLI = "cli"
    IDE = "ide"
    CLOUD = "cloud"
    BROWSER = "browser"
    CUSTOM = "custom"


class AdapterStatus(Enum):
    """Status of an agent adapter."""
    REGISTERED = "registered"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    BLOCKED = "blocked"


@dataclass
class AgentAdapter:
    """Adapter for integrating external agents into AGOS."""
    adapter_id: str
    agent_type: str
    version: str
    capabilities: Set[str] = field(default_factory=set)
    status: AdapterStatus = AdapterStatus.REGISTERED
    supported_tasks: Set[str] = field(default_factory=set)
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    usage_count: int = 0
    
    def activate(self) -> None:
        """Activate the adapter."""
        self.status = AdapterStatus.ACTIVE
    
    def deactivate(self) -> None:
        """Deactivate the adapter."""
        self.status = AdapterStatus.INACTIVE
    
    def record_usage(self) -> None:
        """Record adapter usage."""
        self.usage_count += 1
        self.last_used = datetime.utcnow()


class CapabilityTranslator:
    """Translates capabilities between AGOS and external agents."""
    
    def __init__(self):
        self.translations: Dict[str, str] = {
            "code_generation": "generate_code",
            "code_review": "review_code",
            "execution": "execute_task",
            "analysis": "analyze_data",
            "planning": "create_plan",
        }
    
    def translate_to_agent(self, capability: str) -> str:
        """Translate AGOS capability to agent-specific format."""
        return self.translations.get(capability, capability)
    
    def translate_from_agent(self, capability: str) -> str:
        """Translate agent capability to AGOS format."""
        reverse_translations = {v: k for k, v in self.translations.items()}
        return reverse_translations.get(capability, capability)
    
    def translate_batch(self, capabilities: List[str], to_agent: bool = True) -> List[str]:
        """Translate multiple capabilities."""
        if to_agent:
            return [self.translate_to_agent(c) for c in capabilities]
        return [self.translate_from_agent(c) for c in capabilities]


class TaskTranslator:
    """Translates tasks between AGOS and external agents."""
    
    def __init__(self):
        self.task_templates: Dict[str, Dict[str, Any]] = {}
    
    def translate_to_agent(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Translate AGOS task to agent-specific format."""
        return {
            "task_id": task.get("id", task.get("task_id")),
            "description": task.get("description"),
            "input": task.get("input_data", task.get("input")),
            "constraints": task.get("constraints", {}),
            "expected_output": task.get("expected_output"),
        }
    
    def translate_from_agent(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Translate agent result to AGOS format."""
        return {
            "task_id": result.get("task_id"),
            "output": result.get("output", result.get("result")),
            "success": result.get("success", True),
            "metrics": result.get("metrics", {}),
            "logs": result.get("logs", []),
        }


class ContextTranslator:
    """Translates context between AGOS and external agents."""
    
    def translate_to_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Translate AGOS context to agent-specific format."""
        return {
            "workspace": context.get("workspace"),
            "capabilities": context.get("available_capabilities", []),
            "tools": context.get("available_tools", []),
            "history": context.get("execution_history", []),
            "preferences": context.get("agent_preferences", {}),
        }
    
    def translate_from_agent(self, agent_context: Dict[str, Any]) -> Dict[str, Any]:
        """Translate agent context to AGOS format."""
        return {
            "agent_state": agent_context.get("state", {}),
            "agent_memory": agent_context.get("memory", {}),
            "agent_knowledge": agent_context.get("knowledge", []),
        }


class ResultTranslator:
    """Translates results between AGOS and external agents."""
    
    def translate_to_agos(self, agent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Translate agent result to AGOS format."""
        return {
            "result_id": agent_result.get("id", uuid.uuid4().hex[:8]),
            "success": agent_result.get("success", True),
            "output": agent_result.get("output", agent_result.get("result")),
            "artifacts": agent_result.get("artifacts", []),
            "metrics": agent_result.get("metrics", {}),
            "errors": agent_result.get("errors", []),
            "execution_time": agent_result.get("execution_time", 0),
        }
    
    def translate_from_agos(self, agos_result: Dict[str, Any]) -> Dict[str, Any]:
        """Translate AGOS result to agent format."""
        return {
            "id": agos_result.get("result_id"),
            "success": agos_result.get("success", True),
            "output": agos_result.get("output"),
            "artifacts": agos_result.get("artifacts", []),
        }


class ValidationLayer:
    """Validates adapter operations."""
    
    def __init__(self):
        self.validation_rules: Dict[str, Callable] = {}
    
    def validate(self, adapter: AgentAdapter, operation: str = "default") -> bool:
        """Validate adapter for an operation."""
        if adapter.status == AdapterStatus.BLOCKED:
            return False
        
        if adapter.status == AdapterStatus.INACTIVE:
            return False
        
        rule = self.validation_rules.get(operation)
        if rule:
            return rule(adapter)
        
        return True
    
    def add_rule(self, operation: str, rule: Callable) -> None:
        """Add a validation rule."""
        self.validation_rules[operation] = rule


class SecurityLayer:
    """Security checks for agent adapters."""
    
    def __init__(self):
        self.allowed_operations: Set[str] = {"read", "write", "execute"}
        self.blocked_agents: Set[str] = set()
    
    def check(self, adapter: AgentAdapter, operation: str) -> Dict[str, Any]:
        """Perform security check."""
        if adapter.agent_type in self.blocked_agents:
            return {
                "allowed": False,
                "reason": f"Agent type {adapter.agent_type} is blocked",
            }
        
        if operation not in self.allowed_operations:
            return {
                "allowed": False,
                "reason": f"Operation {operation} not allowed",
            }
        
        return {
            "allowed": True,
            "checked_at": datetime.utcnow().isoformat(),
        }
    
    def block_agent(self, agent_type: str) -> None:
        """Block an agent type."""
        self.blocked_agents.add(agent_type)
    
    def unblock_agent(self, agent_type: str) -> None:
        """Unblock an agent type."""
        self.blocked_agents.discard(agent_type)


class IsolationLayer:
    """Isolation mechanisms for agent adapters."""
    
    def __init__(self):
        self.isolated_adapters: Set[str] = set()
    
    def isolate(self, adapter: AgentAdapter, enabled: bool = True) -> Dict[str, Any]:
        """Enable or disable isolation for an adapter."""
        if enabled:
            self.isolated_adapters.add(adapter.adapter_id)
        else:
            self.isolated_adapters.discard(adapter.adapter_id)
        
        return {
            "isolation": enabled,
            "adapter_id": adapter.adapter_id,
        }
    
    def is_isolated(self, adapter_id: str) -> bool:
        """Check if adapter is isolated."""
        return adapter_id in self.isolated_adapters


class AgentEvolution:
    """Self-evolving agent integration system."""
    
    def __init__(self):
        self.adapters: Dict[str, AgentAdapter] = {}
        self.capability_translator = CapabilityTranslator()
        self.task_translator = TaskTranslator()
        self.context_translator = ContextTranslator()
        self.result_translator = ResultTranslator()
        self.validation = ValidationLayer()
        self.security = SecurityLayer()
        self.isolation = IsolationLayer()
        self.evolution_history: List[Dict[str, Any]] = []
    
    def register_agent(
        self,
        agent_type: str,
        version: str,
        capabilities: Optional[List[str]] = None,
        supported_tasks: Optional[List[str]] = None,
    ) -> AgentAdapter:
        """Register a new agent adapter."""
        adapter = AgentAdapter(
            adapter_id=f"adapter_{agent_type}_{uuid.uuid4().hex[:6]}",
            agent_type=agent_type,
            version=version,
            capabilities=set(capabilities) if capabilities else set(),
            supported_tasks=set(supported_tasks) if supported_tasks else set(),
        )
        self.adapters[adapter.adapter_id] = adapter
        return adapter
    
    def get_adapter(self, adapter_id: str) -> Optional[AgentAdapter]:
        """Get an adapter by ID."""
        return self.adapters.get(adapter_id)
    
    def get_active_adapters(self) -> List[AgentAdapter]:
        """Get all active adapters."""
        return [a for a in self.adapters.values() if a.status == AdapterStatus.ACTIVE]
    
    def execute_task(
        self,
        adapter_id: str,
        task: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute a task through an adapter."""
        adapter = self.adapters.get(adapter_id)
        if not adapter:
            return {"success": False, "error": "Adapter not found"}
        
        if not self.validation.validate(adapter):
            return {"success": False, "error": "Validation failed"}
        
        security_check = self.security.check(adapter, "execute")
        if not security_check.get("allowed"):
            return {"success": False, "error": security_check.get("reason")}
        
        translated_task = self.task_translator.translate_to_agent(task)
        translated_context = self.context_translator.translate_to_agent(context or {})
        
        adapter.record_usage()
        
        return {
            "success": True,
            "adapter_id": adapter_id,
            "translated_task": translated_task,
            "translated_context": translated_context,
        }
    
    def evolve(self) -> Dict[str, Any]:
        """Evolve the agent integration system."""
        evolution_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_adapters": len(self.adapters),
            "active_adapters": len(self.get_active_adapters()),
        }
        
        self.evolution_history.append(evolution_result)
        return evolution_result
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get adapter statistics."""
        by_type: Dict[str, int] = {}
        by_status: Dict[str, int] = {}
        
        for adapter in self.adapters.values():
            by_type[adapter.agent_type] = by_type.get(adapter.agent_type, 0) + 1
            by_status[adapter.status.value] = by_status.get(adapter.status.value, 0) + 1
        
        return {
            "target_agents": TARGET_AGENTS,
            "registered_adapters": len(self.adapters),
            "by_type": by_type,
            "by_status": by_status,
            "total_usage": sum(a.usage_count for a in self.adapters.values()),
        }


# Backwards compatibility
UniversalAgentAdapterFramework = AgentEvolution
