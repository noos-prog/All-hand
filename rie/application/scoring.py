"""Scoring Engine - Calculate quality scores."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from ..domain.repository import Repository
from ..domain.scores import QualityScores, ProductionReadiness
from ..detectors.base_detector import DetectionResult


@dataclass
class ScoreWeights:
    """Weights for scoring components."""
    architecture: float = 0.2
    quality: float = 0.2
    maintainability: float = 0.15
    documentation: float = 0.15
    ai_maturity: float = 0.1
    production_readiness: float = 0.2


class ScoringEngine:
    """
    Scoring Engine.
    
    Scores:
    - Architecture Score
    - Quality Score
    - Maintainability Score
    - Documentation Score
    - AI Maturity Score
    - Production Readiness Score
    """
    
    def __init__(self, weights: ScoreWeights = None):
        self.weights = weights or ScoreWeights()
    
    def calculate_architecture_score(
        self,
        repo: Repository,
        detections: List[DetectionResult],
    ) -> float:
        """Calculate architecture score."""
        score = 0.5  # Base score
        
        # Boost for detected patterns
        arch_detections = [d for d in detections if "Architecture" in d.detector_name]
        if arch_detections:
            avg_confidence = sum(d.confidence for d in arch_detections) / len(arch_detections)
            score = min(1.0, score + (avg_confidence * 0.3))
        
        # Boost for organized directory structure
        if len(repo.directories) > 5:
            score = min(1.0, score + 0.1)
        
        return score
    
    def calculate_quality_score(
        self,
        repo: Repository,
        detections: List[DetectionResult],
    ) -> float:
        """Calculate quality score."""
        score = 0.5
        
        # Check for dependencies (indicates package management)
        if len(repo.dependencies) > 0:
            score = min(1.0, score + 0.2)
        
        # Check for testing
        if repo.has_tests:
            score = min(1.0, score + 0.2)
        
        return score
    
    def calculate_documentation_score(
        self,
        repo: Repository,
    ) -> float:
        """Calculate documentation score."""
        score = 0.3
        
        if repo.has_readme:
            score = min(1.0, score + 0.3)
        
        if repo.has_license:
            score = min(1.0, score + 0.2)
        
        # Check for docs directory
        has_docs = any("doc" in d.name.lower() for d in repo.directories)
        if has_docs:
            score = min(1.0, score + 0.2)
        
        return score
    
    def calculate_ai_maturity_score(
        self,
        detections: List[DetectionResult],
    ) -> float:
        """Calculate AI maturity score."""
        ai_detections = [d for d in detections if "AI" in d.detector_name]
        
        if not ai_detections:
            return 0.0
        
        max_confidence = max(d.confidence for d in ai_detections)
        count = len([d for d in ai_detections if d.detected])
        
        return min(1.0, (max_confidence * 0.6) + (count * 0.1))
    
    def calculate_production_readiness_score(
        self,
        repo: Repository,
    ) -> float:
        """Calculate production readiness score."""
        readiness = ProductionReadiness(
            has_cicd=repo.has_ci,
            has_testing=repo.has_tests,
            has_documentation=repo.has_readme,
            has_containerization=repo.has_docker,
        )
        return readiness.get_score() / 100.0
    
    def calculate_scores(
        self,
        repo: Repository,
        detections: List[DetectionResult],
    ) -> QualityScores:
        """Calculate all quality scores."""
        return QualityScores(
            architecture=self.calculate_architecture_score(repo, detections),
            quality=self.calculate_quality_score(repo, detections),
            maintainability=0.5,
            documentation=self.calculate_documentation_score(repo),
            ai_maturity=self.calculate_ai_maturity_score(detections),
            production_readiness=self.calculate_production_readiness_score(repo),
        )
