#!/usr/bin/env python3
"""
ARI - Test Suite
===============

Tests for the AGOS Research Infrastructure.
Run with: python test_ari.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, '01-Research-Data-Lake'))
sys.path.insert(0, os.path.join(base_dir, '06-Evaluation-Engine'))
sys.path.insert(0, os.path.join(base_dir, '10-Dashboards'))

from repository import (
    Repository, RepositoryMetrics, RepositoryDataLake,
    Language, RepositoryStatus
)
from provider import (
    Provider, ProviderMetrics, ProviderRegistry,
    ProviderType, ProviderStatus
)
from benchmark import (
    Benchmark, BenchmarkSuite, BenchmarkCase,
    BenchmarkRunner, BenchmarkType
)
from engine import (
    EvaluationEngine, EvaluationTask, TaskType
)
from sandbox import (
    Sandbox, SandboxFactory, SecurityPolicy,
    SecurityLevel, SandboxType
)
from judge import (
    JudgeEngine, JudgementCriteria, JudgementType
)
from genome import (
    GenomeEngine, Genome, Gene, GeneType
)
from leaderboard import (
    Leaderboard, LeaderboardEntry, RankingEngine, RankingType
)
from reports import (
    ReportGenerator, ReportType, ReportFormat
)


def test_repository():
    """Test repository module."""
    print("\n=== Testing Repository Module ===")
    
    # Create repository
    repo = Repository(
        repo_id="repo_001",
        name="example-repo",
        full_name="user/example-repo",
        url="https://github.com/user/example-repo",
        description="An example repository",
        primary_language=Language.PYTHON,
        topics=("ai", "ml"),
    )
    repo.metrics.stars = 1000
    repo.metrics.has_readme = True
    repo.metrics.has_license = True
    
    print(f"  Repository: {repo.full_name}")
    print(f"  Language: {repo.primary_language.value}")
    print(f"  Stars: {repo.metrics.stars}")
    print(f"  Health: {repo.metrics.get_health_score():.1%}")
    
    # Test data lake
    lake = RepositoryDataLake()
    lake.add_repository(repo)
    
    results = lake.search(language=Language.PYTHON, min_stars=500)
    print(f"  Search results: {len(results)}")
    
    print("  ✓ Repository module tests passed")


def test_provider():
    """Test provider module."""
    print("\n=== Testing Provider Module ===")
    
    # Create provider
    provider = Provider(
        provider_id="provider_001",
        name="openai",
        provider_type=ProviderType.LLM,
        display_name="OpenAI GPT-4",
        description="OpenAI's GPT-4 model",
        capabilities=("text-generation", "coding", "reasoning"),
    )
    provider.metrics.success_rate = 0.95
    provider.metrics.avg_latency_ms = 500
    provider.metrics.cost_per_request = 0.03
    
    print(f"  Provider: {provider.display_name}")
    print(f"  Success Rate: {provider.metrics.success_rate:.1%}")
    print(f"  Overall Score: {provider.metrics.get_overall_score():.1%}")
    
    # Test registry
    registry = ProviderRegistry()
    registry.register(provider)
    
    providers = registry.search(provider_type=ProviderType.LLM)
    print(f"  Registry search: {len(providers)}")
    
    print("  ✓ Provider module tests passed")


def test_benchmark():
    """Test benchmark module."""
    print("\n=== Testing Benchmark Module ===")
    
    # Create benchmark suite
    cases = [
        BenchmarkCase(
            case_id="case_001",
            name="API Generation",
            description="Generate a REST API",
            input_data={"spec": "openapi"},
            difficulty="medium",
        ),
        BenchmarkCase(
            case_id="case_002",
            name="Bug Fix",
            description="Fix a bug in Python code",
            input_data={"code": "def foo(): pass"},
            difficulty="easy",
        ),
    ]
    
    suite = BenchmarkSuite(
        suite_id="suite_001",
        name="Code Generation Suite",
        description="Tests for code generation",
        cases=tuple(cases),
        benchmark_type=BenchmarkType.INTEGRATION,
    )
    
    print(f"  Suite: {suite.name}")
    print(f"  Cases: {len(suite.cases)}")
    
    # Test runner
    runner = BenchmarkRunner()
    
    print("  ✓ Benchmark module tests passed")


def test_evaluation():
    """Test evaluation engine."""
    print("\n=== Testing Evaluation Engine ===")
    
    # Create task
    task = EvaluationTask(
        task_id="task_001",
        name="Generate API",
        description="Generate a REST API",
        task_type=TaskType.CODE_GENERATION,
        prompt="Create a REST API with Flask",
        difficulty="medium",
    )
    
    print(f"  Task: {task.name}")
    print(f"  Type: {task.task_type.value}")
    
    # Test engine
    engine = EvaluationEngine()
    print(f"  Engine initialized: {engine is not None}")
    
    print("  ✓ Evaluation engine tests passed")


def test_sandbox():
    """Test sandbox module."""
    print("\n=== Testing Sandbox Module ===")
    
    # Create sandbox
    policy = SecurityPolicy(
        security_level=SecurityLevel.HIGH,
        allow_network=False,
        allow_subprocess=False,
    )
    
    factory = SandboxFactory()
    sandbox = factory.create_isolated_sandbox("python")
    
    # Execute code
    result = sandbox.execute("print('Hello, World!')", "python")
    
    print(f"  Execution: {result.success}")
    print(f"  Output: {result.stdout.strip()}")
    
    print("  ✓ Sandbox module tests passed")


def test_judge():
    """Test judge engine."""
    print("\n=== Testing Judge Engine ===")
    
    # Create judge
    engine = JudgeEngine()
    
    # Create config
    criteria = [
        {"name": "Correctness", "weight": 2.0, "pass_threshold": 80.0},
        {"name": "Readability", "weight": 1.0, "pass_threshold": 70.0},
    ]
    
    config = engine.create_config("Code Quality", criteria)
    
    print(f"  Config: {config.name}")
    print(f"  Criteria: {len(config.criteria)}")
    
    print("  ✓ Judge engine tests passed")


def test_genome():
    """Test genome engine."""
    print("\n=== Testing Genome Engine ===")
    
    # Create genome
    engine = GenomeEngine()
    
    genes = [
        {"name": "coding", "type": "capability", "value": 0.9},
        {"name": "reasoning", "type": "capability", "value": 0.95},
        {"name": "speed", "type": "trait", "value": 0.8},
    ]
    
    genome = engine.create_genome("TestAgent", "coding_agent", genes)
    
    print(f"  Genome: {genome.name}")
    print(f"  Genes: {len(genome.genes)}")
    
    # Analyze
    analysis = engine.analyze_genome(genome.genome_id)
    print(f"  Capabilities: {analysis.get('capabilities', {}).get('capability_count', 0)}")
    
    print("  ✓ Genome engine tests passed")


def test_leaderboard():
    """Test leaderboard module."""
    print("\n=== Testing Leaderboard Module ===")
    
    # Create provider data
    providers = [
        {"provider_id": "p1", "name": "Provider A", "success_rate": 0.9, "avg_latency_ms": 500},
        {"provider_id": "p2", "name": "Provider B", "success_rate": 0.85, "avg_latency_ms": 400},
        {"provider_id": "p3", "name": "Provider C", "success_rate": 0.95, "avg_latency_ms": 600},
    ]
    
    # Create leaderboard
    engine = RankingEngine()
    leaderboard = engine.rank_providers(providers)
    
    print(f"  Leaderboard: {leaderboard.name}")
    print(f"  Entries: {leaderboard.total_entries}")
    
    top = leaderboard.get_top(3)
    print(f"  Top 3:")
    for entry in top:
        print(f"    {entry.rank}. {entry.entity_name} - {entry.overall_score:.1%}")
    
    print("  ✓ Leaderboard module tests passed")


def test_reports():
    """Test reports module."""
    print("\n=== Testing Reports Module ===")
    
    # Create generator
    generator = ReportGenerator()
    
    # Generate report
    report = generator.generate_report(
        report_type=ReportType.SUMMARY_REPORT,
        title="Test Report",
        sections=[
            {"title": "Overview", "content": "This is a test report."},
            {"title": "Results", "content": "All tests passed."},
        ],
        summary="Test summary.",
    )
    
    print(f"  Report: {report.title}")
    print(f"  Sections: {len(report.sections)}")
    
    # Format
    json_output = generator.format_report(report, ReportFormat.JSON)
    print(f"  Format: JSON ({len(json_output)} chars)")
    
    print("  ✓ Reports module tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("ARI - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_repository()
        test_provider()
        test_benchmark()
        test_evaluation()
        test_sandbox()
        test_judge()
        test_genome()
        test_leaderboard()
        test_reports()
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
