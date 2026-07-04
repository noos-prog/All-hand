"""Universal Scheduler Runtime."""
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import (
    Schedule, ScheduleType, ScheduleStatus, ExecutionCalendar
)


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
        
        # Add to calendar
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
    
    def update_schedule(self, schedule_id: str, **kwargs) -> Optional[Schedule]:
        """Update schedule attributes."""
        schedule = self.schedules.get(schedule_id)
        if not schedule:
            return None
        
        for key, value in kwargs.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
        
        schedule.updated_at = datetime.now()
        return schedule
    
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
        
        # If recurring, schedule next run
        if schedule.is_recurring and schedule.interval_seconds:
            schedule.next_run_at = datetime.now() + timedelta(seconds=schedule.interval_seconds)
        
        return True
    
    def complete_schedule(self, schedule_id: str) -> bool:
        """Mark a schedule as completed."""
        schedule = self.schedules.get(schedule_id)
        if not schedule:
            return False
        
        schedule.status = ScheduleStatus.COMPLETED
        schedule.completed_at = datetime.now()
        schedule.updated_at = datetime.now()
        
        # Handle recurring schedules
        if schedule.is_recurring:
            if schedule.max_runs and schedule.run_count >= schedule.max_runs:
                schedule.status = ScheduleStatus.COMPLETED
            else:
                schedule.status = ScheduleStatus.READY
                if schedule.interval_seconds:
                    schedule.next_run_at = datetime.now() + timedelta(seconds=schedule.interval_seconds)
        
        return True
    
    def fail_schedule(self, schedule_id: str, error: str = "") -> bool:
        """Mark a schedule as failed."""
        schedule = self.schedules.get(schedule_id)
        if not schedule:
            return False
        
        schedule.retry_count += 1
        
        if schedule.retry_enabled and schedule.retry_count < schedule.max_retries:
            # Schedule retry
            schedule.status = ScheduleStatus.PENDING
            schedule.next_run_at = datetime.now() + timedelta(seconds=schedule.retry_delay_seconds)
        else:
            schedule.status = ScheduleStatus.FAILED
        
        schedule.metadata["last_error"] = error
        schedule.updated_at = datetime.now()
        
        return True
    
    def get_ready_schedules(self) -> List[Schedule]:
        """Get all schedules ready to execute."""
        now = datetime.now()
        ready = []
        
        for schedule in self.schedules.values():
            if schedule.status != ScheduleStatus.READY:
                continue
            
            # Check if it's time to execute
            if schedule.execute_at <= now:
                # Check dependencies
                if not self._check_dependencies(schedule):
                    schedule.status = ScheduleStatus.BLOCKED
                    continue
                
                ready.append(schedule)
        
        # Sort by priority
        ready.sort(key=lambda s: s.priority, reverse=True)
        
        return ready
    
    def get_calendar(self) -> ExecutionCalendar:
        """Get the execution calendar."""
        self.calendar.current_time = datetime.now()
        return self.calendar
    
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
