"""
AGOS Workflow Pipeline
=====================

Workflow execution pipeline with steps, conditions, and error handling.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class PipelineStatus(Enum):
    """Pipeline status."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(Enum):
    """Step status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


@dataclass
class StepResult:
    """Result of a step execution."""
    step_id: str
    status: StepStatus
    output: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: float = 0.0
    retry_count: int = 0


@dataclass
class ExecutionContext:
    """Execution context shared between steps."""
    pipeline_id: str
    workflow_id: Optional[str] = None
    mission_id: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    artifacts: Dict[str, Any] = field(default_factory=dict)
    history: List[StepResult] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    
    def set_var(self, key: str, value: Any) -> None:
        """Set a variable."""
        self.variables[key] = value
    
    def get_var(self, key: str, default: Any = None) -> Any:
        """Get a variable."""
        return self.variables.get(key, default)
    
    def add_artifact(self, name: str, data: Any) -> None:
        """Add an artifact."""
        self.artifacts[name] = data
    
    def get_artifact(self, name: str) -> Optional[Any]:
        """Get an artifact."""
        return self.artifacts.get(name)


@dataclass 
class PipelineStep:
    """A pipeline step."""
    id: str
    name: str
    handler: Callable[[ExecutionContext], Any]
    condition: Optional[Callable[[ExecutionContext], bool]] = None
    retry_count: int = 0
    retry_delay: float = 1.0
    timeout: Optional[float] = None
    on_failure: Optional[str] = None  # Step ID to run on failure


@dataclass
class PipelineConfig:
    """Pipeline configuration."""
    name: str = "Pipeline"
    max_parallel: int = 1
    continue_on_error: bool = False
    save_state: bool = True
    enable_logging: bool = True


class Pipeline:
    """
    Workflow Execution Pipeline.
    
    Handles sequential and parallel step execution with:
    - Conditions
    - Error handling
    - Retry logic
    - State management
    - Artifact collection
    
    Usage:
        pipeline = Pipeline(config=PipelineConfig(name="MyPipeline"))
        
        pipeline.add_step(PipelineStep(
            id="step1",
            name="First Step",
            handler=lambda ctx: do_something(ctx),
        ))
        
        pipeline.add_step(PipelineStep(
            id="step2", 
            name="Second Step",
            handler=lambda ctx: do_something_else(ctx),
            condition=lambda ctx: ctx.get_var("step1_success", False),
        ))
        
        context = ExecutionContext(pipeline_id=pipeline.id)
        result = pipeline.run(context)
    """
    
    def __init__(
        self,
        config: Optional[PipelineConfig] = None,
        steps: Optional[List[PipelineStep]] = None,
    ):
        """Initialize pipeline."""
        self.id = f"pipeline-{uuid.uuid4().hex[:8]}"
        self.config = config or PipelineConfig()
        self.steps: List[PipelineStep] = steps or []
        self.status = PipelineStatus.IDLE
        
        # Execution tracking
        self._current_step: Optional[str] = None
        self._context: Optional[ExecutionContext] = None
        self._results: List[StepResult] = []
    
    def add_step(self, step: PipelineStep) -> 'Pipeline':
        """Add a step to the pipeline."""
        self.steps.append(step)
        return self
    
    def add_steps(self, steps: List[PipelineStep]) -> 'Pipeline':
        """Add multiple steps."""
        self.steps.extend(steps)
        return self
    
    def get_step(self, step_id: str) -> Optional[PipelineStep]:
        """Get a step by ID."""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None
    
    def run(self, context: Optional[ExecutionContext] = None) -> List[StepResult]:
        """
        Run the pipeline.
        
        Args:
            context: Execution context (created if not provided)
            
        Returns:
            List of step results
        """
        self.status = PipelineStatus.RUNNING
        self._results = []
        self._context = context or ExecutionContext(pipeline_id=self.id)
        
        for step in self.steps:
            self._current_step = step.id
            
            # Check condition
            if step.condition and not step.condition(self._context):
                result = StepResult(
                    step_id=step.id,
                    status=StepStatus.SKIPPED,
                )
                self._results.append(result)
                continue
            
            # Execute step
            result = self._execute_step(step)
            self._results.append(result)
            self._context.history.append(result)
            
            # Handle failure
            if result.status == StepStatus.FAILED:
                if step.on_failure:
                    self._run_on_failure(step.on_failure)
                
                if not self.config.continue_on_error:
                    self.status = PipelineStatus.FAILED
                    break
        
        # Determine final status
        if self.status == PipelineStatus.RUNNING:
            failed_count = sum(1 for r in self._results if r.status == StepStatus.FAILED)
            if failed_count > 0:
                self.status = PipelineStatus.FAILED
            else:
                self.status = PipelineStatus.COMPLETED
        
        return self._results
    
    def _execute_step(self, step: PipelineStep) -> StepResult:
        """Execute a single step with retry logic."""
        result = StepResult(
            step_id=step.id,
            status=StepStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        
        for attempt in range(step.retry_count + 1):
            try:
                output = step.handler(self._context)
                result.output = output
                result.status = StepStatus.COMPLETED
                result.completed_at = datetime.utcnow()
                result.duration_ms = (
                    result.completed_at - result.started_at
                ).total_seconds() * 1000
                result.retry_count = attempt
                return result
                
            except Exception as e:
                if attempt < step.retry_count:
                    result.status = StepStatus.RETRYING
                    import time
                    time.sleep(step.retry_delay)
                else:
                    result.status = StepStatus.FAILED
                    result.error = str(e)
                    result.completed_at = datetime.utcnow()
                    result.duration_ms = (
                        result.completed_at - result.started_at
                    ).total_seconds() * 1000
                    result.retry_count = attempt
        
        return result
    
    def _run_on_failure(self, step_id: str) -> None:
        """Run the on_failure handler."""
        step = self.get_step(step_id)
        if step:
            try:
                step.handler(self._context)
            except Exception:
                pass  # Ignore errors in failure handlers
    
    def pause(self) -> bool:
        """Pause the pipeline."""
        if self.status == PipelineStatus.RUNNING:
            self.status = PipelineStatus.PAUSED
            return True
        return False
    
    def resume(self) -> bool:
        """Resume the pipeline."""
        if self.status == PipelineStatus.PAUSED:
            self.status = PipelineStatus.RUNNING
            return True
        return False
    
    def cancel(self) -> bool:
        """Cancel the pipeline."""
        self.status = PipelineStatus.CANCELLED
        return True
    
    def get_results(self) -> List[StepResult]:
        """Get all step results."""
        return self._results
    
    def get_context(self) -> Optional[ExecutionContext]:
        """Get execution context."""
        return self._context
    
    def get_summary(self) -> Dict[str, Any]:
        """Get pipeline execution summary."""
        return {
            "id": self.id,
            "name": self.config.name,
            "status": self.status.value,
            "total_steps": len(self.steps),
            "completed": sum(1 for r in self._results if r.status == StepStatus.COMPLETED),
            "failed": sum(1 for r in self._results if r.status == StepStatus.FAILED),
            "skipped": sum(1 for r in self._results if r.status == StepStatus.SKIPPED),
            "current_step": self._current_step,
            "context": {
                "variables": self._context.variables if self._context else {},
                "artifacts": list(self._context.artifacts.keys()) if self._context else [],
            } if self._context else None,
        }


# Global pipeline instance
_pipeline: Optional[Pipeline] = None


def get_pipeline() -> Pipeline:
    """Get the global pipeline instance."""
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline()
    return _pipeline


def create_pipeline(name: str, steps: Optional[List[PipelineStep]] = None) -> Pipeline:
    """Create a new pipeline."""
    config = PipelineConfig(name=name)
    return Pipeline(config=config, steps=steps)
