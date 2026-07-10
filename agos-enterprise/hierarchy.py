#!/usr/bin/env python3
"""
AGOS Enterprise - Hierarchy Module
==================================

Implements the 4-layer hierarchy:
1. Skill (Smallest Unit) - Atomic function
2. Capability (Multiple Skills) - Combined skills
3. Service (Multiple Capabilities) - Complete solutions
4. Department (Multiple Services) - Organizational units

The hierarchy is the backbone of enterprise-scale orchestration.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from datetime import datetime
import hashlib
import json


class HierarchyLevel(Enum):
    """Levels in the enterprise hierarchy."""
    SKILL = "skill"
    CAPABILITY = "capability"
    SERVICE = "service"
    DEPARTMENT = "department"
    CEO = "ceo"  # Core Brain


class SkillType(Enum):
    """Types of atomic skills."""
    PARSE = "parse"
    FORMAT = "format"
    VALIDATE = "validate"
    EXECUTE = "execute"
    REPORT = "report"
    ANALYZE = "analyze"
    GENERATE = "generate"
    TRANSFORM = "transform"
    STORE = "store"
    RETRIEVE = "retrieve"


class ExecutionStatus(Enum):
    """Status of execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Skill:
    """
    Smallest unit in the hierarchy.
    An atomic function that cannot be broken down further.
    
    Examples:
    - Parse JSON
    - Create File
    - Read Git Diff
    - Format Code
    - Validate Syntax
    """
    skill_id: str                       # Unique identifier
    name: str                           # Human-readable name
    description: str                     # What this skill does
    skill_type: SkillType               # Type of skill
    input_schema: str                   # JSON schema for input
    output_schema: str                  # JSON schema for output
    timeout_ms: int = 5000              # Max execution time
    version: str = "1.0"               # Skill version
    tags: Tuple[str, ...] = ()         # Metadata tags
    is_stateless: bool = True           # Whether skill maintains state
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute this skill with input data.
        Returns output data conforming to output_schema.
        """
        # Placeholder - actual execution done by provider
        return {
            "skill_id": self.skill_id,
            "executed": True,
            "input": input_data,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data against schema."""
        # Simple validation - in production would use JSON Schema
        if not isinstance(input_data, dict):
            return False, "Input must be a dictionary"
        return True, None
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "skill_id": self.skill_id,
            "name": self.name,
            "version": self.version,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]


@dataclass
class SkillExecution:
    """Record of skill execution."""
    execution_id: str
    skill_id: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    status: ExecutionStatus = ExecutionStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    duration_ms: int = 0


