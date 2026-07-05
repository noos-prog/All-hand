"""
AGOS Workflow Registry
==================

Registry for all AGOS workflows.
Every workflow must be registered to be executable by the Kernel.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import threading


class WorkflowStatus(Enum):
    """Workflow status."""
    REGISTERED = "registered"
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStepStatus(Enum):
    """Workflow step status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowStep:
    """
    A step in a workflow.
    
    Attributes:
        id: Step identifier
        name: Human-readable name
        action: Action to perform (capability ID or function)
        inputs: Input parameters
        outputs: Output mappings
        retry_count: Number of retries on failure
        timeout: Timeout in seconds
        conditions: Conditions for step execution
    """
    id: str
    name: str
    action: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, str] = field(default_factory=dict)  # output_name -> variable_name
    retry_count: int = 0
    timeout: int = 300
    conditions: Dict[str, Any] = field(default_factory=dict)
    status: WorkflowStepStatus = WorkflowStepStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class Workflow:
    """
    A registered AGOS workflow.
    
    Attributes:
        id: Unique identifier (e.g., WORKFLOW-000001)
        name: Human-readable name
        description: What this workflow does
        version: Semantic version
        status: Current status
        steps: List of workflow steps
        entry_point: First step ID
        handlers: Map of step IDs to handler functions
        context: Workflow execution context
        results: Workflow execution results
        metadata: Additional metadata
        registered_at: When this was registered
    """
    id: str
    name: str
    description: str = ""
    version: str = "1.0.0"
    status: WorkflowStatus = WorkflowStatus.REGISTERED
    steps: List[WorkflowStep] = field(default_factory=list)
    entry_point: Optional[str] = None
    handlers: Dict[str, Callable] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    results: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    
    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow."""
        self.steps.append(step)
        if self.entry_point is None:
            self.entry_point = step.id
    
    def execute(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the workflow."""
        self.context = initial_input.copy()
        self.status = WorkflowStatus.ACTIVE
        self.started_at = datetime.utcnow()
        self.results = {}
        
        # Build step map
        step_map = {step.id: step for step in self.steps}
        
        # Execute from entry point
        current_id = self.entry_point
        while current_id:
            step = step_map.get(current_id)
            if not step:
                self.error = f"Step {current_id} not found"
                self.status = WorkflowStatus.FAILED
                break
            
            step.status = WorkflowStepStatus.RUNNING
            step.started_at = datetime.utcnow()
            
            try:
                # Get handler
                handler = self.handlers.get(step.action)
                if handler is None:
                    raise ValueError(f"No handler for action {step.action}")
                
                # Resolve inputs from context
                inputs = {}
                for key, value in step.inputs.items():
                    if isinstance(value, str) and value.startswith("$"):
                        inputs[key] = self.context.get(value[1:])
                    else:
                        inputs[key] = value
                
                # Execute handler
                result = handler(inputs)
                step.result = result
                step.status = WorkflowStepStatus.COMPLETED
                step.completed_at = datetime.utcnow()
                
                # Store outputs in context
                for output_name, var_name in step.outputs.items():
                    self.context[var_name] = result.get(output_name) if isinstance(result, dict) else result
                
                # Move to next step
                current_id = step.conditions.get("next_step")
                
            except Exception as e:
                step.error = str(e)
                step.status = WorkflowStepStatus.FAILED
                step.completed_at = datetime.utcnow()
                
                if step.retry_count > 0:
                    step.retry_count -= 1
                    current_id = step.id  # Retry same step
                else:
                    self.error = str(e)
                    self.status = WorkflowStatus.FAILED
                    break
        
        if self.status == WorkflowStatus.ACTIVE:
            self.status = WorkflowStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        
        return self.results
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "status": self.status.value,
            "steps": [
                {
                    "id": s.id,
                    "name": s.name,
                    "action": s.action,
                    "status": s.status.value,
                }
                for s in self.steps
            ],
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
        }


class WorkflowRegistry:
    """
    Thread-safe singleton registry for all AGOS workflows.
    
    Usage:
        registry = WorkflowRegistry.get_instance()
        registry.register(
            id="WORKFLOW-000001",
            name="Repository Analysis",
            steps=[step1, step2],
        )
        workflow = registry.get("WORKFLOW-000001")
        result = workflow.execute({"url": "..."})
    """
    
    _instance: Optional['WorkflowRegistry'] = None
    _lock = threading.Lock()
    
    def __init__(self):
        """Initialize registry."""
        self._workflows: Dict[str, Workflow] = {}
        self._lock = threading.RLock()
    
    @classmethod
    def get_instance(cls) -> 'WorkflowRegistry':
        """Get singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def register(
        self,
        id: str,
        name: str,
        description: str = "",
        version: str = "1.0.0",
        steps: Optional[List[WorkflowStep]] = None,
        handlers: Optional[Dict[str, Callable]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Register a workflow.
        
        Args:
            id: Unique identifier
            name: Human-readable name
            description: What this workflow does
            version: Semantic version
            steps: List of workflow steps
            handlers: Map of action names to handler functions
            metadata: Additional metadata
            
        Returns:
            The workflow ID
        """
        with self._lock:
            if id in self._workflows:
                return id  # Already registered
            
            workflow = Workflow(
                id=id,
                name=name,
                description=description,
                version=version,
                steps=steps or [],
                handlers=handlers or {},
                metadata=metadata or {},
            )
            
            self._workflows[id] = workflow
            return id
    
    def unregister(self, id: str) -> bool:
        """Unregister a workflow."""
        with self._lock:
            if id in self._workflows:
                del self._workflows[id]
                return True
            return False
    
    def get(self, id: str) -> Optional[Workflow]:
        """Get a registered workflow."""
        return self._workflows.get(id)
    
    def list_all(self) -> List[Workflow]:
        """List all registered workflows."""
        return list(self._workflows.values())
    
    def list_by_status(self, status: WorkflowStatus) -> List[Workflow]:
        """List workflows by status."""
        return [w for w in self._workflows.values() if w.status == status]
    
    def check_health(self) -> Dict[str, Any]:
        """Check health of all workflows."""
        return {
            "total": len(self._workflows),
            "active": len([w for w in self._workflows.values() if w.status == WorkflowStatus.ACTIVE]),
            "completed": len([w for w in self._workflows.values() if w.status == WorkflowStatus.COMPLETED]),
            "failed": len([w for w in self._workflows.values() if w.status == WorkflowStatus.FAILED]),
        }
    
    def reset(self) -> None:
        """Reset registry (for testing)."""
        with self._lock:
            self._workflows.clear()

_workflow_registry_instance = None
_workflow_registry_lock = threading.Lock()
def get_workflow_registry() -> WorkflowRegistry:
    global _workflow_registry_instance
    if _workflow_registry_instance is None:
        with _workflow_registry_lock:
            if _workflow_registry_instance is None:
                _workflow_registry_instance = WorkflowRegistry()
    return _workflow_registry_instance

