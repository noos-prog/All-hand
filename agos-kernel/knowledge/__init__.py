"""Knowledge Interface - Kernel must never communicate directly with any database."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class Operation(Enum):
    """Knowledge operations."""
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    SEARCH = "search"
    EXISTS = "exists"


@dataclass
class KnowledgeQuery:
    """Query for knowledge operations."""
    collection: str
    id: Optional[str] = None
    filter: Optional[Dict[str, Any]] = None
    projection: Optional[List[str]] = None
    limit: int = 100
    offset: int = 0
    
    @classmethod
    def create(cls, collection: str, **kwargs) -> 'KnowledgeQuery':
        """Create a query."""
        return cls(collection=collection, **kwargs)


@dataclass
class KnowledgeResult:
    """Result of knowledge operation."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    operation: Operation = Operation.READ
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "operation": self.operation.value,
            "timestamp": self.timestamp.isoformat()
        }


class IKnowledgeProvider(ABC):
    """
    Knowledge Provider Interface.
    All knowledge providers must implement this interface.
    
    Rules:
    ❌ Kernel never communicates directly with database
    ✅ Storage agnostic
    ✅ Database independent
    ✅ Replaceable
    """
    
    @abstractmethod
    def read(self, query: KnowledgeQuery) -> KnowledgeResult:
        """Read data."""
        pass
    
    @abstractmethod
    def write(self, collection: str, data: Dict[str, Any]) -> KnowledgeResult:
        """Write data."""
        pass
    
    @abstractmethod
    def update(self, collection: str, id: str, data: Dict[str, Any]) -> KnowledgeResult:
        """Update data."""
        pass
    
    @abstractmethod
    def delete(self, collection: str, id: str) -> KnowledgeResult:
        """Delete data."""
        pass
    
    @abstractmethod
    def search(self, collection: str, query: str) -> KnowledgeResult:
        """Search data."""
        pass
    
    @abstractmethod
    def exists(self, collection: str, id: str) -> bool:
        """Check if data exists."""
        pass


class InMemoryKnowledgeProvider(IKnowledgeProvider):
    """
    In-memory knowledge provider for testing.
    """
    
    def __init__(self):
        self._store: Dict[str, Dict[str, Dict[str, Any]]] = {}
    
    def read(self, query: KnowledgeQuery) -> KnowledgeResult:
        """Read data."""
        try:
            collection = self._store.get(query.collection, {})
            
            if query.id:
                data = collection.get(query.id)
                if data is None:
                    return KnowledgeResult(success=False, data=None, error="Not found", operation=Operation.READ)
                return KnowledgeResult(success=True, data=data, operation=Operation.READ)
            
            # Return filtered results
            results = list(collection.values())
            
            if query.filter:
                results = [r for r in results if self._matches_filter(r, query.filter)]
            
            return KnowledgeResult(success=True, data=results, operation=Operation.READ)
            
        except Exception as e:
            return KnowledgeResult(success=False, error=str(e), operation=Operation.READ)
    
    def write(self, collection: str, data: Dict[str, Any]) -> KnowledgeResult:
        """Write data."""
        try:
            if collection not in self._store:
                self._store[collection] = {}
            
            id = data.get("id", str(uuid4()))
            data["id"] = id
            data["created_at"] = datetime.utcnow().isoformat()
            
            self._store[collection][id] = data
            return KnowledgeResult(success=True, data={"id": id}, operation=Operation.WRITE)
            
        except Exception as e:
            return KnowledgeResult(success=False, error=str(e), operation=Operation.WRITE)
    
    def update(self, collection: str, id: str, data: Dict[str, Any]) -> KnowledgeResult:
        """Update data."""
        try:
            if collection not in self._store or id not in self._store[collection]:
                return KnowledgeResult(success=False, error="Not found", operation=Operation.UPDATE)
            
            existing = self._store[collection][id]
            existing.update(data)
            existing["updated_at"] = datetime.utcnow().isoformat()
            
            return KnowledgeResult(success=True, data=existing, operation=Operation.UPDATE)
            
        except Exception as e:
            return KnowledgeResult(success=False, error=str(e), operation=Operation.UPDATE)
    
    def delete(self, collection: str, id: str) -> KnowledgeResult:
        """Delete data."""
        try:
            if collection in self._store and id in self._store[collection]:
                del self._store[collection][id]
                return KnowledgeResult(success=True, operation=Operation.DELETE)
            
            return KnowledgeResult(success=False, error="Not found", operation=Operation.DELETE)
            
        except Exception as e:
            return KnowledgeResult(success=False, error=str(e), operation=Operation.DELETE)
    
    def search(self, collection: str, query: str) -> KnowledgeResult:
        """Search data."""
        try:
            collection_data = self._store.get(collection, {})
            results = []
            
            for item in collection_data.values():
                # Simple text search
                text = json.dumps(item).lower()
                if query.lower() in text:
                    results.append(item)
            
            return KnowledgeResult(success=True, data=results, operation=Operation.SEARCH)
            
        except Exception as e:
            return KnowledgeResult(success=False, error=str(e), operation=Operation.SEARCH)
    
    def exists(self, collection: str, id: str) -> bool:
        """Check if data exists."""
        return collection in self._store and id in self._store[collection]
    
    def _matches_filter(self, data: Dict[str, Any], filter: Dict[str, Any]) -> bool:
        """Check if data matches filter."""
        for key, value in filter.items():
            if key not in data or data[key] != value:
                return False
        return True


class KnowledgeInterface:
    """
    Knowledge Interface.
    Provides unified access to knowledge operations.
    """
    
    def __init__(self, provider: IKnowledgeProvider):
        self._provider = provider
    
    def read(self, collection: str, id: str = None, **kwargs) -> KnowledgeResult:
        """Read data."""
        query = KnowledgeQuery(collection=collection, id=id, **kwargs)
        return self._provider.read(query)
    
    def write(self, collection: str, data: Dict[str, Any]) -> KnowledgeResult:
        """Write data."""
        return self._provider.write(collection, data)
    
    def update(self, collection: str, id: str, data: Dict[str, Any]) -> KnowledgeResult:
        """Update data."""
        return self._provider.update(collection, id, data)
    
    def delete(self, collection: str, id: str) -> KnowledgeResult:
        """Delete data."""
        return self._provider.delete(collection, id)
    
    def search(self, collection: str, query: str) -> KnowledgeResult:
        """Search data."""
        return self._provider.search(collection, query)
    
    def exists(self, collection: str, id: str) -> bool:
        """Check if data exists."""
        return self._provider.exists(collection, id)


import json  # Add for search
