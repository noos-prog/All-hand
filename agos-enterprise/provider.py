#!/usr/bin/env python3
"""
AGOS Enterprise - Provider Module
=================================

Providers are the "employees" of the enterprise.
They execute skills and capabilities.
Providers NEVER manage - only execute.

Examples:
- Jest → Unit Testing
- Playwright → E2E Testing
- Semgrep → Security Testing
- SonarQube → Code Quality
- CodeQL → Security Analysis
- GitHub → Version Control
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
import hashlib
import json


class ProviderType(Enum):
    """Types of providers (employees)."""
    TESTING = "testing"
    SECURITY = "security"
    CODE_QUALITY = "code_quality"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    DATA_PROCESSING = "data_processing"
    COMMUNICATION = "communication"
    STORAGE = "storage"
    COMPUTE = "compute"
    AI_LLM = "ai_llm"


class ProviderStatus(Enum):
    """Status of a provider."""
    AVAILABLE = "available"
    BUSY = "busy"
    MAINTENANCE = "maintenance"
    DISABLED = "disabled"
    CERTIFICATION_PENDING = "certification_pending"


class ProviderTier(Enum):
    """Provider tier/certification level."""
    EXPERIMENTAL = "experimental"
    BETA = "beta"
    STABLE = "stable"
    ENTERPRISE = "enterprise"


@dataclass(frozen=True)
class ProviderCapability:
    """
    A capability that a provider can execute.
    """
    capability_id: str                  # ID of capability
    skill_ids: Tuple[str, ...]         # Skills this provider handles
    max_concurrent: int = 1            # Max concurrent executions
    avg_duration_ms: int = 5000        # Average execution time
    success_rate: float = 0.95         # Historical success rate
    version: str = "1.0"


@dataclass
class ProviderMetrics:
    """Performance metrics for a provider."""
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    total_duration_ms: int = 0
    last_execution_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    last_failure_at: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_executions == 0:
            return 0.0
        return self.successful_executions / self.total_executions
    
    @property
    def avg_duration_ms(self) -> int:
        """Calculate average duration."""
        if self.total_executions == 0:
            return 0
        return self.total_duration_ms // self.total_executions
    
    @property
    def availability(self) -> float:
        """Calculate availability (uptime percentage)."""
        # Simplified - would track actual uptime
        if self.total_executions == 0:
            return 1.0
        return (self.total_executions - self.failed_executions) / self.total_executions


@dataclass
class Provider:
    """
    A provider is an employee that executes skills.
    
    Characteristics:
    - Providers NEVER manage
    - Providers are replaceable
    - Providers must be certified
    - Providers have performance metrics
    """
    provider_id: str                   # Unique identifier
    name: str                          # Human-readable name
    provider_type: ProviderType        # Type of provider
    description: str                   # What this provider does
    version: str = "1.0"
    tier: ProviderTier = ProviderTier.STABLE
    status: ProviderStatus = ProviderStatus.AVAILABLE
    
    # Capabilities this provider can execute
    capabilities: Tuple[ProviderCapability, ...] = ()
    
    # Configuration
    endpoint: Optional[str] = None     # API endpoint (if remote)
    api_key: Optional[str] = None     # API key (if needed)
    config: Dict[str, Any] = field(default_factory=dict)
    
    # Metrics
    metrics: ProviderMetrics = field(default_factory=ProviderMetrics)
    
    # Certification
    certified_at: Optional[datetime] = None
    certification_valid_until: Optional[datetime] = None
    certification_authority: Optional[str] = None
    
    # Security
    security_scanned_at: Optional[datetime] = None
    security_scan_result: Optional[str] = None
    
    # Metadata
    tags: Tuple[str, ...] = ()
    documentation_url: Optional[str] = None
    support_contact: Optional[str] = None
    
    def execute(
        self,
        skill_id: str,
        input_data: Dict[str, Any],
        timeout_ms: int = 30000,
    ) -> Dict[str, Any]:
        """
        Execute a skill.
        
        Returns execution result with:
        - success: bool
        - output: result data
        - error: error message (if failed)
        - duration_ms: execution time
        """
        start_time = datetime.utcnow()
        
        # Check if provider can execute this skill
        if not self._can_execute(skill_id):
            return {
                "success": False,
                "error": f"Provider {self.provider_id} cannot execute skill {skill_id}",
                "duration_ms": 0,
            }
        
        # Check status
        if self.status != ProviderStatus.AVAILABLE:
            return {
                "success": False,
                "error": f"Provider {self.provider_id} is not available (status: {self.status.value})",
                "duration_ms": 0,
            }
        
        # Execute (placeholder - actual execution depends on provider type)
        try:
            # Simulate execution
            result = self._do_execute(skill_id, input_data, timeout_ms)
            
            # Update metrics
            self._record_success()
            
            return {
                "success": True,
                "output": result,
                "duration_ms": (datetime.utcnow() - start_time).total_seconds() * 1000,
            }
            
        except Exception as e:
            # Update metrics
            self._record_failure(str(e))
            
            return {
                "success": False,
                "error": str(e),
                "duration_ms": (datetime.utcnow() - start_time).total_seconds() * 1000,
            }
    
    def _can_execute(self, skill_id: str) -> bool:
        """Check if provider can execute this skill."""
        for cap in self.capabilities:
            if skill_id in cap.skill_ids:
                return True
        return False
    
    def _do_execute(
        self,
        skill_id: str,
        input_data: Dict[str, Any],
        timeout_ms: int,
    ) -> Dict[str, Any]:
        """
        Actual execution logic.
        Override this in subclasses for real providers.
        """
        # Placeholder - in production this would call actual provider
        return {
            "skill_id": skill_id,
            "executed": True,
            "input": input_data,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def _record_success(self) -> None:
        """Record successful execution."""
        self.metrics.total_executions += 1
        self.metrics.successful_executions += 1
        self.metrics.last_execution_at = datetime.utcnow()
        self.metrics.last_success_at = datetime.utcnow()
    
    def _record_failure(self, error: str) -> None:
        """Record failed execution."""
        self.metrics.total_executions += 1
        self.metrics.failed_executions += 1
        self.metrics.last_execution_at = datetime.utcnow()
        self.metrics.last_failure_at = datetime.utcnow()
    
    def is_certified(self) -> bool:
        """Check if provider is currently certified."""
        if self.certified_at is None:
            return False
        if self.certification_valid_until is None:
            return True
        return datetime.utcnow() < self.certification_valid_until
    
    def is_security_scanned(self) -> bool:
        """Check if provider has recent security scan."""
        if self.security_scanned_at is None:
            return False
        # Scan valid for 30 days
        return datetime.utcnow() - self.security_scanned_at < timedelta(days=30)
    
    def is_available(self) -> bool:
        """Check if provider is available for execution."""
        return (
            self.status == ProviderStatus.AVAILABLE and
            self.is_certified() and
            self.is_security_scanned()
        )
    
    def get_capability(self, capability_id: str) -> Optional[ProviderCapability]:
        """Get a specific capability."""
        for cap in self.capabilities:
            if cap.capability_id == capability_id:
                return cap
        return None
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get provider health status."""
        return {
            "provider_id": self.provider_id,
            "name": self.name,
            "type": self.provider_type.value,
            "status": self.status.value,
            "tier": self.tier.value,
            "is_available": self.is_available(),
            "is_certified": self.is_certified(),
            "is_security_scanned": self.is_security_scanned(),
            "metrics": {
                "total_executions": self.metrics.total_executions,
                "success_rate": round(self.metrics.success_rate, 3),
                "avg_duration_ms": self.metrics.avg_duration_ms,
                "availability": round(self.metrics.availability, 3),
                "last_execution_at": (
                    self.metrics.last_execution_at.isoformat()
                    if self.metrics.last_execution_at else None
                ),
            },
        }
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "provider_id": self.provider_id,
            "name": self.name,
            "type": self.provider_type.value,
            "version": self.version,
            "capabilities": [c.capability_id for c in self.capabilities],
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]


