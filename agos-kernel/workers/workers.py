"""AGOS Workers."""
import uuid
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class WorkerStatus(Enum):
    """Worker status."""
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"


@dataclass
class Worker:
    """A worker."""
    id: str
    name: str
    status: WorkerStatus = WorkerStatus.IDLE
    current_task: Optional[str] = None
    completed_tasks: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkerPool:
    """
    Worker Pool.
    
    Manages a pool of workers for parallel execution.
    
    Usage:
        pool = WorkerPool(size=4)
        pool.start()
        pool.submit(my_task, args)
        pool.shutdown()
    """
    
    def __init__(self, size: int = 4):
        """Initialize worker pool."""
        self._size = size
        self._workers: Dict[str, Worker] = {}
        self._queue: List[tuple] = []
        self._running = False
        self._lock = threading.Lock()
    
    def create_workers(self) -> None:
        """Create workers."""
        for i in range(self._size):
            worker = Worker(
                id=f"worker-{uuid.uuid4().hex[:8]}",
                name=f"Worker-{i+1}",
            )
            self._workers[worker.id] = worker
    
    def start(self) -> None:
        """Start the worker pool."""
        if self._running:
            return
        
        self.create_workers()
        self._running = True
        
        for worker in self._workers.values():
            thread = threading.Thread(target=self._worker_loop, args=(worker,))
            thread.daemon = True
            thread.start()
    
    def submit(self, handler: Callable, *args, **kwargs) -> None:
        """Submit a task to the pool."""
        with self._lock:
            self._queue.append((handler, args, kwargs))
    
    def _worker_loop(self, worker: Worker) -> None:
        """Worker loop."""
        while self._running:
            task = None
            
            with self._lock:
                if self._queue:
                    task = self._queue.pop(0)
            
            if task:
                worker.status = WorkerStatus.BUSY
                handler, args, kwargs = task
                
                try:
                    handler(*args, **kwargs)
                    worker.completed_tasks += 1
                except:
                    pass
                
                worker.status = WorkerStatus.IDLE
            else:
                import time
                time.sleep(0.1)
    
    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the worker pool."""
        self._running = False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get worker pool statistics."""
        return {
            "pool_size": self._size,
            "active_workers": sum(1 for w in self._workers.values() if w.status == WorkerStatus.BUSY),
            "idle_workers": sum(1 for w in self._workers.values() if w.status == WorkerStatus.IDLE),
            "total_completed": sum(w.completed_tasks for w in self._workers.values()),
            "queue_size": len(self._queue),
        }


_worker_pool: Optional[WorkerPool] = None


def get_worker_pool(size: int = 4) -> WorkerPool:
    """Get the global worker pool."""
    global _worker_pool
    if _worker_pool is None:
        _worker_pool = WorkerPool(size=size)
    return _worker_pool
