#!/usr/bin/env python3
"""
ARI - Provider Module
=================

Provider registry and capability mapping.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class ProviderType(Enum):
    """Types of providers."""
    LLM = "llm"
    AGENT = "agent"
    CODING_AGENT = "coding_agent"
    BROWSER_AGENT = "browser_agent"
    IDE_AGENT = "ide_agent"
    MCP_SERVER = "mcp_server"
    API = "api"
    TOOL = "tool"


class ProviderStatus(Enum):
    """Provider status."""
    UNKNOWN = "unknown"
    REGISTERED = "registered"
    BENCHMARKING = "benchmarking"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"


@dataclass
class ProviderMetrics:
    """Metrics for a provider."""
    # Performance
    success_rate: float = 0.0
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    
    # Cost
    cost_per_1k_tokens: float = 0.0
    cost_per_request: float = 0.0
    avg_cost_per_task: float = 0.0
    
    # Quality
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    
    # Usage
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    
    # Capabilities
    capabilities_tested: int = 0
    capabilities_passed: int = 0
    
    def get_overall_score(self) -> float:
        """Calculate overall provider score."""
        if self.total_requests == 0:
            return 0.0
        
        success_weight = 0.3
        latency_weight = 0.2
        cost_weight = 0.2
        quality_weight = 0.3
        
        # Success score (higher is better)
        success_score = self.success_rate
        
        # Latency score (lower is better)
        latency_score = max(0, 1 - (self.avg_latency_ms / 10000))
        
        # Cost score (lower is better)
        cost_score = max(0, 1 - (self.cost_per_request / 10))
        
        # Quality score
        quality_score = self.f1_score if self.f1_score > 0 else self.accuracy
        
        total = (
            success_weight * success_score +
            latency_weight * latency_score +
            cost_weight * cost_score +
            quality_weight * quality_score
        )
        
        return round(total, 3)


@dataclass
class CapabilityScore:
    """Score for a specific capability."""
    capability: str
    success_rate: float
    avg_latency_ms: float
    avg_cost: float
    sample_size: int
    last_tested: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability": self.capability,
            "success_rate": f"{self.success_rate:.1%}",
            "avg_latency_ms": f"{self.avg_latency_ms:.0f}ms",
            "avg_cost": f"${self.avg_cost:.4f}",
            "sample_size": self.sample_size,
        }


@dataclass
class Provider:
    """
    A provider in the registry.
    """
    provider_id: str
    name: str
    provider_type: ProviderType
    
    # Identification
    display_name: str
    description: Optional[str] = None
    website: Optional[str] = None
    documentation_url: Optional[str] = None
    
    # Classification
    capabilities: Tuple[str, ...] = ()    # What it can do
    supported_languages: Tuple[str, ...] = ()  # Languages supported
    supported_frameworks: Tuple[str, ...] = ()  # Frameworks
    
    # Authentication
    auth_type: str = "api_key"          # api_key, oauth, etc.
    requires_auth: bool = True
    
    # Metrics
    metrics: ProviderMetrics = field(default_factory=ProviderMetrics)
    capability_scores: Tuple[CapabilityScore, ...] = ()
    
    # Status
    status: ProviderStatus = ProviderStatus.UNKNOWN
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_benchmarked: Optional[str] = None
    
    # API
    api_endpoint: Optional[str] = None
    api_version: Optional[str] = None
    
    # Limits
    rate_limit_per_minute: Optional[int] = None
    max_tokens_per_request: Optional[int] = None
    
    def get_capability_score(self, capability: str) -> Optional[CapabilityScore]:
        """Get score for a specific capability."""
        for score in self.capability_scores:
            if score.capability == capability:
                return score
        return None
    
    def get_best_capability(self) -> Optional[str]:
        """Get the best performing capability."""
        if not self.capability_scores:
            return None
        return max(self.capability_scores, key=lambda s: s.success_rate).capability
    
    def get_overall_score(self) -> float:
        """Get overall provider score."""
        return self.metrics.get_overall_score()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get provider summary."""
        return {
            "name": self.display_name,
            "type": self.provider_type.value,
            "status": self.status.value,
            "success_rate": f"{self.metrics.success_rate:.1%}",
            "overall_score": f"{self.get_overall_score():.1%}",
            "capabilities": len(self.capabilities),
        }


