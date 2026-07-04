"""
Invariant Registry
EXECUTION-KERNEL-FINALIZATION-000002

Central registry for all kernel invariants.
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json


@dataclass
class InvariantDefinition:
    """Definition of a kernel invariant."""
    id: str
    name: str
    category: str
    rule: str
    severity: str  # critical, high, medium, low
    check_function: Optional[Callable] = None
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'rule': self.rule,
            'severity': self.severity,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat(),
        }
    
    @property
    def fingerprint(self) -> str:
        """Generate unique fingerprint for this invariant."""
        content = f"{self.id}:{self.name}:{self.rule}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


class InvariantRegistry:
    """
    Central registry for kernel invariants.
    
    Manages registration, lookup, and lifecycle of all invariants.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._invariants: Dict[str, InvariantDefinition] = {}
        self._categories: Dict[str, List[str]] = {}
        self._severity_levels = ['critical', 'high', 'medium', 'low']
    
    def register(self, invariant: InvariantDefinition) -> None:
        """Register a new invariant."""
        if invariant.id in self._invariants:
            raise ValueError(f"Invariant {invariant.id} already registered")
        
        self._invariants[invariant.id] = invariant
        
        if invariant.category not in self._categories:
            self._categories[invariant.category] = []
        self._categories[invariant.category].append(invariant.id)
    
    def unregister(self, invariant_id: str) -> bool:
        """Unregister an invariant."""
        if invariant_id not in self._invariants:
            return False
        
        invariant = self._invariants.pop(invariant_id)
        self._categories[invariant.category].remove(invariant_id)
        return True
    
    def get(self, invariant_id: str) -> Optional[InvariantDefinition]:
        """Get an invariant by ID."""
        return self._invariants.get(invariant_id)
    
    def get_by_category(self, category: str) -> List[InvariantDefinition]:
        """Get all invariants in a category."""
        ids = self._categories.get(category, [])
        return [self._invariants[i] for i in ids]
    
    def get_by_severity(self, severity: str) -> List[InvariantDefinition]:
        """Get all invariants of a severity level."""
        if severity not in self._severity_levels:
            return []
        return [i for i in self._invariants.values() if i.severity == severity]
    
    def get_enabled(self) -> List[InvariantDefinition]:
        """Get all enabled invariants."""
        return [i for i in self._invariants.values() if i.enabled]
    
    def get_all(self) -> List[InvariantDefinition]:
        """Get all registered invariants."""
        return list(self._invariants.values())
    
    def enable(self, invariant_id: str) -> bool:
        """Enable an invariant."""
        if invariant_id not in self._invariants:
            return False
        self._invariants[invariant_id].enabled = True
        return True
    
    def disable(self, invariant_id: str) -> bool:
        """Disable an invariant."""
        if invariant_id not in self._invariants:
            return False
        self._invariants[invariant_id].enabled = False
        return True
    
    @property
    def count(self) -> int:
        """Total number of registered invariants."""
        return len(self._invariants)
    
    @property
    def categories(self) -> List[str]:
        """List all invariant categories."""
        return list(self._categories.keys())
    
    def export_manifest(self) -> Dict:
        """Export registry as manifest."""
        return {
            'total_invariants': self.count,
            'categories': {cat: len(ids) for cat, ids in self._categories.items()},
            'severity_breakdown': {
                sev: len(self.get_by_severity(sev))
                for sev in self._severity_levels
            },
            'invariants': [i.to_dict() for i in self.get_all()],
        }
    
    def get_fingerprint(self) -> str:
        """Generate fingerprint of entire registry state."""
        content = json.dumps(
            {k: v.to_dict() for k, v in self._invariants.items()},
            sort_keys=True
        )
        return hashlib.sha256(content.encode()).hexdigest()


# Global registry instance
_registry = InvariantRegistry()


def get_registry() -> InvariantRegistry:
    """Get the global invariant registry."""
    return _registry
