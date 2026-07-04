"""Universal Project DNA Generator."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set


@dataclass
class ProjectDNA:
    """Complete DNA of a project."""
    # Identity
    id: str = ""
    name: str = ""
    path: str = ""
    version: str = "1.0.0"
    
    # Technology Stack
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    build_systems: List[str] = field(default_factory=list)
    package_managers: List[str] = field(default_factory=list)
    
    # Architecture
    architecture_style: str = ""
    layers: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)
    
    # Patterns
    patterns: List[str] = field(default_factory=list)
    anti_patterns: List[str] = field(default_factory=list)
    
    # Dependencies
    internal_dependencies: List[str] = field(default_factory=list)
    external_dependencies: List[str] = field(default_factory=list)
    
    # Capabilities
    capabilities: List[str] = field(default_factory=list)
    commands: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    apis: List[str] = field(default_factory=list)
    
    # Providers
    providers: List[str] = field(default_factory=list)
    databases: List[str] = field(default_factory=list)
    queues: List[str] = field(default_factory=list)
    storage: List[str] = field(default_factory=list)
    
    # Knowledge
    knowledge_objects: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    
    # Quality
    complexity_score: float = 0.0
    maintainability_index: float = 0.0
    test_coverage: float = 0.0
    code_quality_score: float = 0.0
    
    # Metrics
    total_files: int = 0
    total_lines: int = 0
    total_functions: int = 0
    total_classes: int = 0
    depth: int = 0
    
    # Evolution
    commit_count: int = 0
    last_commit: Optional[str] = None
    contributors: List[str] = field(default_factory=list)
    
    # Risks
    risks: List[str] = field(default_factory=list)
    technical_debt: List[str] = field(default_factory=list)
    
    # Metadata
    generated_at: datetime = field(default_factory=datetime.now)
    genome_version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "architecture_style": self.architecture_style,
            "capabilities_count": len(self.capabilities),
            "providers_count": len(self.providers),
            "complexity_score": self.complexity_score,
            "maintainability_index": self.maintainability_index,
        }
    
    def to_fingerprint(self) -> str:
        """Generate a fingerprint hash of the project."""
        import hashlib
        
        components = [
            str(sorted(self.languages)),
            str(sorted(self.frameworks)),
            self.architecture_style,
            str(len(self.capabilities)),
        ]
        
        fingerprint = hashlib.md5("|".join(components).encode()).hexdigest()
        return fingerprint
    
    def to_signature(self) -> Dict[str, Any]:
        """Generate a signature for comparison."""
        return {
            "primary_language": self.languages[0] if self.languages else "unknown",
            "primary_framework": self.frameworks[0] if self.frameworks else "none",
            "architecture": self.architecture_style,
            "complexity_bucket": self._get_complexity_bucket(),
            "capabilities_count": len(self.capabilities),
        }
    
    def _get_complexity_bucket(self) -> str:
        """Get complexity bucket."""
        if self.complexity_score < 0.3:
            return "simple"
        elif self.complexity_score < 0.5:
            return "moderate"
        elif self.complexity_score < 0.7:
            return "complex"
        return "very_complex"
    
    def get_genome_summary(self) -> str:
        """Get a summary of the genome."""
        return f"""
