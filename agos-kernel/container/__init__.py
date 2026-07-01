"""Dependency Injection Container."""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type


class Lifetime(Enum):
    """Service lifetime."""
    SINGLETON = "singleton"      # One instance for the entire application
    SCOPED = "scoped"          # One instance per scope
    TRANSIENT = "transient"    # New instance each time


@dataclass
class ServiceRegistration:
    """Service registration."""
    service_type: Type
    implementation_type: Optional[Type] = None
    factory: Optional[Callable] = None
    lifetime: Lifetime = Lifetime.TRANSIENT
    instance: Optional[Any] = None


class Container:
    """
    Dependency Injection Container.
    
    Rules:
    - No manual dependency creation
    - No service locator usage
    - No hidden dependencies
    """
    
    def __init__(self):
        self._registrations: Dict[Type, ServiceRegistration] = {}
        self._singletons: Dict[Type, Any] = {}
    
    def register(
        self,
        service_type: Type,
        implementation: Optional[Type] = None,
        factory: Optional[Callable] = None,
        lifetime: Lifetime = Lifetime.TRANSIENT
    ) -> None:
        """Register a service."""
        reg = ServiceRegistration(
            service_type=service_type,
            implementation_type=implementation or service_type,
            factory=factory,
            lifetime=lifetime
        )
        self._registrations[service_type] = reg
    
    def register_instance(self, service_type: Type, instance: Any) -> None:
        """Register an existing instance as singleton."""
        self._registrations[service_type] = ServiceRegistration(
            service_type=service_type,
            implementation_type=type(instance),
            lifetime=Lifetime.SINGLETON,
            instance=instance
        )
        self._singletons[service_type] = instance
    
    def resolve(self, service_type: Type) -> Any:
        """Resolve a service."""
        reg = self._registrations.get(service_type)
        
        if reg is None:
            raise ValueError(f"Service not registered: {service_type}")
        
        # Singleton - return cached instance
        if reg.lifetime == Lifetime.SINGLETON:
            if service_type not in self._singletons:
                self._singletons[service_type] = self._create_instance(reg)
            return self._singletons[service_type]
        
        # Scoped - create new instance
        if reg.lifetime == Lifetime.SCOPED:
            return self._create_instance(reg)
        
        # Transient - always create new
        return self._create_instance(reg)
    
    def _create_instance(self, reg: ServiceRegistration) -> Any:
        """Create a new instance."""
        if reg.factory:
            return reg.factory()
        
        if reg.implementation_type:
            return reg.implementation_type()
        
        raise ValueError("Cannot create instance: no factory or implementation")
    
    def create_scope(self) -> 'ScopedContainer':
        """Create a scoped container."""
        return ScopedContainer(self)


class ScopedContainer:
    """Scoped container for scoped dependencies."""
    
    def __init__(self, parent: Container):
        self._parent = parent
        self._instances: Dict[Type, Any] = {}
    
    def resolve(self, service_type: Type) -> Any:
        """Resolve a service in this scope."""
        if service_type not in self._instances:
            reg = self._parent._registrations.get(service_type)
            if reg and reg.lifetime == Lifetime.SCOPED:
                self._instances[service_type] = self._parent._create_instance(reg)
            else:
                return self._parent.resolve(service_type)
        return self._instances[service_type]
    
    def dispose(self) -> None:
        """Dispose the scope."""
        self._instances.clear()


class ServiceResolver:
    """Resolves services from container."""
    
    def __init__(self, container: Container):
        self._container = container
    
    def resolve(self, service_type: Type) -> Any:
        """Resolve a service."""
        return self._container.resolve(service_type)
    
    def resolve_all(self, service_types: List[Type]) -> List[Any]:
        """Resolve multiple services."""
        return [self._container.resolve(st) for st in service_types]


class LifetimeManager:
    """Manages service lifetimes."""
    
    def __init__(self, container: Container):
        self._container = container
    
    def register_infrastructure(self, service_type: Type, implementation: Type) -> None:
        """Register infrastructure service as singleton."""
        self._container.register(
            service_type=service_type,
            implementation=implementation,
            lifetime=Lifetime.SINGLETON
        )
    
    def register_transient(self, service_type: Type, implementation: Type) -> None:
        """Register transient service."""
        self._container.register(
            service_type=service_type,
            implementation=implementation,
            lifetime=Lifetime.TRANSIENT
        )
    
    def register_scoped(self, service_type: Type, implementation: Type) -> None:
        """Register scoped service."""
        self._container.register(
            service_type=service_type,
            implementation=implementation,
            lifetime=Lifetime.SCOPED
        )
