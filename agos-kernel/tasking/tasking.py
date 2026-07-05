"""AGOS Tasking."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """A task."""
    id: str
    name: str
    handler: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.NORMAL
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TaskManager:
    """
    Task Manager.
    
    Manages tasks for execution.
    
    Usage:
        manager = TaskManager()
        task = manager.create_task("my_task", my_handler)
        manager.execute(task.id)
    """
    
    def __init__(self):
        """Initialize task manager."""
        self._tasks: Dict[str, Task] = {}
        self._queue: List[str] = []
    
    def create_task(
        self,
        name: str,
        handler: Callable,
        args: tuple = None,
        kwargs: Dict[str, Any] = None,
        priority: TaskPriority = TaskPriority.NORMAL,
    ) -> Task:
        """Create a task."""
        task = Task(
            id=f"task-{uuid.uuid4().hex[:8]}",
            name=name,
            handler=handler,
            args=args or (),
            kwargs=kwargs or {},
            priority=priority,
        )
        self._tasks[task.id] = task
        self._queue.append(task.id)
        self._sort_queue()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)
    
    def execute(self, task_id: str) -> bool:
        """Execute a task."""
        task = self._tasks.get(task_id)
        if not task or task.status != TaskStatus.PENDING:
            return False
        
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        
        try:
            task.result = task.handler(*task.args, **task.kwargs)
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            return True
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            return False
    
    def cancel(self, task_id: str) -> bool:
        """Cancel a task."""
        task = self._tasks.get(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            return True
        return False
    
    def get_next(self) -> Optional[Task]:
        """Get the next task from queue."""
        if not self._queue:
            return None
        
        task_id = self._queue.pop(0)
        return self._tasks.get(task_id)
    
    def _sort_queue(self) -> None:
        """Sort the queue by priority."""
        self._queue.sort(
            key=lambda tid: self._tasks[tid].priority.value if tid in self._tasks else 0,
            reverse=True,
        )
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """List tasks."""
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks


_task_manager: Optional[TaskManager] = None


def get_task_manager() -> TaskManager:
    """Get the global task manager."""
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManager()
    return _task_manager
