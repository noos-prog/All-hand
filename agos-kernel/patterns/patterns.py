"""AGOS Design Patterns."""
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


class Singleton:
    """Singleton decorator."""
    
    _instances: Dict[type, Any] = {}
    
    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class Factory:
    """Factory pattern."""
    
    _registry: Dict[str, Callable] = {}
    
    @classmethod
    def register(cls, name: str, creator: Callable) -> None:
        """Register a creator."""
        cls._registry[name] = creator
    
    @classmethod
    def create(cls, name: str, *args, **kwargs) -> Any:
        """Create an instance."""
        if name not in cls._registry:
            raise ValueError(f"Unknown type: {name}")
        return cls._registry[name](*args, **kwargs)
    
    @classmethod
    def get_registry(cls) -> Dict[str, Callable]:
        """Get the registry."""
        return cls._registry


class Adapter:
    """Adapter pattern."""
    
    def __init__(self, adaptee: Any):
        """Initialize adapter."""
        self._adaptee = adaptee
    
    def __getattr__(self, name: str) -> Any:
        """Forward attribute access."""
        return getattr(self._adaptee, name)


class Strategy(ABC):
    """Strategy pattern base."""
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute the strategy."""
        pass


class StrategyContext:
    """Context for strategy pattern."""
    
    def __init__(self, strategy: Strategy):
        """Initialize context."""
        self._strategy = strategy
    
    def set_strategy(self, strategy: Strategy) -> None:
        """Set a new strategy."""
        self._strategy = strategy
    
    def execute_strategy(self, *args, **kwargs) -> Any:
        """Execute current strategy."""
        return self._strategy.execute(*args, **kwargs)


class Registry:
    """Generic registry pattern."""
    
    _items: Dict[str, Any] = {}
    
    @classmethod
    def register(cls, key: str, item: Any) -> None:
        """Register an item."""
        cls._items[key] = item
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Get an item."""
        return cls._items.get(key)
    
    @classmethod
    def unregister(cls, key: str) -> bool:
        """Unregister an item."""
        if key in cls._items:
            del cls._items[key]
            return True
        return False
    
    @classmethod
    def list_all(cls) -> Dict[str, Any]:
        """List all items."""
        return cls._items.copy()


def get_registry() -> Registry:
    """Get the registry instance."""
    return Registry
