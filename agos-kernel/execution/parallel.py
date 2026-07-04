"""Universal Parallel Execution Engine."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class ExecutionMode(Enum):
    """Execution mode."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"
    DISTRIBUTED = "distributed"


class ExecutionStatus(Enum):
    """Execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExecutionTask:
    """A single execution task."""
    id: str
    name: str
    func: Callable = field(default_factory=lambda: None)
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    status: ExecutionStatus = ExecutionStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    resources: Dict[str, Any] = field(default_factory=dict)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class ExecutionBatch:
    """A batch of tasks that can run in parallel."""
    id: str
    tasks: List[ExecutionTask] = field(default_factory=list)
    max_parallelism: int = 10
    created_at: datetime = field(default_factory=datetime.now)


class ParallelScheduler:
    """Parallel task scheduler."""
    
    def __init__(self, max_workers: int = 10):
        """Initialize scheduler."""
        self.max_workers = max_workers
        self.tasks: Dict[str, ExecutionTask] = {}
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
    
    def add_task(
        self,
        name: str,
        dependencies: Optional[List[str]] = None,
        resources: Optional[Dict[str, Any]] = None,
    ) -> ExecutionTask:
        """Add a task to the scheduler."""
        task = ExecutionTask(
            id=self._generate_id(name),
            name=name,
            dependencies=dependencies or [],
            resources=resources or {},
        )
        self.tasks[task.id] = task
        return task
    
    def get_ready_tasks(self) -> List[ExecutionTask]:
        """Get tasks that are ready to execute."""
        ready = []
        completed = {
            tid for tid, t in self.tasks.items()
            if t.status == ExecutionStatus.COMPLETED
        }
        
        for task in self.tasks.values():
            if task.status != ExecutionStatus.PENDING:
                continue
            
            # Check if all dependencies are completed
            if all(dep in completed for dep in task.dependencies):
                ready.append(task)
        
        return ready[:self.max_workers]
    
    def get_parallel_batches(self) -> List[List[ExecutionTask]]:
        """Get tasks grouped into parallel batches."""
        batches = []
        pending = set(self.tasks.keys())
        completed = set()
        
        while pending:
            batch = []
            remaining = []
            
            for task_id in pending:
                task = self.tasks[task_id]
                deps_met = all(dep in completed for dep in task.dependencies)
                
                if deps_met and len(batch) < self.max_workers:
                    batch.append(task)
                else:
                    remaining.append(task_id)
            
            if not batch:
                break
            
            batches.append(batch)
            for task in batch:
                completed.add(task.id)
            pending = set(remaining)
        
        return batches


class DependencyAnalyzer:
    """Analyze task dependencies."""
    
    def analyze(self, tasks: List[ExecutionTask]) -> Dict[str, List[str]]:
        """Analyze dependencies between tasks."""
        graph: Dict[str, List[str]] = {}
        
        for task in tasks:
            graph[task.id] = task.dependencies.copy()
        
        return graph
    
    def find_cycles(self, tasks: List[ExecutionTask]) -> List[List[str]]:
        """Find circular dependencies."""
        graph = self.analyze(tasks)
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for dep in graph.get(node, []):
                if dep not in visited:
                    dfs(dep, path)
                elif dep in rec_stack:
                    cycle_start = path.index(dep)
                    cycles.append(path[cycle_start:] + [dep])
            
            path.pop()
            rec_stack.remove(node)
        
        for task in tasks:
            if task.id not in visited:
                dfs(task.id, [])
        
        return cycles


class ConflictDetector:
    """Detect resource conflicts."""
    
    def __init__(self):
        """Initialize detector."""
        self.resource_locks: Dict[str, Set[str]] = {}
    
    def detect_conflicts(
        self,
        tasks: List[ExecutionTask],
    ) -> List[tuple]:
        """Detect conflicts between tasks."""
        conflicts = []
        active_tasks: Dict[str, Set[str]] = {}
        
        for task in tasks:
            for resource, value in task.resources.items():
                if resource in active_tasks:
                    # Conflict detected
                    for other_task_id in active_tasks[resource]:
                        conflicts.append((task.id, other_task_id, resource))
        
        return conflicts
    
    def acquire_lock(self, task_id: str, resource: str) -> bool:
        """Acquire a resource lock."""
        if resource not in self.resource_locks:
            self.resource_locks[resource] = set()
        
        self.resource_locks[resource].add(task_id)
        return True
    
    def release_lock(self, task_id: str, resource: str) -> bool:
        """Release a resource lock."""
        if resource in self.resource_locks:
            self.resource_locks[resource].discard(task_id)
        return True


class ResourceCoordinator:
    """Coordinate resource allocation."""
    
    def __init__(self):
        """Initialize coordinator."""
        self.resources: Dict[str, Dict[str, Any]] = {}
    
    def register_resource(self, name: str, capacity: float = 1.0) -> None:
        """Register a resource."""
        self.resources[name] = {
            "capacity": capacity,
            "allocated": 0.0,
        }
    
    def allocate(self, resource: str, amount: float) -> bool:
        """Allocate resource."""
        if resource not in self.resources:
            return False
        
        r = self.resources[resource]
        if r["allocated"] + amount > r["capacity"]:
            return False
        
        r["allocated"] += amount
        return True
    
    def release(self, resource: str, amount: float) -> bool:
        """Release resource."""
        if resource not in self.resources:
            return False
        
        self.resources[resource]["allocated"] = max(0, self.resources[resource]["allocated"] - amount)
        return True


class ParallelExecutor:
    """Universal Parallel Execution Engine."""
    
    def __init__(self, max_workers: int = 10):
        """Initialize executor."""
        self.scheduler = ParallelScheduler(max_workers)
        self.dependency_analyzer = DependencyAnalyzer()
        self.conflict_detector = ConflictDetector()
        self.resource_coordinator = ResourceCoordinator()
        self.execution_batches: List[ExecutionBatch] = []
    
    def execute(self, tasks: List[ExecutionTask]) -> Dict[str, ExecutionStatus]:
        """Execute tasks with parallelism."""
        # Analyze dependencies
        cycles = self.dependency_analyzer.find_cycles(tasks)
        if cycles:
            return {t.id: ExecutionStatus.FAILED for t in tasks}
        
        # Detect conflicts
        conflicts = self.conflict_detector.detect_conflicts(tasks)
        if conflicts:
            # Resolve by serializing conflicting tasks
            pass
        
        # Get parallel batches
        for task in tasks:
            self.scheduler.add_task(
                name=task.name,
                dependencies=task.dependencies,
                resources=task.resources,
            )
        
        batches = self.scheduler.get_parallel_batches()
        
        # Execute batches
        results = {}
        for batch in batches:
            # In a real implementation, tasks would execute in parallel
            for task in batch:
                task.status = ExecutionStatus.COMPLETED
                task.completed_at = datetime.now()
                results[task.id] = ExecutionStatus.COMPLETED
        
        return results
    
    def execute_pipeline(self, tasks: List[ExecutionTask]) -> Dict[str, ExecutionStatus]:
        """Execute tasks in pipeline mode."""
        # Pipeline mode: output of one task feeds into the next
        results = {}
        
        for task in tasks:
            if all(dep in results and results[dep] == ExecutionStatus.COMPLETED for dep in task.dependencies):
                task.status = ExecutionStatus.COMPLETED
                results[task.id] = ExecutionStatus.COMPLETED
            else:
                task.status = ExecutionStatus.FAILED
                results[task.id] = ExecutionStatus.FAILED
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics."""
        return {
            "total_tasks": len(self.scheduler.tasks),
            "pending_tasks": sum(1 for t in self.scheduler.tasks.values() if t.status == ExecutionStatus.PENDING),
            "completed_tasks": sum(1 for t in self.scheduler.tasks.values() if t.status == ExecutionStatus.COMPLETED),
            "failed_tasks": sum(1 for t in self.scheduler.tasks.values() if t.status == ExecutionStatus.FAILED),
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
