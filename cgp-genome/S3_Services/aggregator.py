#!/usr/bin/env python3
"""
CGP - Service Aggregator
=======================

Services aggregated from capabilities.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class ServiceCategory(Enum):
    """Categories of services."""
    BACKEND = "backend"
    FRONTEND = "frontend"
    DEVOPS = "devops"
    QA = "qa"
    SECURITY = "security"
    DATA = "data"
    ML = "ml"
    MOBILE = "mobile"
    API = "api"


@dataclass
class ServiceMetrics:
    """Metrics for a service."""
    avg_duration_seconds: int = 3600
    avg_cost: float = 5.0
    success_rate: float = 0.85
    throughput_per_day: int = 10


@dataclass
class Service:
    """
    A service aggregated from capabilities.
    
    Example:
      Backend Development = API Design + Database Design + 
                            Code Generation + Testing + Deployment
    """
    service_id: str
    name: str
    category: ServiceCategory
    
    # Description
    description: str = ""
    
    # Composition
    required_capabilities: Tuple[str, ...] = ()
    optional_capabilities: Tuple[str, ...] = ()
    capability_order: Tuple[str, ...] = ()
    
    # Dependencies
    depends_on_services: Tuple[str, ...] = ()
    depended_by_services: Tuple[str, ...] = ()
    
    # Metrics
    metrics: ServiceMetrics = field(default_factory=ServiceMetrics)
    
    # SLA
    sla_uptime: float = 0.99
    sla_response_time_ms: int = 1000
    
    # Compliance
    compliance_requirements: Tuple[str, ...] = ()
    
    # Metadata
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: Tuple[str, ...] = ()
    
    def get_capability_count(self) -> int:
        """Get total number of capabilities."""
        return len(self.required_capabilities) + len(self.optional_capabilities)


class ServiceAggregator:
    """
    Aggregates capabilities into services.
    """
    
    def __init__(self, capability_registry=None):
        self.capability_registry = capability_registry
    
    def aggregate(
        self,
        service_id: str,
        name: str,
        category: ServiceCategory,
        capability_ids: List[str],
        required: List[str] = None,
        optional: List[str] = None
    ) -> Service:
        """Aggregate capabilities into a service."""
        service = Service(
            service_id=service_id,
            name=name,
            category=category,
            required_capabilities=tuple(required or capability_ids),
            optional_capabilities=tuple(optional or []),
            capability_order=tuple(capability_ids),
        )
        return service
    
    def decompose(self, service: Service) -> List[str]:
        """Get ordered list of capabilities."""
        return list(service.capability_order)


class ServiceRegistry:
    """
    Registry of all services.
    """
    
    def __init__(self):
        self._services: Dict[str, Service] = {}
        self._by_category: Dict[ServiceCategory, List[str]] = {}
    
    def register(self, service: Service) -> str:
        """Register a service."""
        self._services[service.service_id] = service
        
        if service.category not in self._by_category:
            self._by_category[service.category] = []
        self._by_category[service.category].append(service.service_id)
        
        return service.service_id
    
    def get(self, service_id: str) -> Optional[Service]:
        """Get a service by ID."""
        return self._services.get(service_id)
    
    def get_by_category(self, category: ServiceCategory) -> List[Service]:
        """Get all services in a category."""
        service_ids = self._by_category.get(category, [])
        return [self._services[sid] for sid in service_ids if sid in self._services]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        by_category = {cat.value: len(ids) for cat, ids in self._by_category.items()}
        
        return {
            "total_services": len(self._services),
            "by_category": by_category,
        }
