"""DNA Generator - Generate Repository DNA."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
import uuid

from ..domain.repository import Repository
from ..domain.repository_dna import (
    RepositoryDNA, DNAVersion, TechnologyStack, AIStack,
    ArchitecturePattern, Capability, Evidence, DependencyInfo
)
from ..detectors.base_detector import DetectionResult
from .scoring import ScoringEngine


@dataclass
class GenerationContext:
    """Context for DNA generation."""
    repo: Repository
    detections: List[DetectionResult]
    scores: Dict[str, float]


class DNAGenerator:
    """
    DNA Generator v2.
    
    Generates RepositoryDNA v2 with:
    ✅ Identity
    ✅ Technology Stack
    ✅ Architecture
    ✅ Capabilities (with confidence)
    ✅ AI Stack
    ✅ Providers
    ✅ Dependencies
    ✅ Quality Scores
    ✅ Production Readiness
    ✅ Confidence Scores
    ✅ Evidence References
    """
    
    def __init__(self):
        self.scoring_engine = ScoringEngine()
    
    def generate(self, context: GenerationContext) -> RepositoryDNA:
        """Generate Repository DNA from detection results."""
        dna = RepositoryDNA(
            dna_id=str(uuid.uuid4()),
            version=DNAVersion.V2,
            repo_name=context.repo.name,
            repo_url=context.repo.url,
            repo_owner=context.repo.owner,
        )
        
        # Extract technology stack
        dna.technology_stack = self._extract_technology_stack(context)
        
        # Extract architecture patterns
        dna.architecture_patterns = self._extract_architecture_patterns(context)
        
        # Extract capabilities
        dna.capabilities = self._extract_capabilities(context)
        
        # Extract AI stack
        dna.ai_stack = self._extract_ai_stack(context)
        
        # Extract dependencies
        dna.dependencies = self._extract_dependencies(context)
        
        # Calculate scores
        scores = self.scoring_engine.calculate_scores(context.repo, context.detections)
        dna.architecture_score = scores.architecture
        dna.quality_score = scores.quality
        dna.maintainability_score = scores.maintainability
        dna.documentation_score = scores.documentation
        dna.ai_maturity_score = scores.ai_maturity
        dna.production_readiness_score = scores.production_readiness
        
        # Calculate overall confidence
        confidences = [d.confidence for d in context.detections]
        dna.overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Collect evidence
        dna.evidence = self._collect_evidence(context)
        
        return dna
    
    def _extract_technology_stack(self, context: GenerationContext) -> TechnologyStack:
        """Extract technology stack from detections."""
        stack = TechnologyStack()
        
        lang_detection = self._get_detection(context, "LanguageDetector")
        if lang_detection and lang_detection.detected:
            stack.languages = lang_detection.data.get("languages", {})
        
        framework_detection = self._get_detection(context, "FrameworkDetector")
        if framework_detection and framework_detection.detected:
            stack.frameworks = framework_detection.data.get("frameworks", [])
        
        return stack
    
    def _extract_architecture_patterns(
        self,
        context: GenerationContext,
    ) -> List[ArchitecturePattern]:
        """Extract architecture patterns."""
        arch_detection = self._get_detection(context, "ArchitectureDetector")
        if not arch_detection or not arch_detection.detected:
            return []
        
        patterns = []
        for pattern_data in arch_detection.data.get("patterns", []):
            patterns.append(ArchitecturePattern(
                pattern_name=pattern_data["pattern"],
                confidence=pattern_data["confidence"],
            ))
        
        return patterns
    
    def _extract_capabilities(
        self,
        context: GenerationContext,
    ) -> List[Capability]:
        """Extract capabilities."""
        cap_detection = self._get_detection(context, "CapabilityDetector")
        if not cap_detection or not cap_detection.detected:
            return []
        
        capabilities = []
        for cap_data in cap_detection.data.get("capabilities", []):
            capabilities.append(Capability(
                capability_name=cap_data["name"],
                confidence=cap_data["confidence"],
            ))
        
        return capabilities
    
    def _extract_ai_stack(self, context: GenerationContext) -> AIStack:
        """Extract AI stack."""
        ai_stack = AIStack()
        
        ai_detection = self._get_detection(context, "AIStackDetector")
        if ai_detection and ai_detection.detected:
            ai_stack.llm_providers = ai_detection.data.get("llm_providers", [])
            ai_stack.ml_frameworks = ai_detection.data.get("ml_frameworks", [])
            ai_stack.embedding_models = ai_detection.data.get("embedding_models", [])
            ai_stack.vector_databases = ai_detection.data.get("vector_databases", [])
        
        return ai_stack
    
    def _extract_dependencies(
        self,
        context: GenerationContext,
    ) -> List[DependencyInfo]:
        """Extract dependency information."""
        deps_by_manager: Dict[str, List[Dict[str, str]]] = {}
        
        for dep in context.repo.dependencies:
            if dep.package_manager not in deps_by_manager:
                deps_by_manager[dep.package_manager] = []
            deps_by_manager[dep.package_manager].append({
                "name": dep.name,
                "version": dep.version,
            })
        
        return [
            DependencyInfo(
                package_manager=pm,
                dependencies=deps,
            )
            for pm, deps in deps_by_manager.items()
        ]
    
    def _collect_evidence(self, context: GenerationContext) -> List[Evidence]:
        """Collect all evidence."""
        all_evidence = []
        for detection in context.detections:
            all_evidence.extend(detection.evidence)
        return all_evidence
    
    def _get_detection(
        self,
        context: GenerationContext,
        detector_name: str,
    ) -> DetectionResult:
        """Get detection result by detector name."""
        for detection in context.detections:
            if detection.detector_name == detector_name:
                return detection
        return None
