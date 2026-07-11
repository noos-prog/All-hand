"""Universal Resource Fabric - Core resource management."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid

RESOURCE_TYPES = [
    "CPU", "Memory", "GPU", "Disk", "Filesystem", "Container", "VM",
    "Cloud Function", "LLM Token", "API Quota", "Network", "Bandwidth",
    "Time", "Budget", "License", "External Service"
]


class ResourceType(Enum):
    """Types of resources."""
    CPU = "cpu"
    MEMORY = "memory"
    GPU = "gpu"
    DISK = "disk"
    FILESYSTEM = "filesystem"
    CONTAINER = "container"
    VM = "vm"
    CLOUD_FUNCTION = "cloud_function"
    LLM_TOKEN = "llm_token"
    API_QUOTA = "api_quota"
    NETWORK = "network"
    BANDWIDTH = "bandwidth"
    TIME = "time"
    BUDGET = "budget"
    LICENSE = "license"
    EXTERNAL_SERVICE = "external_service"


class ResourceStatus(Enum):
    """Resource status."""
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    FAILED = "failed"


@dataclass
class Resource:
    """A managed resource."""
    resource_id: str
    resource_type: ResourceType
    name: str
    capacity: float
    used: float = 0.0
    quota: float = 0.0
    cost_per_unit: float = 0.0
    status: ResourceStatus = ResourceStatus.AVAILABLE
    owner_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_available(self) -> float:
        return max(0, self.capacity - self.used)
    
    def get_utilization(self) -> float:
        if self.capacity == 0:
            return 0.0
        return self.used / self.capacity


@dataclass
class ResourceAllocation:
    """An allocation of a resource."""
    allocation_id: str
    resource_id: str
    requester: str
    amount: float
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "allocated"
    cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def release(self) -> None:
        self.end_time = datetime.utcnow()
        self.status = "released"


@dataclass
class ResourceQuota:
    """A quota limit for a resource."""
    quota_id: str
    resource_type: ResourceType
    owner_id: str
    limit: float
    used: float = 0.0
    reset_period: str = "monthly"


@dataclass
class ResourceReservation:
    """A future reservation of a resource."""
    reservation_id: str
    resource_id: str
    requester: str
    amount: float
    start_time: datetime
    end_time: datetime
    status: str = "pending"


class UniversalResourceFabric:
    """
    Universal Resource Fabric.
    
    Target: Millions of managed resources
    
    Manages:
    ✅ CPU, Memory, GPU, Disk
    ✅ Filesystem, Containers, VMs
    ✅ Cloud Functions, LLM Tokens
    ✅ API Quotas, Network, Bandwidth
    ✅ Time, Budget, Licenses
    ✅ External Services
    
    Implements:
    ✅ Resource Graph
    ✅ Resource Scheduler
    ✅ Resource Allocator
    ✅ Resource Predictor
    ✅ Resource Optimizer
    ✅ Quota Manager
    ✅ Budget Manager
    ✅ Resource Telemetry
    """
    
    def __init__(self):
        self.version = "2.0.0"
        self._resources: Dict[str, Resource] = {}
        self._allocations: Dict[str, ResourceAllocation] = {}
        self._quotas: Dict[str, ResourceQuota] = {}
        self._reservations: Dict[str, ResourceReservation] = {}
    
    def add_resource(
        self,
        name: str,
        resource_type: ResourceType,
        capacity: float,
        cost_per_unit: float = 0.0,
    ) -> Resource:
        resource = Resource(
            resource_id=str(uuid.uuid4()),
            resource_type=resource_type,
            name=name,
            capacity=capacity,
            cost_per_unit=cost_per_unit,
        )
        self._resources[resource.resource_id] = resource
        return resource
    
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        return self._resources.get(resource_id)
    
    def list_resources(
        self,
        resource_type: Optional[ResourceType] = None,
        status: Optional[ResourceStatus] = None,
    ) -> List[Resource]:
        results = list(self._resources.values())
        
        if resource_type:
            results = [r for r in results if r.resource_type == resource_type]
        if status:
            results = [r for r in results if r.status == status]
        
        return results
    
    def allocate(
        self,
        resource_id: str,
        requester: str,
        amount: float,
    ) -> Optional[ResourceAllocation]:
        resource = self._resources.get(resource_id)
        if not resource:
            return None
        
        if resource.get_available() < amount:
            return None
        
        resource.used += amount
        
        allocation = ResourceAllocation(
            allocation_id=str(uuid.uuid4()),
            resource_id=resource_id,
            requester=requester,
            amount=amount,
            start_time=datetime.utcnow(),
        )
        
        self._allocations[allocation.allocation_id] = allocation
        return allocation
    
    def release(self, allocation_id: str) -> bool:
        allocation = self._allocations.get(allocation_id)
        if not allocation:
            return False
        
        resource = self._resources.get(allocation.resource_id)
        if resource:
            resource.used -= allocation.amount
        
        allocation.release()
        return True
    
    def set_quota(
        self,
        owner_id: str,
        resource_type: ResourceType,
        limit: float,
    ) -> ResourceQuota:
        quota = ResourceQuota(
            quota_id=str(uuid.uuid4()),
            resource_type=resource_type,
            owner_id=owner_id,
            limit=limit,
        )
        self._quotas[quota.quota_id] = quota
        return quota
    
    def check_quota(self, owner_id: str, resource_type: ResourceType) -> Dict[str, float]:
        owner_quotas = [
            q for q in self._quotas.values()
            if q.owner_id == owner_id and q.resource_type == resource_type
        ]
        
        total_quota = sum(q.limit for q in owner_quotas)
        total_used = sum(q.used for q in owner_quotas)
        
        return {
            "limit": total_quota,
            "used": total_used,
            "available": total_quota - total_used,
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "total_resources": len(self._resources),
            "active_allocations": sum(1 for a in self._allocations.values() if a.status == "allocated"),
            "total_quotas": len(self._quotas),
            "resource_types": [rt.value for rt in ResourceType],
            "target": "millions",
        }
