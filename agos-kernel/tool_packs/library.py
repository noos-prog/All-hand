"""AGOS Tool Packs Library."""
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ToolPackMetadata:
    """Tool pack metadata."""
    id: str
    name: str
    category: str
    version: str = "1.0.0"
    description: str = ""


class ToolPack:
    """An engineering tool pack."""
    
    def __init__(self, name: str, category: str, description: str = ""):
        self.metadata = ToolPackMetadata(
            id=f"tool-{uuid.uuid4().hex[:8]}",
            name=name,
            category=category,
            description=description,
        )
        self.capabilities: List[str] = []
        self.version_command = ""
        self.health_command = ""


# Tool Packs
TOOL_PACKS = {
    # Version Control
    "git": ToolPack("Git", "vcs", "Git version control"),
    "git_lfs": ToolPack("Git LFS", "vcs", "Git Large File Storage"),
    
    # Containers
    "docker": ToolPack("Docker", "container", "Docker container runtime"),
    "podman": ToolPack("Podman", "container", "Podman container engine"),
    "buildah": ToolPack("Buildah", "container", "Buildah container builder"),
    "containerd": ToolPack("containerd", "container", "containerd runtime"),
    
    # Orchestration
    "kubernetes": ToolPack("Kubernetes", "orchestration", "Kubernetes orchestration"),
    "helm": ToolPack("Helm", "orchestration", "Helm package manager"),
    
    # Infrastructure as Code
    "terraform": ToolPack("Terraform", "iac", "HashiCorp Terraform"),
    "opentofu": ToolPack("OpenTofu", "iac", "OpenTofu IaC"),
    "ansible": ToolPack("Ansible", "iac", "Ansible automation"),
    "pulumi": ToolPack("Pulumi", "iac", "Pulumi IaC"),
    "packer": ToolPack("Packer", "iac", "HashiCorp Packer"),
    
    # Secrets & Service Mesh
    "vault": ToolPack("Vault", "secrets", "HashiCorp Vault"),
    "consul": ToolPack("Consul", "service_mesh", "HashiCorp Consul"),
    "nomad": ToolPack("Nomad", "orchestration", "HashiCorp Nomad"),
    
    # CI/CD
    "jenkins": ToolPack("Jenkins", "cicd", "Jenkins CI/CD"),
    "github_actions": ToolPack("GitHub Actions", "cicd", "GitHub Actions"),
    "gitlab_ci": ToolPack("GitLab CI", "cicd", "GitLab CI/CD"),
    "argocd": ToolPack("ArgoCD", "gitops", "ArgoCD GitOps"),
    "fluxcd": ToolPack("FluxCD", "gitops", "FluxCD GitOps"),
    
    # Browser Automation
    "playwright": ToolPack("Playwright", "browser", "Playwright browser automation"),
    "puppeteer": ToolPack("Puppeteer", "browser", "Puppeteer browser automation"),
    "selenium": ToolPack("Selenium", "browser", "Selenium browser automation"),
    "cypress": ToolPack("Cypress", "browser", "Cypress E2E testing"),
    
    # Testing
    "vitest": ToolPack("Vitest", "testing", "Vite-native testing"),
    "jest": ToolPack("Jest", "testing", "Jest JavaScript testing"),
    "mocha": ToolPack("Mocha", "testing", "Mocha testing framework"),
    "pytest": ToolPack("Pytest", "testing", "Python testing"),
    "junit": ToolPack("JUnit", "testing", "Java testing"),
    
    # Build Tools
    "maven": ToolPack("Maven", "build", "Apache Maven"),
    "gradle": ToolPack("Gradle", "build", "Gradle build tool"),
    
    # Package Managers
    "npm": ToolPack("npm", "package", "Node Package Manager"),
    "pnpm": ToolPack("pnpm", "package", "pnpm package manager"),
    "yarn": ToolPack("Yarn", "package", "Yarn package manager"),
    "poetry": ToolPack("Poetry", "package", "Python Poetry"),
    "pip": ToolPack("pip", "package", "Python pip"),
    "cargo": ToolPack("Cargo", "package", "Rust Cargo"),
    "go_toolchain": ToolPack("Go Toolchain", "language", "Go language toolchain"),
    "dotnet_cli": ToolPack(".NET CLI", "language", ".NET Command Line"),
    "java_toolchain": ToolPack("Java Toolchain", "language", "Java SDK"),
    
    # Language Runtimes
    "nodejs": ToolPack("Node.js", "runtime", "Node.js runtime"),
    "python": ToolPack("Python", "runtime", "Python runtime"),
    "go": ToolPack("Go", "runtime", "Go runtime"),
    "rust": ToolPack("Rust", "runtime", "Rust toolchain"),
    "java": ToolPack("Java", "runtime", "Java runtime"),
    "kotlin": ToolPack("Kotlin", "runtime", "Kotlin toolchain"),
    "swift": ToolPack("Swift", "runtime", "Swift toolchain"),
    "flutter": ToolPack("Flutter", "mobile", "Flutter SDK"),
    "android_sdk": ToolPack("Android SDK", "mobile", "Android SDK"),
    "xcode": ToolPack("Xcode", "mobile", "Xcode IDE"),
    
    # Database Tools
    "redis_cli": ToolPack("Redis CLI", "database", "Redis CLI"),
    "postgresql_cli": ToolPack("PostgreSQL CLI", "database", "PostgreSQL psql"),
    "mysql_cli": ToolPack("MySQL CLI", "database", "MySQL client"),
    "mongodb_tools": ToolPack("MongoDB Tools", "database", "MongoDB CLI tools"),
    "neo4j_tools": ToolPack("Neo4j Tools", "database", "Neo4j tools"),
    
    # Visualization
    "graphviz": ToolPack("Graphviz", "visualization", "Graphviz graphviz"),
    "plantuml": ToolPack("PlantUML", "visualization", "PlantUML diagram"),
    "mermaid": ToolPack("Mermaid", "visualization", "Mermaid diagrams"),
    
    # Custom
    "custom_sdk": ToolPack("Custom SDK", "custom", "Custom Tool SDK"),
}


class ToolPackLibrary:
    """Library of tool packs."""
    
    def __init__(self):
        self.packs = TOOL_PACKS
    
    def get(self, name: str) -> ToolPack:
        return self.packs.get(name)
    
    def list_all(self) -> List[ToolPack]:
        return list(self.packs.values())
    
    def list_by_category(self, category: str) -> List[ToolPack]:
        return [p for p in self.packs.values() if p.metadata.category == category]


_library = ToolPackLibrary()


def get_library() -> ToolPackLibrary:
    return _library