#!/usr/bin/env python3
"""
CGP - Evolution Tracker
=====================

Track how capabilities evolve over time.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class EvolutionTrend(Enum):
    """Evolution trend."""
    GROWING = "growing"
    STABLE = "stable"
    DECLINING = "declining"


@dataclass
class EvolutionEvent:
    """An event in capability evolution."""
    event_id: str
    capability_id: str
    event_type: str  # added, improved, deprecated, removed
    description: str
    timestamp: str
    project_id: Optional[str] = None


@dataclass
class Evolution:
    """Evolution analysis for a capability."""
    capability_id: str
    
    first_appeared: str = ""
    first_project: str = ""
    
    growth_rate: float = 0.0
    trend: EvolutionTrend = EvolutionTrend.STABLE
    
    major_improvements: Tuple[str, ...] = ()
    deprecations: Tuple[str, ...] = ()
    
    adoption_count: int = 0
    abandonment_count: int = 0
    
    future_trends: Tuple[str, ...] = ()
    
    analyzed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class TrendPrediction:
    """Predicted trend."""
    capability_id: str
    predicted_trend: EvolutionTrend
    confidence: float
    time_horizon_days: int
    factors: Tuple[str, ...] = ()


class EvolutionTracker:
    """
    Track capability evolution.
    """
    
    def __init__(self):
        self._events: List[EvolutionEvent] = []
        self._capability_history: Dict[str, List[EvolutionEvent]] = {}
    
    def record_event(self, event: EvolutionEvent) -> None:
        """Record an evolution event."""
        self._events.append(event)
        
        if event.capability_id not in self._capability_history:
            self._capability_history[event.capability_id] = []
        self._capability_history[event.capability_id].append(event)
    
    def get_history(self, capability_id: str) -> List[EvolutionEvent]:
        """Get evolution history for a capability."""
        return self._capability_history.get(capability_id, [])
    
    def get_all_events(self) -> List[EvolutionEvent]:
        """Get all evolution events."""
        return self._events
    
    def calculate_growth_rate(self, capability_id: str) -> float:
        """Calculate growth rate for a capability."""
        history = self._capability_history.get(capability_id, [])
        if not history:
            return 0.0
        
        additions = sum(1 for e in history if e.event_type == "added")
        removals = sum(1 for e in history if e.event_type == "removed")
        
        if additions + removals == 0:
            return 0.0
        
        return (additions - removals) / (additions + removals)


class EvolutionAnalyzer:
    """
    Analyzes capability evolution.
    """
    
    def __init__(self, tracker: EvolutionTracker):
        self.tracker = tracker
    
    def analyze(self, capability_id: str) -> Evolution:
        """Analyze evolution of a capability."""
        history = self.tracker.get_history(capability_id)
        
        if not history:
            return Evolution(capability_id=capability_id)
        
        # Find first appearance
        sorted_history = sorted(history, key=lambda e: e.timestamp)
        first = sorted_history[0]
        
        # Calculate growth rate
        growth_rate = self.tracker.calculate_growth_rate(capability_id)
        
        # Determine trend
        if growth_rate > 0.2:
            trend = EvolutionTrend.GROWING
        elif growth_rate < -0.2:
            trend = EvolutionTrend.DECLINING
        else:
            trend = EvolutionTrend.STABLE
        
        # Find improvements and deprecations
        improvements = [e.description for e in history if e.event_type == "improved"]
        deprecations = [e.description for e in history if e.event_type == "deprecated"]
        
        # Count adoptions
        adoptions = sum(1 for e in history if e.event_type == "added")
        abandonments = sum(1 for e in history if e.event_type == "removed")
        
        return Evolution(
            capability_id=capability_id,
            first_appeared=first.timestamp,
            first_project=first.project_id or "",
            growth_rate=growth_rate,
            trend=trend,
            major_improvements=tuple(improvements),
            deprecations=tuple(deprecations),
            adoption_count=adoptions,
            abandonment_count=abandonments,
        )


class TrendPredictor:
    """
    Predict capability trends.
    """
    
    def __init__(self, analyzer: EvolutionAnalyzer):
        self.analyzer = analyzer
    
    def predict(
        self,
        capability_id: str,
        time_horizon_days: int = 90
    ) -> TrendPrediction:
        """Predict trend for a capability."""
        evolution = self.analyzer.analyze(capability_id)
        
        # Simple prediction based on current trend
        predicted_trend = evolution.trend
        confidence = 0.5
        
        # Adjust confidence based on data
        if evolution.adoption_count > 10:
            confidence = 0.8
        
        factors = []
        if evolution.trend == EvolutionTrend.GROWING:
            factors.append("High adoption rate")
        elif evolution.trend == EvolutionTrend.DECLINING:
            factors.append("Declining usage")
        
        return TrendPrediction(
            capability_id=capability_id,
            predicted_trend=predicted_trend,
            confidence=confidence,
            time_horizon_days=time_horizon_days,
            factors=tuple(factors),
        )
