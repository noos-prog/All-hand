"""Resource Allocator - Intelligent resource allocation."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class AllocationStrategy(Enum):
    """Resource allocation strategies."""
    FIRST_FIT = "first_fit"
    BEST_FIT = "best_fit"
    WORST_FIT = "worst_fit"
    RANDOM = "random"
    PRIORITY = "priority"
    FAIR_SHARE = "fair_share"


@dataclass
class ResourceNode:
    """A node in the resource pool."""
    node_id: str
    name: str
    capacity: float
    available: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourcePool:
    """A pool of homogeneous resources."""
    pool_id: str
    name: str
    resource_type: str
    nodes: List[ResourceNode] = field(default_factory=list)
    
    def get_total_capacity(self) -> float:
        return sum(n.capacity for n in self.nodes)
    
    def get_total_available(self) -> float:
        return sum(n.available for n in self.nodes)


@dataclass
class AllocationResult:
    """Result of an allocation attempt."""
    success: bool
    allocation_id: Optional[str] = None
    node_id: Optional[str] = None
    amount: float = 0.0
    error: Optional[str] = None


class ResourceAllocator:
    """Intelligent resource allocator."""
    
    def __init__(self):
        self.pools: Dict[str, ResourcePool] = {}
        self.allocations: Dict[str, Dict[str, Any]] = {}
        self.strategy: AllocationStrategy = AllocationStrategy.BEST_FIT
    
    def create_pool(
        self,
        name: str,
        resource_type: str,
        node_count: int = 1,
        capacity_per_node: float = 100.0,
    ) -> ResourcePool:
        nodes = [
            ResourceNode(
                node_id=str(uuid.uuid4()),
                name=f"{name}-node-{i}",
                capacity=capacity_per_node,
                available=capacity_per_node,
            )
            for i in range(node_count)
        ]
        
        pool = ResourcePool(
            pool_id=str(uuid.uuid4()),
            name=name,
            resource_type=resource_type,
            nodes=nodes,
        )
        
        self.pools[pool.pool_id] = pool
        return pool
    
    def allocate(
        self,
        pool_id: str,
        amount: float,
        requester: str,
    ) -> AllocationResult:
        pool = self.pools.get(pool_id)
        if not pool:
            return AllocationResult(
                success=False,
                error="Pool not found",
            )
        
        if pool.get_total_available() < amount:
            return AllocationResult(
                success=False,
                error="Insufficient resources",
            )
        
        # Find best node based on strategy
        node = self._select_node(pool, amount)
        if not node:
            return AllocationResult(
                success=False,
                error="No suitable node found",
            )
        
        # Allocate
        node.available -= amount
        
        allocation_id = str(uuid.uuid4())
        self.allocations[allocation_id] = {
            "pool_id": pool_id,
            "node_id": node.node_id,
            "amount": amount,
            "requester": requester,
            "allocated_at": datetime.utcnow().isoformat(),
        }
        
        return AllocationResult(
            success=True,
            allocation_id=allocation_id,
            node_id=node.node_id,
            amount=amount,
        )
    
    def release(self, allocation_id: str) -> bool:
        allocation = self.allocations.get(allocation_id)
        if not allocation:
            return False
        
        pool = self.pools.get(allocation["pool_id"])
        if pool:
            for node in pool.nodes:
                if node.node_id == allocation["node_id"]:
                    node.available += allocation["amount"]
                    break
        
        del self.allocations[allocation_id]
        return True
    
    def _select_node(
        self,
        pool: ResourcePool,
        amount: float,
    ) -> Optional[ResourceNode]:
        suitable = [n for n in pool.nodes if n.available >= amount]
        
        if not suitable:
            return None
        
        if self.strategy == AllocationStrategy.FIRST_FIT:
            return suitable[0]
        elif self.strategy == AllocationStrategy.BEST_FIT:
            return min(suitable, key=lambda n: n.available)
        elif self.strategy == AllocationStrategy.WORST_FIT:
            return max(suitable, key=lambda n: n.available)
        
        return suitable[0]
