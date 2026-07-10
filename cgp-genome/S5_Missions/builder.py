#!/usr/bin/env python3
"""
CGP - Mission Builder
====================

Missions built from departments.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class MissionStatus(Enum):
    """Status of a mission."""
    PLANNING = "planning"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MissionPriority(Enum):
    """Priority levels."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


@dataclass
class MissionMetrics:
    """Metrics for a mission."""
    estimated_duration_seconds: int = 0
    actual_duration_seconds: int = 0
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    progress_percentage: float = 0.0
    success_rate: float = 0.0


@dataclass
class Mission:
    """
    A mission - full project decomposed into departments.
    
    Example:
      Build SaaS = Backend + Frontend + QA + DevOps + Documentation
    """
    mission_id: str
    name: str
    
    # Description
    description: str = ""
    
    # Composition
    required_departments: Tuple[str, ...] = ()
    optional_departments: Tuple[str, ...] = ()
    department_order: Tuple[str, ...] = ()
    
    # Status
    status: MissionStatus = MissionStatus.PLANNING
    priority: MissionPriority = MissionPriority.NORMAL
    
    # Metrics
    metrics: MissionMetrics = field(default_factory=MissionMetrics)
    
    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)
    
    # Timeline
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    # Metadata
    version: str = "1.0"
    tags: Tuple[str, ...] = ()
    
    def get_department_count(self) -> int:
        """Get total number of departments."""
        return len(self.required_departments) + len(self.optional_departments)


class MissionBuilder:
    """
    Builds missions from departments.
    """
    
    def __init__(self, department_registry=None):
        self.department_registry = department_registry
    
    def build(
        self,
        mission_id: str,
        name: str,
        department_ids: List[str],
        required: List[str] = None,
        optional: List[str] = None
    ) -> Mission:
        """Build a mission from departments."""
        mission = Mission(
            mission_id=mission_id,
            name=name,
            required_departments=tuple(required or department_ids),
            optional_departments=tuple(optional or []),
            department_order=tuple(department_ids),
        )
        return mission
    
    def decompose(self, mission: Mission) -> List[str]:
        """Get ordered list of departments."""
        return list(mission.department_order)
    
    def get_execution_plan(self, mission: Mission) -> List[Dict[str, Any]]:
        """Generate execution plan."""
        plan = []
        
        for dept_id in mission.department_order:
            plan.append({
                "department_id": dept_id,
                "action": "execute",
                "depends_on": plan[-1]["department_id"] if plan else None,
            })
        
        return plan


class MissionExecutor:
    """
    Executes missions.
    """
    
    def __init__(self):
        self._executors: Dict[str, Any] = {}
    
    def register_executor(
        self,
        department_id: str,
        executor: Any
    ) -> None:
        """Register an executor for a department."""
        self._executors[department_id] = executor
    
    def execute(self, mission: Mission) -> Mission:
        """Execute a mission."""
        mission.status = MissionStatus.RUNNING
        mission.started_at = datetime.utcnow().isoformat()
        
        # Execute each department in order
        for dept_id in mission.department_order:
            if dept_id in self._executors:
                # Execute
                pass
        
        mission.status = MissionStatus.COMPLETED
        mission.completed_at = datetime.utcnow().isoformat()
        
        return mission


class MissionRegistry:
    """
    Registry of all missions.
    """
    
    def __init__(self):
        self._missions: Dict[str, Mission] = {}
        self._by_status: Dict[MissionStatus, List[str]] = {}
    
    def register(self, mission: Mission) -> str:
        """Register a mission."""
        self._missions[mission.mission_id] = mission
        
        if mission.status not in self._by_status:
            self._by_status[mission.status] = []
        self._by_status[mission.status].append(mission.mission_id)
        
        return mission.mission_id
    
    def get(self, mission_id: str) -> Optional[Mission]:
        """Get a mission by ID."""
        return self._missions.get(mission_id)
    
    def get_by_status(self, status: MissionStatus) -> List[Mission]:
        """Get all missions with a status."""
        mission_ids = self._by_status.get(status, [])
        return [self._missions[mid] for mid in mission_ids if mid in self._missions]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        by_status = {status.value: len(ids) for status, ids in self._by_status.items()}
        
        return {
            "total_missions": len(self._missions),
            "by_status": by_status,
        }