@dataclass
class Capability:
    """
    A combination of multiple Skills.
    Solves a complete problem by composing skills.
    
    Examples:
    - Code Review (parse + analyze + format + report)
    - Bug Fix (detect + locate + modify + test)
    - API Generation (scaffold + model + route + document)
    """
    capability_id: str                  # Unique identifier
    name: str                           # Human-readable name
    description: str                    # What this capability does
    skills: Tuple[Skill, ...]          # Skills composing this capability
    required_capabilities: Tuple[str, ...] = ()  # Other capabilities needed
    version: str = "1.0"
    tags: Tuple[str, ...] = ()
    estimated_duration_ms: int = 60000   # Estimated execution time
    success_rate: float = 0.95          # Historical success rate
    
    def __post_init__(self):
        """Validate capability composition."""
        if not self.skills:
            raise ValueError(f"Capability {self.capability_id} must have at least one skill")
        
        # Validate skill dependencies
        skill_ids = {s.skill_id for s in self.skills}
        for req in self.required_capabilities:
            if req not in skill_ids:
                pass  # External dependencies allowed
    
    def get_skill_by_type(self, skill_type: SkillType) -> Optional[Skill]:
        """Get a skill of specific type."""
        for skill in self.skills:
            if skill.skill_type == skill_type:
                return skill
        return None
    
    def get_execution_order(self) -> List[Skill]:
        """Get skills in execution order based on dependencies."""
        # Simple ordering - in production would use dependency graph
        return list(self.skills)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute capability by running skills in order.
        """
        context = {"input": input_data, "intermediate": {}}
        execution_log = []
        
        for skill in self.get_execution_order():
            try:
                # Validate input for this skill
                valid, error = skill.validate_input(context["intermediate"])
                if not valid:
                    raise ValueError(f"Skill {skill.skill_id} validation failed: {error}")
                
                # Execute skill
                result = skill.execute(context["intermediate"])
                context["intermediate"][skill.skill_id] = result
                execution_log.append({
                    "skill_id": skill.skill_id,
                    "status": "success",
                    "timestamp": datetime.utcnow().isoformat(),
                })
                
            except Exception as e:
                execution_log.append({
                    "skill_id": skill.skill_id,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                })
                raise
        
        return {
            "capability_id": self.capability_id,
            "success": True,
            "output": context["intermediate"],
            "execution_log": execution_log,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "capability_id": self.capability_id,
            "name": self.name,
            "skills": [s.skill_id for s in self.skills],
            "version": self.version,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]


@dataclass
class Service:
    """
    A combination of multiple Capabilities.
    Solves a complete business problem.
    
    Examples:
    - Backend Development
    - Security Audit
    - Testing Service
    """
    service_id: str                     # Unique identifier
    name: str                           # Human-readable name
    description: str                    # What this service does
    capabilities: Tuple[Capability, ...] # Capabilities in this service
    department_id: str                   # Parent department
    version: str = "1.0"
    tags: Tuple[str, ...] = ()
    service_level: str = "standard"     # standard, premium, enterprise
    endpoints: Tuple[str, ...] = ()     # API endpoints
    
    def __post_init__(self):
        """Validate service composition."""
        if not self.capabilities:
            raise ValueError(f"Service {self.service_id} must have at least one capability")
    
    def get_capability(self, capability_id: str) -> Optional[Capability]:
        """Get a specific capability."""
        for cap in self.capabilities:
            if cap.capability_id == capability_id:
                return cap
        return None
    
    def get_all_skills(self) -> List[Skill]:
        """Get all skills from all capabilities."""
        skills = []
        for cap in self.capabilities:
            skills.extend(cap.skills)
        return skills
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get service health status."""
        return {
            "service_id": self.service_id,
            "name": self.name,
            "capabilities_count": len(self.capabilities),
            "skills_count": len(self.get_all_skills()),
            "status": "healthy",
            "version": self.version,
        }
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "service_id": self.service_id,
            "name": self.name,
            "capabilities": [c.capability_id for c in self.capabilities],
            "department_id": self.department_id,
            "version": self.version,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]


