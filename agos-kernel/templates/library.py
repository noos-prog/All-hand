"""AGOS Template Library."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class TemplateMetadata:
    """Template metadata."""
    id: str
    name: str
    category: str
    version: str = "1.0.0"
    description: str = ""


@dataclass
class TemplateFile:
    """A template file."""
    path: str
    content: str


@dataclass
class Template:
    """A reusable template."""
    
    def __init__(self, name: str, category: str, description: str = ""):
        """Initialize template."""
        self.metadata = TemplateMetadata(
            id=f"template-{uuid.uuid4().hex[:8]}",
            name=name,
            category=category,
            description=description,
        )
        self.files: List[TemplateFile] = []


# Template Library
TEMPLATES = {
    "backend_service": Template("BackendService", "service", "Backend microservice template"),
    "rest_api": Template("RESTAPI", "api", "REST API service template"),
    "graphql_service": Template("GraphQLService", "api", "GraphQL service template"),
    "grpc_service": Template("gRPCService", "api", "gRPC service template"),
    "cli": Template("CLI", "tool", "Command-line interface template"),
    "sdk": Template("SDK", "library", "SDK template"),
    "microservice": Template("Microservice", "service", "Microservice template"),
    "monolith": Template("Monolith", "service", "Monolith template"),
    "event_driven": Template("EventDriven", "service", "Event-driven template"),
    "worker": Template("Worker", "service", "Worker template"),
    "scheduler": Template("Scheduler", "service", "Scheduler template"),
    "plugin": Template("Plugin", "extension", "Plugin template"),
    "extension": Template("Extension", "extension", "Extension template"),
    "capability": Template("Capability", "extension", "Capability template"),
    "provider": Template("Provider", "extension", "Provider template"),
    "adapter": Template("Adapter", "extension", "Adapter template"),
    "workflow": Template("Workflow", "extension", "Workflow template"),
    "repository": Template("Repository", "repository", "Repository template"),
    "docker": Template("Docker", "infrastructure", "Docker template"),
    "kubernetes": Template("Kubernetes", "infrastructure", "K8s template"),
    "terraform": Template("Terraform", "infrastructure", "Terraform template"),
    "helm": Template("Helm", "infrastructure", "Helm template"),
    "cicd": Template("CICD", "infrastructure", "CI/CD template"),
    "github_actions": Template("GitHubActions", "infrastructure", "GitHub Actions template"),
    "gitlab_ci": Template("GitLabCI", "infrastructure", "GitLab CI template"),
    "testing": Template("Testing", "quality", "Testing template"),
    "benchmark": Template("Benchmark", "quality", "Benchmark template"),
    "architecture": Template("Architecture", "docs", "Architecture template"),
    "documentation": Template("Documentation", "docs", "Documentation template"),
    "adr": Template("ADR", "docs", "ADR template"),
    "security_review": Template("SecurityReview", "review", "Security review template"),
    "performance_review": Template("PerformanceReview", "review", "Performance review template"),
    "incident_report": Template("IncidentReport", "review", "Incident report template"),
    "migration": Template("Migration", "operational", "Migration template"),
    "release": Template("Release", "operational", "Release template"),
    "domain": Template("Domain", "extension", "Domain template"),
}


class TemplateLibrary:
    """Library of templates."""
    
    def __init__(self):
        self.templates = TEMPLATES
    
    def get(self, name: str) -> Template:
        return self.templates.get(name)
    
    def list_all(self) -> List[Template]:
        return list(self.templates.values())
    
    def list_by_category(self, category: str) -> List[Template]:
        return [t for t in self.templates.values() if t.metadata.category == category]


_library = TemplateLibrary()


def get_library() -> TemplateLibrary:
    return _library