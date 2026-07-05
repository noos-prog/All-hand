"""
AGOS Component Registry
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type
import threading

class ComponentStatus(Enum):
    REGISTERED = "registered"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    FAILED = "failed"

class ComponentType(Enum):
    RUNTIME = "runtime"
    ENGINE = "engine"
    CAPABILITY = "capability"
    PROVIDER = "provider"
    ADAPTER = "adapter"
    SKILL = "skill"
    WORKFLOW = "workflow"
    KNOWLEDGE = "knowledge"
    GOVERNANCE = "governance"

@dataclass
class Component:
    id: str
    name: str
    component_type: ComponentType
    version: str = "1.0.0"
    status: ComponentStatus = ComponentStatus.REGISTERED
    cls: Optional[Type] = None
    instance: Optional[Any] = None
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    activated_at: Optional[datetime] = None
    error: Optional[str] = None
    
    def activate(self) -> bool:
        try:
            if self.instance is None and self.cls is not None:
                self.instance = self.cls()
            if self.instance is not None:
                self.status = ComponentStatus.ACTIVE
                self.activated_at = datetime.utcnow()
                return True
            return False
        except Exception as e:
            self.status = ComponentStatus.FAILED
            self.error = str(e)
            return False
    
    def deactivate(self) -> bool:
        self.status = ComponentStatus.INACTIVE
        self.instance = None
        return True

_component_registry_instance = None
_component_registry_lock = threading.Lock()

class ComponentRegistry:
    def __init__(self):
        self._components: Dict[str, Component] = {}
        self._lock = threading.RLock()
    
    def register(self, cls: Type, name: Optional[str] = None,
                 component_id: Optional[str] = None,
                 component_type: Optional[ComponentType] = None,
                 version: str = "1.0.0",
                 dependencies: Optional[List[str]] = None,
                 metadata: Optional[Dict[str, Any]] = None) -> str:
        with self._lock:
            if component_id is None:
                component_id = cls.__name__.lower()
            if name is None:
                name = cls.__name__
            if component_id in self._components:
                return component_id
            component = Component(
                id=component_id, name=name,
                component_type=component_type or ComponentType.RUNTIME,
                version=version, cls=cls,
                dependencies=dependencies or [],
                metadata=metadata or {},
            )
            self._components[component_id] = component
            return component_id
    
    def unregister(self, component_id: str) -> bool:
        with self._lock:
            if component_id in self._components:
                del self._components[component_id]
                return True
            return False
    
    def get(self, component_id: str) -> Optional[Component]:
        return self._components.get(component_id)
    
    def list_all(self) -> List[Component]:
        return list(self._components.values())
    
    def list_active(self) -> List[Component]:
        return [c for c in self._components.values() if c.status == ComponentStatus.ACTIVE]
    
    def activate_all(self) -> Dict[str, bool]:
        results = {}
        activated = set()
        def sort_key(component: Component) -> tuple:
            score = len([d for d in component.dependencies if d not in activated])
            return (score, component.id)
        sorted_components = sorted(self._components.values(), key=sort_key)
        for component in sorted_components:
            deps_satisfied = all(d in activated for d in component.dependencies)
            if deps_satisfied:
                success = component.activate()
                results[component.id] = success
                if success:
                    activated.add(component.id)
            else:
                results[component.id] = False
        return results
    
    def deactivate_all(self) -> None:
        for component in self._components.values():
            component.deactivate()
    
    def check_health(self) -> Dict[str, Any]:
        return {
            "total": len(self._components),
            "active": len(self.list_active()),
            "failed": len([c for c in self._components.values() if c.status == ComponentStatus.FAILED]),
            "components": {c.id: c.status.value for c in self._components.values()},
        }

def get_component_registry() -> ComponentRegistry:
    global _component_registry_instance
    if _component_registry_instance is None:
        with _component_registry_lock:
            if _component_registry_instance is None:
                _component_registry_instance = ComponentRegistry()
    return _component_registry_instance
