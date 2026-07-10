#!/usr/bin/env python3
"""
CGP - Department Organizer
=========================

Departments organized from services.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class DepartmentDomain(Enum):
    """Domains of departments."""
    ENGINEERING = "engineering"
    OPERATIONS = "operations"
    QA = "qa"
    RESEARCH = "research"
    SECURITY = "security"
    DATA = "data"
    PRODUCT = "product"


@dataclass
class DepartmentMetrics:
    """Metrics for a department."""
    avg_throughput_per_day: int = 50
    avg_cost_per_mission: float = 50.0
    success_rate: float = 0.85
    team_size: int = 5


@dataclass
class Department:
    """
    A department containing services.
    
    Example:
      QA Department = Testing + Security + Performance + Reporting
    """
    department_id: str
    name: str
    domain: DepartmentDomain
    
    # Description
    description: str = ""
    
    # Composition
    required_services: Tuple[str, ...] = ()
    optional_services: Tuple[str, ...] = ()
    service_order: Tuple[str, ...] = ()
    
    # Organization
    head_capability: str = ""  # Main service/capability
    supporting_services: Tuple[str, ...] = ()
    
    # Metrics
    metrics: DepartmentMetrics = field(default_factory=DepartmentMetrics)
    
    # Collaboration
    collaborates_with: Tuple[str, ...] = ()  # Other department IDs
    
    # Metadata
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: Tuple[str, ...] = ()
    
    def get_service_count(self) -> int:
        """Get total number of services."""
        return len(self.required_services) + len(self.optional_services)


class DepartmentOrganizer:
    """
    Organizes services into departments.
    """
    
    def __init__(self, service_registry=None):
        self.service_registry = service_registry
    
    def organize(
        self,
        department_id: str,
        name: str,
        domain: DepartmentDomain,
        service_ids: List[str],
        required: List[str] = None,
        optional: List[str] = None
    ) -> Department:
        """Organize services into a department."""
        department = Department(
            department_id=department_id,
            name=name,
            domain=domain,
            required_services=tuple(required or service_ids),
            optional_services=tuple(optional or []),
            service_order=tuple(service_ids),
        )
        return department


class DepartmentRegistry:
    """
    Registry of all departments.
    """
    
    def __init__(self):
        self._departments: Dict[str, Department] = {}
        self._by_domain: Dict[DepartmentDomain, List[str]] = {}
    
    def register(self, department: Department) -> str:
        """Register a department."""
        self._departments[department.department_id] = department
        
        if department.domain not in self._by_domain:
            self._by_domain[department.domain] = []
        self._by_domain[department.domain].append(department.department_id)
        
        return department.department_id
    
    def get(self, department_id: str) -> Optional[Department]:
        """Get a department by ID."""
        return self._departments.get(department_id)
    
    def get_by_domain(self, domain: DepartmentDomain) -> List[Department]:
        """Get all departments in a domain."""
        dept_ids = self._by_domain.get(domain, [])
        return [self._departments[did] for did in dept_ids if did in self._departments]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        by_domain = {domain.value: len(ids) for domain, ids in self._by_domain.items()}
        
        return {
            "total_departments": len(self._departments),
            "by_domain": by_domain,
        }
