"""
Engineering Intelligence Pipeline
PHASE-02: EXECUTION-000003 - Engineering Intelligence Pipeline

Orchestrates the conversion of repositories to Engineering Intelligence Packages.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

from agos_kernel.civilization.intelligence_pipeline.intelligence_package import (
    EngineeringIntelligencePackage,
    RepositoryIdentity,
    RepositoryDNA,
    TechnologyStack,
    ArchitectureSummary,
    DependencyInfo,
    QualityProfile,
    SecurityProfile,
    PerformanceProfile,
    TestingProfile,
    DocumentationProfile,
    EvidencePackage,
    Recommendation,
    TrustLevel,
    RiskLevel,
)
from agos_kernel.civilization.intelligence_pipeline.stages import (
    PipelineStage,
    RepositoryFingerprintStage,
    TechnologyDetectionStage,
    LanguageDetectionStage,
    DependencyResolutionStage,
    ArchitectureAnalysisStage,
    CodeGraphConstructionStage,
    EvidenceGenerationStage,
)


@dataclass
class PipelineResult:
    """Result of pipeline execution."""
    success: bool = False
    package: Optional[EngineeringIntelligencePackage] = None
    stages_completed: List[str] = field(default_factory=list)
    stages_failed: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    execution_time_ms: float = 0.0


class EngineeringIntelligencePipeline:
    """
    Engineering Intelligence Pipeline.
    
    Converts raw repositories into structured Engineering Intelligence Packages.
    
    Pipeline stages:
    1. Repository Fingerprint
    2. Technology Detection
    3. Language Detection
    4. Framework Detection
    5. Dependency Resolution
    6. Repository Structure Analysis
    7. Architecture Analysis
    8. Code Graph Construction
    9. Knowledge Graph Enrichment
    10. Policy Evaluation
    11. Evidence Generation
    12. Repository DNA
    13. Engineering Intelligence Package
    """
    
    VERSION = "1.0"
    
    def __init__(self):
        self.stages: List[PipelineStage] = []
        self._setup_stages()
    
    def _setup_stages(self):
        """Setup pipeline stages."""
        self.stages = [
            RepositoryFingerprintStage(),
            TechnologyDetectionStage(),
            LanguageDetectionStage(),
            DependencyResolutionStage(),
            ArchitectureAnalysisStage(),
            CodeGraphConstructionStage(),
            EvidenceGenerationStage(),
        ]
    
    def run(self, repo_path: str) -> PipelineResult:
        """
        Run the pipeline on a repository.
        
        Returns Engineering Intelligence Package.
        """
        import time
        start_time = time.time()
        
        result = PipelineResult()
        context = {}
        package = EngineeringIntelligencePackage()
        
        print("=" * 60)
        print("ENGINEERING INTELLIGENCE PIPELINE")
        print("=" * 60)
        print(f"Repository: {repo_path}")
        print(f"Pipeline Version: {self.VERSION}")
        print()
        
        # Run each stage
        for i, stage in enumerate(self.stages, 1):
            print(f"[{i}/{len(self.stages)}] Running {stage.name}...")
            
            try:
                stage_result = stage.process(repo_path, context)
                
                if stage_result.success:
                    print(f"  ✓ {stage.name} completed")
                    result.stages_completed.append(stage.name)
                    context[stage.name] = stage_result.data
                    
                    # Enrich package with stage data
                    self._enrich_package(package, stage.name, stage_result.data)
                    
                    if stage_result.warnings:
                        for warning in stage_result.warnings[:2]:
                            print(f"  ⚠ {warning}")
                            package.warnings.append(warning)
                else:
                    print(f"  ✗ {stage.name} failed")
                    result.stages_failed.append(stage.name)
                    if stage_result.errors:
                        result.errors.extend(stage_result.errors)
                        
            except Exception as e:
                print(f"  ✗ {stage.name} error: {e}")
                result.stages_failed.append(stage.name)
                result.errors.append(str(e))
        
        # Calculate execution time
        result.execution_time_ms = (time.time() - start_time) * 1000
        
        # Finalize package
        package.stages_completed = result.stages_completed.copy()
        package.errors = result.errors.copy()
        
        # Calculate trust and risk
        self._calculate_trust_risk(package, context)
        
        # Generate recommendations
        self._generate_recommendations(package, context)
        
        # Generate DNA
        self._generate_dna(package, context)
        
        # Set result
        result.package = package
        result.success = len(result.stages_failed) == 0
        
        print()
        print("=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)
        print(f"Stages Completed: {len(result.stages_completed)}/{len(self.stages)}")
        print(f"Execution Time: {result.execution_time_ms:.2f}ms")
        print(f"Status: {'SUCCESS' if result.success else 'FAILED'}")
        print()
        
        if package.identity.name:
            print(f"Repository: {package.identity.name}")
            print(f"Languages: {', '.join(package.technology_stack.languages.keys())}")
            print(f"Modules: {package.architecture_summary.modules}")
            print(f"Trust Score: {package.trust_score:.1f}")
        
        return result
    
    def _enrich_package(self, package: EngineeringIntelligencePackage, stage: str, data: Dict) -> None:
        """Enrich the package with stage data."""
        if stage == 'repository_fingerprint':
            package.identity.name = data.get('name', '')
            package.identity.url = data.get('remote_url', '')
            package.mark_stage_complete(stage)
        
        elif stage == 'technology_detection':
            tech = TechnologyStack()
            tech.frameworks = data.get('frameworks', [])
            tech.build_systems = data.get('build_systems', [])
            tech.runtimes = data.get('runtimes', [])
            tech.databases = data.get('databases', [])
            package.technology_stack = tech
            package.mark_stage_complete(stage)
        
        elif stage == 'language_detection':
            package.identity.language = data.get('primary_language', '')
            package.technology_stack.languages = data.get('languages', {})
            package.mark_stage_complete(stage)
        
        elif stage == 'dependency_resolution':
            dep = DependencyInfo()
            dep.total_count = data.get('total', 0)
            dep.direct_dependencies = [{'name': d} for d in data.get('direct', [])]
            dep.internal_dependencies = data.get('internal', [])
            package.dependency_info = dep
            package.mark_stage_complete(stage)
        
        elif stage == 'architecture_analysis':
            arch = ArchitectureSummary()
            arch.modules = data.get('modules', 0)
            arch.classes = data.get('classes', 0)
            arch.patterns = data.get('patterns', [])
            package.architecture_summary = arch
            package.mark_stage_complete(stage)
        
        elif stage == 'code_graph_construction':
            package.mark_stage_complete(stage)
        
        elif stage == 'evidence_generation':
            evidence = EvidencePackage()
            evidence.evidence_id = data.get('evidence_id', '')
            evidence.artifacts = data.get('artifacts', [])
            evidence.signatures = data.get('signatures', [])
            package.evidence = evidence
            package.mark_stage_complete(stage)
    
    def _calculate_trust_risk(self, package: EngineeringIntelligencePackage, context: Dict) -> None:
        """Calculate trust and risk scores."""
        trust_score = 50.0
        risk_score = 50.0
        
        # Factors that increase trust
        if package.identity.language:
            trust_score += 10
        if package.architecture_summary.modules > 0:
            trust_score += 10
        if package.dependency_info.total_count > 0:
            trust_score += 5
        if package.technology_stack.frameworks:
            trust_score += 5
        
        # Factors that increase risk
        if len(package.errors) > 5:
            risk_score += 20
        if package.dependency_info.total_count > 100:
            risk_score += 10
        
        # Clamp scores
        trust_score = max(0, min(100, trust_score))
        risk_score = max(0, min(100, risk_score))
        
        package.trust_score = trust_score
        package.trust_level = TrustLevel.HIGH if trust_score > 70 else (
            TrustLevel.MEDIUM if trust_score > 40 else TrustLevel.LOW
        )
        package.risk_level = RiskLevel.LOW if risk_score < 30 else (
            RiskLevel.MEDIUM if risk_score < 60 else RiskLevel.HIGH
        )
    
    def _generate_recommendations(self, package: EngineeringIntelligencePackage, context: Dict) -> None:
        """Generate recommendations."""
        recommendations = []
        
        # Documentation recommendations
        if package.technology_stack.languages and not package.documentation_profile.has_readme:
            recommendations.append(Recommendation(
                priority="high",
                category="documentation",
                title="Add README.md",
                description="Repository lacks a README file",
                effort_hours=1.0,
                impact="Improves discoverability and understanding",
            ))
        
        # Testing recommendations
        if package.testing_profile.test_files == 0:
            recommendations.append(Recommendation(
                priority="medium",
                category="testing",
                title="Add tests",
                description="No test files found",
                effort_hours=8.0,
                impact="Improves code quality and reliability",
            ))
        
        # Dependency recommendations
        if package.dependency_info.total_count > 50:
            recommendations.append(Recommendation(
                priority="low",
                category="dependencies",
                title="Review dependencies",
                description="Large number of dependencies may increase maintenance burden",
                effort_hours=2.0,
                impact="Reduces security and maintenance risk",
            ))
        
        package.recommendations = recommendations
    
    def _generate_dna(self, package: EngineeringIntelligencePackage, context: Dict) -> None:
        """Generate repository DNA."""
        import hashlib
        
        fingerprint_data = context.get('repository_fingerprint', {})
        lang_data = context.get('language_detection', {})
        arch_data = context.get('architecture_analysis', {})
        
        # Calculate hashes
        structure = fingerprint_data.get('hash', '')
        code = str(lang_data.get('languages', {}))
        config = str(package.technology_stack.__dict__)
        
        dna = RepositoryDNA()
        dna.structure_hash = structure
        dna.code_hash = hashlib.sha256(code.encode()).hexdigest()[:16]
        dna.config_hash = hashlib.sha256(config.encode()).hexdigest()[:16]
        dna.dependency_hash = hashlib.sha256(
            str(package.dependency_info.__dict__).encode()
        ).hexdigest()[:16]
        
        dna.combined_hash = hashlib.sha256(
            f"{dna.structure_hash}{dna.code_hash}{dna.config_hash}{dna.dependency_hash}".encode()
        ).hexdigest()[:32]
        
        dna.signature = hashlib.sha256(
            f"{dna.combined_hash}{package.generated_at}".encode()
        ).hexdigest()[:32]
        
        package.dna = dna
    
    def save_package(self, package: EngineeringIntelligencePackage, output_path: str) -> None:
        """Save package to file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(package.to_dict(), f, indent=2, default=str)
        
        print(f"Package saved to: {path}")
    
    def load_package(self, input_path: str) -> EngineeringIntelligencePackage:
        """Load package from file."""
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        # Reconstruct package (simplified)
        package = EngineeringIntelligencePackage()
        package.__dict__.update(data)
        
        return package
