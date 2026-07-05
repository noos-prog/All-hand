"""
AGOS Resource Manager
====================

Manages system resources like CPU, memory, disk, and network.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ResourceType(Enum):
    """Resource type."""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    GPU = "gpu"
    STORAGE = "storage"


class ResourceStatus(Enum):
    """Resource status."""
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    RESERVED = "reserved"
    EXHAUSTED = "exhausted"


@dataclass
class Resource:
    """A system resource."""
    id: str
    name: str
    resource_type: ResourceType
    capacity: float
    used: float = 0.0
    unit: str = ""
    status: ResourceStatus = ResourceStatus.AVAILABLE
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def available(self) -> float:
        """Get available capacity."""
        return max(0, self.capacity - self.used)
    
    @property
    def utilization(self) -> float:
        """Get utilization percentage."""
        if self.capacity <= 0:
            return 0.0
        return (self.used / self.capacity) * 100


@dataclass
class ResourceAllocation:
    """Resource allocation record."""
    id: str
    resource_id: str
    requester_id: str
    amount: float
    allocated_at: datetime = field(default_factory=datetime.now)
    released_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ResourceManager:
    """
    Resource Manager.
    
    Manages system resources for workloads and tasks.
    
    Usage:
        manager = ResourceManager()
        
        manager.add_resource(
            name="cpu_cores",
            resource_type=ResourceType.CPU,
            capacity=8.0,
            unit="cores",
        )
        
        allocation = manager.allocate(
            resource_name="cpu_cores",
            requester_id="task-123",
            amount=2.0,
        )
        
        manager.release(allocation.id)
    """
    
    def __init__(self):
        """Initialize resource manager."""
        self._resources: Dict[str, Resource] = {}
        self._allocations: Dict[str, ResourceAllocation] = {}
    
    def add_resource(
        self,
        name: str,
        resource_type: ResourceType,
        capacity: float,
        unit: str = "",
    ) -> Resource:
        """Add a resource."""
        resource = Resource(
            id=f"res-{uuid.uuid4().hex[:8]}",
            name=name,
            resource_type=resource_type,
            capacity=capacity,
            unit=unit,
        )
        self._resources[name] = resource
        return resource
    
    def get_resource(self, name: str) -> Optional[Resource]:
        """Get a resource by name."""
        return self._resources.get(name)
    
    def allocate(
        self,
        resource_name: str,
        requester_id: str,
        amount: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[ResourceAllocation]:
        """Allocate resources."""
        resource = self._resources.get(resource_name)
        if not resource:
            return None
        
        if resource.available < amount:
            return None
        
        allocation = ResourceAllocation(
            id=f"alloc-{uuid.uuid4().hex[:8]}",
            resource_id=resource.id,
            requester_id=requester_id,
            amount=amount,
            metadata=metadata or {},
        )
        
        resource.used += amount
        resource.status = ResourceStatus.ALLOCATED if resource.available == 0 else ResourceStatus.AVAILABLE
        
        self._allocations[allocation.id] = allocation
        return allocation
    
    def release(self, allocation_id: str) -> bool:
        """Release an allocation."""
        allocation = self._allocations.get(allocation_id)
        if not allocation or allocation.released_at:
            return False
        
        resource = None
        for res in self._resources.values():
            if res.id == allocation.resource_id:
                resource = res
                break
        
        if resource:
            resource.used = max(0, resource.used - allocation.amount)
            resource.status = ResourceStatus.AVAILABLE if resource.used < resource.capacity else ResourceStatus.ALLOCATED
        
        allocation.released_at = datetime.now()
        return True
    
    def get_allocation(self, allocation_id: str) -> Optional[ResourceAllocation]:
        """Get an allocation by ID."""
        return self._allocations.get(allocation_id)
    
    def get_allocations_for(self, requester_id: str) -> List[ResourceAllocation]:
        """Get allocations for a requester."""
        return [
            a for a in self._allocations.values()
            if a.requester_id == requester_id and not a.released_at
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get resource statistics."""
        return {
            "total_resources": len(self._resources),
            "total_allocations": len(self._allocations),
            "active_allocations": sum(1 for a in self._allocations.values() if not a.released_at),
            "resources": {
                name: {
                    "capacity": r.capacity,
                    "used": r.used,
                    "available": r.available,
                    "utilization": r.utilization,
                    "status": r.status.value,
                }
                for name, r in self._resources.items()
            },
        }


# Global instance
_resource_manager: Optional[ResourceManager] = None


def get_resource_manager() -> ResourceManager:
    """Get the global resource manager."""
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager
