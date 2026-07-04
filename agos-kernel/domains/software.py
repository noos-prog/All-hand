"""Domain 1-10 Implementations."""
from .base import Domain


# DOMAIN-000001: Software Engineering
class SoftwareEngineeringDomain(Domain):
    """Software Engineering Domain."""
    
    def __init__(self):
        super().__init__("SoftwareEngineering", "Core software engineering practices")
        
        self.contribute_capability("CodeAnalysis", "1.0", "Analyze code quality and patterns")
        self.contribute_capability("CodeGeneration", "1.0", "Generate code from specifications")
        self.contribute_knowledge("patterns", "1.0", {
            "singleton": "Ensure a class has only one instance",
            "factory": "Create objects without specifying exact class",
            "observer": "Notify multiple objects about state changes",
            "strategy": "Select algorithms at runtime",
            "adapter": "Convert interface of a class",
        })
        self.contribute_policy("code_review", "1.0", [
            {"rule": "no_secrets", "description": "No hardcoded secrets"},
            {"rule": "test_coverage", "threshold": 80},
        ])
        self.contribute_workflow("code_review", "1.0", [
            {"step": "analyze", "skill": "AnalyzeCode"},
            {"step": "review", "skill": "ReviewPatterns"},
            {"step": "report", "skill": "GenerateReport"},
        ])


# DOMAIN-000002: Backend Engineering
class BackendEngineeringDomain(Domain):
    """Backend Engineering Domain."""
    
    def __init__(self):
        super().__init__("BackendEngineering", "Backend services and APIs")
        
        self.contribute_capability("APIAnalysis", "1.0", "Analyze API design")
        self.contribute_capability("DatabaseAnalysis", "1.0", "Analyze database patterns")
        self.contribute_knowledge("patterns", "1.0", {
            "rest": "RESTful API design patterns",
            "graphql": "GraphQL schema patterns",
            "grpc": "gRPC service patterns",
            "mqtt": "Message queue patterns",
        })
        self.contribute_policy("api_design", "1.0", [
            {"rule": "versioning", "required": True},
            {"rule": "error_format", "required": True},
        ])
        self.contribute_workflow("api_review", "1.0", [
            {"step": "analyze", "skill": "AnalyzeAPI"},
            {"step": "validate", "skill": "ValidateContracts"},
            {"step": "report", "skill": "GenerateReport"},
        ])


# DOMAIN-000003: Frontend Engineering
class FrontendEngineeringDomain(Domain):
    """Frontend Engineering Domain."""
    
    def __init__(self):
        super().__init__("FrontendEngineering", "Frontend web development")
        
        self.contribute_capability("ComponentAnalysis", "1.0", "Analyze frontend components")
        self.contribute_capability("UIAnalysis", "1.0", "Analyze UI patterns")
        self.contribute_knowledge("patterns", "1.0", {
            "component": "Component architecture patterns",
            "state": "State management patterns",
            "routing": "Routing patterns",
            "styling": "CSS/Styling patterns",
        })


# DOMAIN-000004: Mobile Engineering
class MobileEngineeringDomain(Domain):
    """Mobile Engineering Domain."""
    
    def __init__(self):
        super().__init__("MobileEngineering", "Mobile application development")
        
        self.contribute_capability("MobileAnalysis", "1.0", "Analyze mobile apps")
        self.contribute_knowledge("patterns", "1.0", {
            "mvvm": "Model-View-ViewModel pattern",
            "mvi": "Model-View-Intent pattern",
            "navigation": "Navigation patterns",
        })


# DOMAIN-000005: Desktop Engineering
class DesktopEngineeringDomain(Domain):
    """Desktop Engineering Domain."""
    
    def __init__(self):
        super().__init__("DesktopEngineering", "Desktop application development")
        
        self.contribute_capability("DesktopAnalysis", "1.0", "Analyze desktop apps")


# DOMAIN-000006: DevOps Engineering
class DevOpsEngineeringDomain(Domain):
    """DevOps Engineering Domain."""
    
    def __init__(self):
        super().__init__("DevOpsEngineering", "DevOps and CI/CD practices")
        
        self.contribute_capability("CIAnalysis", "1.0", "Analyze CI/CD pipelines")
        self.contribute_capability("ContainerAnalysis", "1.0", "Analyze containers")
        self.contribute_knowledge("patterns", "1.0", {
            "cicd": "CI/CD pipeline patterns",
            "container": "Container orchestration patterns",
            "infrastructure": "Infrastructure as code patterns",
        })
        self.contribute_workflow("cicd_review", "1.0", [
            {"step": "analyze", "skill": "AnalyzeCI"},
            {"step": "validate", "skill": "ValidatePipeline"},
            {"step": "report", "skill": "GenerateReport"},
        ])


# DOMAIN-000007: Cloud Engineering
class CloudEngineeringDomain(Domain):
    """Cloud Engineering Domain."""
    
    def __init__(self):
        super().__init__("CloudEngineering", "Cloud infrastructure")
        
        self.contribute_capability("CloudAnalysis", "1.0", "Analyze cloud architectures")
        self.contribute_capability("CostAnalysis", "1.0", "Analyze cloud costs")
        self.contribute_knowledge("providers", "1.0", {
            "aws": "AWS services and patterns",
            "gcp": "Google Cloud patterns",
            "azure": "Azure patterns",
        })


# DOMAIN-000008: Platform Engineering
class PlatformEngineeringDomain(Domain):
    """Platform Engineering Domain."""
    
    def __init__(self):
        super().__init__("PlatformEngineering", "Internal developer platforms")
        
        self.contribute_capability("PlatformAnalysis", "1.0", "Analyze platform maturity")


# DOMAIN-000009: Infrastructure Engineering
class InfrastructureEngineeringDomain(Domain):
    """Infrastructure Engineering Domain."""
    
    def __init__(self):
        super().__init__("InfrastructureEngineering", "Infrastructure as code")
        
        self.contribute_capability("TerraformAnalysis", "1.0", "Analyze Terraform configs")
        self.contribute_capability("KubernetesAnalysis", "1.0", "Analyze K8s configs")
        self.contribute_knowledge("patterns", "1.0", {
            "terraform": "Terraform patterns",
            "kubernetes": "Kubernetes patterns",
            "helm": "Helm chart patterns",
        })


# DOMAIN-000010: Site Reliability Engineering
class SREDomain(Domain):
    """Site Reliability Engineering Domain."""
    
    def __init__(self):
        super().__init__("SRE", "Site reliability engineering")
        
        self.contribute_capability("ReliabilityAnalysis", "1.0", "Analyze system reliability")
        self.contribute_capability("IncidentAnalysis", "1.0", "Analyze incidents")
        self.contribute_knowledge("slos", "1.0", {
            "availability": "Availability SLOs",
            "latency": "Latency SLOs",
            "errors": "Error rate SLOs",
        })


# Registry
DOMAINS = {
    "software": SoftwareEngineeringDomain,
    "backend": BackendEngineeringDomain,
    "frontend": FrontendEngineeringDomain,
    "mobile": MobileEngineeringDomain,
    "desktop": DesktopEngineeringDomain,
    "devops": DevOpsEngineeringDomain,
    "cloud": CloudEngineeringDomain,
    "platform": PlatformEngineeringDomain,
    "infrastructure": InfrastructureEngineeringDomain,
    "sre": SREDomain,
}


def get_domain(name: str) -> Domain:
    """Get a domain by name."""
    domain_class = DOMAINS.get(name)
    if not domain_class:
        raise ValueError(f"Unknown domain: {name}")
    return domain_class()