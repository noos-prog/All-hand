#!/usr/bin/env python3
"""
AGOS Intelligence - Time Machine
===============================

Review any mission in history.
See what knowledge was available then.
Understand why decisions were made.

Time Machine allows you to:
- View past missions in full detail
- See state of knowledge at that time
- Compare with similar missions
- Replay mission execution
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json


class MissionStatus(Enum):
    """Status of a mission."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class TimelineEvent:
    """An event in the mission timeline."""
    event_id: str
    event_type: str              # e.g., "decision_made", "task_started", "task_completed"
    timestamp: str
    data: Dict[str, Any]
    actor: str                   # Who/what triggered this event
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
        }


@dataclass
class MissionSnapshot:
    """
    Complete snapshot of a mission at a point in time.
    
    Contains:
    - Mission info
    - State at that time
    - Knowledge available
    - Decisions made
    - Timeline of events
    """
    mission_id: str
    goal: str
    status: MissionStatus
    created_at: str
    completed_at: Optional[str] = None
    
    # State snapshot
    knowledge_available: Dict[str, Any] = field(default_factory=dict)
    repositories_analyzed: int = 0
    benchmarks_available: int = 0
    success_rate_at_time: float = 0.0
    
    # Decisions snapshot
    decisions: Tuple[Dict[str, Any], ...] = ()
    providers_selected: Tuple[str, ...] = ()
    reasoning_for_selections: Optional[str] = None
    
    # Timeline
    timeline: Tuple[TimelineEvent, ...] = ()
    
    # Results
    outcome: Optional[Dict[str, Any]] = None
    lessons_learned: Tuple[str, ...] = ()
    
    # Metadata
    duration_seconds: int = 0
    cost_usd: float = 0.0
    mode_used: str = "instant"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "goal": self.goal,
            "status": self.status.value,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "knowledge_available": self.knowledge_available,
            "repositories_analyzed": self.repositories_analyzed,
            "benchmarks_available": self.benchmarks_available,
            "success_rate_at_time": self.success_rate_at_time,
            "decisions": list(self.decisions),
            "providers_selected": list(self.providers_selected),
            "reasoning_for_selections": self.reasoning_for_selections,
            "timeline": [e.to_dict() for e in self.timeline],
            "outcome": self.outcome,
            "lessons_learned": list(self.lessons_learned),
            "duration_seconds": self.duration_seconds,
            "cost_usd": self.cost_usd,
            "mode_used": self.mode_used,
        }


@dataclass
class MissionReplay:
    """Replay of a past mission for analysis."""
    mission_id: str
    replay_id: str
    started_at: str
    
    # Events that would occur
    planned_events: Tuple[TimelineEvent, ...] = ()
    
    # What changed since then
    knowledge_delta: Dict[str, Any] = field(default_factory=dict)
    benchmarks_delta: Dict[str, Any] = field(default_factory=dict)
    
    # Recommendations
    would_recommend_same: bool = True
    recommendations: Tuple[str, ...] = ()


