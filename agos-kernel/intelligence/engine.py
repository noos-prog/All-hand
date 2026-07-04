"""Universal Engineering Intelligence Platform v2."""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

from .repository.analyzer import RepositoryAnalyzer
from .repository.models import RepositoryGenome
from .code.analyzer import CodeIntelligenceEngine
from .code.models import CodeGenome
from .architecture.analyzer import ArchitectureAnalyzer
from .architecture.models import ArchitectureGenome
from .knowledge import KnowledgeExtractor, KnowledgeExtraction
from .capability import CapabilityDiscoveryEngine, Capability
from .provider import ProviderDiscoveryEngine, ProviderProfile
from .dna import ProjectDNAGenerator, ProjectDNA


@dataclass
class AnalysisReport:
    """Complete analysis report."""
    repository: Optional[RepositoryGenome] = None
    code: Optional[CodeGenome] = None
    architecture: Optional[ArchitectureGenome] = None
    knowledge: Optional[KnowledgeExtraction] = None
    capabilities: List[Capability] = field(default_factory=list)
    providers: List[ProviderProfile] = field(default_factory=list)
    project_dna: Optional[ProjectDNA] = None
    
    # Summary
    summary: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Metadata
    analyzed_at: datetime = field(default_factory=datetime.now)
    analysis_duration_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "repository": self.repository.to_dict() if self.repository else {},
            "code": self.code.to_dict() if self.code else {},
            "architecture": self.architecture.to_dict() if self.architecture else {},
            "capabilities_count": len(self.capabilities),
            "providers_count": len(self.providers),
            "knowledge_count": self.knowledge.total_knowledge if self.knowledge else 0,
            "project_dna": self.project_dna.to_dict() if self.project_dna else {},
            "summary": self.summary,
        }


