"""Universal Scheduler Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional

from .models import (
    Schedule, ScheduleType, ScheduleStatus, ExecutionCalendar
)


@dataclass
class ScheduleConfig:
    """Scheduler configuration."""
    max_concurrent: int = 4
    default_priority: int = 0
    default_retry_enabled: bool = True
    default_max_retries: int = 3
    default_retry_delay: float = 60.0
    timezone: str = "UTC"


@dataclass
class ScheduledTask:
    """A scheduled task wrapper."""
    id: str
    name: str
    handler: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    schedule: Optional[Schedule] = None
    last_result: Any = None
    last_error: Optional[str] = None


class SchedulerRuntime:
    """Universal Scheduler Runtime."""
    
    def __init__(self):
        """Initialize scheduler runtime."""
        self.schedules: Dict[str, Schedule] = {}
        self.calendar = ExecutionCalendar()
    
    def create_schedule(
        self,
        name: str,
        schedule_type: ScheduleType,
        execute_at: Optional[datetime] = None,
        payload: Optional[Dict[str, Any]] = None,
        priority: int = 0,
        depends_on: Optional[List[str]] = None,
        is_recurring: bool = False,
        interval_seconds: Optional[float] = None,
        max_retries: int = 3,
    ) -> Schedule:
        """Create a new schedule."""
        schedule_id = self._generate_id(name)
        
        schedule = Schedule(
            id=schedule_id,
            name=name,
            schedule_type=schedule_type,
            execute_at=execute_at or datetime.now(),
            priority=priority,
            depends_on=depends_on or [],
            is_recurring=is_recurring,
            interval_seconds=interval_seconds,
            max_retries=max_retries,
            payload=payload or {},
        )
        
        schedule.status = ScheduleStatus.READY
        schedule.created_at = datetime.now()
        schedule.updated_at = datetime.now()
        
        self.calendar.schedules.append(schedule)
        self.schedules[schedule_id] = schedule
        
        return schedule
    
    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        """Get schedule by ID."""
        return self.schedules.get(schedule_id)
    
    def list_schedules(
        self,
        status: Optional[ScheduleStatus] = None,
        schedule_type: Optional[ScheduleType] = None,
    ) -> List[Schedule]:
        """List schedules with optional filtering."""
        schedules = list(self.schedules.values())
        
        if status:
            schedules = [s for s in schedules if s.status == status]
        
        if schedule_type:
            schedules = [s for s in schedules if s.schedule_type == schedule_type]
        
        return schedules
    
    def cancel_schedule(self, schedule_id: str) -> bool:
        """Cancel a schedule."""
        schedule = self.schedules.get(schedule_id)
        if not schedule:
            return False
        
        schedule.status = ScheduleStatus.CANCELLED
        schedule.updated_at = datetime.now()
        return True
    
    def execute_now(self, schedule_id: str) -> bool:
        """Execute a schedule immediately."""
        schedule = self.schedules.get(schedule_id)
        if not schedule:
            return False
        
        if schedule.status in [ScheduleStatus.RUNNING, ScheduleStatus.BLOCKED]:
            return False
        
        schedule.status = ScheduleStatus.RUNNING
        schedule.last_run_at = datetime.now()
        schedule.run_count += 1
        schedule.updated_at = datetime.now()
        
        if schedule.is_recurring and schedule.interval_seconds:
            schedule.next_run_at = datetime.now() + timedelta(seconds=schedule.interval_seconds)
        
        return True
    
    def get_ready_schedules(self) -> List[Schedule]:
        """Get all schedules ready to execute."""
        now = datetime.now()
        ready = []
        
        for schedule in self.schedules.values():
            if schedule.status != ScheduleStatus.READY:
                continue
            
            if schedule.execute_at <= now:
                if not self._check_dependencies(schedule):
                    schedule.status = ScheduleStatus.BLOCKED
                    continue
                ready.append(schedule)
        
        ready.sort(key=lambda s: s.priority, reverse=True)
        return ready
    
    def _check_dependencies(self, schedule: Schedule) -> bool:
        """Check if all dependencies are completed."""
        for dep_id in schedule.depends_on:
            dep = self.schedules.get(dep_id)
            if dep and dep.status != ScheduleStatus.COMPLETED:
                return False
        return True
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]


class TaskScheduler:
    """
    High-level Task Scheduler.
    
    Wraps SchedulerRuntime with task-based API.
    """
    
    def __init__(self, config: Optional[ScheduleConfig] = None):
        """Initialize task scheduler."""
        self.config = config or ScheduleConfig()
        self._runtime = SchedulerRuntime()
        self._tasks: Dict[str, ScheduledTask] = {}
        self._running = False
    
    def schedule(
        self,
        name: str,
        handler: Callable,
        args: tuple = None,
        kwargs: Dict[str, Any] = None,
        schedule_type: ScheduleType = ScheduleType.SCHEDULED,
        execute_at: Optional[datetime] = None,
        is_recurring: bool = False,
        interval_seconds: Optional[float] = None,
    ) -> ScheduledTask:
        """Schedule a task."""
        schedule = self._runtime.create_schedule(
            name=name,
            schedule_type=schedule_type,
            execute_at=execute_at,
            is_recurring=is_recurring,
            interval_seconds=interval_seconds,
        )
        
        task = ScheduledTask(
            id=schedule.id,
            name=name,
            handler=handler,
            args=args or (),
            kwargs=kwargs or {},
            schedule=schedule,
        )
        
        self._tasks[task.id] = task
        return task
    
    def unschedule(self, task_id: str) -> bool:
        """Unschedule a task."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return self._runtime.cancel_schedule(task_id)
        return False
    
    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """Get a task by ID."""
        return self._tasks.get(task_id)
    
    def list_tasks(self) -> List[ScheduledTask]:
        """List all tasks."""
        return list(self._tasks.values())
    
    def execute_now(self, task_id: str) -> bool:
        """Execute a task immediately."""
        return self._runtime.execute_now(task_id)
    
    def start(self) -> None:
        """Start the scheduler."""
        self._running = True
    
    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        return {
            "total_tasks": len(self._tasks),
            "running": self._running,
        }


# Global scheduler instance
_scheduler: Optional[TaskScheduler] = None


def get_scheduler() -> TaskScheduler:
    """Get the global scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = TaskScheduler()
    return _scheduler
