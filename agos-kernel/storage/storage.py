"""AGOS Storage."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class StorageType(Enum):
    """Storage type."""
    MEMORY = "memory"
    DISK = "disk"
    DATABASE = "database"
    CLOUD = "cloud"


class StorageStatus(Enum):
    """Storage status."""
    AVAILABLE = "available"
    FULL = "full"
    ERROR = "error"


@dataclass
class Storage:
    """A storage."""
    id: str
    name: str
    storage_type: StorageType
    path: str
    capacity: int = 0
    used: int = 0
    status: StorageStatus = StorageStatus.AVAILABLE
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def available(self) -> int:
        """Get available space."""
        return max(0, self.capacity - self.used)


class StorageManager:
    """
    Storage Manager.
    
    Manages storage operations.
    
    Usage:
        manager = StorageManager()
        manager.add_storage("cache", StorageType.DISK, "/tmp/agos-cache")
        manager.store("cache", "key", "value")
    """
    
    def __init__(self):
        """Initialize storage manager."""
        self._storages: Dict[str, Storage] = {}
        self._data: Dict[str, Dict[str, Any]] = {}
    
    def add_storage(
        self,
        name: str,
        storage_type: StorageType,
        path: str,
        capacity: int = 0,
    ) -> Storage:
        """Add a storage."""
        storage = Storage(
            id=f"storage-{uuid.uuid4().hex[:8]}",
            name=name,
            storage_type=storage_type,
            path=path,
            capacity=capacity,
        )
        self._storages[name] = storage
        self._data[name] = {}
        
        if storage_type == StorageType.DISK:
            Path(path).mkdir(parents=True, exist_ok=True)
        
        return storage
    
    def get_storage(self, name: str) -> Optional[Storage]:
        """Get a storage by name."""
        return self._storages.get(name)
    
    def store(self, storage_name: str, key: str, value: Any) -> bool:
        """Store a value."""
        if storage_name not in self._data:
            return False
        
        self._data[storage_name][key] = value
        
        storage = self._storages[storage_name]
        storage.used += 1
        
        return True
    
    def retrieve(self, storage_name: str, key: str) -> Optional[Any]:
        """Retrieve a value."""
        if storage_name not in self._data:
            return None
        return self._data[storage_name].get(key)
    
    def delete(self, storage_name: str, key: str) -> bool:
        """Delete a value."""
        if storage_name not in self._data:
            return False
        
        if key in self._data[storage_name]:
            del self._data[storage_name][key]
            storage = self._storages[storage_name]
            storage.used = max(0, storage.used - 1)
            return True
        return False
    
    def list_keys(self, storage_name: str) -> List[str]:
        """List all keys in a storage."""
        if storage_name not in self._data:
            return []
        return list(self._data[storage_name].keys())
    
    def clear(self, storage_name: str) -> bool:
        """Clear a storage."""
        if storage_name not in self._data:
            return False
        
        self._data[storage_name].clear()
        self._storages[storage_name].used = 0
        return True


_storage_manager: Optional[StorageManager] = None


def get_storage_manager() -> StorageManager:
    """Get the global storage manager."""
    global _storage_manager
    if _storage_manager is None:
        _storage_manager = StorageManager()
    return _storage_manager
