"""AGOS Meta Repository - The single source of truth describing the entire AGOS civilization."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

REQUIRED_FIELDS = ["Unique ID", "Version", "Owner", "Lifecycle", "Dependencies", "Compatibility", "Status", "Metadata", "Tags", "Documentation", "Schema", "Validation Rules"]

META_SECTIONS = ["architecture", "contracts", "events", "domains", "capabilities", "providers", "skills", "missions", "workflows", "policies", "knowledge", "schemas", "benchmarks", "standards", "taxonomy", "ontology", "graphs", "registry"]

@dataclass
class MetaObject:
    """Every object in the Meta Repository must have these fields."""
    unique_id: str
    version: str
    owner: str
    lifecycle: str  # Draft, Experimental, Preview, Stable, Deprecated, Archived, Removed
    dependencies: List[str] = field(default_factory=list)
    compatibility: List[str] = field(default_factory=list)
    status: str = "active"
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    documentation: str = ""
    schema: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)

class MetaObjectValidator:
    """Validates that a MetaObject has all required fields."""
    def validate(self, obj: MetaObject) -> bool:
        for field_name in REQUIRED_FIELDS:
            if not hasattr(obj, field_name.lower().replace(" ", "_")):
                return False
        return True

class MetaRepository:
    """
    AGOS Meta Repository v1
    
    The Meta Repository becomes the single source of truth describing the entire AGOS civilization.
    The Meta Repository contains no business logic.
    It contains only metadata, schemas, graphs, manifests, contracts, policies and architectural knowledge.
    
    Sections:
    ✅ architecture, contracts, events, domains, capabilities
    ✅ providers, skills, missions, workflows, policies
    ✅ knowledge, schemas, benchmarks, standards, taxonomy
    ✅ ontology, graphs, registry
    
    Every Object Has:
    ✅ Unique ID, Version, Owner, Lifecycle, Dependencies
    ✅ Compatibility, Status, Metadata, Tags, Documentation
    ✅ Schema, Validation Rules
    """
    def __init__(self):
        self.version = "1.0.0"
        self._objects: Dict[str, MetaObject] = {}
        self.validator = MetaObjectValidator()
    
    def register(self, obj: MetaObject) -> bool:
        """Register a new meta object."""
        if self.validator.validate(obj):
            self._objects[obj.unique_id] = obj
            return True
        return False
    
    def get(self, unique_id: str) -> MetaObject:
        """Get a meta object by ID."""
        return self._objects.get(unique_id)
    
    def search(self, **filters) -> List[MetaObject]:
        """Search meta objects by filters."""
        results = []
        for obj in self._objects.values():
            match = True
            for key, value in filters.items():
                if hasattr(obj, key):
                    if getattr(obj, key) != value:
                        match = False
                        break
            if match:
                results.append(obj)
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get repository statistics."""
        return {
            "version": self.version,
            "total_objects": len(self._objects),
            "sections": META_SECTIONS,
            "required_fields": REQUIRED_FIELDS
        }