class TimeMachine:
    """
    The Time Machine for reviewing past missions.
    
    Allows viewing any mission in history with:
    - Full timeline of events
    - State of knowledge at that time
    - All decisions made and why
    - What was learned
    """
    
    def __init__(self, knowledge_base=None):
        self._knowledge_base = knowledge_base
        self._missions: Dict[str, MissionSnapshot] = {}
        self._replays: Dict[str, MissionReplay] = {}
        self._initialized = False
    
    def record_mission_start(
        self,
        mission_id: str,
        goal: str,
        mode: str,
        context: Dict[str, Any]
    ) -> str:
        """Record the start of a mission."""
        snapshot = MissionSnapshot(
            mission_id=mission_id,
            goal=goal,
            status=MissionStatus.RUNNING,
            created_at=datetime.utcnow().isoformat(),
            mode_used=mode,
            knowledge_available=self._capture_knowledge_state(),
        )
        
        self._missions[mission_id] = snapshot
        return mission_id
    
    def record_event(
        self,
        mission_id: str,
        event_type: str,
        data: Dict[str, Any],
        actor: str = "system"
    ) -> str:
        """Record an event in the mission timeline."""
        mission = self._missions.get(mission_id)
        if not mission:
            return None
        
        event = TimelineEvent(
            event_id=f"{mission_id}_evt_{len(mission.timeline)}",
            event_type=event_type,
            timestamp=datetime.utcnow().isoformat(),
            data=data,
            actor=actor,
        )
        
        # Update timeline
        new_timeline = mission.timeline + (event,)
        
        updated_mission = MissionSnapshot(
            mission_id=mission.mission_id,
            goal=mission.goal,
            status=mission.status,
            created_at=mission.created_at,
            completed_at=mission.completed_at,
            knowledge_available=mission.knowledge_available,
            repositories_analyzed=mission.repositories_analyzed,
            benchmarks_available=mission.benchmarks_available,
            success_rate_at_time=mission.success_rate_at_time,
            decisions=mission.decisions,
            providers_selected=mission.providers_selected,
            reasoning_for_selections=mission.reasoning_for_selections,
            timeline=new_timeline,
            outcome=mission.outcome,
            lessons_learned=mission.lessons_learned,
            duration_seconds=mission.duration_seconds,
            cost_usd=mission.cost_usd,
            mode_used=mission.mode_used,
        )
        
        self._missions[mission_id] = updated_mission
        
        return event.event_id
    
    def record_decision(
        self,
        mission_id: str,
        decision: Dict[str, Any]
    ) -> None:
        """Record a decision made during mission."""
        mission = self._missions.get(mission_id)
        if not mission:
            return
        
        new_decisions = mission.decisions + (decision,)
        
        updated_mission = MissionSnapshot(
            mission_id=mission.mission_id,
            goal=mission.goal,
            status=mission.status,
            created_at=mission.created_at,
            completed_at=mission.completed_at,
            knowledge_available=mission.knowledge_available,
            repositories_analyzed=mission.repositories_analyzed,
            benchmarks_available=mission.benchmarks_available,
            success_rate_at_time=mission.success_rate_at_time,
            decisions=new_decisions,
            providers_selected=mission.providers_selected,
            reasoning_for_selections=mission.reasoning_for_selections,
            timeline=mission.timeline,
            outcome=mission.outcome,
            lessons_learned=mission.lessons_learned,
            duration_seconds=mission.duration_seconds,
            cost_usd=mission.cost_usd,
            mode_used=mission.mode_used,
        )
        
        self._missions[mission_id] = updated_mission
    
    def record_provider_selection(
        self,
        mission_id: str,
        provider: str,
        reason: str
    ) -> None:
        """Record provider selection."""
        mission = self._missions.get(mission_id)
        if not mission:
            return
        
        new_providers = mission.providers_selected + (provider,)
        
        # Append to reasoning
        new_reasoning = (
            (mission.reasoning_for_selections or "") +
            f"\n{provider}: {reason}"
        ).strip()
        
        updated_mission = MissionSnapshot(
            mission_id=mission.mission_id,
            goal=mission.goal,
            status=mission.status,
            created_at=mission.created_at,
            completed_at=mission.completed_at,
            knowledge_available=mission.knowledge_available,
            repositories_analyzed=mission.repositories_analyzed,
            benchmarks_available=mission.benchmarks_available,
            success_rate_at_time=mission.success_rate_at_time,
            decisions=mission.decisions,
            providers_selected=new_providers,
            reasoning_for_selections=new_reasoning,
            timeline=mission.timeline,
            outcome=mission.outcome,
            lessons_learned=mission.lessons_learned,
            duration_seconds=mission.duration_seconds,
            cost_usd=mission.cost_usd,
            mode_used=mission.mode_used,
        )
        
        self._missions[mission_id] = updated_mission
    
    def complete_mission(
        self,
        mission_id: str,
        outcome: Dict[str, Any],
        lessons: List[str],
        duration_seconds: int,
        cost_usd: float
    ) -> None:
        """Complete a mission and record final state."""
        mission = self._missions.get(mission_id)
        if not mission:
            return
        
        updated_mission = MissionSnapshot(
            mission_id=mission.mission_id,
            goal=mission.goal,
            status=MissionStatus.COMPLETED,
            created_at=mission.created_at,
            completed_at=datetime.utcnow().isoformat(),
            knowledge_available=mission.knowledge_available,
            repositories_analyzed=mission.repositories_analyzed,
            benchmarks_available=mission.benchmarks_available,
            success_rate_at_time=mission.success_rate_at_time,
            decisions=mission.decisions,
            providers_selected=mission.providers_selected,
            reasoning_for_selections=mission.reasoning_for_selections,
            timeline=mission.timeline,
            outcome=outcome,
            lessons_learned=tuple(lessons),
            duration_seconds=duration_seconds,
            cost_usd=cost_usd,
            mode_used=mission.mode_used,
        )
        
        self._missions[mission_id] = updated_mission
    
    def get_mission(self, mission_id: str) -> Optional[MissionSnapshot]:
        """Get a mission by ID."""
        return self._missions.get(mission_id)
    
    def get_mission_timeline(self, mission_id: str) -> List[TimelineEvent]:
        """Get the full timeline of a mission."""
        mission = self._missions.get(mission_id)
        if not mission:
            return []
        return list(mission.timeline)
    
    def list_missions(
        self,
        status: Optional[MissionStatus] = None,
        limit: int = 50
    ) -> List[MissionSnapshot]:
        """List missions with optional filtering."""
        missions = list(self._missions.values())
        
        if status:
            missions = [m for m in missions if m.status == status]
        
        # Sort by creation time (newest first)
        missions.sort(key=lambda m: m.created_at, reverse=True)
        
        return missions[:limit]
    
    def compare_missions(
        self,
        mission_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare multiple missions."""
        missions = [self._missions.get(mid) for mid in mission_ids]
        missions = [m for m in missions if m is not None]
        
        if not missions:
            return {"error": "No missions found"}
        
        comparison = {
            "missions_compared": len(missions),
            "missions": [
                {
                    "id": m.mission_id,
                    "goal": m.goal,
                    "status": m.status.value,
                    "duration_seconds": m.duration_seconds,
                    "cost_usd": m.cost_usd,
                    "providers_used": list(m.providers_selected),
                }
                for m in missions
            ],
            "similarities": self._find_similarities(missions),
            "differences": self._find_differences(missions),
        }
        
        return comparison
    
    def _find_similarities(self, missions: List[MissionSnapshot]) -> List[str]:
        """Find similarities between missions."""
        similarities = []
        
        # Same mode used
        modes = set(m.mode_used for m in missions)
        if len(modes) == 1:
            similarities.append(f"All used {modes.pop()} mode")
        
        # Same providers
        all_providers = [set(m.providers_selected) for m in missions]
        common_providers = set.intersection(*all_providers) if all_providers else set()
        if common_providers:
            similarities.append(f"Common providers: {', '.join(common_providers)}")
        
        return similarities
    
    def _find_differences(self, missions: List[MissionSnapshot]) -> List[str]:
        """Find differences between missions."""
        differences = []
        
        # Duration differences
        durations = [m.duration_seconds for m in missions]
        if max(durations) - min(durations) > 60:
            differences.append("Significant duration variation")
        
        # Cost differences
        costs = [m.cost_usd for m in missions]
        if max(costs) - min(costs) > 5:
            differences.append("Significant cost variation")
        
        # Success rate differences
        rates = [m.success_rate_at_time for m in missions]
        if rates and max(rates) - min(rates) > 0.1:
            differences.append("Knowledge state varied significantly")
        
        return differences
    
    def replay_mission(self, mission_id: str) -> Optional[MissionReplay]:
        """Generate a replay of a mission with current context."""
        mission = self._missions.get(mission_id)
        if not mission:
            return None
        
        replay_id = f"replay_{mission_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate what changed since then
        current_knowledge = self._capture_knowledge_state()
        knowledge_delta = {
            k: {
                "before": mission.knowledge_available.get(k),
                "after": current_knowledge.get(k),
            }
            for k in set(list(mission.knowledge_available.keys()) +
                       list(current_knowledge.keys()))
            if mission.knowledge_available.get(k) != current_knowledge.get(k)
        }
        
        # Generate recommendations
        recommendations = []
        if knowledge_delta:
            recommendations.append("Knowledge base has evolved - review new evidence")
        
        if mission.status == MissionStatus.COMPLETED:
            # Check if we would still recommend the same approach
            would_recommend = True
            if knowledge_delta:
                recommendations.append("Consider alternative approaches based on new knowledge")
                would_recommend = False
        
        replay = MissionReplay(
            mission_id=mission_id,
            replay_id=replay_id,
            started_at=datetime.utcnow().isoformat(),
            planned_events=mission.timeline,
            knowledge_delta=knowledge_delta,
            would_recommend_same=would_recommend,
            recommendations=tuple(recommendations),
        )
        
        self._replays[replay_id] = replay
        return replay
    
    def _capture_knowledge_state(self) -> Dict[str, Any]:
        """Capture current state of knowledge base."""
        if self._knowledge_base:
            stats = self._knowledge_base.get_statistics()
            return {
                "total_knowledge": stats.get("total_knowledge", 0),
                "total_evidence": stats.get("total_evidence", 0),
                "average_confidence": stats.get("average_confidence", 0),
                "by_category": stats.get("by_category", {}),
            }
        return {}
    
    def find_similar_missions(
        self,
        goal: str,
        limit: int = 5
    ) -> List[MissionSnapshot]:
        """Find missions similar to a given goal."""
        goal_lower = goal.lower()
        keywords = set(goal_lower.split())
        
        scored_missions = []
        for mission in self._missions.values():
            if mission.status != MissionStatus.COMPLETED:
                continue
            
            # Calculate similarity
            mission_keywords = set(mission.goal.lower().split())
            common = keywords & mission_keywords
            if common:
                score = len(common) / max(len(keywords), len(mission_keywords))
                scored_missions.append((score, mission))
        
        # Sort by score (highest first)
        scored_missions.sort(key=lambda x: x[0], reverse=True)
        
        return [m for _, m in scored_missions[:limit]]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get time machine statistics."""
        missions = list(self._missions.values())
        
        by_status = {}
        total_duration = 0
        total_cost = 0.0
        
        for mission in missions:
            status = mission.status.value
            by_status[status] = by_status.get(status, 0) + 1
            total_duration += mission.duration_seconds
            total_cost += mission.cost_usd
        
        return {
            "total_missions": len(missions),
            "by_status": by_status,
            "completed_missions": len([m for m in missions if m.status == MissionStatus.COMPLETED]),
            "total_duration_seconds": total_duration,
            "total_cost_usd": round(total_cost, 2),
            "average_duration_seconds": total_duration / len(missions) if missions else 0,
            "total_replays": len(self._replays),
        }
