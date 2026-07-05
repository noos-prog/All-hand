"""
AGOS Task Queue Implementation
==============================

Asynchronous task queue with priority support.
"""

import heapq
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import time


class QueuePriority(Enum):
    """Task priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class QueueStatus(Enum):
    """Queue status."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


@dataclass
class QueueConfig:
    """Queue configuration."""
    max_size: int = 10000
    max_workers: int = 4
    poll_interval: float = 0.1
    enable_priority: bool = True
    allow_retry: bool = True
    max_retries: int = 3


@dataclass
class QueueTask:
    """A queue task."""
    id: str
    name: str
    handler: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    priority: QueuePriority = QueuePriority.NORMAL
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def sort_key(self) -> tuple:
        """Sort key for priority queue."""
        return (self.priority.value, self.created_at.timestamp())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority.name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": str(self.result)[:100] if self.result else None,
            "error": self.error,
            "retry_count": self.retry_count,
        }


class TaskQueue:
    """
    Asynchronous Task Queue.
    
    Features:
    - Priority-based execution
    - Retry support
    - Task tracking
    - Worker threads
    
    Usage:
        queue = TaskQueue(config=QueueConfig(max_workers=4))
        queue.start()
        
        task = queue.enqueue(
            name="my_task",
            handler=my_function,
            args=(arg1, arg2),
            priority=QueuePriority.HIGH,
        )
        
        # Wait for result
        result = queue.wait_for(task.id)
        
        queue.stop()
    """
    
    def __init__(self, config: Optional[QueueConfig] = None):
        """Initialize task queue."""
        self.config = config or QueueConfig()
        self.status = QueueStatus.IDLE
        
        self._tasks: Dict[str, QueueTask] = {}
        self._pending: List[QueueTask] = []
        self._running: Dict[str, QueueTask] = {}
        self._completed: Dict[str, QueueTask] = {}
        
        self._lock = threading.Lock()
        self._workers: List[threading.Thread] = []
        self._stop_event = threading.Event()
    
    def start(self) -> bool:
        """Start the queue workers."""
        if self.status != QueueStatus.IDLE:
            return False
        
        self.status = QueueStatus.RUNNING
        self._stop_event.clear()
        
        for i in range(self.config.max_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                args=(i,),
                daemon=True,
                name=f"QueueWorker-{i}",
            )
            worker.start()
            self._workers.append(worker)
        
        return True
    
    def stop(self, timeout: float = 5.0) -> bool:
        """Stop the queue."""
        self.status = QueueStatus.STOPPED
        self._stop_event.set()
        
        for worker in self._workers:
            worker.join(timeout=timeout / len(self._workers))
        
        self._workers.clear()
        return True
    
    def pause(self) -> bool:
        """Pause the queue."""
        if self.status == QueueStatus.RUNNING:
            self.status = QueueStatus.PAUSED
            return True
        return False
    
    def resume(self) -> bool:
        """Resume the queue."""
        if self.status == QueueStatus.PAUSED:
            self.status = QueueStatus.RUNNING
            return True
        return False
    
    def enqueue(
        self,
        name: str,
        handler: Callable,
        args: tuple = None,
        kwargs: Dict[str, Any] = None,
        priority: QueuePriority = QueuePriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> QueueTask:
        """
        Enqueue a task.
        
        Args:
            name: Task name
            handler: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            priority: Task priority
            metadata: Additional metadata
            
        Returns:
            QueueTask
        """
        task = QueueTask(
            id=f"task-{uuid.uuid4().hex[:8]}",
            name=name,
            handler=handler,
            args=args or (),
            kwargs=kwargs or {},
            priority=priority,
            metadata=metadata or {},
        )
        
        with self._lock:
            self._tasks[task.id] = task
            heapq.heappush(self._pending, task)
        
        return task
    
    def enqueue_many(
        self,
        tasks: List[Dict[str, Any]],
    ) -> List[QueueTask]:
        """Enqueue multiple tasks."""
        result = []
        for task_def in tasks:
            task = self.enqueue(
                name=task_def.get("name", "task"),
                handler=task_def.get("handler"),
                args=task_def.get("args"),
                kwargs=task_def.get("kwargs"),
                priority=task_def.get("priority", QueuePriority.NORMAL),
            )
            result.append(task)
        return result
    
    def get_task(self, task_id: str) -> Optional[QueueTask]:
        """Get a task by ID."""
        with self._lock:
            return self._tasks.get(task_id)
    
    def cancel(self, task_id: str) -> bool:
        """Cancel a task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return False
            
            if task.status == "pending":
                task.status = "cancelled"
                # Remove from pending queue
                self._pending = [t for t in self._pending if t.id != task_id]
                heapq.heapify(self._pending)
                return True
            
            return False
    
    def retry(self, task_id: str) -> bool:
        """Retry a failed task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task.status != "failed":
                return False
            
            if task.retry_count < self.config.max_retries:
                task.status = "pending"
                task.error = None
                task.retry_count += 1
                heapq.heappush(self._pending, task)
                return True
            
            return False
    
    def wait_for(self, task_id: str, timeout: Optional[float] = None) -> Any:
        """Wait for a task to complete."""
        start = time.time()
        
        while True:
            task = self.get_task(task_id)
            if not task:
                return None
            
            if task.status == "completed":
                return task.result
            
            if task.status == "failed":
                raise RuntimeError(task.error)
            
            if timeout and (time.time() - start) >= timeout:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")
            
            time.sleep(0.05)
    
    def _worker_loop(self, worker_id: int) -> None:
        """Worker thread loop."""
        while not self._stop_event.is_set():
            if self.status == QueueStatus.PAUSED:
                time.sleep(0.1)
                continue
            
            task = self._get_next_task()
            if task:
                self._execute_task(task)
            else:
                time.sleep(self.config.poll_interval)
    
    def _get_next_task(self) -> Optional[QueueTask]:
        """Get next task from queue."""
        with self._lock:
            if self._pending:
                task = heapq.heappop(self._pending)
                task.status = "running"
                task.started_at = datetime.now()
                self._running[task.id] = task
                return task
            return None
    
    def _execute_task(self, task: QueueTask) -> None:
        """Execute a task."""
        try:
            result = task.handler(*task.args, **task.kwargs)
            task.result = result
            task.status = "completed"
            task.completed_at = datetime.now()
        except Exception as e:
            task.error = str(e)
            task.status = "failed"
            task.completed_at = datetime.now()
            
            if self.config.allow_retry and task.retry_count < self.config.max_retries:
                # Re-enqueue for retry
                task.status = "pending"
                task.retry_count += 1
                with self._lock:
                    heapq.heappush(self._pending, task)
        finally:
            with self._lock:
                if task.id in self._running:
                    del self._running[task.id]
                self._completed[task.id] = task
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        with self._lock:
            return {
                "status": self.status.value,
                "total_tasks": len(self._tasks),
                "pending": len(self._pending),
                "running": len(self._running),
                "completed": sum(1 for t in self._completed.values() if t.status == "completed"),
                "failed": sum(1 for t in self._completed.values() if t.status == "failed"),
                "workers": len(self._workers),
            }
    
    def list_tasks(
        self,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """List tasks."""
        tasks = list(self._tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return [t.to_dict() for t in tasks[:limit]]


# Global queue instance
_queue: Optional[TaskQueue] = None


def get_queue() -> TaskQueue:
    """Get the global task queue instance."""
    global _queue
    if _queue is None:
        _queue = TaskQueue()
        _queue.start()
    return _queue
