"""Universal Project Intelligence - Understanding any software project."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class AnalysisType(Enum):
    """Types of analysis."""
    ARCHITECTURE = "architecture"
    DEPENDENCIES = "dependencies"
    PATTERNS = "patterns"
    CODE_OWNERSHIP = "code_ownership"
    BUILD_SYSTEM = "build_system"
    TESTING_STRATEGY = "testing_strategy"
    SECURITY = "security"
    PERFORMANCE = "performance"
    TECHNICAL_DEBT = "technical_debt"
    AI_COMPONENTS = "ai_components"


@dataclass
class ProjectGraph:
    """Project dependency graph."""
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    edges: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"nodes": self.nodes, "edges": self.edges}


@dataclass
class DependencyGraph:
    """Package dependency graph."""
    packages: List[str] = field(default_factory=list)
    versions: Dict[str, str] = field(default_factory=dict)
    conflicts: List[str] = field(default_factory=list)


@dataclass
class ArchitectureGraph:
    """Architecture component graph."""
    components: List[str] = field(default_factory=list)
    relationships: List[Dict[str, str]] = field(default_factory=list)
    layers: List[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    """Risk assessment for a project."""
    risk_type: str
    level: str  # low, medium, high, critical
    description: str
    affected_areas: List[str] = field(default_factory=list)
    mitigation: str = ""


@dataclass
class ProjectIntelligenceReport:
    """Complete project intelligence report."""
    project_url: str
    project_name: str
    generated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Analysis results
    architecture: Dict[str, Any] = field(default_factory=dict)
    dependencies: Dict[str, Any] = field(default_factory=dict)
    patterns: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    modules: List[str] = field(default_factory=list)
    
    # Graphs
    project_graph: Optional[ProjectGraph] = None
    dependency_graph: Optional[DependencyGraph] = None
    architecture_graph: Optional[ArchitectureGraph] = None
    
    # Risks
    risks: List[RiskAssessment] = field(default_factory=list)
    
    # Metrics
    total_files: int = 0
    total_lines: int = 0
    complexity_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_url": self.project_url,
            "project_name": self.project_name,
            "generated_at": self.generated_at.isoformat(),
            "architecture": self.architecture,
            "dependencies": self.dependencies,
            "patterns": self.patterns,
            "services": self.services,
            "modules": self.modules,
            "risks": [
                {"type": r.risk_type, "level": r.level, "description": r.description}
                for r in self.risks
            ],
            "metrics": {
                "total_files": self.total_files,
                "total_lines": self.total_lines,
                "complexity_score": self.complexity_score
            }
        }


class ProjectAnalyzer:
    """
    Universal Project Intelligence.
    
    Analyzes:
    - Architecture
    - Dependencies
    - Packages
    - Frameworks
    - Patterns
    - Services
    - Modules
    - Code Ownership
    - Build System
    - Testing Strategy
    - Deployment Strategy
    - Security
    - Performance
    - Technical Debt
    - AI Components
    
    Generates:
    - Project Graph
    - Dependency Graph
    - Architecture Graph
    - Knowledge Graph
    - Risk Graph
    
    Predicts:
    - Refactoring Risk
    - Merge Risk
    - Deployment Risk
    - Security Risk
    - Performance Risk
    """
    
    def __init__(self):
        self.version = "1.0.0"
    
    def analyze(
        self,
        project_path: str,
        files: Dict[str, Any],
        directory_tree: List[str]
    ) -> ProjectIntelligenceReport:
        """Analyze a project."""
        report = ProjectIntelligenceReport(
            project_url=project_path,
            project_name=project_path.split("/")[-1]
        )
        
        # Analyze architecture
        report.architecture = self._analyze_architecture(directory_tree)
        
        # Analyze dependencies
        report.dependencies = self._analyze_dependencies(files)
        
        # Detect patterns
        report.patterns = self._detect_patterns(files)
        
        # Analyze modules
        report.modules = self._analyze_modules(directory_tree)
        
        # Calculate metrics
        report.total_files = len(files)
        report.total_lines = self._count_lines(files)
        report.complexity_score = self._calculate_complexity(files, directory_tree)
        
        # Generate graphs
        report.project_graph = self._generate_project_graph(directory_tree)
        report.architecture_graph = self._generate_architecture_graph(directory_tree)
        
        # Assess risks
        report.risks = self._assess_risks(report)
        
        return report
    
    def _analyze_architecture(self, directories: List[str]) -> Dict[str, Any]:
        """Analyze architecture patterns."""
        arch = {"type": "unknown", "patterns": []}
        
        # Detect common patterns
        if any("domain" in d.lower() for d in directories):
            arch["patterns"].append("clean_architecture")
        if any("adapter" in d.lower() for d in directories):
            arch["patterns"].append("hexagonal")
        if any("service" in d.lower() for d in directories):
            arch["patterns"].append("layered")
        if any("microservice" in d.lower() for d in directories):
            arch["type"] = "microservices"
        elif any("app" in d.lower() for d in directories):
            arch["type"] = "monolith"
        
        return arch
    
    def _analyze_dependencies(self, files: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze dependencies."""
        deps = {"managers": [], "packages": []}
        
        for path in files.keys():
            path_lower = path.lower()
            if "package.json" in path_lower:
                deps["managers"].append("npm")
            if "requirements.txt" in path_lower or "pyproject.toml" in path_lower:
                deps["managers"].append("pip")
            if "go.mod" in path_lower:
                deps["managers"].append("go")
            if "Cargo.toml" in path_lower:
                deps["managers"].append("cargo")
        
        return deps
    
    def _detect_patterns(self, files: Dict[str, Any]) -> List[str]:
        """Detect code patterns."""
        patterns = []
        
        for path in files.keys():
            path_lower = path.lower()
            if "test" in path_lower:
                patterns.append("testing")
            if "docker" in path_lower:
                patterns.append("containerization")
            if "ci" in path_lower or "github" in path_lower:
                patterns.append("ci_cd")
        
        return list(set(patterns))
    
    def _analyze_modules(self, directories: List[str]) -> List[str]:
        """Analyze project modules."""
        modules = set()
        for d in directories:
            parts = d.split("/")
            if len(parts) > 0 and parts[0] not in [".", ".."]:
                modules.add(parts[0])
        return list(modules)
    
    def _count_lines(self, files: Dict[str, Any]) -> int:
        """Count total lines."""
        return 0  # Would need actual file content
    
    def _calculate_complexity(self, files: Dict[str, Any], directories: List[str]) -> float:
        """Calculate complexity score."""
        file_count = len(files)
        dir_count = len(directories)
        return min((file_count + dir_count) / 100, 10.0)
    
    def _generate_project_graph(self, directories: List[str]) -> ProjectGraph:
        """Generate project graph."""
        nodes = [{"id": d, "type": "directory"} for d in directories[:50]]
        return ProjectGraph(nodes=nodes, edges=[])
    
    def _generate_architecture_graph(self, directories: List[str]) -> ArchitectureGraph:
        """Generate architecture graph."""
        components = self._analyze_modules(directories)
        return ArchitectureGraph(components=components, relationships=[])
    
    def _assess_risks(self, report: ProjectIntelligenceReport) -> List[RiskAssessment]:
        """Assess project risks."""
        risks = []
        
        # Complexity risk
        if report.complexity_score > 7:
            risks.append(RiskAssessment(
                risk_type="complexity",
                level="medium",
                description="High complexity score",
                mitigation="Consider refactoring"
            ))
        
        # Dependency risk
        if not report.dependencies.get("managers"):
            risks.append(RiskAssessment(
                risk_type="dependencies",
                level="low",
                description="No dependency managers detected",
                mitigation="Add package manager"
            ))
        
        return risks
