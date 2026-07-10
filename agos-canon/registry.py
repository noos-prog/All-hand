#!/usr/bin/env python3
"""
AGOS Canon - Registry
=====================

Central registry for tracking canon and constitutional compliance.
Maintains history of all validations and violations.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timedelta
import json
import hashlib
import threading


class RegistryStatus(Enum):
    """Status of a registered component."""
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    VIOLATION = "violation"
    UNKNOWN = "unknown"


@dataclass
class ComponentRecord:
    """Record of a component in the registry."""
    component_id: str                    # Unique identifier
    component_type: str                  # Type (module, contract, etc.)
    name: str                            # Human-readable name
    version: str                         # Current version
    status: RegistryStatus               # Compliance status
    last_validated: datetime             # Last validation time
    last_hash: str                      # Hash at last validation
    violation_count: int = 0            # Number of active violations
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def needs_revalidation(self, max_age_hours: int = 24) -> bool:
        """Check if component needs revalidation."""
        age = datetime.utcnow() - self.last_validated
        return age > timedelta(hours=max_age_hours)
    
    def is_stale(self, max_age_days: int = 7) -> bool:
        """Check if record is stale."""
        age = datetime.utcnow() - self.last_validated
        return age > timedelta(days=max_age_days)


@dataclass
class ViolationRecord:
    """Record of a violation in the registry."""
    violation_id: str                    # Unique violation ID
    component_id: str                    # Component this violation belongs to
    rule_id: str                         # Canon or Article ID
    severity: str                        # critical, high, medium, low
    description: str                      # Violation description
    first_seen: datetime                 # First time violation seen
    last_seen: datetime                 # Last time violation seen
    occurrence_count: int = 1           # How many times seen
    auto_fixed: bool = False             # Whether this was auto-fixed
    waived: bool = False                 # Whether this was waived
    waiver_reason: Optional[str] = None # Reason for waiver
    
    def acknowledge(self) -> None:
        """Mark violation as seen again."""
        self.last_seen = datetime.utcnow()
        self.occurrence_count += 1


class CanonRegistry:
    """
    Central registry for AGOS canon and constitution compliance.
    
    Tracks:
    - All registered components
    - All violations (historical and current)
    - Validation history
    - Waiver requests
    """
    
    _instance: Optional['CanonRegistry'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'CanonRegistry':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize registry state."""
        self._components: Dict[str, ComponentRecord] = {}
        self._violations: Dict[str, ViolationRecord] = {}
        self._validation_history: List[Dict[str, Any]] = []
        self._lock_internal = threading.RLock()
        self._initialized = True
    
    # ============ COMPONENT MANAGEMENT ============
    
    def register_component(
        self,
        component_id: str,
        component_type: str,
        name: str,
        version: str = "1.0",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ComponentRecord:
        """
        Register a new component in the registry.
        
        If component already exists, updates its info.
        """
        with self._lock_internal:
            if component_id in self._components:
                record = self._components[component_id]
                record.name = name
                record.version = version
                record.metadata.update(metadata or {})
                return record
            
            record = ComponentRecord(
                component_id=component_id,
                component_type=component_type,
                name=name,
                version=version,
                status=RegistryStatus.UNKNOWN,
                last_validated=datetime.utcnow(),
                last_hash="",
                metadata=metadata or {},
            )
            self._components[component_id] = record
            return record
    
    def unregister_component(self, component_id: str) -> bool:
        """Remove a component from the registry."""
        with self._lock_internal:
            if component_id in self._components:
                del self._components[component_id]
                # Also remove related violations
                to_remove = [
                    vid for vid, v in self._violations.items()
                    if v.component_id == component_id
                ]
                for vid in to_remove:
                    del self._violations[vid]
                return True
            return False
    
    def get_component(self, component_id: str) -> Optional[ComponentRecord]:
        """Get a component record."""
        return self._components.get(component_id)
    
    def list_components(
        self,
        component_type: Optional[str] = None,
        status: Optional[RegistryStatus] = None,
    ) -> List[ComponentRecord]:
        """List components with optional filtering."""
        with self._lock_internal:
            results = list(self._components.values())
            
            if component_type:
                results = [r for r in results if r.component_type == component_type]
            
            if status:
                results = [r for r in results if r.status == status]
            
            return results
    
    def get_components_needing_revalidation(self, max_age_hours: int = 24) -> List[ComponentRecord]:
        """Get components that need revalidation."""
        return [
            r for r in self._components.values()
            if r.needs_revalidation(max_age_hours)
        ]
    
    # ============ VIOLATION MANAGEMENT ============
    
    def record_violation(
        self,
        violation_id: str,
        component_id: str,
        rule_id: str,
        severity: str,
        description: str,
    ) -> ViolationRecord:
        """Record a new violation or update existing."""
        with self._lock_internal:
            if violation_id in self._violations:
                record = self._violations[violation_id]
                record.acknowledge()
                return record
            
            record = ViolationRecord(
                violation_id=violation_id,
                component_id=component_id,
                rule_id=rule_id,
                severity=severity,
                description=description,
                first_seen=datetime.utcnow(),
                last_seen=datetime.utcnow(),
            )
            self._violations[violation_id] = record
            
            # Update component violation count
            if component_id in self._components:
                self._components[component_id].violation_count += 1
            
            return record
    
    def waive_violation(self, violation_id: str, reason: str) -> bool:
        """Waive a violation with justification."""
        with self._lock_internal:
            if violation_id not in self._violations:
                return False
            
            record = self._violations[violation_id]
            record.waived = True
            record.waiver_reason = reason
            return True
    
    def get_violations(
        self,
        component_id: Optional[str] = None,
        rule_id: Optional[str] = None,
        severity: Optional[str] = None,
        include_waived: bool = False,
    ) -> List[ViolationRecord]:
        """Get violations with optional filtering."""
        with self._lock_internal:
            results = list(self._violations.values())
            
            if component_id:
                results = [v for v in results if v.component_id == component_id]
            
            if rule_id:
                results = [v for v in results if v.rule_id == rule_id]
            
            if severity:
                results = [v for v in results if v.severity == severity]
            
            if not include_waived:
                results = [v for v in results if not v.waived]
            
            return results
    
    def get_active_violations(self) -> List[ViolationRecord]:
        """Get all active (non-waived) violations."""
        return self.get_violations(include_waived=False)
    
    def get_critical_violations(self) -> List[ViolationRecord]:
        """Get all critical violations."""
        return self.get_violations(severity="critical")
    
    # ============ VALIDATION RECORDING ============
    
    def record_validation(
        self,
        component_id: str,
        is_compliant: bool,
        violation_count: int,
        hash: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record a validation result."""
        with self._lock_internal:
            # Update component record
            if component_id in self._components:
                record = self._components[component_id]
                record.last_validated = datetime.utcnow()
                record.last_hash = hash
                
                if violation_count == 0:
                    record.status = RegistryStatus.COMPLIANT
                elif violation_count <= 3:
                    record.status = RegistryStatus.PARTIAL
                else:
                    record.status = RegistryStatus.VIOLATION
            
            # Add to history
            entry = {
                "component_id": component_id,
                "timestamp": datetime.utcnow().isoformat(),
                "is_compliant": is_compliant,
                "violation_count": violation_count,
                "hash": hash,
                "metadata": metadata or {},
            }
            self._validation_history.append(entry)
            
            # Trim history if too long
            if len(self._validation_history) > 10000:
                self._validation_history = self._validation_history[-5000:]
    
    def get_validation_history(
        self,
        component_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get validation history."""
        with self._lock_internal:
            history = self._validation_history
            
            if component_id:
                history = [h for h in history if h["component_id"] == component_id]
            
            return history[-limit:]
    
    # ============ STATISTICS ============
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        with self._lock_internal:
            components = list(self._components.values())
            violations = [v for v in self._violations.values() if not v.waived]
            
            status_counts = {}
            for c in components:
                status_counts[c.status.value] = status_counts.get(c.status.value, 0) + 1
            
            severity_counts = {}
            for v in violations:
                severity_counts[v.severity] = severity_counts.get(v.severity, 0) + 1
            
            return {
                "total_components": len(components),
                "total_violations": len(violations),
                "components_by_status": status_counts,
                "violations_by_severity": severity_counts,
                "validation_history_entries": len(self._validation_history),
                "components_needing_revalidation": len(self.get_components_needing_revalidation()),
                "critical_violations": len(self.get_critical_violations()),
            }
    
    def get_compliance_score(self) -> float:
        """
        Calculate overall compliance score (0-100).
        
        100 = all components fully compliant
        0 = system non-functional due to critical violations
        """
        with self._lock_internal:
            if not self._components:
                return 100.0
            
            critical_violations = len(self.get_critical_violations())
            if critical_violations > 0:
                return 0.0
            
            components = list(self._components.values())
            compliant_count = sum(
                1 for c in components if c.status == RegistryStatus.COMPLIANT
            )
            partial_count = sum(
                1 for c in components if c.status == RegistryStatus.PARTIAL
            )
            
            total = len(components)
            if total == 0:
                return 100.0
            
            # 100% for compliant, 50% for partial, 0% for violation
            score = (compliant_count * 100 + partial_count * 50) / total
            return round(score, 2)
    
    # ============ EXPORT/IMPORT ============
    
    def export_state(self) -> Dict[str, Any]:
        """Export registry state for persistence."""
        with self._lock_internal:
            return {
                "version": "1.0",
                "exported_at": datetime.utcnow().isoformat(),
                "components": {
                    cid: {
                        "component_id": r.component_id,
                        "component_type": r.component_type,
                        "name": r.name,
                        "version": r.version,
                        "status": r.status.value,
                        "last_validated": r.last_validated.isoformat(),
                        "last_hash": r.last_hash,
                        "violation_count": r.violation_count,
                        "metadata": r.metadata,
                    }
                    for cid, r in self._components.items()
                },
                "violations": {
                    vid: {
                        "violation_id": v.violation_id,
                        "component_id": v.component_id,
                        "rule_id": v.rule_id,
                        "severity": v.severity,
                        "description": v.description,
                        "first_seen": v.first_seen.isoformat(),
                        "last_seen": v.last_seen.isoformat(),
                        "occurrence_count": v.occurrence_count,
                        "auto_fixed": v.auto_fixed,
                        "waived": v.waived,
                        "waiver_reason": v.waiver_reason,
                    }
                    for vid, v in self._violations.items()
                },
            }
    
    def import_state(self, state: Dict[str, Any]) -> None:
        """Import registry state from persistence."""
        with self._lock_internal:
            # Import components
            for cid, data in state.get("components", {}).items():
                record = ComponentRecord(
                    component_id=data["component_id"],
                    component_type=data["component_type"],
                    name=data["name"],
                    version=data["version"],
                    status=RegistryStatus(data["status"]),
                    last_validated=datetime.fromisoformat(data["last_validated"]),
                    last_hash=data["last_hash"],
                    violation_count=data["violation_count"],
                    metadata=data.get("metadata", {}),
                )
                self._components[cid] = record
            
            # Import violations
            for vid, data in state.get("violations", {}).items():
                record = ViolationRecord(
                    violation_id=data["violation_id"],
                    component_id=data["component_id"],
                    rule_id=data["rule_id"],
                    severity=data["severity"],
                    description=data["description"],
                    first_seen=datetime.fromisoformat(data["first_seen"]),
                    last_seen=datetime.fromisoformat(data["last_seen"]),
                    occurrence_count=data["occurrence_count"],
                    auto_fixed=data["auto_fixed"],
                    waived=data["waived"],
                    waiver_reason=data["waiver_reason"],
                )
                self._violations[vid] = record
    
    def compute_registry_hash(self) -> str:
        """Compute deterministic hash of registry state."""
        state = self.export_state()
        state_json = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_json.encode()).hexdigest()[:16]


# Singleton accessor
def get_registry() -> CanonRegistry:
    """Get the singleton registry instance."""
    return CanonRegistry()
