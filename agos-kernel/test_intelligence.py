#!/usr/bin/env python3
"""Test script for Engineering Intelligence Platform."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from intelligence import (
    EngineeringIntelligencePlatform,
    analyze_repository,
)

def test_repository_analysis():
    """Test repository analysis."""
    print("=" * 60)
    print("Testing Repository Analysis")
    print("=" * 60)
    
    platform = EngineeringIntelligencePlatform("/workspace/All-hand/agos-kernel")
    report = platform.analyze()
    
    # Repository
    if report.repository:
        print(f"✓ Repository analyzed")
        print(f"  - Languages: {[l.value for l in report.repository.languages]}")
        print(f"  - Frameworks: {[f.value for f in report.repository.frameworks]}")
        print(f"  - Files: {report.repository.metrics.total_files}")
        print(f"  - Lines: {report.repository.metrics.total_lines}")
    else:
        print("✗ Repository analysis failed")
        if report.errors:
            print(f"  Errors: {report.errors}")
    
    return report

def test_code_analysis(report):
    """Test code analysis."""
    print("\n" + "=" * 60)
    print("Testing Code Analysis")
    print("=" * 60)
    
    if report.code:
        print(f"✓ Code analyzed")
        print(f"  - Files: {len(report.code.files)}")
        print(f"  - Functions: {report.code.total_functions}")
        print(f"  - Classes: {report.code.total_classes}")
        print(f"  - Complexity: {report.code.health.complexity_score:.2f}")
    else:
        print("✗ Code analysis failed")

def test_architecture_analysis(report):
    """Test architecture analysis."""
    print("\n" + "=" * 60)
    print("Testing Architecture Analysis")
    print("=" * 60)
    
    if report.architecture:
        print(f"✓ Architecture analyzed")
        print(f"  - Style: {report.architecture.style.value}")
        print(f"  - Confidence: {report.architecture.confidence:.2f}")
        print(f"  - Layers: {len(report.architecture.layers)}")
        print(f"  - Components: {len(report.architecture.components)}")
        print(f"  - Score: {report.architecture.score.overall:.2f}")
    else:
        print("✗ Architecture analysis failed")

def test_capability_discovery(report):
    """Test capability discovery."""
    print("\n" + "=" * 60)
    print("Testing Capability Discovery")
    print("=" * 60)
    
    if report.capabilities:
        print(f"✓ Capabilities discovered: {len(report.capabilities)}")
        for cap in report.capabilities[:5]:
            print(f"  - {cap.name} ({cap.type})")
        if len(report.capabilities) > 5:
            print(f"  ... and {len(report.capabilities) - 5} more")
    else:
        print("✗ Capability discovery failed")

def test_provider_discovery(report):
    """Test provider discovery."""
    print("\n" + "=" * 60)
    print("Testing Provider Discovery")
    print("=" * 60)
    
    if report.providers:
        print(f"✓ Providers discovered: {len(report.providers)}")
        for provider in report.providers[:5]:
            print(f"  - {provider.name} ({provider.type})")
        if len(report.providers) > 5:
            print(f"  ... and {len(report.providers) - 5} more")
    else:
        print("✗ Provider discovery failed")

def test_project_dna(report):
    """Test project DNA generation."""
    print("\n" + "=" * 60)
    print("Testing Project DNA Generation")
    print("=" * 60)
    
    if report.project_dna:
        print(f"✓ Project DNA generated")
        print(f"  - ID: {report.project_dna.id}")
        print(f"  - Name: {report.project_dna.name}")
        print(f"  - Languages: {report.project_dna.languages}")
        print(f"  - Complexity: {report.project_dna.complexity_score:.2f}")
        print(f"  - Maintainability: {report.project_dna.maintainability_index:.2f}")
    else:
        print("✗ Project DNA generation failed")

def test_knowledge_extraction(report):
    """Test knowledge extraction."""
    print("\n" + "=" * 60)
    print("Testing Knowledge Extraction")
    print("=" * 60)
    
    if report.knowledge:
        print(f"✓ Knowledge extracted: {report.knowledge.total_knowledge} items")
        print(f"  - Best Practices: {len(report.knowledge.best_practices)}")
        print(f"  - Patterns: {len(report.knowledge.patterns)}")
        print(f"  - Decisions: {len(report.knowledge.decisions)}")
        print(f"  - Technologies: {len(report.knowledge.technologies)}")
    else:
        print("✗ Knowledge extraction failed")

def test_query_engine():
    """Test query engine."""
    print("\n" + "=" * 60)
    print("Testing Query Engine")
    print("=" * 60)
    
    platform = EngineeringIntelligencePlatform("/workspace/All-hand/agos-kernel")
    report = platform.analyze()
    
    # Test queries
    result = platform.query("analyzer")
    print(f"✓ Query 'analyzer': {result.count} results")
    
    result = platform.query("test", query_type="file")
    print(f"✓ Query 'test' (files): {result.count} results")

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("ENGINEERING INTELLIGENCE PLATFORM v2 - TEST SUITE")
    print("=" * 60)
    
    # Run tests
    report = test_repository_analysis()
    test_code_analysis(report)
    test_architecture_analysis(report)
    test_capability_discovery(report)
    test_provider_discovery(report)
    test_project_dna(report)
    test_knowledge_extraction(report)
    test_query_engine()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)
    
    # Summary
    print("\nSummary:")
    print(f"  - Analysis completed in {report.analysis_duration_seconds:.2f}s")
    print(f"  - Errors: {len(report.errors)}")
    print(f"  - Warnings: {len(report.warnings)}")

if __name__ == "__main__":
    main()
