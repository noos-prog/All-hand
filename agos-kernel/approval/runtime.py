"""Universal Approval Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ApprovalStatus(Enum):
    """Approval status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    SKIPPED = "skipped"


class ApprovalSource(Enum):
    """Approval source."""
    AUTOMATIC = "automatic"
    POLICY = "policy"
    EVIDENCE = "evidence"
    HUMAN = "human"
    ORGANIZATION = "organization"


@dataclass
class ApprovalRule:
    """An approval rule."""
    id: str
    name: str
    conditions: Dict[str, Any] = field(default_factory=dict)
    approvers: List[str] = field(default_factory=list)
    auto_approve: bool = False


@dataclass
class ApprovalRequest:
    """An approval request."""
    id: str
    request_type: str
    description: str
    source: ApprovalSource
    status: ApprovalStatus = ApprovalStatus.PENDING
    requester: str = ""
    approvers: List[str] = field(default_factory=list)
    approved_by: List[str] = field(default_factory=list)
    rejected_by: str = ""
    reason: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    decided_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class ApprovalRuntime:
    """Universal Approval Runtime."""
    
    def __init__(self):
        """Initialize approval runtime."""
        self.requests: Dict[str, ApprovalRequest] = {}
        self.rules: Dict[str, ApprovalRule] = {}
        self.history: List[ApprovalRequest] = []
    
    def create_request(
        self,
        request_type: str,
        description: str,
        source: ApprovalSource = ApprovalSource.AUTOMATIC,
        requester: str = "",
        evidence: Optional[Dict[str, Any]] = None,
    ) -> ApprovalRequest:
        """Create an approval request."""
        request = ApprovalRequest(
            id=self._generate_id("approval"),
            request_type=request_type,
            description=description,
            source=source,
            requester=requester,
            evidence=evidence or {},
        )
        
        self.requests[request.id] = request
        return request
    
    def add_rule(self, rule: ApprovalRule) -> None:
        """Add an approval rule."""
        self.rules[rule.id] = rule
    
    def approve(self, request_id: str, approver: str, reason: str = "") -> bool:
        """Approve a request."""
        request = self.requests.get(request_id)
        if not request:
            return False
        
        request.status = ApprovalStatus.APPROVED
        request.approved_by.append(approver)
        request.reason = reason
        request.decided_at = datetime.now()
        
        self.history.append(request)
        return True
    
    def reject(self, request_id: str, rejected_by: str, reason: str) -> bool:
        """Reject a request."""
        request = self.requests.get(request_id)
        if not request:
            return False
        
        request.status = ApprovalStatus.REJECTED
        request.rejected_by = rejected_by
        request.reason = reason
        request.decided_at = datetime.now()
        
        self.history.append(request)
        return True
    
    def skip(self, request_id: str, reason: str) -> bool:
        """Skip approval."""
        request = self.requests.get(request_id)
        if not request:
            return False
        
        request.status = ApprovalStatus.SKIPPED
        request.reason = reason
        request.decided_at = datetime.now()
        
        self.history.append(request)
        return True
    
    def check_policy(self, request_type: str, evidence: Dict[str, Any]) -> bool:
        """Check if request should be auto-approved by policy."""
        for rule in self.rules.values():
            if rule.request_type == request_type or rule.request_type == "*":
                if rule.auto_approve:
                    return True
        return False
    
    def get_request(self, request_id: str) -> Optional[ApprovalRequest]:
        """Get request by ID."""
        return self.requests.get(request_id)
    
    def list_requests(
        self,
        status: Optional[ApprovalStatus] = None,
        source: Optional[ApprovalSource] = None,
    ) -> List[ApprovalRequest]:
        """List approval requests."""
        requests = list(self.requests.values())
        
        if status:
            requests = [r for r in requests if r.status == status]
        
        if source:
            requests = [r for r in requests if r.source == source]
        
        return requests
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get approval analytics."""
        total = len(self.history)
        approved = sum(1 for r in self.history if r.status == ApprovalStatus.APPROVED)
        rejected = sum(1 for r in self.history if r.status == ApprovalStatus.REJECTED)
        
        return {
            "total_requests": total,
            "approved": approved,
            "rejected": rejected,
            "pending": len(self.requests),
            "approval_rate": approved / total if total > 0 else 0,
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