class ProviderPool:
    """
    A pool of providers that can execute skills.
    Manages provider selection and load balancing.
    """
    
    def __init__(self):
        self._providers: Dict[str, Provider] = {}
        self._capability_index: Dict[str, List[str]] = {}  # skill_id -> provider_ids
    
    def register(self, provider: Provider) -> None:
        """Register a provider."""
        self._providers[provider.provider_id] = provider
        
        # Update capability index
        for cap in provider.capabilities:
            for skill_id in cap.skill_ids:
                if skill_id not in self._capability_index:
                    self._capability_index[skill_id] = []
                if provider.provider_id not in self._capability_index[skill_id]:
                    self._capability_index[skill_id].append(provider.provider_id)
    
    def unregister(self, provider_id: str) -> bool:
        """Unregister a provider."""
        if provider_id not in self._providers:
            return False
        
        provider = self._providers[provider_id]
        
        # Remove from index
        for cap in provider.capabilities:
            for skill_id in cap.skill_ids:
                if skill_id in self._capability_index:
                    if provider_id in self._capability_index[skill_id]:
                        self._capability_index[skill_id].remove(provider_id)
        
        del self._providers[provider_id]
        return True
    
    def get_provider(self, provider_id: str) -> Optional[Provider]:
        """Get a provider by ID."""
        return self._providers.get(provider_id)
    
    def find_providers_for_skill(self, skill_id: str) -> List[Provider]:
        """Find all providers that can execute a skill."""
        provider_ids = self._capability_index.get(skill_id, [])
        return [
            self._providers[pid] for pid in provider_ids
            if pid in self._providers
        ]
    
    def find_available_provider_for_skill(
        self,
        skill_id: str,
        prefer_tier: Optional[ProviderTier] = None,
    ) -> Optional[Provider]:
        """
        Find the best available provider for a skill.
        Uses tier preference and load balancing.
        """
        available = [
            p for p in self.find_providers_for_skill(skill_id)
            if p.is_available()
        ]
        
        if not available:
            return None
        
        # Filter by tier if specified
        if prefer_tier:
            tier_providers = [p for p in available if p.tier == prefer_tier]
            if tier_providers:
                available = tier_providers
        
        # Select provider with lowest load (simplified)
        # In production would use actual load metrics
        return available[0]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get pool statistics."""
        by_type = {}
        by_status = {}
        by_tier = {}
        
        for provider in self._providers.values():
            # By type
            ptype = provider.provider_type.value
            by_type[ptype] = by_type.get(ptype, 0) + 1
            
            # By status
            status = provider.status.value
            by_status[status] = by_status.get(status, 0) + 1
            
            # By tier
            tier = provider.tier.value
            by_tier[tier] = by_tier.get(tier, 0) + 1
        
        return {
            "total_providers": len(self._providers),
            "by_type": by_type,
            "by_status": by_status,
            "by_tier": by_tier,
            "available_providers": len([
                p for p in self._providers.values() if p.is_available()
            ]),
            "capabilities_indexed": len(self._capability_index),
        }
