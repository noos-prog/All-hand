#!/usr/bin/env python3
"""
AGOS Enterprise - Test Suite
============================

Tests for the enterprise model components.
Run with: python test_enterprise.py
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hierarchy import (
    Skill, Capability, Service, Department,
    HierarchyLevel, SkillType, ExecutionStatus,
    EnterpriseHierarchy
)
from core_brain import (
    CoreBrain, BrainDecision, BrainDecisionType,
    BrainStrategy, DecisionConfidence, Strategy
)
from provider import (
    Provider, ProviderType, ProviderStatus, ProviderTier,
    ProviderCapability, ProviderMetrics, ProviderPool
)
from marketplace import (
    Marketplace, ProviderListing, ListingStatus, ReviewDecision,
    CertificationResult, SecurityScanResult
)
from capability_pack import (
    CapabilityPack, PackType, PackStatus,
    PackRegistry, PackCapability, PackRequirement,
    create_healthcare_pack, create_fintech_pack
)
from orchestrator import (
    EnterpriseOrchestrator, ExecutionRequest,
    ExecutionPriority, ExecutionState
)
from benchmark import (
    BenchmarkRunner, BenchmarkType, BenchmarkStatus,
    TestCase
)


def test_hierarchy():
    """Test hierarchy module."""
    print("\n=== Testing Hierarchy ===")
    
    # Create skills
    skill_parse = Skill(
        skill_id="skill_parse_json",
        name="Parse JSON",
        description="Parse JSON data",
        skill_type=SkillType.PARSE,
        input_schema='{"type": "object"}',
        output_schema='{"type": "object"}',
    )
    
    skill_format = Skill(
        skill_id="skill_format_output",
        name="Format Output",
        description="Format data for output",
        skill_type=SkillType.FORMAT,
        input_schema='{"type": "object"}',
        output_schema='{"type": "string"}',
    )
    
    # Create capability
    capability = Capability(
        capability_id="cap_json_process",
        name="JSON Processing",
        description="Complete JSON processing",
        skills=(skill_parse, skill_format),
    )
    
    # Create service
    service = Service(
        service_id="svc_data_processing",
        name="Data Processing Service",
        description="Complete data processing",
        capabilities=(capability,),
        department_id="dept_data",
    )
    
    # Create department
    department = Department(
        department_id="dept_data",
        name="Data Department",
        description="Handles all data operations",
        services=(service,),
        priority=1,
    )
    
    # Test hierarchy
    hierarchy = EnterpriseHierarchy()
    hierarchy.register_department(department)
    
    stats = hierarchy.get_statistics()
    print(f"  Departments: {stats['departments']}")
    print(f"  Services: {stats['services']}")
    print(f"  Capabilities: {stats['capabilities']}")
    print(f"  Skills: {stats['skills']}")
    
    # Test path lookup
    path = hierarchy.get_path_to_capability("cap_json_process")
    assert path is not None
    print(f"  Path to capability: {path['department']['name']} > {path['service']['name']}")
    
    # Test capability execution
    result = capability.execute({"data": "test"})
    assert result["success"] == True
    print(f"  Capability execution: {result['success']}")
    
    print("  ✓ Hierarchy tests passed")


def test_core_brain():
    """Test core brain module."""
    print("\n=== Testing Core Brain ===")
    
    # Create brain
    brain = CoreBrain()
    
    # Create strategy
    strategy = Strategy(
        strategy_id="fast_strategy",
        name="Speed Optimized",
        description="Prioritize speed over cost",
        priorities={"speed": 0.6, "cost": 0.2, "quality": 0.2},
        speed_weight=0.6,
        cost_weight=0.2,
        quality_weight=0.2,
    )
    
    # Set strategy
    brain.set_strategy(strategy)
    print(f"  Strategy set: {strategy.name}")
    
    # Test routing
    hierarchy_info = {
        "departments": {
            "dept_qa": {
                "capabilities": ["cap_testing"],
                "availability": 0.9,
            },
            "dept_devops": {
                "capabilities": ["cap_deployment"],
                "availability": 1.0,
            },
        }
    }
    
    decision = brain.route_request(
        request={"type": "test", "capability": "cap_testing"},
        hierarchy_info=hierarchy_info,
    )
    
    print(f"  Routed to: {decision.department_id}")
    print(f"  Decision confidence: {decision.confidence.value}")
    
    # Test budget allocation
    budget_decision = brain.allocate_budget("dept_qa", 5000.0)
    print(f"  Budget allocated: ${budget_decision.estimated_cost}")
    
    # Test approval
    approved, approval_decision = brain.approve_request({
        "request_id": "req_001",
        "estimated_cost": 100.0,
        "department_id": "dept_qa",
    })
    print(f"  Request approved: {approved}")
    
    # Get stats
    stats = brain.get_statistics()
    print(f"  Total decisions: {stats['total_decisions']}")
    
    print("  ✓ Core Brain tests passed")


def test_provider():
    """Test provider module."""
    print("\n=== Testing Provider ===")
    
    # Create provider capability
    provider_cap = ProviderCapability(
        capability_id="cap_json_process",
        skill_ids=("skill_parse_json", "skill_format_output"),
        max_concurrent=3,
        avg_duration_ms=100,
        success_rate=0.98,
    )
    
    # Create provider
    provider = Provider(
        provider_id="prov_json_processor",
        name="JSON Processor",
        description="Processes JSON data",
        provider_type=ProviderType.DATA_PROCESSING,
        capabilities=(provider_cap,),
        certified_at=datetime(2024, 1, 1),
        certification_valid_until=datetime(2025, 1, 1),
    )
    
    print(f"  Provider: {provider.name}")
    print(f"  Is certified: {provider.is_certified()}")
    
    # Test execution
    result = provider.execute(
        skill_id="skill_parse_json",
        input_data={"test": "data"},
    )
    
    print(f"  Execution success: {result['success']}")
    
    # Test health status
    health = provider.get_health_status()
    print(f"  Success rate: {health['metrics']['success_rate']}")
    
    # Test provider pool
    pool = ProviderPool()
    pool.register(provider)
    
    stats = pool.get_statistics()
    print(f"  Pool providers: {stats['total_providers']}")
    
    print("  ✓ Provider tests passed")


def test_marketplace():
    """Test marketplace module."""
    print("\n=== Testing Marketplace ===")
    
    # Create marketplace
    marketplace = Marketplace()
    
    # Create certification
    cert = CertificationResult(
        certified=True,
        certification_id="cert_001",
        certified_at=datetime(2024, 1, 1),
        valid_until=datetime(2025, 1, 1),
        tier="stable",
        authority="AGOS",
    )
    
    # Create security scan
    security = SecurityScanResult(
        scanned=True,
        scan_id="scan_001",
        scanned_at=datetime(2024, 1, 1),
        vulnerabilities_found=0,
        severity="none",
        passed=True,
    )
    
    # Create listing
    listing = ProviderListing(
        listing_id="list_001",
        provider_id="prov_test",
        name="Test Provider",
        description="A test provider",
        provider_type="testing",
        tier="stable",
        capabilities=({"capability_id": "cap_test", "name": "Test"}),
        certification=cert,
        security_scan=security,
        tags=("testing", "qa"),
        documentation_url="https://docs.example.com",
    )
    
    # Register listing
    marketplace.create_listing(listing)
    
    # Submit for review
    marketplace.submit_for_review("list_001")
    print(f"  Listing status: {listing.status.value}")
    
    # Approve listing
    marketplace.review_listing(
        "list_001",
        ReviewDecision.APPROVE,
        "admin",
        "Looks good!"
    )
    print(f"  Approved status: {listing.status.value}")
    
    # Test search
    results = marketplace.search(query="test")
    print(f"  Search results: {len(results)}")
    
    stats = marketplace.get_statistics()
    print(f"  Published listings: {stats['published']}")
    
    print("  ✓ Marketplace tests passed")


def test_capability_pack():
    """Test capability pack module."""
    print("\n=== Testing Capability Pack ===")
    
    # Create registry
    registry = PackRegistry()
    
    # Register built-in packs
    healthcare_pack = create_healthcare_pack()
    fintech_pack = create_fintech_pack()
    
    registry.register(healthcare_pack)
    registry.register(fintech_pack)
    
    print(f"  Registered packs: {len(registry.list_all())}")
    
    # Search packs
    results = registry.search(tags=["compliance"])
    print(f"  Compliance packs: {len(results)}")
    
    # Check requirements
    available_caps = {"cap_hipaa_compliance"}
    available_skills = {"skill_validate_phi", "skill_check_access"}
    
    met, unmet = healthcare_pack.check_requirements_met(
        available_caps,
        available_skills,
    )
    print(f"  Requirements met: {met}")
    
    stats = registry.get_statistics()
    print(f"  Registry stats: {stats}")
    
    print("  ✓ Capability Pack tests passed")


def test_orchestrator():
    """Test orchestrator module."""
    print("\n=== Testing Orchestrator ===")
    
    # Create orchestrator with dependencies
    brain = CoreBrain()
    hierarchy = EnterpriseHierarchy()
    pool = ProviderPool()
    marketplace = Marketplace()
    
    orchestrator = EnterpriseOrchestrator(
        core_brain=brain,
        hierarchy=hierarchy,
        provider_pool=pool,
        marketplace=marketplace,
    )
    
    # Create execution request
    request = ExecutionRequest(
        request_id="req_test_001",
        intent="Run tests on the codebase",
        context={"repo": "test-repo"},
        priority=ExecutionPriority.HIGH,
    )
    
    print(f"  Request: {request.intent}")
    
    # Execute
    result = orchestrator.execute(request)
    print(f"  Execution success: {result.success}")
    print(f"  Events: {len(result.events)}")
    
    metrics = orchestrator.get_metrics()
    print(f"  Total requests: {metrics['total_requests']}")
    
    print("  ✓ Orchestrator tests passed")


def test_benchmark():
    """Test benchmark module."""
    print("\n=== Testing Benchmark ===")
    
    # Create provider
    provider = Provider(
        provider_id="prov_test",
        name="Test Provider",
        description="Test provider",
        provider_type=ProviderType.TESTING,
        capabilities=(
            ProviderCapability(
                capability_id="cap_test",
                skill_ids=("skill_test",),
            ),
        ),
    )
    
    # Create benchmark runner
    runner = BenchmarkRunner()
    
    # Register test cases
    test_cases = [
        TestCase(
            case_id="test_001",
            name="Basic Test",
            input_data={"value": 1},
        ),
        TestCase(
            case_id="test_002",
            name="Edge Case",
            input_data={"value": 100},
        ),
    ]
    runner.register_test_cases("cap_test", test_cases)
    
    # Run benchmark
    result = runner.run_benchmark(
        provider=provider,
        capability_id="cap_test",
        iterations=10,
    )
    
    print(f"  Benchmark status: {result.status.value}")
    print(f"  Score: {result.metrics.score}")
    print(f"  Error rate: {result.metrics.error_rate}")
    print(f"  Recommendation: {result.recommendation}")
    
    stats = runner.get_statistics()
    print(f"  Total benchmarks: {stats['total_benchmarks']}")
    
    print("  ✓ Benchmark tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("AGOS ENTERPRISE - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_hierarchy()
        test_core_brain()
        test_provider()
        test_marketplace()
        test_capability_pack()
        test_orchestrator()
        test_benchmark()
        
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
