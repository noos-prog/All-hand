"""
CAPABILITY-000009: Architecture Extraction

PURPOSE: Extract architectural model.

VERSION: 1.0.0
"""
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class ArchitectureLayer:
    """An architectural layer."""
    name: str
    components: List[str] = field(default_factory=list)

@dataclass
class ArchitectureModel:
    """Extracted architecture model."""
    layers: List[ArchitectureLayer] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "layers": [{"name": l.name, "components": l.components} for l in self.layers],
            "patterns": self.patterns,
            "entry_points": self.entry_points,
            "extracted_at": self.extracted_at.isoformat(),
        }

class ArchitectureExtractionCapability:
    """
    CAPABILITY-000009: Architecture Extraction
    """
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000009"
    
    @property
    def name(self) -> str:
        return "ArchitectureExtraction"
    
    @property
    def description(self) -> str:
        return "Extracts architectural model"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> ArchitectureModel:
        """Execute architecture extraction."""
        path = input_data.get("path", "")
        if not path:
            raise ValueError("Path is required")
        
        # Detect architecture patterns
        patterns = self._detect_patterns(path)
        
        # Find entry points
        entry_points = self._find_entry_points(path)
        
        # Extract layers
        layers = self._extract_layers(path)
        
        return ArchitectureModel(
            layers=layers,
            patterns=patterns,
            entry_points=entry_points,
        )
    
    def _detect_patterns(self, path: str) -> List[str]:
        """Detect architectural patterns."""
        patterns = []
        
        # MVC
        if os.path.exists(os.path.join(path, "controllers")) or \
           os.path.exists(os.path.join(path, "views")):
            patterns.append("MVC")
        
        # Layered
        if os.path.exists(os.path.join(path, "layers")) or \
           os.path.exists(os.path.join(path, "core")):
            patterns.append("Layered")
        
        # Microservices
        if os.path.exists(os.path.join(path, "services")):
            patterns.append("Microservices")
        
        # Monolith
        if os.path.exists(os.path.join(path, "app")) and \
           os.path.exists(os.path.join(path, "app", "models")):
            patterns.append("Monolith")
        
        return patterns
    
    def _find_entry_points(self, path: str) -> List[str]:
        """Find application entry points."""
        entry_points = []
        
        candidates = [
            "main.py", "app.py", "index.py", "server.py",
            "src/main.py", "src/index.js", "app/main.go",
            "cmd/main.go", "bin/main"
        ]
        
        for root, dirs, files in os.walk(path):
            if ".git" in root:
                continue
            for f in files:
                if f in candidates:
                    entry_points.append(os.path.join(root, f))
        
        return entry_points
    
    def _extract_layers(self, path: str) -> List[ArchitectureLayer]:
        """Extract architectural layers."""
        layers = []
        
        # Common layer names
        layer_names = {
            "api": ["api", "controllers", "endpoints", "routes"],
            "service": ["services", "business", "domain", "logic"],
            "data": ["models", "entities", "schemas"],
            "repository": ["repositories", "dal", "data_access"],
            "infrastructure": ["infrastructure", "adapters", "providers"],
        }
        
        for layer_name, dir_names in layer_names.items():
            components = []
            for root, dirs, files in os.walk(path):
                if ".git" in root:
                    continue
                for d in dirs:
                    if any(ln in d.lower() for ln in dir_names):
                        components.append(os.path.join(root, d))
            
            if components:
                layers.append(ArchitectureLayer(
                    name=layer_name,
                    components=[os.path.relpath(c, path) for c in components[:10]]
                ))
        
        return layers
