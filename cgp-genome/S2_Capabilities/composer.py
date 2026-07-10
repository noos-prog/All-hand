#!/usr/bin/env python3
"""
CGP - Capability Composer
=========================

Capabilities composed of skills.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class CapabilityCategory(Enum):
    """Categories of capabilities."""
    CODING = "coding"
    REVIEW = "review"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    SECURITY = "security"
    ANALYSIS = "analysis"
    DOCUMENTATION = "documentation"
    MONITORING = "monitoring"
    DATA = "data"
    INTEGRATION = "integration"


@dataclass
class CapabilityMetrics:
    """Metrics for a capability."""
    avg_duration_seconds: int = 30
    avg_cost: float = 0.05
    success_rate: float = 0.9
    sample_size: int = 0
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0


@dataclass
class Capability:
    """
    A capability composed of skills.
    
    Examples:
    - Code Review = Read File + Search Code + Generate Text + Write File
    - Bug Fix = Git Diff + Read Tests + Execute Tests + Generate Patch
    """
    capability_id: str
    name: str
    category: CapabilityCategory
    
    # Description
    description: str = ""
    
    # Composition
    required_skills: Tuple[str, ...] = ()    # Required skill IDs
    optional_skills: Tuple[str, ...] = ()     # Optional skill IDs
    skill_order: Tuple[str, ...] = ()         # Execution order
    
    # Implementation
    default_provider: str = ""               # Default provider ID
    alternative_providers: Tuple[str, ...] = ()
    
    # Metrics
    metrics: CapabilityMetrics = field(default_factory=CapabilityMetrics)
    
    # Quality
    verifiers: Tuple[str, ...] = ()          # Verification methods
    benchmarks: Tuple[str, ...] = ()        # Benchmark IDs
    
    # Schema
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    
    # Difficulty
    difficulty: str = "medium"  # trivial, easy, medium, hard, expert
    
    # Relationships
    composes: Tuple[str, ...] = ()          # Skills this composes
    provides: Tuple[str, ...] = ()          # Other capabilities this provides
    depends_on: Tuple[str, ...] = ()        # Other capabilities this depends on
    
    # Metadata
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: Tuple[str, ...] = ()
    
    def get_total_skill_count(self) -> int:
        """Get total number of skills."""
        return len(self.required_skills) + len(self.optional_skills)
    
    def get_complexity_score(self) -> float:
        """Calculate complexity score based on skills."""
        base = len(self.required_skills) * 0.1
        return min(1.0, base)


@dataclass
class CapabilityExecution:
    """Execution record of a capability."""
    execution_id: str
    capability_id: str
    provider_id: str
    success: bool
    duration_ms: int
    cost: float
    timestamp: str
    skill_results: Dict[str, bool] = field(default_factory=dict)


class CapabilityComposer:
    """
    Composes capabilities from skills.
    """
    
    def __init__(self, skill_registry=None):
        self.skill_registry = skill_registry
        self._composition_templates: Dict[str, List[str]] = {}
        
        # Register default templates
        self._register_default_templates()
    
    def _register_default_templates(self) -> None:
        """Register default composition templates."""
        self._composition_templates = {
            "code_generation": [
                "read_file", "parse_code", "generate_code", "write_file"
            ],
            "code_review": [
                "read_file", "search_code", "lint_code", "generate_text"
            ],
            "bug_fix": [
                "git_diff", "read_file", "search_code", "generate_code", "write_file"
            ],
            "testing": [
                "generate_code", "run_tests", "parse_json", "generate_markdown"
            ],
            "deployment": [
                "read_file", "run_build", "run_command", "call_rest_api"
            ],
            "api_design": [
                "read_file", "generate_code", "format_code", "write_file"
            ],
        }
    
    def compose(
        self,
        capability_id: str,
        name: str,
        category: CapabilityCategory,
        skill_ids: List[str],
        required: List[str] = None,
        optional: List[str] = None
    ) -> Capability:
        """Compose a capability from skills."""
        capability = Capability(
            capability_id=capability_id,
            name=name,
            category=category,
            required_skills=tuple(required or skill_ids),
            optional_skills=tuple(optional or []),
            skill_order=tuple(skill_ids),
            composes=tuple(skill_ids),
        )
        return capability
    
    def compose_from_template(
        self,
        capability_id: str,
        name: str,
        category: CapabilityCategory,
        template_name: str
    ) -> Capability:
        """Compose a capability from a template."""
        if template_name not in self._composition_templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        skill_ids = self._composition_templates[template_name]
        return self.compose(capability_id, name, category, skill_ids)
    
    def decompose(self, capability: Capability) -> List[str]:
        """Get ordered list of skills."""
        return list(capability.skill_order)
    
    def get_dependency_order(self, capability: Capability) -> List[str]:
        """Get skills in dependency order."""
        skills = list(capability.skill_order)
        # In a real implementation, would use topological sort
        return skills


class CapabilityRegistry:
    """
    Registry of all capabilities.
    """
    
    def __init__(self):
        self._capabilities: Dict[str, Capability] = {}
        self._by_category: Dict[CapabilityCategory, List[str]] = {}
        self._by_provider: Dict[str, List[str]] = {}
        self._executions: List[CapabilityExecution] = []
        
        # Register default capabilities
        self._register_default_capabilities()
    
    def _register_default_capabilities(self) -> None:
        """Register default capabilities."""
        default_capabilities = [
            Capability(
                capability_id="code_generation",
                name="Code Generation",
                category=CapabilityCategory.CODING,
                description="Generate code from requirements",
                required_skills=("read_file", "generate_code", "write_file"),
                skill_order=("read_file", "generate_code", "write_file"),
                metrics=CapabilityMetrics(
                    avg_duration_seconds=30,
                    avg_cost=0.05,
                    success_rate=0.9,
                ),
            ),
            Capability(
                capability_id="code_review",
                name="Code Review",
                category=CapabilityCategory.REVIEW,
                description="Review code for issues",
                required_skills=("read_file", "search_code", "lint_code", "generate_text"),
                skill_order=("read_file", "search_code", "lint_code", "generate_text"),
                metrics=CapabilityMetrics(
                    avg_duration_seconds=60,
                    avg_cost=0.10,
                    success_rate=0.85,
                ),
            ),
            Capability(
                capability_id="bug_fix",
                name="Bug Fix",
                category=CapabilityCategory.CODING,
                description="Fix bugs in code",
                required_skills=("git_diff", "search_code", "generate_code", "write_file"),
                skill_order=("git_diff", "search_code", "generate_code", "write_file"),
                metrics=CapabilityMetrics(
                    avg_duration_seconds=120,
                    avg_cost=0.20,
                    success_rate=0.8,
                ),
            ),
            Capability(
                capability_id="testing",
                name="Testing",
                category=CapabilityCategory.TESTING,
                description="Write and run tests",
                required_skills=("generate_code", "run_tests", "parse_json"),
                skill_order=("generate_code", "run_tests", "parse_json"),
                metrics=CapabilityMetrics(
                    avg_duration_seconds=45,
                    avg_cost=0.08,
                    success_rate=0.9,
                ),
            ),
            Capability(
                capability_id="deployment",
                name="Deployment",
                category=CapabilityCategory.DEPLOYMENT,
                description="Deploy application",
                required_skills=("run_build", "run_command", "call_rest_api"),
                skill_order=("run_build", "run_command", "call_rest_api"),
                metrics=CapabilityMetrics(
                    avg_duration_seconds=180,
                    avg_cost=0.30,
                    success_rate=0.85,
                ),
            ),
        ]
        
        for cap in default_capabilities:
            self.register(cap)
    
    def register(self, capability: Capability) -> str:
        """Register a capability."""
        self._capabilities[capability.capability_id] = capability
        
        # Index by category
        if capability.category not in self._by_category:
            self._by_category[capability.category] = []
        self._by_category[capability.category].append(capability.capability_id)
        
        # Index by provider
        if capability.default_provider:
            if capability.default_provider not in self._by_provider:
                self._by_provider[capability.default_provider] = []
            self._by_provider[capability.default_provider].append(capability.capability_id)
        
        return capability.capability_id
    
    def get(self, capability_id: str) -> Optional[Capability]:
        """Get a capability by ID."""
        return self._capabilities.get(capability_id)
    
    def get_by_category(self, category: CapabilityCategory) -> List[Capability]:
        """Get all capabilities in a category."""
        cap_ids = self._by_category.get(category, [])
        return [self._capabilities[cid] for cid in cap_ids if cid in self._capabilities]
    
    def get_by_provider(self, provider_id: str) -> List[Capability]:
        """Get all capabilities by a provider."""
        cap_ids = self._by_provider.get(provider_id, [])
        return [self._capabilities[cid] for cid in cap_ids if cid in self._capabilities]
    
    def search(self, query: str, limit: int = 10) -> List[Capability]:
        """Search capabilities by name or description."""
        query_lower = query.lower()
        results = []
        
        for cap in self._capabilities.values():
            if query_lower in cap.name.lower() or query_lower in cap.description.lower():
                results.append(cap)
        
        return results[:limit]
    
    def find_by_skills(self, skill_ids: List[str]) -> List[Capability]:
        """Find capabilities that use specific skills."""
        results = []
        skill_set = set(skill_ids)
        
        for cap in self._capabilities.values():
            cap_skills = set(cap.required_skills)
            if skill_set & cap_skills:  # Intersection
                results.append(cap)
        
        return results
    
    def record_execution(self, execution: CapabilityExecution) -> None:
        """Record a capability execution."""
        self._executions.append(execution)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        by_category = {cat.value: len(ids) for cat, ids in self._by_category.items()}
        
        return {
            "total_capabilities": len(self._capabilities),
            "by_category": by_category,
            "total_executions": len(self._executions),
            "successful_executions": sum(1 for e in self._executions if e.success),
        }


class CapabilityAnalyzer:
    """
    Analyzes capabilities.
    """
    
    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry
    
    def analyze_coverage(
        self,
        required_capabilities: List[str]
    ) -> Dict[str, Any]:
        """Analyze coverage of required capabilities."""
        covered = []
        missing = []
        
        for cap_id in required_capabilities:
            if self.registry.get(cap_id):
                covered.append(cap_id)
            else:
                missing.append(cap_id)
        
        coverage = len(covered) / len(required_capabilities) if required_capabilities else 0
        
        return {
            "total_required": len(required_capabilities),
            "covered": len(covered),
            "missing": len(missing),
            "coverage": coverage,
            "missing_capabilities": missing,
        }
    
    def analyze_overlap(
        self,
        capability_ids: List[str]
    ) -> Dict[str, Any]:
        """Analyze overlap between capabilities."""
        caps = [self.registry.get(cid) for cid in capability_ids if self.registry.get(cid)]
        
        if len(caps) < 2:
            return {"error": "Need at least 2 capabilities"}
        
        skill_sets = [set(c.required_skills) for c in caps]
        shared = skill_sets[0]
        unique = [set() for _ in caps]
        
        for i, ss in enumerate(skill_sets):
            shared &= ss
            for j, other in enumerate(skill_sets):
                if i != j:
                    unique[i] |= (ss - other)
        
        return {
            "capabilities": [c.capability_id for c in caps],
            "shared_skills": list(shared),
            "unique_skills": [list(u) for u in unique],
            "overlap_percentage": len(shared) / len(skill_sets[0]) if skill_sets[0] else 0,
        }
