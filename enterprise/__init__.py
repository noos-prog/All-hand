"""AGOS Enterprise Platform - Enterprise-grade orchestration and governance."""

from .operating import (
    EnterpriseOperations, OperationsManager, Tenant, TenantStatus, SLALevel,
    Organization, Department, Workspace
)
from .analytics import (
    EnterpriseAnalytics, AnalyticsEngine, Metric, MetricType, Dashboard, Report
)
from .security import (
    EnterpriseSecurity, SecurityManager, Permission, AccessToken,
    SecurityPolicy, AuditLog
)
from .governance import (
    EnterpriseGovernance, GovernanceFramework, Policy, PolicyType, ComplianceStatus,
    ComplianceReport, AuditTrail
)
from .cloud import (
    EnterpriseCloud, CloudIntegration, CloudProvider, DeploymentStatus, Deployment,
    CloudRegion, ResourceQuota
)

__all__ = [
    # Operating
    "EnterpriseOperations", "OperationsManager", "Tenant", "TenantStatus", "SLALevel",
    "Organization", "Department", "Workspace",
    # Analytics
    "EnterpriseAnalytics", "AnalyticsEngine", "Metric", "MetricType",
    "Dashboard", "Report",
    # Security
    "EnterpriseSecurity", "SecurityManager", "Permission", "AccessToken",
    "SecurityPolicy", "AuditLog",
    # Governance
    "EnterpriseGovernance", "GovernanceFramework", "Policy", "PolicyType", "ComplianceStatus",
    "ComplianceReport", "AuditTrail",
    # Cloud
    "EnterpriseCloud", "CloudIntegration", "CloudProvider", "DeploymentStatus", "Deployment",
    "CloudRegion", "ResourceQuota",
]

__version__ = "1.0.0"