@dataclass
class Department:
    """
    Top-level organizational unit.
    Contains multiple Services.
    
    Examples:
    - QA Department
    - DevOps Department
    - Research Department
    """
    department_id: str                   # Unique identifier
    name: str                           # Human-readable name
    description: str                    # What this department does
    services: Tuple[Service, ...]      # Services in this department
    parent_department_id: Optional[str] = None  # For nested departments
    version: str = "1.0"
    tags: Tuple[str, ...] = ()
    budget_allocation: float = 0.0     # Budget for this department
    priority: int = 1                  # Department priority (1=highest)
    
    def __post_init__(self):
        """Validate department composition."""
        if not self.services:
            raise ValueError(f"Department {self.department_id} must have at least one service")
    
    def get_service(self, service_id: str) -> Optional[Service]:
        """Get a specific service."""
        for service in self.services:
            if service.service_id == service_id:
                return service
        return None
    
    def get_all_capabilities(self) -> List[Capability]:
        """Get all capabilities from all services."""
        capabilities = []
        for service in self.services:
            capabilities.extend(service.capabilities)
        return capabilities
    
    def get_all_skills(self) -> List[Skill]:
        """Get all skills from all capabilities."""
        skills = []
        for service in self.services:
            skills.extend(service.get_all_skills())
        return skills
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get department statistics."""
        capabilities = self.get_all_capabilities()
        skills = self.get_all_skills()
        
        return {
            "department_id": self.department_id,
            "name": self.name,
            "services_count": len(self.services),
            "capabilities_count": len(capabilities),
            "skills_count": len(skills),
            "budget_allocation": self.budget_allocation,
            "priority": self.priority,
            "version": self.version,
        }
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "department_id": self.department_id,
            "name": self.name,
            "services": [s.service_id for s in self.services],
            "parent": self.parent_department_id,
            "version": self.version,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]


class EnterpriseHierarchy:
    """
    Manages the complete enterprise hierarchy.
    Provides access to all levels of the organization.
    """
    
    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._capabilities: Dict[str, Capability] = {}
        self._services: Dict[str, Service] = {}
        self._departments: Dict[str, Department] = {}
        self._initialized = False
    
    def register_skill(self, skill: Skill) -> None:
        """Register a skill."""
        self._skills[skill.skill_id] = skill
        self._initialized = False
    
    def register_capability(self, capability: Capability) -> None:
        """Register a capability."""
        self._capabilities[capability.capability_id] = capability
        self._initialized = False
    
    def register_service(self, service: Service) -> None:
        """Register a service."""
        self._services[service.service_id] = service
        self._initialized = False
    
    def register_department(self, department: Department) -> None:
        """Register a department."""
        self._departments[department.department_id] = department
        self._initialized = False
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID."""
        return self._skills.get(skill_id)
    
    def get_capability(self, capability_id: str) -> Optional[Capability]:
        """Get a capability by ID."""
        return self._capabilities.get(capability_id)
    
    def get_service(self, service_id: str) -> Optional[Service]:
        """Get a service by ID."""
        return self._services.get(service_id)
    
    def get_department(self, department_id: str) -> Optional[Department]:
        """Get a department by ID."""
        return self._departments.get(department_id)
    
    def find_capabilities_by_tag(self, tag: str) -> List[Capability]:
        """Find capabilities with a specific tag."""
        return [
            cap for cap in self._capabilities.values()
            if tag in cap.tags
        ]
    
    def find_services_by_capability(self, capability_id: str) -> List[Service]:
        """Find services that provide a specific capability."""
        return [
            svc for svc in self._services.values()
            if any(c.capability_id == capability_id for c in svc.capabilities)
        ]
    
    def get_path_to_capability(self, capability_id: str) -> Optional[Dict[str, Any]]:
        """Get the full path from department to capability."""
        for dept in self._departments.values():
            for svc in dept.services:
                for cap in svc.capabilities:
                    if cap.capability_id == capability_id:
                        return {
                            "department": {
                                "id": dept.department_id,
                                "name": dept.name,
                            },
                            "service": {
                                "id": svc.service_id,
                                "name": svc.name,
                            },
                            "capability": {
                                "id": cap.capability_id,
                                "name": cap.name,
                            },
                            "skills": [
                                {"id": s.skill_id, "name": s.name, "type": s.skill_type.value}
                                for s in cap.skills
                            ],
                        }
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get hierarchy statistics."""
        all_skills = []
        all_caps = []
        for dept in self._departments.values():
            all_skills.extend(dept.get_all_skills())
            all_caps.extend(dept.get_all_capabilities())
        
        return {
            "departments": len(self._departments),
            "services": len(self._services),
            "capabilities": len(all_caps),
            "skills": len(all_skills),
            "registered_skills": len(self._skills),
            "registered_capabilities": len(self._capabilities),
        }
    
    def compute_hash(self) -> str:
        """Compute deterministic hash of entire hierarchy."""
        data = {
            "departments": [d.compute_hash() for d in self._departments.values()],
            "services": [s.compute_hash() for s in self._services.values()],
            "capabilities": [c.compute_hash() for c in self._capabilities.values()],
            "skills": [s.compute_hash() for s in self._skills.values()],
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]
