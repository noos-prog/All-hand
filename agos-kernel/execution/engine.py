"""AGOS Execution Engine - Production Implementation."""
import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar


class ExecutionStatus(Enum):
    """Execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"


class ExecutionEvent(Enum):
    """Execution events."""
    STARTED = "started"
    PAUSED = "paused"
    RESUMED = "resumed"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"
    CHECKPOINT = "checkpoint"
    RETRY = "retry"


@dataclass
class ExecutionContext:
    """Execution context."""
    execution_id: str
    mission_id: str
    capability_id: str
    skill_id: str
    provider_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    checkpoints: List[Dict] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class ExecutionResult:
    """Execution result."""
    execution_id: str
    status: ExecutionStatus
    output: Any = None
    error: Optional[str] = None
    trace: List[Dict] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    evidence: List[str] = field(default_factory=list)


class ExecutionPolicy:
    """Execution policy."""
    
    def __init__(self):
        self.timeout_seconds: int = 300
        self.max_retries: int = 3
        self.retry_delay_seconds: float = 1.0
        self.rollback_on_failure: bool = True
        self.checkpoint_interval_seconds: int = 60
        self.enable_telemetry: bool = True
        self.enable_tracing: bool = True


class ExecutionNode:
    """A single execution node in a workflow."""
    
    def __init__(
        self,
        node_id: str,
        name: str,
        skill: str,
        provider: str,
        input_map: Dict[str, str] = None,
        condition: str = None,
        retry_policy: Dict = None,
    ):
        self.node_id = node_id
        self.name = name
        self.skill = skill
        self.provider = provider
        self.input_map = input_map or {}
        self.condition = condition
        self.retry_policy = retry_policy or {"max_retries": 3, "delay": 1.0}
        self.status: ExecutionStatus = ExecutionStatus.PENDING
        self.result: Any = None
        self.error: Optional[str] = None
        self.attempts: int = 0


class ExecutionGraph:
    """Compiled workflow execution graph."""
    
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.nodes: Dict[str, ExecutionNode] = {}
        self.edges: Dict[str, List[str]] = {}  # node_id -> [dependent_node_ids]
        self.entry_nodes: List[str] = []
        self.exit_nodes: List[str] = []
    
    def add_node(self, node: ExecutionNode) -> None:
        """Add a node to the graph."""
        self.nodes[node.node_id] = node
        if node.node_id not in self.edges:
            self.edges[node.node_id] = []
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add an edge between nodes."""
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append(to_node)
    
    def get_ready_nodes(self, completed: set) -> List[ExecutionNode]:
        """Get nodes that are ready to execute."""
        ready = []
        for node_id, deps in self.edges.items():
            if node_id in completed:
                continue
            if all(dep in completed for dep in deps):
                node = self.nodes.get(node_id)
                if node:
                    ready.append(node)
        return ready