Project: {self.name}
Languages: {', '.join(self.languages) or 'None'}
Frameworks: {', '.join(self.frameworks) or 'None'}
Architecture: {self.architecture_style or 'Unknown'}
Capabilities: {len(self.capabilities)}
Providers: {len(self.providers)}
Complexity: {self.complexity_score:.2f}
Maintainability: {self.maintainability_index:.2f}
"""


class ProjectDNAGenerator:
    """Generates DNA for projects."""
    
    def __init__(self, root_path: str):
        """Initialize generator."""
        self.root_path = root_path
        self.dna = ProjectDNA()
    
    def generate(
        self,
        repo_genome: Any = None,
        code_genome: Any = None,
        arch_genome: Any = None,
        capabilities: List[Any] = None,
        providers: List[Any] = None,
        knowledge: Any = None
    ) -> ProjectDNA:
        """Generate complete project DNA."""
        
        self.dna.path = self.root_path
        self.dna.name = self._extract_name()
        
        # Extract from repository genome
        if repo_genome:
            self._extract_from_repo(repo_genome)
        
        # Extract from code genome
        if code_genome:
            self._extract_from_code(code_genome)
        
        # Extract from architecture genome
        if arch_genome:
            self._extract_from_architecture(arch_genome)
        
        # Extract capabilities
        if capabilities:
            self._extract_capabilities(capabilities)
        
        # Extract providers
        if providers:
            self._extract_providers(providers)
        
        # Extract knowledge
        if knowledge:
            self._extract_knowledge(knowledge)
        
        # Calculate derived metrics
        self._calculate_metrics()
        
        # Generate ID
        self.dna.id = self._generate_id()
        
        return self.dna
    
    def _extract_name(self) -> str:
        """Extract project name from path."""
        import os
        return os.path.basename(os.path.abspath(self.root_path))
    
    def _extract_from_repo(self, repo_genome: Any) -> None:
        """Extract data from repository genome."""
        # Languages
        self.dna.languages = [l.value for l in repo_genome.languages]
        
        # Frameworks
        self.dna.frameworks = [f.value for f in repo_genome.frameworks]
        
        # Build systems
        self.dna.build_systems = [b.value for b in repo_genome.build_systems]
        
        # Package managers
        self.dna.package_managers = list(repo_genome.package_managers)
        
        # Metrics
        self.dna.total_files = repo_genome.metrics.total_files
        self.dna.total_lines = repo_genome.metrics.total_lines
        self.dna.depth = repo_genome.metrics.depth
        
        # Providers
        self.dna.databases = [d.value for d in repo_genome.databases]
        self.dna.queues = [q.value for q in repo_genome.queues]
    
    def _extract_from_code(self, code_genome: Any) -> None:
        """Extract data from code genome."""
        self.dna.total_functions = code_genome.total_functions
        self.dna.total_classes = code_genome.total_classes
        self.dna.total_lines = code_genome.total_lines
        
        # Patterns
        self.dna.patterns = [p.type.value for p in code_genome.patterns]
        
        # Quality metrics
        self.dna.complexity_score = code_genome.health.complexity_score
        self.dna.code_quality_score = code_genome.health.maintainability_index
    
    def _extract_from_architecture(self, arch_genome: Any) -> None:
        """Extract data from architecture genome."""
        self.dna.architecture_style = arch_genome.style.value
        self.dna.layers = [l.name for l in arch_genome.layers]
        self.dna.components = list(arch_genome.components.keys())
        
        # Quality
        self.dna.maintainability_index = arch_genome.score.maintainability
        
        # Risks
        self.dna.risks = [r.name for r in arch_genome.risks]
    
    def _extract_capabilities(self, capabilities: List[Any]) -> None:
        """Extract capability information."""
        for cap in capabilities:
            self.dna.capabilities.append(cap.name)
            
            if cap.type == "command":
                self.dna.commands.append(cap.name)
            elif cap.type == "service":
                self.dna.services.append(cap.name)
            elif cap.type == "api":
                self.dna.apis.append(cap.name)
    
    def _extract_providers(self, providers: List[Any]) -> None:
        """Extract provider information."""
        for provider in providers:
            self.dna.providers.append(provider.name)
            
            if provider.type == "database":
                self.dna.databases.append(provider.name)
            elif provider.type == "queue":
                self.dna.queues.append(provider.name)
            elif provider.type == "storage":
                self.dna.storage.append(provider.name)
    
    def _extract_knowledge(self, knowledge: Any) -> None:
        """Extract knowledge information."""
        if hasattr(knowledge, 'knowledge_objects'):
            self.dna.knowledge_objects = [ko.id for ko in knowledge.knowledge_objects]
        
        if hasattr(knowledge, 'decisions'):
            self.dna.decisions = [d.title for d in knowledge.decisions]
    
    def _calculate_metrics(self) -> None:
        """Calculate derived metrics."""
        # Complexity based on multiple factors
        complexity = 0.0
        
        if self.dna.total_files > 100:
            complexity += 0.2
        if self.dna.total_files > 500:
            complexity += 0.2
        if self.dna.total_lines > 10000:
            complexity += 0.1
        if self.dna.total_lines > 100000:
            complexity += 0.2
        
        if len(self.dna.languages) > 2:
            complexity += 0.1
        if len(self.dna.capabilities) > 10:
            complexity += 0.1
        if len(self.dna.providers) > 5:
            complexity += 0.1
        
        self.dna.complexity_score = min(complexity, 1.0)
        
        # Maintainability based on code quality
        if self.dna.code_quality_score > 0:
            self.dna.maintainability_index = self.dna.code_quality_score
        else:
            # Estimate based on structure
            maintainability = 1.0
            if len(self.dna.patterns) < 2:
                maintainability -= 0.2
            if len(self.dna.risks) > 3:
                maintainability -= 0.3
            self.dna.maintainability_index = max(maintainability, 0.0)
    
    def _generate_id(self) -> str:
        """Generate unique ID for the project."""
        import hashlib
        import os
        
        components = [
            self.dna.name,
            str(sorted(self.dna.languages)),
            self.dna.architecture_style,
            self.root_path,
        ]
        
        hash_input = "|".join(components).encode()
        return hashlib.sha256(hash_input).hexdigest()[:16]
