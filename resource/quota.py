"""Quota Management - Track and enforce resource quotas."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class QuotaPolicy(Enum):
    """Quota enforcement policies."""
    HARD = "hard"  # Deny when exceeded
    SOFT = "soft"  # Warn when exceeded
    FAIR_SHARE = "fair_share"


@dataclass
class QuotaLimit:
    """A quota limit."""
    limit_id: str
    owner_id: str
    resource_type: str
    limit: float
    used: float = 0.0
    policy: QuotaPolicy = QuotaPolicy.HARD
    reset_period: str = "monthly"
    last_reset: datetime = field(default_factory=datetime.utcnow)


@dataclass
class QuotaUsage:
    """Current quota usage."""
    limit_id: str
    resource_type: str
    used: float
    limit: float
    remaining: float
    utilization_percent: float


@dataclass
class QuotaManager:
    """Manage resource quotas."""
    
    def __init__(self):
        self._quotas: Dict[str, QuotaLimit] = {}
    
    def set_quota(
        self,
        owner_id: str,
        resource_type: str,
        limit: float,
        policy: QuotaPolicy = QuotaPolicy.HARD,
    ) -> QuotaLimit:
        quota = QuotaLimit(
            limit_id=str(uuid.uuid4()),
            owner_id=owner_id,
            resource_type=resource_type,
            limit=limit,
            policy=policy,
        )
        self._quotas[quota.limit_id] = quota
        return quota
    
    def check_quota(
        self,
        owner_id: str,
        resource_type: str,
        requested: float,
    ) -> Dict[str, Any]:
        owner_quotas = [
            q for q in self._quotas.values()
            if q.owner_id == owner_id and q.resource_type == resource_type
        ]
        
        total_limit = sum(q.limit for q in owner_quotas)
        total_used = sum(q.used for q in owner_quotas)
        remaining = total_limit - total_used
        
        allowed = remaining >= requested
        hard_limit_exceeded = any(
            q.policy == QuotaPolicy.HARD and (q.used + requested) > q.limit
            for q in owner_quotas
        )
        
        return {
            "allowed": allowed and not hard_limit_exceeded,
            "total_limit": total_limit,
            "total_used": total_used,
            "remaining": remaining,
            "requested": requested,
            "utilization_percent": (total_used / total_limit * 100) if total_limit > 0 else 0,
        }
    
    def consume(
        self,
        owner_id: str,
        resource_type: str,
        amount: float,
    ) -> bool:
        check = self.check_quota(owner_id, resource_type, amount)
        if not check["allowed"]:
            return False
        
        for quota in self._quotas.values():
            if quota.owner_id == owner_id and quota.resource_type == resource_type:
                quota.used += amount
        return True
    
    def release(
        self,
        owner_id: str,
        resource_type: str,
        amount: float,
    ) -> None:
        for quota in self._quotas.values():
            if quota.owner_id == owner_id and quota.resource_type == resource_type:
                quota.used = max(0, quota.used - amount)
    
    def get_usage(
        self,
        owner_id: str,
        resource_type: Optional[str] = None,
    ) -> List[QuotaUsage]:
        quotas = [
            q for q in self._quotas.values()
            if q.owner_id == owner_id and (resource_type is None or q.resource_type == resource_type)
        ]
        
        return [
            QuotaUsage(
                limit_id=q.limit_id,
                resource_type=q.resource_type,
                used=q.used,
                limit=q.limit,
                remaining=max(0, q.limit - q.used),
                utilization_percent=(q.used / q.limit * 100) if q.limit > 0 else 0,
            )
            for q in quotas
        ]
