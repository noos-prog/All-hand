"""Universal Resource Runtime."""
import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    Resource, ResourceType, ResourceStatus, ResourceAllocation, ResourceUsage, ResourceQuota
)


class ResourceRuntime:
    """Universal Resource Runtime."""
    
    def __init__(self):
        """Initialize resource runtime."""
        self.resources: Dict[str, Resource] = {}
        self.allocations: Dict[str, ResourceAllocation] = {}
    
    def create_resource(
        self,
        name: str,
        resource_type: ResourceType,
        capacity: float,
        unit: str = "",
    ) -> Resource:
        """Create a new resource."""
        resource_id = self._generate_id(name)
        
        resource = Resource(
            id=resource_id,
            name=name,
            resource_type=resource_type,
            capacity=capacity,
            unit=unit,
        )
        
        self.resources[resource_id] = resource
        return resource
    
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """Get resource by ID."""
        return self.resources.get(resource_id)
    
    def list_resources(
        self,
        resource_type: Optional[ResourceType] = None,
        status: Optional[ResourceStatus] = None,
    ) -> List[Resource]:
        """List resources with optional filtering."""
        resources = list(self.resources.values())
        
        if resource_type:
            resources = [r for r in resources if r.resource_type == resource_type]
        
        if status:
            resources = [r for r in resources if r.status == status]
        
        return resources
    
    def allocate(
        self,
        resource_id: str,
        amount: float,
        allocated_to: str,
    ) -> Optional[ResourceAllocation]:
        """Allocate resource to a consumer."""
        resource = self.resources.get(resource_id)
        if not resource:
            return None
        
        # Check availability
        if resource.available_capacity < amount:
            return None
        
        allocation = ResourceAllocation(
            id=self._generate_id(f"alloc-{allocated_to}"),
            resource_type=resource.resource_type,
            amount=amount,
            unit=resource.unit,
            allocated_at=datetime.now(),
            allocated_to=allocated_to,
        )
        
        resource.allocations.append(allocation)
        self.allocations[allocation.id] = allocation
        resource.updated_at = datetime.now()
        
        return allocation
    
    def release(self, allocation_id: str) -> bool:
        """Release an allocation."""
        allocation = self.allocations.get(allocation_id)
        if not allocation:
            return False
        
        # Find and update resource
        for resource in self.resources.values():
            if resource.resource_type == allocation.resource_type:
                for a in resource.allocations:
                    if a.id == allocation_id:
                        a.released_at = datetime.now()
                        resource.updated_at = datetime.now()
                        del self.allocations[allocation_id]
                        return True
        
        return False
    
    def monitor(self, resource_id: str, usage: ResourceUsage) -> bool:
        """Update resource usage monitoring."""
        resource = self.resources.get(resource_id)
        if not resource:
            return False
        
        resource.usage = usage
        resource.updated_at = datetime.now()
        
        # Update status based on usage
        if resource.utilization_percent >= 90:
            resource.status = ResourceStatus.EXHAUSTED
        elif resource.utilization_percent >= 70:
            resource.status = ResourceStatus.ALLOCATED
        
        return True
    
    def forecast(self, resource_id: str, hours: int = 24) -> Dict[str, Any]:
        """Forecast resource usage."""
        resource = self.resources.get(resource_id)
        if not resource:
            return {}
        
        # Simple linear forecast
        current_usage = resource.utilization_percent
        
        return {
            "resource_id": resource_id,
            "current_usage_percent": current_usage,
            "forecast_hours": hours,
            "predicted_peak_percent": min(current_usage + (hours * 0.5), 100),
            "days_until_exhaustion": (100 - current_usage) / (hours * 0.5) if hours > 0 else float('inf'),
        }
    
    def optimize(self, resource_id: str) -> Dict[str, Any]:
        """Suggest resource optimizations."""
        resource = self.resources.get(resource_id)
        if not resource:
            return {}
        
        suggestions = []
        
        if resource.utilization_percent < 30:
            suggestions.append({
                "type": "downscale",
                "message": f"Consider reducing {resource.name} capacity",
                "potential_savings": resource.capacity * 0.5,
            })
        
        if resource.utilization_percent > 80:
            suggestions.append({
                "type": "upscale",
                "message": f"Consider increasing {resource.name} capacity",
                "recommended_capacity": resource.capacity * 1.5,
            })
        
        return {
            "resource_id": resource_id,
            "current_utilization": resource.utilization_percent,
            "suggestions": suggestions,
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
