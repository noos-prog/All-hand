#!/usr/bin/env python3
"""
AGOS Kernel System
=================

The central orchestrator for all AGOS components.
Controls lifecycle, dependencies, and execution flow.

RULES (from Constitution):
- Kernel never contains business logic
- Kernel orchestrates only
- Every action passes through governance
- Every result is logged
- Every error is recorded
"""

import logging
import os
import sys
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# Ensure proper imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from registry.component import get_component_registry, ComponentRegistry, ComponentType, Component
from registry.cap_registry import get_capability_registry, CapabilityRegistry, CapabilityType, Capability
from registry.provider_registry import get_provider_registry, ProviderRegistry, ProviderType, Provider
from registry.workflow_registry import get_workflow_registry, WorkflowRegistry, WorkflowStatus
from registry.knowledge_registry import get_knowledge_registry, KnowledgeRegistry, KnowledgeType, KnowledgeEntry


class KernelStatus(Enum):
    """Kernel status."""
    INITIALIZING = "initializing"
    BOOTSTRAPPING = "bootstrapping"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    SHUTDOWN = "shutdown"


class KernelEvent(Enum):
    """Kernel events."""
    STARTED = "kernel_started"
    COMPONENT_REGISTERED = "component_registered"
    COMPONENT_ACTIVATED = "component_activated"
    WORKFLOW_EXECUTED = "workflow_executed"
    KNOWLEDGE_STORED = "knowledge_stored"
    ERROR = "kernel_error"
    SHUTDOWN = "kernel_shutdown"


@dataclass
class KernelConfig:
    """Kernel configuration."""
    name: str = "AGOS-Kernel"
    version: str = "1.0.0"
    enable_logging: bool = True
    enable_governance: bool = True
    enable_knowledge: bool = True
    bootstrap_timeout: int = 60
    health_check_interval: int = 60


@dataclass
class ExecutionLog:
    """Log of an execution."""
    id: str
    timestamp: datetime
    component: str
    action: str
    input: Dict[str, Any]
    output: Any
    error: Optional[str] = None
    duration_ms: float = 0


@dataclass
class KernelState:
    """Current kernel state."""
    status: KernelStatus = KernelStatus.INITIALIZING
    components_registered: int = 0
    components_active: int = 0
    workflows_executed: int = 0
    knowledge_entries: int = 0
    errors: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    uptime_seconds: float = 0


