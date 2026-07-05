"""
AGOS Long-Running Operations Manager
==================================

Manages long-running operations, background tasks, and async workflows.
"""

import asyncio
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class TaskPriority(Enum):
    """Task priority."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class LongRunningTask:
    """A long-running task."""
    id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.NORMAL
    handler: Callable = field(default=None)
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    
    # Progress tracking
    progress: float = 0.0
    progress_message: str = ""
    
    # Timing
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration: Optional[int] = None  # seconds
    
    # Result
    result: Any = None
    error: Optional[str] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "priority": self.priority.name,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": str(self.result)[:100] if self.result else None,
            "error": self.error,
        }


class LongRunningManager:
    """
    Long-Running Operations Manager.
    
    Manages long-running operations with:
    - Progress tracking
    - Cancellation support
    - Timeout handling
    - Retry logic
    - Event notifications
    
    Usage:
        manager = LongRunningManager()
        
        task = manager.create_task(
            name="data_processing",
            handler=process_data,
            args=(data,),
        )
        
        manager.start_task(task.id)
        
        # Monitor progress
        while task.status == TaskStatus.RUNNING:
            print(f"Progress: {task.progress}%")
            time.sleep(1)
    """
    
    def __init__(self):
        """Initialize manager."""
        self._tasks: Dict[str, LongRunningTask] = {}
        self._task_threads: Dict[str, threading.Thread] = {}
        self._stop_events: Dict[str, threading.Event] = {}
        self._lock = threading.Lock()
    
    def create_task(
        self,
        name: str,
        handler: Callable,
        args: tuple = None,
        kwargs: Dict[str, Any] = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout: Optional[int] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> LongRunningTask:
        """
        Create a long-running task.
        
        Args:
            name: Task name
            handler: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            priority: Task priority
            timeout: Timeout in seconds
            tags: Task tags
            metadata: Additional metadata
            
        Returns:
            LongRunningTask
        """
        task = LongRunningTask(
            id=f"task-{uuid.uuid4().hex[:8]}",
            name=name,
            handler=handler,
            args=args or (),
            kwargs=kwargs or {},
            priority=priority,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        if timeout:
            task.metadata["timeout"] = timeout
        
        with self._lock:
            self._tasks[task.id] = task
        
        return task
    
    def start_task(self, task_id: str) -> bool:
        """Start a task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task.status != TaskStatus.PENDING:
                return False
        
        # Create stop event
        stop_event = threading.Event()
        self._stop_events[task_id] = stop_event
        
        # Create and start thread
        thread = threading.Thread(
            target=self._run_task,
            args=(task_id, stop_event),
            daemon=True,
            name=f"LR-Task-{task_id}",
        )
        
        with self._lock:
            self._task_threads[task_id] = thread
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
        
        thread.start()
        return True
    
    def _run_task(self, task_id: str, stop_event: threading.Event) -> None:
        """Run a task in a thread."""
        with self._lock:
            task = self._tasks.get(task_id)
        
        if not task:
            return
        
        try:
            # Check for timeout
            timeout = task.metadata.get("timeout")
            
            if asyncio.iscoroutinefunction(task.handler):
                # Run async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(
                        asyncio.wait_for(
                            task.handler(*task.args, **task.kwargs),
                            timeout=timeout,
                        )
                    )
                finally:
                    loop.close()
            else:
                # Run sync function with progress callback
                def progress_callback(progress: float, message: str = ""):
                    with self._lock:
                        task.progress = progress
                        task.progress_message = message
                
                result = task.handler(
                    *task.args,
                    progress_callback=progress_callback,
                    stop_event=stop_event,
                    **task.kwargs,
                )
            
            with self._lock:
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.progress = 100.0
                task.completed_at = datetime.now()
        
        except asyncio.TimeoutError:
            with self._lock:
                task.status = TaskStatus.TIMEOUT
                task.error = f"Task timed out after {timeout} seconds"
                task.completed_at = datetime.now()
        
        except Exception as e:
            with self._lock:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.completed_at = datetime.now()
        
        finally:
            with self._lock:
                if task_id in self._task_threads:
                    del self._task_threads[task_id]
                if task_id in self._stop_events:
                    del self._stop_events[task_id]
    
    def pause_task(self, task_id: str) -> bool:
        """Pause a running task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task.status != TaskStatus.RUNNING:
                return False
            
            task.status = TaskStatus.PAUSED
            return True
    
    def resume_task(self, task_id: str) -> bool:
        """Resume a paused task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task.status != TaskStatus.PAUSED:
                return False
            
            task.status = TaskStatus.RUNNING
            return True
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return False
            
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                return False
            
            # Signal stop
            if task_id in self._stop_events:
                self._stop_events[task_id].set()
            
            task.status = TaskStatus.CANCELLED
            task.completed_at = datetime.now()
            return True
    
    def get_task(self, task_id: str) -> Optional[LongRunningTask]:
        """Get a task by ID."""
        with self._lock:
            return self._tasks.get(task_id)
    
    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        tags: Optional[List[str]] = None,
    ) -> List[LongRunningTask]:
        """List tasks."""
        with self._lock:
            tasks = list(self._tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        if tags:
            tasks = [t for t in tasks if any(tag in t.tags for tag in tags)]
        
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    
    def wait_for(self, task_id: str, timeout: Optional[float] = None) -> Any:
        """Wait for a task to complete."""
        start = time.time()
        
        while True:
            task = self.get_task(task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED, TaskStatus.TIMEOUT]:
                if task.status == TaskStatus.FAILED:
                    raise RuntimeError(task.error)
                return task.result
            
            if timeout and (time.time() - start) >= timeout:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout} seconds")
            
            time.sleep(0.1)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        with self._lock:
            tasks = list(self._tasks.values())
        
        return {
            "total_tasks": len(tasks),
            "pending": sum(1 for t in tasks if t.status == TaskStatus.PENDING),
            "running": sum(1 for t in tasks if t.status == TaskStatus.RUNNING),
            "paused": sum(1 for t in tasks if t.status == TaskStatus.PAUSED),
            "completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in tasks if t.status == TaskStatus.FAILED),
            "cancelled": sum(1 for t in tasks if t.status == TaskStatus.CANCELLED),
        }


# Global manager instance
_manager: Optional[LongRunningManager] = None


def get_manager() -> LongRunningManager:
    """Get the global long-running manager."""
    global _manager
    if _manager is None:
        _manager = LongRunningManager()
    return _manager
