#!/usr/bin/env python3
"""
CGP - Reuse Engine
=================

Analyze capability reuse across projects.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class ReuseStatus(Enum):
    """Reuse status levels."""
    MISSING = "missing"
    EMERGING = "emerging"
    GROWING = "growing"
    MATURE = "mature"
    DOMINANT = "dominant"


@dataclass
class ReuseScore:
    """Reuse score for a capability."""
    capability_id: str
    project_count: int
    reuse_score: float
    status: ReuseStatus
    avg_quality: float = 0.0
    avg_cost: float = 0.0
    projects: Tuple[str, ...] = ()


@dataclass
class ReuseAnalysis:
    """Analysis of capability reuse."""
    capability_id: str
    capability_name: str
    
    project_count: int
    projects: Tuple[str, ...] = ()
    
    reuse_score: float = 0.0
    status: ReuseStatus = ReuseStatus.EMERGING
    
    avg_quality: float = 0.0
    avg_cost: float = 0.0
    avg_duration_seconds: int = 0
    
    trend: str = "stable"
    
    analyzed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class ReuseEngine:
    """
    Engine for analyzing capability reuse.
    """
    
    def __init__(self):
        self._usage_map: Dict[str, List[str]] = {}  # capability_id -> project_ids
        self._project_caps: Dict[str, List[str]] = {}  # project_id -> capability_ids
    
    def record_usage(self, project_id: str, capability_id: str) -> None:
        """Record that a project uses a capability."""
        # Update capability -> projects map
        if capability_id not in self._usage_map:
            self._usage_map[capability_id] = []
        if project_id not in self._usage_map[capability_id]:
            self._usage_map[capability_id].append(project_id)
        
        # Update project -> capabilities map
        if project_id not in self._project_caps:
            self._project_caps[project_id] = []
        if capability_id not in self._project_caps[project_id]:
            self._project_caps[project_id].append(capability_id)
    
    def get_projects_with(self, capability_id: str) -> List[str]:
        """Get all projects that use a capability."""
        return self._usage_map.get(capability_id, [])
    
    def get_capabilities_of(self, project_id: str) -> List[str]:
        """Get all capabilities used by a project."""
        return self._project_caps.get(project_id, [])
    
    def calculate_reuse_score(self, project_count: int) -> float:
        """Calculate reuse score based on project count."""
        if project_count == 0:
            return 0.0
        elif project_count < 3:
            return 0.2
        elif project_count < 10:
            return 0.5
        elif project_count < 50:
            return 0.8
        else:
            return 1.0
    
    def determine_status(self, project_count: int) -> ReuseStatus:
        """Determine reuse status based on project count."""
        if project_count == 0:
            return ReuseStatus.MISSING
        elif project_count < 3:
            return ReuseStatus.EMERGING
        elif project_count < 10:
            return ReuseStatus.GROWING
        elif project_count < 50:
            return ReuseStatus.MATURE
        else:
            return ReuseStatus.DOMINANT


class ReuseAnalyzer:
    """
    Analyzes capability reuse.
    """
    
    def __init__(self, engine: ReuseEngine):
        self.engine = engine
    
    def analyze(self, capability_id: str) -> ReuseAnalysis:
        """Analyze reuse of a capability."""
        projects = self.engine.get_projects_with(capability_id)
        project_count = len(projects)
        
        reuse_score = self.engine.calculate_reuse_score(project_count)
        status = self.engine.determine_status(project_count)
        
        return ReuseAnalysis(
            capability_id=capability_id,
            capability_name=capability_id,
            project_count=project_count,
            projects=tuple(projects),
            reuse_score=reuse_score,
            status=status,
        )
    
    def find_most_reused(self, limit: int = 10) -> List[ReuseScore]:
        """Find most reused capabilities."""
        scores = []
        
        for cap_id, projects in self.engine._usage_map.items():
            score = self.engine.calculate_reuse_score(len(projects))
            status = self.engine.determine_status(len(projects))
            
            scores.append(ReuseScore(
                capability_id=cap_id,
                project_count=len(projects),
                reuse_score=score,
                status=status,
                projects=tuple(projects),
            ))
        
        scores.sort(key=lambda s: s.reuse_score, reverse=True)
        return scores[:limit]
    
    def find_never_reused(self) -> List[str]:
        """Find capabilities that are never reused."""
        never_reused = []
        
        for cap_id in self.engine._usage_map.keys():
            if len(self.engine._usage_map[cap_id]) == 0:
                never_reused.append(cap_id)
        
        return never_reused
