"""Universal Engineering Knowledge Extractor."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set


@dataclass
class BestPractice:
    """A best practice."""
    id: str
    name: str
    description: str
    category: str
    evidence: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    source: str = ""
    language: Optional[str] = None
    framework: Optional[str] = None


@dataclass
class CodePattern:
    """A code pattern."""
    id: str
    name: str
    type: str  # creational, structural, behavioral
    description: str
    components: List[str] = field(default_factory=list)
    code_snippets: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)


@dataclass
class AntiPattern:
    """An anti-pattern."""
    id: str
    name: str
    description: str
    symptoms: List[str] = field(default_factory=list)
    consequences: List[str] = field(default_factory=list)
    solutions: List[str] = field(default_factory=list)


@dataclass
class ArchitectureDecision:
    """An architecture decision."""
    id: str
    title: str
    context: str
    decision: str
    rationale: str
    alternatives: List[str] = field(default_factory=list)
    consequences: List[str] = field(default_factory=list)
    status: str = "accepted"


@dataclass
class TechnologyChoice:
    """A technology choice."""
    id: str
    technology: str
    category: str  # language, framework, database, etc.
    purpose: str
    alternatives: List[str] = field(default_factory=list)
    rationale: str = ""


@dataclass
class CodingStandard:
    """Coding standard."""
    id: str
    name: str
    language: str
    rules: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)


@dataclass
class PerformanceOptimization:
    """Performance optimization technique."""
    id: str
    name: str
    description: str
    applicability: List[str] = field(default_factory=list)
    code_examples: List[str] = field(default_factory=list)
    benchmarks: Dict[str, float] = field(default_factory=dict)


@dataclass
class SecurityPractice:
    """Security best practice."""
    id: str
    name: str
    category: str
    description: str
    implementation: str
    references: List[str] = field(default_factory=list)


@dataclass
class TestingStrategy:
    """Testing strategy."""
    id: str
    name: str
    description: str
    types: List[str] = field(default_factory=list)  # unit, integration, e2e
    coverage_target: float = 0.0
    tools: List[str] = field(default_factory=list)


@dataclass
class DeploymentStrategy:
    """Deployment strategy."""
    id: str
    name: str
    description: str
    steps: List[str] = field(default_factory=list)
    rollback_plan: str = ""


@dataclass
class KnowledgeObject:
    """A knowledge object."""
    id: str
    type: str  # best_practice, pattern, anti_pattern, etc.
    name: str
    content: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    source_repository: str = ""
    confidence: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class KnowledgeExtraction:
    """Result of knowledge extraction."""
    best_practices: List[BestPractice] = field(default_factory=list)
    patterns: List[CodePattern] = field(default_factory=list)
    anti_patterns: List[AntiPattern] = field(default_factory=list)
    decisions: List[ArchitectureDecision] = field(default_factory=list)
    technologies: List[TechnologyChoice] = field(default_factory=list)
    coding_standards: List[CodingStandard] = field(default_factory=list)
    optimizations: List[PerformanceOptimization] = field(default_factory=list)
    security_practices: List[SecurityPractice] = field(default_factory=list)
    testing_strategies: List[TestingStrategy] = field(default_factory=list)
    deployment_strategies: List[DeploymentStrategy] = field(default_factory=list)
    
    knowledge_objects: List[KnowledgeObject] = field(default_factory=list)
    
    @property
    def total_knowledge(self) -> int:
        """Total knowledge items extracted."""
        return (
            len(self.best_practices) +
            len(self.patterns) +
            len(self.anti_patterns) +
            len(self.decisions) +
            len(self.technologies) +
            len(self.coding_standards) +
            len(self.optimizations) +
            len(self.security_practices) +
            len(self.testing_strategies) +
            len(self.deployment_strategies)
        )


class KnowledgeExtractor:
    """Extracts reusable engineering knowledge from projects."""
    
    def __init__(self):
        """Initialize extractor."""
        self.extraction = KnowledgeExtraction()
    
    def extract_from_analysis(
        self,
        repo_genome: Any = None,
        code_genome: Any = None,
        arch_genome: Any = None,
        source_repo: str = ""
    ) -> KnowledgeExtraction:
        """Extract knowledge from analysis results."""
        
        # Extract best practices
        if code_genome:
            self._extract_from_code(code_genome, source_repo)
        
        # Extract architecture decisions
        if arch_genome:
            self._extract_from_architecture(arch_genome, source_repo)
        
        # Extract technologies
        if repo_genome:
            self._extract_from_repository(repo_genome, source_repo)
        
        # Convert to knowledge objects
        self._create_knowledge_objects(source_repo)
        
        return self.extraction
    
    def _extract_from_code(self, code_genome: Any, source_repo: str) -> None:
        """Extract knowledge from code analysis."""
        
        # Extract patterns
        for pattern in code_genome.patterns:
            self.extraction.patterns.append(CodePattern(
                id=f"pattern_{pattern.type.value}_{len(self.extraction.patterns)}",
                name=pattern.name,
                type=self._classify_pattern_type(pattern.type.value),
                description=pattern.description,
                components=[p.file for p in code_genome.patterns if p.type == pattern.type],
                use_cases=["General use case"]
            ))
        
        # Extract best practices
        for symbol in code_genome.all_symbols:
            if symbol.docstring:
                self.extraction.best_practices.append(BestPractice(
                    id=f"bp_{symbol.name}_{len(self.extraction.best_practices)}",
                    name=f"Document {symbol.type.value}: {symbol.name}",
                    description=symbol.docstring,
                    category="documentation",
                    evidence=[f"{symbol.file}:{symbol.location.line}"]
                ))
    
    def _extract_from_architecture(self, arch_genome: Any, source_repo: str) -> None:
        """Extract knowledge from architecture analysis."""
        
        # Extract architecture decisions
        if arch_genome.style:
            self.extraction.decisions.append(ArchitectureDecision(
                id=f"adr_{len(self.extraction.decisions) + 1}",
                title=f"Architecture Style: {arch_genome.style.value}",
                context="Architecture style selection",
                decision=arch_genome.style.value,
                rationale=f"Detected with {arch_genome.confidence * 100:.0f}% confidence",
                status="accepted"
            ))
        
        # Extract best practices from layers
        for layer in arch_genome.layers:
            self.extraction.best_practices.append(BestPractice(
                id=f"bp_layer_{layer.name}_{len(self.extraction.best_practices)}",
                name=f"Layer separation: {layer.name}",
                description=f"Layer type: {layer.type.value}",
                category="architecture",
                evidence=[f"Layer at level {layer.level}"]
            ))
    
    def _extract_from_repository(self, repo_genome: Any, source_repo: str) -> None:
        """Extract knowledge from repository analysis."""
        
        # Extract technology choices
        for lang in repo_genome.languages:
            self.extraction.technologies.append(TechnologyChoice(
                id=f"tech_{lang.value}_{len(self.extraction.technologies)}",
                technology=lang.value,
                category="language",
                purpose="Primary development language",
                rationale=f"Found in {repo_genome.metrics.languages.get(lang.value, 0)} files"
            ))
        
        # Extract framework choices
        for framework in repo_genome.frameworks:
            self.extraction.technologies.append(TechnologyChoice(
                id=f"tech_{framework.value}_{len(self.extraction.technologies)}",
                technology=framework.value,
                category="framework",
                purpose="Development framework"
            ))
        
        # Extract testing strategy
        if repo_genome.test_frameworks:
            self.extraction.testing_strategies.append(TestingStrategy(
                id=f"test_{len(self.extraction.testing_strategies)}",
                name="Testing framework usage",
                description="Testing frameworks detected in project",
                types=["unit", "integration"],
                tools=list(repo_genome.test_frameworks)
            ))
    
    def _classify_pattern_type(self, pattern_name: str) -> str:
        """Classify pattern type."""
        if pattern_name in ['singleton', 'factory', 'builder', 'prototype']:
            return 'creational'
        elif pattern_name in ['adapter', 'decorator', 'facade', 'proxy', 'composite']:
            return 'structural'
        elif pattern_name in ['observer', 'strategy', 'command', 'state']:
            return 'behavioral'
        return 'architectural'
    
    def _create_knowledge_objects(self, source_repo: str) -> None:
        """Convert extracted knowledge to knowledge objects."""
        
        # Best practices
        for bp in self.extraction.best_practices:
            self.extraction.knowledge_objects.append(KnowledgeObject(
                id=bp.id,
                type="best_practice",
                name=bp.name,
                content={
                    "description": bp.description,
                    "category": bp.category,
                    "evidence": bp.evidence,
                    "examples": bp.examples
                },
                tags=[bp.category, bp.language or "general"],
                source_repository=source_repo
            ))
        
        # Patterns
        for p in self.extraction.patterns:
            self.extraction.knowledge_objects.append(KnowledgeObject(
                id=p.id,
                type="pattern",
                name=p.name,
                content={
                    "type": p.type,
                    "description": p.description,
                    "components": p.components,
                    "use_cases": p.use_cases
                },
                tags=[p.type, "design"],
                source_repository=source_repo
            ))
        
        # Decisions
        for d in self.extraction.decisions:
            self.extraction.knowledge_objects.append(KnowledgeObject(
                id=d.id,
                type="architecture_decision",
                name=d.title,
                content={
                    "context": d.context,
                    "decision": d.decision,
                    "rationale": d.rationale,
                    "alternatives": d.alternatives,
                    "status": d.status
                },
                tags=["architecture", "decision"],
                source_repository=source_repo
            ))
