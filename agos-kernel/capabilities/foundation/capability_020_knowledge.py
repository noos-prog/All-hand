"""
CAPABILITY-000020: Engineering Knowledge Extraction

PURPOSE: Extract and structure engineering knowledge from repository.

VERSION: 1.0.0
"""
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class EngineeringKnowledge:
    """Structured engineering knowledge."""
    patterns: List[str] = field(default_factory=list)
    practices: List[str] = field(default_factory=list)
    architecture: str = ""
    decisions: List[str] = field(default_factory=list)
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "patterns": self.patterns,
            "practices": self.practices,
            "architecture": self.architecture,
            "decisions": self.decisions,
            "extracted_at": self.extracted_at.isoformat(),
        }

class KnowledgeExtractionCapability:
    """
    CAPABILITY-000020: Engineering Knowledge Extraction
    """
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000020"
    
    @property
    def name(self) -> str:
        return "KnowledgeExtraction"
    
    @property
    def description(self) -> str:
        return "Extracts engineering knowledge from repository"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> EngineeringKnowledge:
        """Execute knowledge extraction."""
        path = input_data.get("path", "")
        if not path:
            raise ValueError("Path is required")
        
        patterns = []
        practices = []
        decisions = []
        architecture = "Unknown"
        
        # Extract patterns from code structure
        for root, dirs, files in os.walk(path):
            if ".git" in root:
                continue
            
            # Detect patterns from directory names
            dir_names = set(d.lower() for d in dirs)
            if {"controllers", "models", "views"} <= dir_names:
                patterns.append("MVC")
            if {"services", "repositories"} <= dir_names:
                patterns.append("Layered")
            if {"api", "endpoints"} <= dir_names:
                patterns.append("REST API")
            if {"handlers", "events"} <= dir_names:
                patterns.append("Event-Driven")
        
        # Extract practices from file patterns
        if any(f.endswith(".py") for f in os.listdir(path)):
            practices.append("Python")
        if any(f.endswith(".ts") or f.endswith(".tsx") for f in os.listdir(path)):
            practices.append("TypeScript")
        
        # Set architecture based on patterns
        if "MVC" in patterns:
            architecture = "MVC"
        elif "Layered" in patterns:
            architecture = "Layered"
        
        return EngineeringKnowledge(
            patterns=list(set(patterns)),
            practices=list(set(practices)),
            architecture=architecture,
            decisions=decisions,
        )
