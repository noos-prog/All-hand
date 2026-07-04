"""Universal Resource Runtime - Data Models."""
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
    TPU = "tpu"
    STORAGE = "storage"
    BANDWIDTH = "bandwidth"
    TOKENS = "tokens"
    API_QUOTA = "api_quota"
    TIME = "time"
    BUDGET = "budget"
    ENERGY = "energy"


class ResourceStatus(Enum):
    """Resource status."""
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    RESERVED = "reserved"
    EXHAUSTED = "exhausted"
    ERROR = "error"


@dataclass
class ResourceAllocation:
    """Resource allocation record."""
    id: str
    resource_type: ResourceType
    amount: float
    unit: str
    allocated_at: datetime
    allocated_to: str  # workspace_id or execution_id
    released_at: Optional[datetime] = None


@dataclass
class ResourceUsage:
    """Current resource usage."""
    timestamp: datetime = field(default_factory=datetime.now)
    cpu_percent: float = 0.0
    memory_mb: int = 0
    disk_mb: int = 0
    network_mbps: float = 0.0
    gpu_percent: float = 0.0


@dataclass
class ResourceQuota:
    """Resource quota."""
    resource_type: ResourceType
    limit: float
    used: float = 0.0
    unit: str = ""


@dataclass
class Resource:
    """Universal Resource."""
    id: str
    name: str
    resource_type: ResourceType
    
    # Capacity
    capacity: float
    unit: str
    
    # Status
    status: ResourceStatus = ResourceStatus.AVAILABLE
    
    # Usage
    usage: ResourceUsage = field(default_factory=ResourceUsage)
    
    # Quotas
    quotas: List[ResourceQuota] = field(default_factory=list)
    
    # Allocations
    allocations: List[ResourceAllocation] = field(default_factory=list)
    
    # Relationships
    workspace_id: Optional[str] = None
    environment_id: Optional[str] = None
    
    # Cost
    cost_per_unit: float = 0.0
    currency: str = "USD"
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def available_capacity(self) -> float:
        """Get available capacity."""
        allocated = sum(a.amount for a in self.allocations if a.released_at is None)
        return max(0, self.capacity - allocated)
    
    @property
    def utilization_percent(self) -> float:
        """Get utilization percentage."""
        if self.capacity == 0:
            return 0.0
        allocated = sum(a.amount for a in self.allocations if a.released_at is None)
        return (allocated / self.capacity) * 100