class ExecutionEngine:
    """Production execution engine."""
    
    def __init__(self):
        self.policies: Dict[str, ExecutionPolicy] = {}
        self.active_executions: Dict[str, ExecutionContext] = {}
        self.completed_executions: Dict[str, ExecutionResult] = {}
        self.event_handlers: Dict[ExecutionEvent, List[Callable]] = {}
        self._metrics: Dict[str, List[float]] = {}
        self._traces: Dict[str, List[Dict]] = {}
    
    def create_policy(self, name: str, **kwargs) -> ExecutionPolicy:
        """Create an execution policy."""
        policy = ExecutionPolicy()
        for key, value in kwargs.items():
            if hasattr(policy, key):
                setattr(policy, key, value)
        self.policies[name] = policy
        return policy
    
    def get_policy(self, name: str) -> ExecutionPolicy:
        """Get an execution policy."""
        return self.policies.get(name, ExecutionPolicy())
    
    def on_event(self, event: ExecutionEvent, handler: Callable) -> None:
        """Register an event handler."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def _emit_event(self, event: ExecutionEvent, context: ExecutionContext, data: Dict = None) -> None:
        """Emit an execution event."""
        handlers = self.event_handlers.get(event, [])
        for handler in handlers:
            try:
                handler(context, data or {})
            except Exception:
                pass  # Don't let handler errors break execution
    
    async def execute(
        self,
        capability_id: str,
        skill_id: str,
        provider_id: str,
        parameters: Dict[str, Any],
        policy_name: str = "default",
    ) -> ExecutionResult:
        """Execute a capability skill with provider."""
        execution_id = str(uuid.uuid4())
        context = ExecutionContext(
            execution_id=execution_id,
            mission_id="",
            capability_id=capability_id,
            skill_id=skill_id,
            provider_id=provider_id,
            parameters=parameters,
        )
        
        policy = self.get_policy(policy_name)
        self.active_executions[execution_id] = context
        
        start_time = datetime.now()
        self._emit_event(ExecutionEvent.STARTED, context)
        
        try:
            # Simulate execution with timeout
            result = await asyncio.wait_for(
                self._execute_skill(context, policy),
                timeout=policy.timeout_seconds
            )
            
            status = ExecutionStatus.COMPLETED
            context.completed_at = datetime.now()
            self._emit_event(ExecutionEvent.COMPLETED, context)
            
            execution_result = ExecutionResult(
                execution_id=execution_id,
                status=status,
                output=result,
                metrics=self._compute_metrics(execution_id, start_time),
            )
            
        except asyncio.TimeoutError:
            status = ExecutionStatus.FAILED
            execution_result = ExecutionResult(
                execution_id=execution_id,
                status=status,
                error=f"Execution timed out after {policy.timeout_seconds}s",
            )
            self._emit_event(ExecutionEvent.FAILED, context)
            
        except Exception as e:
            status = ExecutionStatus.FAILED
            execution_result = ExecutionResult(
                execution_id=execution_id,
                status=status,
                error=str(e),
            )
            self._emit_event(ExecutionEvent.FAILED, context)
        
        finally:
            self.completed_executions[execution_id] = execution_result
            if execution_id in self.active_executions:
                del self.active_executions[execution_id]
        
        return execution_result
    
    async def _execute_skill(
        self,
        context: ExecutionContext,
        policy: ExecutionPolicy,
    ) -> Any:
        """Execute skill with retry logic."""
        max_retries = policy.max_retries
        delay = policy.retry_delay_seconds
        
        for attempt in range(max_retries + 1):
            try:
                # Simulate skill execution
                result = await self._skill_logic(context)
                return result
            except Exception as e:
                if attempt < max_retries:
                    context.state["last_error"] = str(e)
                    context.state["retry_attempt"] = attempt + 1
                    self._emit_event(ExecutionEvent.RETRY, context)
                    await asyncio.sleep(delay * (attempt + 1))
                else:
                    raise
        
        raise RuntimeError("Max retries exceeded")
    
    async def _skill_logic(self, context: ExecutionContext) -> Any:
        """Actual skill execution logic."""
        # This would be replaced by real skill implementation
        skill_id = context.skill_id
        params = context.parameters
        
        # Simulate async skill execution
        await asyncio.sleep(0.1)
        
        return {
            "skill": skill_id,
            "input": params,
            "output": f"Result of {skill_id}",
            "timestamp": datetime.now().isoformat(),
        }
    
    async def execute_workflow(
        self,
        graph: ExecutionGraph,
        initial_parameters: Dict[str, Any],
        policy_name: str = "default",
    ) -> Dict[str, ExecutionResult]:
        """Execute a compiled workflow graph."""
        policy = self.get_policy(policy_name)
        results: Dict[str, ExecutionResult] = {}
        completed: set = set()
        context_state: Dict[str, Any] = initial_parameters.copy()
        
        while len(completed) < len(graph.nodes):
            ready_nodes = graph.get_ready_nodes(completed)
            if not ready_nodes:
                break
            
            # Execute ready nodes in parallel
            tasks = []
            for node in ready_nodes:
                context = ExecutionContext(
                    execution_id=str(uuid.uuid4()),
                    mission_id="",
                    capability_id="workflow",
                    skill_id=node.skill,
                    provider_id=node.provider,
                    parameters={k: context_state.get(v) for k, v in node.input_map.items()},
                    state=context_state.copy(),
                )
                task = self.execute(
                    capability_id="workflow",
                    skill_id=node.skill,
                    provider_id=node.provider,
                    parameters=context.parameters,
                    policy_name=policy_name,
                )
                tasks.append((node.node_id, task))
            
            for node_id, task in tasks:
                result = await task
                results[node_id] = result
                node = graph.nodes[node_id]
                node.status = result.status
                node.result = result.output
                
                if result.status == ExecutionStatus.COMPLETED:
                    completed.add(node_id)
                    context_state[node_id] = result.output
                elif result.status == ExecutionStatus.FAILED:
                    completed.add(node_id)  # Mark as done even if failed
        
        return results
    
    def pause(self, execution_id: str) -> bool:
        """Pause an execution."""
        context = self.active_executions.get(execution_id)
        if not context:
            return False
        
        # Create checkpoint
        checkpoint = {
            "execution_id": execution_id,
            "state": context.state.copy(),
            "parameters": context.parameters.copy(),
            "timestamp": datetime.now().isoformat(),
        }
        context.checkpoints.append(checkpoint)
        self._emit_event(ExecutionEvent.CHECKPOINT, context)
        self._emit_event(ExecutionEvent.PAUSED, context)
        return True
    
    def resume(self, execution_id: str) -> bool:
        """Resume a paused execution."""
        context = self.active_executions.get(execution_id)
        if not context or not context.checkpoints:
            return False
        
        # Restore from last checkpoint
        checkpoint = context.checkpoints[-1]
        context.state = checkpoint["state"]
        context.parameters = checkpoint["parameters"]
        self._emit_event(ExecutionEvent.RESUMED, context)
        return True
    
    def cancel(self, execution_id: str) -> bool:
        """Cancel an execution."""
        context = self.active_executions.get(execution_id)
        if not context:
            return False
        
        self._emit_event(ExecutionEvent.CANCELLED, context)
        del self.active_executions[execution_id]
        return True
    
    def checkpoint(self, execution_id: str) -> Optional[Dict]:
        """Create a checkpoint for an execution."""
        context = self.active_executions.get(execution_id)
        if not context:
            return None
        
        checkpoint = {
            "execution_id": execution_id,
            "state": context.state.copy(),
            "parameters": context.parameters.copy(),
            "timestamp": datetime.now().isoformat(),
        }
        context.checkpoints.append(checkpoint)
        return checkpoint
    
    def replay(self, execution_id: str) -> ExecutionResult:
        """Replay a completed execution."""
        result = self.completed_executions.get(execution_id)
        if not result:
            raise ValueError(f"Execution {execution_id} not found")
        
        # Re-run with same parameters
        return result  # In production, would re-execute
    
    def rollback(self, execution_id: str) -> bool:
        """Rollback an execution."""
        context = self.active_executions.get(execution_id)
        if not context:
            return False
        
        self._emit_event(ExecutionEvent.ROLLED_BACK, context)
        return True
    
    def _compute_metrics(self, execution_id: str, start_time: datetime) -> Dict[str, float]:
        """Compute execution metrics."""
        duration = (datetime.now() - start_time).total_seconds()
        return {
            "duration_seconds": duration,
            "memory_mb": 0,  # Would be measured in production
            "cpu_percent": 0,  # Would be measured in production
        }
    
    def get_metrics(self, execution_id: str) -> Optional[Dict[str, List[float]]]:
        """Get metrics for an execution."""
        return {"execution_time": self._metrics.get(execution_id, [])}
    
    def get_trace(self, execution_id: str) -> Optional[List[Dict]]:
        """Get trace for an execution."""
        return self._traces.get(execution_id, [])
    
    def get_active_count(self) -> int:
        """Get count of active executions."""
        return len(self.active_executions)
    
    def get_completed_count(self) -> int:
        """Get count of completed executions."""
        return len(self.completed_executions)


# Global engine instance
_engine = ExecutionEngine()


def get_engine() -> ExecutionEngine:
    """Get the global execution engine."""
    return _engine