@dataclass 
class QueryResult:
    """Result of a query."""
    query: str
    results: List[Any] = field(default_factory=list)
    count: int = 0
    score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class EngineeringIntelligencePlatform:
    """
    Universal Engineering Intelligence Platform v2.
    
    Integrates:
    - Repository Intelligence
    - Code Intelligence  
    - Architecture Intelligence
    - Knowledge Extraction
    - Capability Discovery
    - Provider Discovery
    - Project DNA Generation
    - Engineering Index
    - Query Engine
    """
    
    def __init__(self, root_path: str):
        """Initialize platform."""
        self.root_path = Path(root_path)
        self.report: Optional[AnalysisReport] = None
        self.index: Dict[str, Any] = {}
        
        # Components
        self._repo_analyzer = RepositoryAnalyzer(str(self.root_path))
        self._code_engine = CodeIntelligenceEngine(str(self.root_path))
        self._arch_analyzer = ArchitectureAnalyzer(str(self.root_path))
        self._knowledge_extractor = KnowledgeExtractor()
        self._capability_discovery = CapabilityDiscoveryEngine(str(self.root_path))
        self._provider_discovery = ProviderDiscoveryEngine(str(self.root_path))
        self._dna_generator = ProjectDNAGenerator(str(self.root_path))
    
    def analyze(self, options: Optional[Dict[str, bool]] = None) -> AnalysisReport:
        """
        Run complete analysis.
        
        Options:
            - repository: Analyze repository structure (default: True)
            - code: Analyze code (default: True)
            - architecture: Analyze architecture (default: True)
            - knowledge: Extract knowledge (default: True)
            - capabilities: Discover capabilities (default: True)
            - providers: Discover providers (default: True)
            - dna: Generate project DNA (default: True)
        """
        options = options or {
            'repository': True,
            'code': True,
            'architecture': True,
            'knowledge': True,
            'capabilities': True,
            'providers': True,
            'dna': True,
        }
        
        import time
        start_time = time.time()
        
        self.report = AnalysisReport()
        
        # Repository Intelligence
        if options.get('repository'):
            try:
                self.report.repository = self._repo_analyzer.analyze()
            except Exception as e:
                self.report.errors.append(f"Repository analysis failed: {e}")
        
        # Code Intelligence
        if options.get('code'):
            try:
                self.report.code = self._code_engine.analyze()
            except Exception as e:
                self.report.errors.append(f"Code analysis failed: {e}")
        
        # Architecture Intelligence
        if options.get('architecture'):
            try:
                self.report.architecture = self._arch_analyzer.analyze()
            except Exception as e:
                self.report.errors.append(f"Architecture analysis failed: {e}")
        
        # Capability Discovery
        if options.get('capabilities'):
            try:
                self.report.capabilities = self._capability_discovery.discover()
            except Exception as e:
                self.report.errors.append(f"Capability discovery failed: {e}")
        
        # Provider Discovery
        if options.get('providers'):
            try:
                self.report.providers = self._provider_discovery.discover()
            except Exception as e:
                self.report.errors.append(f"Provider discovery failed: {e}")
        
        # Knowledge Extraction
        if options.get('knowledge'):
            try:
                self.report.knowledge = self._knowledge_extractor.extract_from_analysis(
                    repo_genome=self.report.repository,
                    code_genome=self.report.code,
                    arch_genome=self.report.architecture,
                    source_repo=str(self.root_path)
                )
            except Exception as e:
                self.report.errors.append(f"Knowledge extraction failed: {e}")
        
        # Project DNA Generation
        if options.get('dna'):
            try:
                self.report.project_dna = self._dna_generator.generate(
                    repo_genome=self.report.repository,
                    code_genome=self.report.code,
                    arch_genome=self.report.architecture,
                    capabilities=self.report.capabilities,
                    providers=self.report.providers,
                    knowledge=self.report.knowledge
                )
            except Exception as e:
                self.report.errors.append(f"DNA generation failed: {e}")
        
        # Build summary
        self._build_summary()
        
        # Index everything
        self._build_index()
        
        self.report.analysis_duration_seconds = time.time() - start_time
        
        return self.report
    
    def _build_summary(self) -> None:
        """Build analysis summary."""
        if not self.report:
            return
        
        summary = {
            "project_name": self.root_path.name,
            "languages": [],
            "frameworks": [],
            "architecture_style": "unknown",
            "metrics": {},
        }
        
        # Repository summary
        if self.report.repository:
            summary["languages"] = [l.value for l in self.report.repository.languages]
            summary["frameworks"] = [f.value for f in self.report.repository.frameworks]
            summary["metrics"] = {
                "total_files": self.report.repository.metrics.total_files,
                "total_lines": self.report.repository.metrics.total_lines,
                "depth": self.report.repository.metrics.depth,
            }
        
        # Architecture summary
        if self.report.architecture:
            summary["architecture_style"] = self.report.architecture.style.value
        
        self.report.summary = summary
    
    def _build_index(self) -> None:
        """Build search index."""
        if not self.report:
            return
        
        self.index = {
            "files": [],
            "symbols": [],
            "capabilities": [],
            "providers": [],
            "knowledge": [],
        }
        
        # Index files
        if self.report.code:
            self.index["files"] = self.report.code.files
            self.index["symbols"] = [
                {"name": s.name, "type": s.type.value, "file": s.file}
                for s in self.report.code.all_symbols
            ]
        
        # Index capabilities
        self.index["capabilities"] = [
            {"name": c.name, "type": c.type, "path": c.path}
            for c in self.report.capabilities
        ]
        
        # Index providers
        self.index["providers"] = [
            {"name": p.name, "type": p.type, "category": p.category}
            for p in self.report.providers
        ]
        
        # Index knowledge
        if self.report.knowledge:
            self.index["knowledge"] = [
                {"id": ko.id, "type": ko.type, "name": ko.name}
                for ko in self.report.knowledge.knowledge_objects
            ]
    
    # ============ Query Engine ============
    
    def query(self, query_str: str, query_type: str = "all") -> QueryResult:
        """
        Query the indexed data.
        
        Query types:
            - all: Search everywhere
            - file: Search files
            - symbol: Search symbols
            - capability: Search capabilities
            - provider: Search providers
            - knowledge: Search knowledge objects
        """
        query_str_lower = query_str.lower()
        results = []
        
        if query_type == "all":
            # Search everywhere
            results.extend(self._search_index(self.index["files"], query_str_lower, "file"))
            results.extend(self._search_index(self.index["symbols"], query_str_lower, "symbol"))
            results.extend(self._search_index(self.index["capabilities"], query_str_lower, "capability"))
            results.extend(self._search_index(self.index["providers"], query_str_lower, "provider"))
            results.extend(self._search_index(self.index["knowledge"], query_str_lower, "knowledge"))
        
        elif query_type == "file":
            results = self._search_index(self.index["files"], query_str_lower, "file")
        elif query_type == "symbol":
            results = self._search_index(self.index["symbols"], query_str_lower, "symbol")
        elif query_type == "capability":
            results = self._search_index(self.index["capabilities"], query_str_lower, "capability")
        elif query_type == "provider":
            results = self._search_index(self.index["providers"], query_str_lower, "provider")
        elif query_type == "knowledge":
            results = self._search_index(self.index["knowledge"], query_str_lower, "knowledge")
        
        return QueryResult(
            query=query_str,
            results=results,
            count=len(results),
            score=self._calculate_relevance(results, query_str_lower)
        )
    
    def _search_index(self, items: List[Dict], query: str, item_type: str) -> List[Dict]:
        """Search index items."""
        results = []
        for item in items:
            if isinstance(item, str):
                if query in item.lower():
                    results.append({"type": item_type, "value": item})
            else:
                # Check all string values
                for key, value in item.items():
                    if isinstance(value, str) and query in value.lower():
                        results.append({"type": item_type, **item})
                        break
        return results
    
    def _calculate_relevance(self, results: List[Dict], query: str) -> float:
        """Calculate relevance score."""
        if not results:
            return 0.0
        
        # Simple scoring
        exact_matches = sum(1 for r in results if query in str(r.get("name", "")).lower())
        return min(exact_matches / len(results), 1.0)
    
    # ============ Specialized Queries ============
    
    def query_repository(self, query: str) -> List[Any]:
        """Query repository data."""
        if not self.report or not self.report.repository:
            return []
        
        results = []
        repo = self.report.repository
        
        # Search directories
        for d in repo.directories:
            if query.lower() in d.name.lower():
                results.append(d)
        
        # Search modules
        for m in repo.modules:
            if query.lower() in m.name.lower():
                results.append(m)
        
        return results
    
    def query_architecture(self, query: str) -> List[Any]:
        """Query architecture data."""
        if not self.report or not self.report.architecture:
            return []
        
        results = []
        arch = self.report.architecture
        
        # Search components
        for name, comp in arch.components.items():
            if query.lower() in name.lower():
                results.append(comp)
        
        # Search layers
        for layer in arch.layers:
            if query.lower() in layer.name.lower():
                results.append(layer)
        
        return results
    
    def query_dependencies(self, component: str) -> List[str]:
        """Query dependencies of a component."""
        if not self.report or not self.report.code:
            return []
        
        deps = []
        for graph in self.report.code.call_graph:
            if graph.source_file == component or graph.caller == component:
                deps.append(graph.callee)
        
        return deps
    
    def query_symbol_relationships(self, symbol_name: str) -> Dict[str, List[str]]:
        """Query relationships of a symbol."""
        if not self.report or not self.report.code:
            return {}
        
        relationships = {
            "calls": [],
            "called_by": [],
            "imports": [],
            "imported_by": [],
        }
        
        for graph in self.report.code.call_graph:
            if graph.caller == symbol_name:
                relationships["calls"].append(graph.callee)
            if graph.callee == symbol_name:
                relationships["called_by"].append(graph.caller)
        
        for graph in self.report.code.import_graph:
            if graph.source_file == symbol_name:
                relationships["imports"].append(graph.target_module)
        
        return relationships
    
    # ============ Utility Methods ============
    
    def get_capabilities_by_type(self, cap_type: str) -> List[Capability]:
        """Get capabilities by type."""
        if not self.report:
            return []
        return [c for c in self.report.capabilities if c.type == cap_type]
    
    def get_providers_by_type(self, provider_type: str) -> List[ProviderProfile]:
        """Get providers by type."""
        if not self.report:
            return []
        return [p for p in self.report.providers if p.type == provider_type]
    
    def export_report(self, format: str = "json") -> str:
        """Export analysis report."""
        if not self.report:
            return "{}"
        
        if format == "json":
            import json
            return json.dumps(self.report.to_dict(), indent=2)
        elif format == "yaml":
            # Simple YAML conversion
            return str(self.report.to_dict())
        
        return str(self.report)
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get health report."""
        if not self.report:
            return {}
        
        health = {
            "overall": 0.0,
            "details": {},
        }
        
        # Code health
        if self.report.code:
            health["details"]["code"] = {
                "complexity": self.report.code.health.complexity_score,
                "duplication": self.report.code.health.duplication_percentage,
                "coverage": self.report.code.health.test_coverage,
                "doc_coverage": self.report.code.health.doc_coverage,
            }
        
        # Architecture health
        if self.report.architecture:
            health["details"]["architecture"] = {
                "score": self.report.architecture.score.overall,
                "coupling": self.report.architecture.score.coupling,
                "cohesion": self.report.architecture.score.cohesion,
                "violations": len(self.report.architecture.violations),
                "risks": len(self.report.architecture.risks),
            }
        
        # Overall
        if health["details"]:
            health["overall"] = sum(
                d.get("score", d.get("complexity", 0)) 
                for d in health["details"].values()
            ) / len(health["details"])
        
        return health


def analyze_repository(path: str, options: Optional[Dict[str, bool]] = None) -> AnalysisReport:
    """
    Convenience function to analyze a repository.
    
    Usage:
        report = analyze_repository("/path/to/repo")
        print(report.summary)
    """
    platform = EngineeringIntelligencePlatform(path)
    return platform.analyze(options)
