#!/usr/bin/env python3
"""
CGP - Overlap Analyzer
=====================

Analyze overlap between projects.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


@dataclass
class OverlapMatrix:
    """Overlap matrix between multiple projects."""
    project_ids: Tuple[str, ...]
    capability_ids: Tuple[str, ...]
    
    # Matrix: project_id -> [capability_ids used]
    matrix: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    
    # Statistics
    shared_count: int = 0
    total_unique: int = 0
    
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ProjectOverlap:
    """Overlap analysis between two projects."""
    project_a: str
    project_b: str
    
    shared_capabilities: Tuple[str, ...] = ()
    unique_to_a: Tuple[str, ...] = ()
    unique_to_b: Tuple[str, ...] = ()
    
    jaccard_index: float = 0.0
    overlap_percentage_a: float = 0.0  # How much of A is shared
    overlap_percentage_b: float = 0.0  # How much of B is shared


class SimilarityCalculator:
    """
    Calculate similarity between projects.
    """
    
    def jaccard(self, set_a: set, set_b: set) -> float:
        """Calculate Jaccard index."""
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0
    
    def overlap_percentage(self, set_a: set, set_b: set) -> Tuple[float, float]:
        """Calculate overlap percentage for both sets."""
        intersection = len(set_a & set_b)
        pct_a = intersection / len(set_a) if set_a else 0.0
        pct_b = intersection / len(set_b) if set_b else 0.0
        return pct_a, pct_b


class OverlapAnalyzer:
    """
    Analyzes overlap between projects.
    """
    
    def __init__(self):
        self._project_caps: Dict[str, set] = {}  # project_id -> set of capability_ids
        self._calculator = SimilarityCalculator()
    
    def register_project(self, project_id: str, capability_ids: List[str]) -> None:
        """Register a project's capabilities."""
        self._project_caps[project_id] = set(capability_ids)
    
    def analyze_pair(
        self,
        project_a: str,
        project_b: str
    ) -> ProjectOverlap:
        """Analyze overlap between two projects."""
        if project_a not in self._project_caps or project_b not in self._project_caps:
            return ProjectOverlap(project_a=project_a, project_b=project_b)
        
        caps_a = self._project_caps[project_a]
        caps_b = self._project_caps[project_b]
        
        shared = caps_a & caps_b
        unique_a = caps_a - caps_b
        unique_b = caps_b - caps_a
        
        jaccard = self._calculator.jaccard(caps_a, caps_b)
        pct_a, pct_b = self._calculator.overlap_percentage(caps_a, caps_b)
        
        return ProjectOverlap(
            project_a=project_a,
            project_b=project_b,
            shared_capabilities=tuple(shared),
            unique_to_a=tuple(unique_a),
            unique_to_b=tuple(unique_b),
            jaccard_index=jaccard,
            overlap_percentage_a=pct_a,
            overlap_percentage_b=pct_b,
        )
    
    def build_matrix(self, project_ids: List[str]) -> OverlapMatrix:
        """Build overlap matrix for multiple projects."""
        matrix = {}
        all_caps = set()
        
        for pid in project_ids:
            if pid in self._project_caps:
                matrix[pid] = tuple(self._project_caps[pid])
                all_caps |= self._project_caps[pid]
        
        shared_count = 0
        for caps in matrix.values():
            shared_count += len(set(caps) & all_caps)
        
        return OverlapMatrix(
            project_ids=tuple(project_ids),
            capability_ids=tuple(all_caps),
            matrix=matrix,
            shared_count=shared_count,
            total_unique=len(all_caps),
        )
    
    def find_most_similar(
        self,
        project_id: str,
        limit: int = 5
    ) -> List[Tuple[str, float]]:
        """Find most similar projects to a given project."""
        if project_id not in self._project_caps:
            return []
        
        similarities = []
        
        for other_id, caps in self._project_caps.items():
            if other_id != project_id:
                jaccard = self._calculator.jaccard(
                    self._project_caps[project_id],
                    caps
                )
                similarities.append((other_id, jaccard))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:limit]
