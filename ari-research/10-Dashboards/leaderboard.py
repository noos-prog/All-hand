#!/usr/bin/env python3
"""
ARI - Leaderboard
================

Provider and model leaderboards.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class RankingType(Enum):
    """Types of ranking."""
    OVERALL = "overall"
    PERFORMANCE = "performance"
    COST = "cost"
    QUALITY = "quality"
    SPEED = "speed"


@dataclass
class RankingCriteria:
    """Criteria for ranking."""
    criteria_id: str
    name: str
    description: str
    
    # Weight in ranking (0-1)
    weight: float = 1.0
    
    # Higher is better?
    higher_is_better: bool = True
    
    # Scoring function
    score_func: Optional[Callable] = None


@dataclass
class LeaderboardEntry:
    """An entry in the leaderboard."""
    entry_id: str
    entity_id: str                      # Provider or model ID
    entity_name: str
    entity_type: str                    # provider, model
    
    # Rank
    rank: int = 0
    previous_rank: Optional[int] = None
    rank_change: int = 0               # Positive = improved
    
    # Scores
    overall_score: float = 0.0
    criteria_scores: Dict[str, float] = field(default_factory=dict)
    
    # Metrics
    success_rate: float = 0.0
    avg_latency_ms: float = 0.0
    avg_cost: float = 0.0
    sample_size: int = 0
    
    # Metadata
    last_updated: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def get_summary(self) -> Dict[str, Any]:
        """Get entry summary."""
        return {
            "rank": self.rank,
            "name": self.entity_name,
            "score": f"{self.overall_score:.1%}",
            "success_rate": f"{self.success_rate:.1%}",
            "rank_change": f"+{self.rank_change}" if self.rank_change > 0 else str(self.rank_change),
        }


@dataclass
class Leaderboard:
    """A leaderboard."""
    leaderboard_id: str
    name: str
    description: str
    leaderboard_type: RankingType
    
    # Entries
    entries: Tuple[LeaderboardEntry, ...] = ()
    
    # Criteria used
    criteria: Tuple[RankingCriteria, ...] = ()
    
    # Filters
    filters: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Statistics
    total_entries: int = 0
    avg_score: float = 0.0
    
    def get_top(self, count: int = 10) -> List[LeaderboardEntry]:
        """Get top N entries."""
        return list(sorted(self.entries, key=lambda e: e.rank))[:count]
    
    def get_entry(self, entity_id: str) -> Optional[LeaderboardEntry]:
        """Get entry by entity ID."""
        for entry in self.entries:
            if entry.entity_id == entity_id:
                return entry
        return None


class RankingEngine:
    """
    Engine for ranking providers and models.
    """
    
    def __init__(self):
        self._leaderboards: Dict[str, Leaderboard] = {}
        self._default_criteria = self._create_default_criteria()
    
    def _create_default_criteria(self) -> List[RankingCriteria]:
        """Create default ranking criteria."""
        return [
            RankingCriteria(
                criteria_id="success_rate",
                name="Success Rate",
                description="Percentage of successful tasks",
                weight=0.3,
                higher_is_better=True,
            ),
            RankingCriteria(
                criteria_id="performance",
                name="Performance",
                description="Overall performance score",
                weight=0.3,
                higher_is_better=True,
            ),
            RankingCriteria(
                criteria_id="cost_efficiency",
                name="Cost Efficiency",
                description="Value per dollar",
                weight=0.2,
                higher_is_better=True,
            ),
            RankingCriteria(
                criteria_id="speed",
                name="Speed",
                description="Average latency",
                weight=0.2,
                higher_is_better=False,
            ),
        ]
    
    def create_leaderboard(
        self,
        name: str,
        description: str,
        ranking_type: RankingType,
        criteria: List[RankingCriteria] = None
    ) -> Leaderboard:
        """Create a new leaderboard."""
        leaderboard_id = f"lb_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        leaderboard = Leaderboard(
            leaderboard_id=leaderboard_id,
            name=name,
            description=description,
            leaderboard_type=ranking_type,
            criteria=tuple(criteria or self._default_criteria),
        )
        
        self._leaderboards[leaderboard_id] = leaderboard
        return leaderboard
    
    def rank_providers(
        self,
        provider_data: List[Dict[str, Any]],
        criteria: List[RankingCriteria] = None
    ) -> Leaderboard:
        """Rank providers."""
        criteria = criteria or self._default_criteria
        
        # Calculate scores
        entries = []
        for i, data in enumerate(provider_data):
            scores = {}
            overall = 0.0
            total_weight = 0.0
            
            for criterion in criteria:
                value = data.get(criterion.criteria_id, 0)
                
                # Normalize if needed
                if criterion.score_func:
                    value = criterion.score_func(value)
                
                if criterion.higher_is_better:
                    normalized = min(1.0, value)
                else:
                    normalized = max(0, 1 - value)
                
                scores[criterion.criteria_id] = normalized
                overall += normalized * criterion.weight
                total_weight += criterion.weight
            
            if total_weight > 0:
                overall = overall / total_weight
            
            entry = LeaderboardEntry(
                entry_id=f"entry_{i}",
                entity_id=data.get("provider_id", f"provider_{i}"),
                entity_name=data.get("name", f"Provider {i}"),
                entity_type="provider",
                overall_score=overall,
                criteria_scores=scores,
                success_rate=data.get("success_rate", 0),
                avg_latency_ms=data.get("avg_latency_ms", 0),
                avg_cost=data.get("avg_cost", 0),
                sample_size=data.get("sample_size", 0),
            )
            entries.append(entry)
        
        # Sort by overall score
        entries.sort(key=lambda e: e.overall_score, reverse=True)
        
        # Assign ranks
        for i, entry in enumerate(entries):
            entry.rank = i + 1
        
        # Create leaderboard
        leaderboard_id = f"lb_providers_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        leaderboard = Leaderboard(
            leaderboard_id=leaderboard_id,
            name="Provider Leaderboard",
            description="Ranked providers",
            leaderboard_type=RankingType.OVERALL,
            entries=tuple(entries),
            criteria=tuple(criteria),
            total_entries=len(entries),
            avg_score=sum(e.overall_score for e in entries) / len(entries) if entries else 0,
        )
        
        self._leaderboards[leaderboard_id] = leaderboard
        return leaderboard
    
    def rank_models(
        self,
        model_data: List[Dict[str, Any]],
        criteria: List[RankingCriteria] = None
    ) -> Leaderboard:
        """Rank models."""
        criteria = criteria or self._default_criteria
        
        entries = []
        for i, data in enumerate(model_data):
            scores = {}
            overall = 0.0
            total_weight = 0.0
            
            for criterion in criteria:
                value = data.get(criterion.criteria_id, 0)
                
                if criterion.higher_is_better:
                    normalized = min(1.0, value)
                else:
                    normalized = max(0, 1 - value)
                
                scores[criterion.criteria_id] = normalized
                overall += normalized * criterion.weight
                total_weight += criterion.weight
            
            if total_weight > 0:
                overall = overall / total_weight
            
            entry = LeaderboardEntry(
                entry_id=f"entry_{i}",
                entity_id=data.get("model_id", f"model_{i}"),
                entity_name=data.get("name", f"Model {i}"),
                entity_type="model",
                overall_score=overall,
                criteria_scores=scores,
                success_rate=data.get("accuracy", 0),
                avg_latency_ms=data.get("avg_latency_ms", 0),
                avg_cost=data.get("cost_per_1k", 0),
                sample_size=data.get("benchmarks_run", 0),
            )
            entries.append(entry)
        
        entries.sort(key=lambda e: e.overall_score, reverse=True)
        
        for i, entry in enumerate(entries):
            entry.rank = i + 1
        
        leaderboard_id = f"lb_models_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        leaderboard = Leaderboard(
            leaderboard_id=leaderboard_id,
            name="Model Leaderboard",
            description="Ranked models",
            leaderboard_type=RankingType.OVERALL,
            entries=tuple(entries),
            criteria=tuple(criteria),
            total_entries=len(entries),
            avg_score=sum(e.overall_score for e in entries) / len(entries) if entries else 0,
        )
        
        self._leaderboards[leaderboard_id] = leaderboard
        return leaderboard
    
    def get_leaderboard(self, leaderboard_id: str) -> Optional[Leaderboard]:
        """Get a leaderboard by ID."""
        return self._leaderboards.get(leaderboard_id)
    
    def update_rankings(
        self,
        leaderboard_id: str,
        new_data: List[Dict[str, Any]]
    ) -> bool:
        """Update leaderboard with new data."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return False
        
        # Store previous ranks
        previous_ranks = {e.entity_id: e.rank for e in leaderboard.entries}
        
        # Re-rank
        if leaderboard.entity_type == "provider":
            new_leaderboard = self.rank_providers(new_data, list(leaderboard.criteria))
        else:
            new_leaderboard = self.rank_models(new_data, list(leaderboard.criteria))
        
        # Update rank changes
        for entry in new_leaderboard.entries:
            if entry.entity_id in previous_ranks:
                entry.previous_rank = previous_ranks[entry.entity_id]
                entry.rank_change = entry.previous_rank - entry.rank
        
        # Update leaderboard
        self._leaderboards[leaderboard_id] = new_leaderboard
        return True
    
    def export_leaderboard(
        self,
        leaderboard_id: str,
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export leaderboard."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return {"error": "Leaderboard not found"}
        
        return {
            "leaderboard_id": leaderboard.leaderboard_id,
            "name": leaderboard.name,
            "type": leaderboard.leaderboard_type.value,
            "entries": [e.get_summary() for e in leaderboard.entries],
            "total_entries": leaderboard.total_entries,
            "avg_score": leaderboard.avg_score,
            "updated_at": leaderboard.updated_at,
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            "total_leaderboards": len(self._leaderboards),
            "by_type": {
                rt.value: len([
                    lb for lb in self._leaderboards.values()
                    if lb.leaderboard_type == rt
                ])
                for rt in RankingType
            },
        }
