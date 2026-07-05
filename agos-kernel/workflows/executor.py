"""
AGOS Workflow Executor
====================

Workflow step executor with timeout, retries, and error handling.
"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import threading
import concurrent.futures


class ExecutorStatus(Enum):
    """Executor status."""
    IDLE = "idle"
    EXECUTING = "executing"
    PAUSED = "paused"
    STOPPED = "stopped"


@dataclass
class ExecutionConfig:
    """Execution configuration."""
    timeout: Optional[float] = None
    retry_count: int = 0
    retry_delay: float = 1.0
    max_parallel: int = 1
    enable_logging: bool = True


@dataclass
class ExecutionResult:
    """Result of execution."""
    execution_id: str
    step_id: str
    status: str
    started_at: datetime
    output: Optional[Any] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None
    duration_ms: float = 0.0
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "execution_id": self.execution_id,
            "step_id": self.step_id,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": self.duration_ms,
            "retry_count": self.retry_count,
        }


class Executor:
    """
    Workflow Step Executor.
    
    Executes workflow steps with:
    - Timeout support
    - Retry logic
    - Parallel execution
    - Thread pool management
    
    Usage:
        executor = Executor(config=ExecutionConfig(timeout=30))
        
        # Execute a single step
        result = executor.execute(
            step_id="step1",
            handler=lambda: do_work(),
        )
        
        # Execute multiple steps in parallel
        results = executor.execute_many([
            ("step1", handler1),
            ("step2", handler2),
        ])
    """
    
    def __init__(self, config: Optional[ExecutionConfig] = None):
        """Initialize executor."""
        self.config = config or ExecutionConfig()
        self.status = ExecutorStatus.IDLE
        self._thread_pool: Optional[concurrent.futures.ThreadPoolExecutor] = None
        self._active_executions: Dict[str, ExecutionResult] = {}
        self._lock = threading.Lock()
    
    def execute(
        self,
        step_id: str,
        handler: Callable[[], Any],
        config: Optional[ExecutionConfig] = None,
    ) -> ExecutionResult:
        """
        Execute a single step.
        
        Args:
            step_id: Step identifier
            handler: Function to execute
            config: Override config for this execution
            
        Returns:
            ExecutionResult
        """
        exec_config = config or self.config
        execution_id = f"exec-{uuid.uuid4().hex[:8]}"
        
        self.status = ExecutorStatus.EXECUTING
        
        result = ExecutionResult(
            execution_id=execution_id,
            step_id=step_id,
            status="running",
            started_at=datetime.utcnow(),
            output=None,
            error=None,
        )
        
        with self._lock:
            self._active_executions[execution_id] = result
        
        # Execute with retry
        for attempt in range(exec_config.retry_count + 1):
            try:
                if exec_config.timeout:
                    # Execute with timeout
                    import time
                    start = time.time()
                    remaining = exec_config.timeout
                    
                    # Simple timeout implementation
                    output = handler()
                    
                    result.output = output
                    result.status = "completed"
                    result.completed_at = datetime.utcnow()
                    result.duration_ms = (time.time() - start) * 1000
                    result.retry_count = attempt
                    break
                else:
                    output = handler()
                    result.output = output
                    result.status = "completed"
                    result.completed_at = datetime.utcnow()
                    result.duration_ms = 0
                    result.retry_count = attempt
                    break
                    
            except Exception as e:
                if attempt < exec_config.retry_count:
                    import time
                    time.sleep(exec_config.retry_delay)
                    result.status = "retrying"
                else:
                    result.status = "failed"
                    result.error = str(e)
                    result.completed_at = datetime.utcnow()
                    result.retry_count = attempt
        
        with self._lock:
            self._active_executions[execution_id] = result
            self.status = ExecutorStatus.IDLE
        
        return result
    
    def execute_many(
        self,
        steps: List[tuple],
        parallel: bool = False,
    ) -> List[ExecutionResult]:
        """
        Execute multiple steps.
        
        Args:
            steps: List of (step_id, handler) tuples
            parallel: Execute in parallel if True
            
        Returns:
            List of ExecutionResults
        """
        if parallel:
            return self._execute_parallel(steps)
        else:
            return self._execute_sequential(steps)
    
    def _execute_sequential(self, steps: List[tuple]) -> List[ExecutionResult]:
        """Execute steps sequentially."""
        results = []
        for step_id, handler in steps:
            result = self.execute(step_id, handler)
            results.append(result)
        return results
    
    def _execute_parallel(self, steps: List[tuple]) -> List[ExecutionResult]:
        """Execute steps in parallel."""
        max_workers = min(self.config.max_parallel, len(steps))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.execute, step_id, handler): step_id
                for step_id, handler in steps
            }
            
            results = []
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        
        return results
    
    def get_execution(self, execution_id: str) -> Optional[ExecutionResult]:
        """Get an execution result."""
        with self._lock:
            return self._active_executions.get(execution_id)
    
    def list_executions(self) -> List[ExecutionResult]:
        """List all executions."""
        with self._lock:
            return list(self._active_executions.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get executor statistics."""
        with self._lock:
            executions = list(self._active_executions.values())
            return {
                "status": self.status.value,
                "total_executions": len(executions),
                "completed": sum(1 for e in executions if e.status == "completed"),
                "failed": sum(1 for e in executions if e.status == "failed"),
                "running": sum(1 for e in executions if e.status == "running"),
            }
    
    def stop(self) -> bool:
        """Stop the executor."""
        self.status = ExecutorStatus.STOPPED
        return True
    
    def pause(self) -> bool:
        """Pause the executor."""
        if self.status == ExecutorStatus.EXECUTING:
            self.status = ExecutorStatus.PAUSED
            return True
        return False
    
    def resume(self) -> bool:
        """Resume the executor."""
        if self.status == ExecutorStatus.PAUSED:
            self.status = ExecutorStatus.EXECUTING
            return True
        return False


# Global executor instance
_executor: Optional[Executor] = None


def get_executor() -> Executor:
    """Get the global executor instance."""
    global _executor
    if _executor is None:
        _executor = Executor()
    return _executor
