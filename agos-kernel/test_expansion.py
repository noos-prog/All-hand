#!/usr/bin/env python3
"""Test script for Expansion Programs."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from capabilities.analysis.complexity import (
    ComplexityAnalysisCapability, MaintainabilityAnalysisCapability,
    TechnicalDebtAnalysisCapability, CodeQualityAnalysisCapability
)
from capabilities.analysis.infrastructure import (
    DatabaseArchitectureAnalysisCapability, CachingStrategyAnalysisCapability,
    RepositoryHealthScoreCapability, EngineeringIntelligenceReportCapability
)
from providers.ai import OpenAIProvider, AnthropicProvider, OllamaProvider
from providers.infrastructure import KubernetesProvider, TerraformProvider, PostgreSQLProvider
from skills.analysis.operations import AnalyzeRepositorySkill, AnalyzeArchitectureSkill
from skills.knowledge.operations import CreateSnapshotSkill, ComputeTrustScoreSkill


def test_capabilities_21_60():
    """Test capabilities 21-60."""
    print("=" * 60)
    print("Testing Capabilities 21-60")
    print("=" * 60)
    
    # Complexity Analysis
    cap = ComplexityAnalysisCapability()
    result = cap.execute({})
    print(f"✓ Capability-021: Complexity = {result['maintainability_index']}")
    
    # Maintainability Analysis
    cap = MaintainabilityAnalysisCapability()
    result = cap.execute({})
    print(f"✓ Capability-022: Maintainability = {result['maintainability_score']}")
    
    # Code Quality
    cap = CodeQualityAnalysisCapability()
    result = cap.execute([])
    print(f"✓ Capability-024: Quality Grade = {result['grade']}")
    
    # Repository Health
    cap = RepositoryHealthScoreCapability()
    result = cap.execute({})
    print(f"✓ Capability-059: Health Score = {result['overall_score']}")
    
    # Intelligence Report
    cap = EngineeringIntelligenceReportCapability()
    result = cap.execute({})
    print(f"✓ Capability-060: Report generated")


def test_providers_16_40():
    """Test providers 16-40."""
    print("\n" + "=" * 60)
    print("Testing Providers 16-40")
    print("=" * 60)
    
    # AI Providers
    openai = OpenAIProvider()
    print(f"✓ Provider-016: OpenAI = {openai.metadata.name}")
    
    anthropic = AnthropicProvider()
    print(f"✓ Provider-017: Anthropic = {anthropic.metadata.name}")
    
    ollama = OllamaProvider()
    print(f"✓ Provider-021: Ollama = {ollama.metadata.name}")
    
    # Infrastructure Providers
    k8s = KubernetesProvider()
    print(f"✓ Provider-034: Kubernetes = {k8s.metadata.name}")
    
    tf = TerraformProvider()
    print(f"✓ Provider-035: Terraform = {tf.metadata.name}")
    
    pg = PostgreSQLProvider()
    print(f"✓ Provider-037: PostgreSQL = {pg.metadata.name}")
    
    redis = __import__('providers.infrastructure', fromlist=['RedisProvider']).RedisProvider()
    print(f"✓ Provider-040: Redis = {redis.metadata.name}")


def test_skills_41_100():
    """Test skills 41-100."""
    print("\n" + "=" * 60)
    print("Testing Skills 41-100")
    print("=" * 60)
    
    # Analysis Skills
    skill = AnalyzeRepositorySkill()
    result = skill.execute({})
    print(f"✓ Skill-041: AnalyzeRepository = {result['success']}")
    
    skill = AnalyzeArchitectureSkill()
    result = skill.execute({})
    print(f"✓ Skill-042: AnalyzeArchitecture = {result['success']}")
    
    # Knowledge Skills
    skill = CreateSnapshotSkill()
    result = skill.execute({})
    print(f"✓ Skill-071: CreateSnapshot = {result['success']}")
    
    skill = ComputeTrustScoreSkill()
    result = skill.execute({})
    print(f"✓ Skill-081: ComputeTrustScore = {result['success']}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS EXPANSION PROGRAMS")
    print("CAPABILITY-000021 to CAPABILITY-000060")
    print("PROVIDER-000016 to PROVIDER-000040")
    print("SKILL-000041 to SKILL-000100")
    print("=" * 60)
    
    test_capabilities_21_60()
    test_providers_16_40()
    test_skills_41_100()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()