class ProviderRegistry:
    """
    Registry of all providers.
    """
    
    def __init__(self):
        self._providers: Dict[str, Provider] = {}
        self._by_type: Dict[ProviderType, List[str]] = {}
        self._by_capability: Dict[str, List[str]] = {}  # capability -> provider_ids
    
    def register(self, provider: Provider) -> str:
        """Register a provider."""
        self._providers[provider.provider_id] = provider
        
        # Index by type
        if provider.provider_type not in self._by_type:
            self._by_type[provider.provider_type] = []
        self._by_type[provider.provider_type].append(provider.provider_id)
        
        # Index by capability
        for cap in provider.capabilities:
            if cap not in self._by_capability:
                self._by_capability[cap] = []
            self._by_capability[cap].append(provider.provider_id)
        
        provider.status = ProviderStatus.REGISTERED
        return provider.provider_id
    
    def get(self, provider_id: str) -> Optional[Provider]:
        """Get a provider by ID."""
        return self._providers.get(provider_id)
    
    def get_by_type(self, provider_type: ProviderType) -> List[Provider]:
        """Get all providers of a type."""
        ids = self._by_type.get(provider_type, [])
        return [self._providers[i] for i in ids if i in self._providers]
    
    def get_by_capability(self, capability: str) -> List[Provider]:
        """Get all providers supporting a capability."""
        ids = self._by_capability.get(capability, [])
        return [self._providers[i] for i in ids if i in self._providers]
    
    def search(
        self,
        provider_type: Optional[ProviderType] = None,
        capabilities: List[str] = None,
        min_score: float = 0.0,
        limit: int = 100
    ) -> List[Provider]:
        """Search providers."""
        results = list(self._providers.values())
        
        if provider_type:
            results = [p for p in results if p.provider_type == provider_type]
        
        if capabilities:
            results = [
                p for p in results
                if all(c in p.capabilities for c in capabilities)
            ]
        
        if min_score > 0:
            results = [p for p in results if p.get_overall_score() >= min_score]
        
        # Sort by overall score
        results.sort(key=lambda p: p.get_overall_score(), reverse=True)
        
        return results[:limit]
    
    def update_metrics(self, provider_id: str, metrics: ProviderMetrics) -> bool:
        """Update provider metrics."""
        provider = self._providers.get(provider_id)
        if not provider:
            return False
        
        provider.metrics = metrics
        provider.updated_at = datetime.utcnow().isoformat()
        provider.last_benchmarked = datetime.utcnow().isoformat()
        return True
    
    def approve(self, provider_id: str) -> bool:
        """Approve a provider."""
        provider = self._providers.get(provider_id)
        if not provider:
            return False
        
        provider.status = ProviderStatus.APPROVED
        provider.updated_at = datetime.utcnow().isoformat()
        return True
    
    def reject(self, provider_id: str) -> bool:
        """Reject a provider."""
        provider = self._providers.get(provider_id)
        if not provider:
            return False
        
        provider.status = ProviderStatus.REJECTED
        provider.updated_at = datetime.utcnow().isoformat()
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        by_type = {pt.value: len(ids) for pt, ids in self._by_type.items()}
        by_status = {}
        approved_count = 0
        
        for provider in self._providers.values():
            status = provider.status.value
            by_status[status] = by_status.get(status, 0) + 1
            if provider.status == ProviderStatus.APPROVED:
                approved_count += 1
        
        return {
            "total_providers": len(self._providers),
            "by_type": by_type,
            "by_status": by_status,
            "approved_providers": approved_count,
            "total_capabilities_indexed": len(self._by_capability),
        }


class CapabilityMapping:
    """
    Maps capabilities to providers.
    """
    
    def __init__(self, registry: ProviderRegistry):
        self.registry = registry
        self._capability_graph: Dict[str, List[str]] = {}
    
    def add_capability(
        self,
        capability: str,
        provider_ids: List[str],
        scores: Dict[str, float] = None
    ) -> None:
        """Add a capability mapping."""
        self._capability_graph[capability] = provider_ids
    
    def find_best_provider(
        self,
        capability: str,
        criteria: str = "success_rate"
    ) -> Optional[Provider]:
        """Find the best provider for a capability."""
        providers = self.registry.get_by_capability(capability)
        
        if not providers:
            return None
        
        if criteria == "success_rate":
            return max(providers, key=lambda p: p.metrics.success_rate)
        elif criteria == "latency":
            return min(providers, key=lambda p: p.metrics.avg_latency_ms)
        elif criteria == "cost":
            return min(providers, key=lambda p: p.metrics.cost_per_request)
        else:
            return max(providers, key=lambda p: p.get_overall_score())
    
    def rank_providers(
        self,
        capability: str,
        criteria: str = "overall"
    ) -> List[Tuple[Provider, float]]:
        """Rank providers for a capability."""
        providers = self.registry.get_by_capability(capability)
        
        if not providers:
            return []
        
        scored = []
        for p in providers:
            if criteria == "success_rate":
                score = p.metrics.success_rate
            elif criteria == "latency":
                score = 1.0 / max(p.metrics.avg_latency_ms, 1)
            elif criteria == "cost":
                score = 1.0 / max(p.metrics.cost_per_request, 0.001)
            else:
                score = p.get_overall_score()
            scored.append((p, score))
        
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def get_capability_matrix(
        self,
        capabilities: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get capability matrix for multiple capabilities."""
        matrix = {}
        
        for cap in capabilities:
            providers = self.registry.get_by_capability(cap)
            matrix[cap] = [
                {
                    "provider_id": p.provider_id,
                    "name": p.display_name,
                    "success_rate": p.metrics.success_rate,
                    "latency_ms": p.metrics.avg_latency_ms,
                    "cost": p.metrics.cost_per_request,
                }
                for p in providers
            ]
        
        return matrix