class AGOSKernel:
    """
    AGOS Kernel - Central orchestrator for all AGOS components.
    
    Responsibilities:
    1. System bootstrap and initialization
    2. Dependency management
    3. Lifecycle control
    4. Execution orchestration
    5. Logging and monitoring
    6. Governance enforcement
    
    Usage:
        kernel = AGOSKernel()
        kernel.start()
        result = kernel.execute("workflow_id", {"input": data})
        kernel.shutdown()
    """
    
    _instance: Optional['AGOSKernel'] = None
    _lock = threading.Lock()
    
    def __init__(self, config: Optional[KernelConfig] = None):
        """Initialize kernel."""
        self.config = config or KernelConfig()
        self.status = KernelStatus.INITIALIZING
        self.state = KernelState()
        
        # Registries
        self.component_registry = get_component_registry()
        self.capability_registry = get_capability_registry()
        self.provider_registry = get_provider_registry()
        self.workflow_registry = get_workflow_registry()
        self.knowledge_registry = get_knowledge_registry()
        
        # Logging
        self.logger = logging.getLogger(f"agos.kernel.{self.config.name}")
        self._execution_logs: List[ExecutionLog] = []
        self._logs_lock = threading.Lock()
        
        # Events
        self._event_handlers: Dict[KernelEvent, List[callable]] = {
            event: [] for event in KernelEvent
        }
        
        # Health check thread
        self._health_check_thread: Optional[threading.Thread] = None
        self._running = False
    
    @classmethod
    def get_instance(cls) -> 'AGOSKernel':
        """Get singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def start(self) -> bool:
        """
        Start the kernel.
        
        Steps:
        1. Bootstrap - initialize registries
        2. Register built-in components
        3. Register built-in capabilities
        4. Register built-in providers
        5. Register built-in workflows
        6. Activate all components
        7. Start health check thread
        """
        try:
            self.logger.info(f"Starting {self.config.name} v{self.config.version}")
            self.status = KernelStatus.BOOTSTRAPPING
            self.state.started_at = datetime.utcnow()
            
            # Step 1: Register built-in components
            try:
                self._register_builtin_components()
            except Exception as e:
                self.logger.warning(f"Component registration failed (continuing): {e}")
            
            # Step 2: Register built-in capabilities
            try:
                self._register_builtin_capabilities()
            except Exception as e:
                self.logger.warning(f"Capability registration failed (continuing): {e}")
            
            # Step 3: Register built-in providers
            try:
                self._register_builtin_providers()
            except Exception as e:
                self.logger.warning(f"Provider registration failed (continuing): {e}")
            
            # Step 4: Register built-in workflows
            try:
                self._register_builtin_workflows()
            except Exception as e:
                self.logger.warning(f"Workflow registration failed (continuing): {e}")
            
            # Step 5: Activate all components
            try:
                self._activate_components()
            except Exception as e:
                self.logger.warning(f"Component activation failed (continuing): {e}")
            
            # Step 6: Initialize knowledge with base entries
            try:
                self._initialize_knowledge()
            except Exception as e:
                self.logger.warning(f"Knowledge initialization failed (continuing): {e}")
            
            # Step 7: Start health check thread
            self._running = True
            self._health_check_thread = threading.Thread(target=self._health_check_loop, daemon=True)
            self._health_check_thread.start()
            
            self.status = KernelStatus.READY
            self.logger.info(f"Kernel started successfully")
            self._emit_event(KernelEvent.STARTED, {"status": "ready"})
            
            return True
            
        except Exception as e:
            self.logger.error(f"Kernel startup failed: {e}")
            import traceback
            traceback.print_exc()
            self.status = KernelStatus.ERROR
            self.state.errors.append(str(e))
            self._emit_event(KernelEvent.ERROR, {"error": str(e)})
            return False
    
    def _register_builtin_components(self) -> None:
        """Register built-in components."""
        from brain.engine import EngineeringBrain
        from knowledge.runtime import KnowledgeRuntime
        from memory.runtime import MemoryRuntime
        from learning.runtime import LearningRuntime
        from experience.runtime import ExperienceRuntime
        from governance.runtime import GovernanceRuntime
        
        components = [
            (EngineeringBrain, "brain", ComponentType.ENGINE),
            (KnowledgeRuntime, "knowledge", ComponentType.RUNTIME),
            (MemoryRuntime, "memory", ComponentType.RUNTIME),
            (LearningRuntime, "learning", ComponentType.RUNTIME),
            (ExperienceRuntime, "experience", ComponentType.RUNTIME),
            (GovernanceRuntime, "governance", ComponentType.GOVERNANCE),
        ]
        
        for cls, name, comp_type in components:
            self.component_registry.register(
                cls=cls,
                component_id=name,
                component_type=comp_type,
                metadata={"builtin": True}
            )
        
        self.state.components_registered = len(self.component_registry.list_all())
        self.logger.info(f"Registered {self.state.components_registered} components")
    
    def _register_builtin_capabilities(self) -> None:
        """Register built-in capabilities."""
        from capabilities.foundation.capability_001_discovery import RepositoryDiscoveryCapability
        from capabilities.foundation.capability_002_clone import RepositoryCloneCapability
        from capabilities.foundation.capability_004_fingerprint import RepositoryFingerprintCapability
        from capabilities.foundation.capability_006_technology import TechnologyDetectionCapability
        from capabilities.foundation.capability_019_dna import RepositoryDNACapability
        
        capabilities = [
            ("CAP-000001", "Repository Discovery", CapabilityType.REPOSITORY, RepositoryDiscoveryCapability),
            ("CAP-000002", "Repository Clone", CapabilityType.REPOSITORY, RepositoryCloneCapability),
            ("CAP-000004", "Repository Fingerprint", CapabilityType.REPOSITORY, RepositoryFingerprintCapability),
            ("CAP-000006", "Technology Detection", CapabilityType.ANALYSIS, TechnologyDetectionCapability),
            ("CAP-000019", "Repository DNA", CapabilityType.ANALYSIS, RepositoryDNACapability),
        ]
        
        for cap_id, name, cap_type, cls in capabilities:
            self.capability_registry.register(
                id=cap_id,
                name=name,
                capability_type=cap_type,
                handler=cls(),
            )
        
        self.logger.info(f"Registered {len(capabilities)} capabilities")
    
    def _register_builtin_providers(self) -> None:
        """Register built-in providers."""
        from providers.implementation import OpenAIProvider, GitHubProvider, AnthropicProvider
        from providers.filesystem import FilesystemProvider
        
        providers = [
            ("PROV-000001", "OpenAI", ProviderType.LLM, OpenAIProvider),
            ("PROV-000002", "GitHub", ProviderType.GIT, GitHubProvider),
            ("PROV-000003", "Anthropic", ProviderType.LLM, AnthropicProvider),
            ("PROV-000004", "Filesystem", ProviderType.FILESYSTEM, FilesystemProvider),
        ]
        
        for prov_id, name, prov_type, cls in providers:
            self.provider_registry.register(
                id=prov_id,
                name=name,
                provider_type=prov_type,
                handler=cls(),
            )
        
        self.logger.info(f"Registered {len(providers)} providers")
    
    def _register_builtin_workflows(self) -> None:
        """Register built-in workflows."""
        from registry.workflow_registry import WorkflowStep, Workflow
        
        # Repository Analysis Workflow
        workflow = Workflow(
            id="WORKFLOW-000001",
            name="Repository Analysis",
            description="Analyze a repository and generate its DNA",
        )
        
        # Step 1: Discovery
        workflow.add_step(WorkflowStep(
            id="step_1",
            name="Discover Repository",
            action="discover",
            inputs={},
            retry_count=2,
        ))
        
        # Step 2: Clone
        workflow.add_step(WorkflowStep(
            id="step_2",
            name="Clone Repository",
            action="clone",
            inputs={"url": "$discovered_url"},
            retry_count=1,
        ))
        
        # Step 3: Analysis
        workflow.add_step(WorkflowStep(
            id="step_3",
            name="Analyze Repository",
            action="analyze",
            inputs={"path": "$cloned_path"},
            retry_count=0,
        ))
        
        # Step 4: Generate DNA
        workflow.add_step(WorkflowStep(
            id="step_4",
            name="Generate DNA",
            action="generate_dna",
            inputs={"analysis": "$analysis_result"},
            retry_count=0,
        ))
        
        # Register handlers
        workflow.handlers = {
            "discover": self._wf_discover,
            "clone": self._wf_clone,
            "analyze": self._wf_analyze,
            "generate_dna": self._wf_generate_dna,
        }
        
        self.workflow_registry.register(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description,
            steps=workflow.steps,
            handlers=workflow.handlers,
        )
        
        self.logger.info(f"Registered 1 workflow")
    
    def _activate_components(self) -> None:
        """Activate all registered components."""
        results = self.component_registry.activate_all()
        active_count = sum(1 for v in results.values() if v)
        self.state.components_active = active_count
        self.logger.info(f"Activated {active_count}/{len(results)} components")
    
    def _initialize_knowledge(self) -> None:
        """Initialize knowledge base with foundational entries."""
        # Add architecture knowledge
        self.knowledge_registry.add(
            title="AGOS Architecture",
            knowledge_type=KnowledgeType.ARCHITECTURE,
            content={
                "description": "AGOS Kernel-based autonomous engineering system",
                "components": ["Kernel", "Brain", "Runtime", "Registry", "Capability", "Provider", "Workflow"],
                "principles": ["Kernel has no business logic", "Evidence before claims", "Everything is replaceable"],
            },
            tags=["architecture", "agos", "kernel"],
        )
        
        self.state.knowledge_entries = len(self.knowledge_registry.list_all())
    
    def execute(self, workflow_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a workflow.
        
        Args:
            workflow_id: ID of workflow to execute
            input_data: Input data for workflow
            
        Returns:
            Execution result
        """
        if self.status not in [KernelStatus.READY, KernelStatus.RUNNING]:
            return {"error": "Kernel not ready", "status": self.status.value}
        
        start_time = time.time()
        self.status = KernelStatus.RUNNING
        
        log = ExecutionLog(
            id=f"exec_{int(start_time * 1000)}",
            timestamp=datetime.utcnow(),
            component="kernel",
            action="execute_workflow",
            input=input_data,
            output=None,
        )
        
        try:
            # Get workflow
            workflow = self.workflow_registry.get(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            # Execute workflow
            result = workflow.execute(input_data)
            
            log.output = result
            log.duration_ms = (time.time() - start_time) * 1000
            
            # Store in knowledge
            if self.config.enable_knowledge:
                self.knowledge_registry.add(
                    title=f"Workflow Execution: {workflow.name}",
                    knowledge_type=KnowledgeType.EXPERIENCE,
                    content={
                        "workflow_id": workflow_id,
                        "input": input_data,
                        "result": result,
                        "duration_ms": log.duration_ms,
                    },
                    tags=["workflow", workflow_id],
                )
                self.state.knowledge_entries += 1
            
            self.state.workflows_executed += 1
            self._emit_event(KernelEvent.WORKFLOW_EXECUTED, {"workflow_id": workflow_id})
            
            return {"status": "success", "result": result}
            
        except Exception as e:
            log.error = str(e)
            log.duration_ms = (time.time() - start_time) * 1000
            self.state.errors.append(str(e))
            self._emit_event(KernelEvent.ERROR, {"error": str(e)})
            
            return {"status": "error", "error": str(e)}
        
        finally:
            self._log_execution(log)
            self.status = KernelStatus.READY
    
    def _wf_discover(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow step: Discover repository."""
        url = inputs.get("url")
        cap = self.capability_registry.get("CAP-000001")
        if cap and url:
            desc = cap.execute({"source": url})
            return {"discovered_url": desc.url, "path": desc.path}
        return {}
    
    def _wf_clone(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow step: Clone repository."""
        url = inputs.get("url") or inputs.get("$discovered_url")
        cap = self.capability_registry.get("CAP-000002")
        if cap and url:
            result = cap.execute({"source": url})
            return {"cloned_path": result.path}
        return {}
    
    def _wf_analyze(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow step: Analyze repository."""
        path = inputs.get("path") or inputs.get("$cloned_path")
        cap = self.capability_registry.get("CAP-000006")
        if cap and path:
            profile = cap.execute({"path": path})
            return {"analysis_result": profile.to_dict()}
        return {}
    
    def _wf_generate_dna(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow step: Generate DNA."""
        analysis = inputs.get("analysis") or inputs.get("$analysis_result")
        cap = self.capability_registry.get("CAP-000019")
        if cap:
            dna = cap.execute({"path": analysis.get("path") if isinstance(analysis, dict) else None})
            return {"dna": dna.to_dict() if hasattr(dna, 'to_dict') else str(dna)}
        return {}
    
    def _log_execution(self, log: ExecutionLog) -> None:
        """Log an execution."""
        with self._logs_lock:
            self._execution_logs.append(log)
            # Keep only last 1000 logs
            if len(self._execution_logs) > 1000:
                self._execution_logs = self._execution_logs[-1000:]
    
    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get execution logs."""
        with self._logs_lock:
            return [log.__dict__ for log in self._execution_logs[-limit:]]
    
    def get_state(self) -> KernelState:
        """Get current kernel state."""
        self.state.status = self.status
        if self.state.started_at:
            self.state.uptime_seconds = (datetime.utcnow() - self.state.started_at).total_seconds()
        return self.state
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        return {
            "status": "healthy" if self.status == KernelStatus.READY else "degraded",
            "kernel_status": self.status.value,
            "components": self.component_registry.check_health(),
            "capabilities": self.capability_registry.check_health(),
            "providers": self.provider_registry.check_health(),
            "workflows": self.workflow_registry.check_health(),
            "knowledge": self.knowledge_registry.check_health(),
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def _health_check_loop(self) -> None:
        """Background health check loop."""
        while self._running:
            time.sleep(self.config.health_check_interval)
            if self._running:
                self.logger.debug("Health check: OK")
    
    def on_event(self, event: KernelEvent, handler: callable) -> None:
        """Register event handler."""
        if event in self._event_handlers:
            self._event_handlers[event].append(handler)
    
    def _emit_event(self, event: KernelEvent, data: Dict[str, Any]) -> None:
        """Emit kernel event."""
        for handler in self._event_handlers.get(event, []):
            try:
                handler(data)
            except Exception as e:
                self.logger.error(f"Event handler error: {e}")
    
    def shutdown(self) -> bool:
        """Shutdown the kernel."""
        try:
            self.logger.info("Shutting down kernel...")
            self._running = False
            
            # Deactivate components
            self.component_registry.deactivate_all()
            
            # Emit shutdown event
            self._emit_event(KernelEvent.SHUTDOWN, {})
            
            self.status = KernelStatus.SHUTDOWN
            self.logger.info("Kernel shutdown complete")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.shutdown()


# Global kernel instance
def get_kernel() -> AGOSKernel:
    """Get the global kernel instance."""
    return AGOSKernel.get_instance()
