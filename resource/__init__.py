"""AGOS Universal Resource Fabric - Millions of managed resources."""
from .fabric import (
    UniversalResourceFabric, Resource, ResourceType, ResourceStatus,
    ResourceAllocation, ResourceQuota, ResourceReservation
)
from .allocator import (
    ResourceAllocator, AllocationStrategy, AllocationResult,
    ResourcePool, ResourceNode
)
from .scheduler import (
    ResourceScheduler, SchedulePolicy, ScheduleResult,
    ResourceRequest, TimeSlot
)
from .quota import (
    QuotaManager, QuotaLimit, QuotaUsage, QuotaPolicy
)
from .budget import (
    BudgetManager, Budget, BudgetAllocation, CostTracker
)

__all__ = [
    "UniversalResourceFabric", "Resource", "ResourceType", "ResourceStatus",
    "ResourceAllocation", "ResourceQuota", "ResourceReservation",
    "ResourceAllocator", "AllocationStrategy", "AllocationResult",
    "ResourcePool", "ResourceNode",
    "ResourceScheduler", "SchedulePolicy", "ScheduleResult",
    "ResourceRequest", "TimeSlot",
    "QuotaManager", "QuotaLimit", "QuotaUsage", "QuotaPolicy",
    "BudgetManager", "Budget", "BudgetAllocation", "CostTracker",
]

__version__ = "2.0.0"
