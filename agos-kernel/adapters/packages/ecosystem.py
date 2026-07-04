"""Package Ecosystem Adapters."""
from typing import Any, Dict, List, Optional
from ..base import Adapter


# ADAPTER-000008: npm Adapter
class NpmAdapter(Adapter):
    """npm package manager adapter."""
    
    def __init__(self):
        super().__init__("npm", "npm", "Node Package Manager")
        self.metadata.capabilities = ["install", "publish", "search", "info"]


# ADAPTER-000009: pnpm Adapter
class PnpmAdapter(Adapter):
    """pnpm package manager adapter."""
    
    def __init__(self):
        super().__init__("pnpm", "pnpm", "Fast, disk space efficient npm")
        self.metadata.capabilities = ["install", "publish", "search"]


# ADAPTER-000010: Yarn Adapter
class YarnAdapter(Adapter):
    """Yarn package manager adapter."""
    
    def __init__(self):
        super().__init__("Yarn", "yarn", "Yarn package manager")
        self.metadata.capabilities = ["install", "publish", "workspaces"]


# ADAPTER-000011: Maven Adapter
class MavenAdapter(Adapter):
    """Maven package manager adapter."""
    
    def __init__(self):
        super().__init__("Maven", "maven", "Apache Maven")
        self.metadata.capabilities = ["compile", "test", "package", "deploy"]


# ADAPTER-000012: Gradle Adapter
class GradleAdapter(Adapter):
    """Gradle build tool adapter."""
    
    def __init__(self):
        super().__init__("Gradle", "gradle", "Gradle Build Tool")
        self.metadata.capabilities = ["build", "test", "deploy"]


# ADAPTER-000013: NuGet Adapter
class NuGetAdapter(Adapter):
    """NuGet package manager adapter."""
    
    def __init__(self):
        super().__init__("NuGet", "nuget", ".NET Package Manager")
        self.metadata.capabilities = ["install", "publish", "restore"]


# ADAPTER-000014: Cargo Adapter
class CargoAdapter(Adapter):
    """Cargo package manager adapter."""
    
    def __init__(self):
        super().__init__("Cargo", "cargo", "Rust Package Manager")
        self.metadata.capabilities = ["build", "test", "publish", "install"]


# ADAPTER-000015: Go Modules Adapter
class GoModulesAdapter(Adapter):
    """Go modules adapter."""
    
    def __init__(self):
        super().__init__("GoModules", "go", "Go Module Management")
        self.metadata.capabilities = ["get", "mod", "build", "test"]


# ADAPTER-000016: Composer Adapter
class ComposerAdapter(Adapter):
    """Composer package manager adapter."""
    
    def __init__(self):
        super().__init__("Composer", "composer", "PHP Package Manager")
        self.metadata.capabilities = ["install", "require", "update"]


# ADAPTER-000017: pip Adapter
class PipAdapter(Adapter):
    """pip package manager adapter."""
    
    def __init__(self):
        super().__init__("pip", "pip", "Python Package Installer")
        self.metadata.capabilities = ["install", "search", "download"]


# ADAPTER-000018: Poetry Adapter
class PoetryAdapter(Adapter):
    """Poetry package manager adapter."""
    
    def __init__(self):
        super().__init__("Poetry", "poetry", "Python Dependency Management")
        self.metadata.capabilities = ["install", "add", "build", "publish"]


# Registry
PACKAGE_ADAPTERS = {
    "npm": NpmAdapter,
    "pnpm": PnpmAdapter,
    "yarn": YarnAdapter,
    "maven": MavenAdapter,
    "gradle": GradleAdapter,
    "nuget": NuGetAdapter,
    "cargo": CargoAdapter,
    "go": GoModulesAdapter,
    "composer": ComposerAdapter,
    "pip": PipAdapter,
    "poetry": PoetryAdapter,
}


def get_adapter(name: str):
    """Get a package adapter."""
    adapter_class = PACKAGE_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()