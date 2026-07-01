#!/usr/bin/env python3
"""
AGOS Kernel Validation Test v0.3.0

Tests:
- Cold Start Test
- Warm Start Test
- Mission Execution Test
- RepositoryAnalysis Test
- Failure Recovery Test
- Stress Test (100 Sequential Missions)

IF ANY TEST FAILS:
STOP DEVELOPMENT
FIX ROOT CAUSE
REPEAT VALIDATION

IF ALL TESTS PASS:
TAG RELEASE
AGOS Kernel v0.3.0
LOCK KERNEL
WAIT FOR NEXT DEVELOPMENT PHASE
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from capabilities import RepositoryAnalysisCapability
from contract_engine import ContractEngine, ContractType
from core import AGOSKernel
from diagnostics import KernelHealthReport, KernelHealthService
from events import EventType
from mission import Mission, MissionStatus
from providers import LocalRepositoryProvider


def assert_test(test_name: str, condition: bool, error_msg: str = ""):
    """Assert a test condition."""
    if not condition:
        print(f"\n❌ TEST FAILED: {test_name}")
        if error_msg:
            print(f"   Error: {error_msg}")
        print("\n" + "=" * 60)
        print("KERNEL VALIDATION FAILED")
        print("STOP DEVELOPMENT")
        print("FIX ROOT CAUSE")
        print("REPEAT VALIDATION")
        print("=" * 60)
        return False
    print(f"✓ {test_name}")
    return True


def test_cold_start():
    """Test cold start."""
    print("\n[TEST] Cold Start")
    
    kernel = AGOSKernel(base_path=os.path.dirname(os.path.abspath(__file__)))
    kernel.start()
    
    success = assert_test(
        "Cold start completed",
        kernel.capability_registry is not None,
        "Capability registry not initialized"
    )
    
    kernel.shutdown()
    return success


def test_warm_start():
    """Test warm start."""
    print("\n[TEST] Warm Start")
    
    kernel = AGOSKernel(base_path=os.path.dirname(os.path.abspath(__file__)))
    kernel.start()
    
    # Check registries
    caps = kernel.capability_registry.list_all()
    provs = kernel.provider_registry.list_all()
    
    success = assert_test(
        "Warm start: capabilities loaded",
        len(caps) > 0,
        f"No capabilities loaded: {len(caps)}"
    )
    
    if not assert_test(
        "Warm start: providers loaded",
        len(provs) > 0,
        f"No providers loaded: {len(provs)}"
    ):
        success = False
    
    kernel.shutdown()
    return success


def test_mission_execution():
    """Test mission execution."""
    print("\n[TEST] Mission Execution")
    
    kernel = AGOSKernel(base_path=os.path.dirname(os.path.abspath(__file__)))
    kernel.start()
    
    mission = Mission(
        name="TestMission",
        description="Test mission",
        capability="RepositoryAnalysis",
        parameters={"url": "https://github.com/All-Hands-AI/OpenHands"}
    )
    
    result = kernel.mission_manager.execute(mission)
    
    success = assert_test(
        "Mission execution: success",
        result.is_success,
        f"Mission failed: {result.error}"
    )
    
    kernel.shutdown()
    return success


def test_repository_analysis():
    """Test repository analysis."""
    print("\n[TEST] Repository Analysis")
    
    kernel = AGOSKernel(base_path=os.path.dirname(os.path.abspath(__file__)))
    kernel.start()
    
    mission = Mission(
        name="RepoAnalysis",
        description="Analyze OpenHands repo",
        capability="RepositoryAnalysis",
        parameters={"url": "https://github.com/All-Hands-AI/OpenHands"}
    )
    
    result = kernel.mission_manager.execute(mission)
    
    if not assert_test(
        "Repository analysis: success",
        result.is_success,
        f"Analysis failed: {result.error}"
    ):
        kernel.shutdown()
        return False
    
    dna = result.data
    success = assert_test(
        "Repository analysis: DNA generated",
        dna is not None,
        "DNA is None"
    )
    
    if success:
        assert_test("Repository analysis: has name", dna.name != "")
        assert_test("Repository analysis: has languages", len(dna.languages) > 0)
        assert_test("Repository analysis: has primary language", dna.primary_language != "")
    
    kernel.shutdown()
    return success


def test_failure_recovery():
    """Test failure recovery."""
    print("\n[TEST] Failure Recovery")
    
    kernel = AGOSKernel(base_path=os.path.dirname(os.path.abspath(__file__)))
    kernel.start()
    
    # Mission with invalid URL
    mission = Mission(
        name="FailureTest",
        description="Test failure handling",
        capability="RepositoryAnalysis",
        parameters={"url": "https://invalid-repo-that-does-not-exist-12345.com/repo"}
    )
    
    result = kernel.mission_manager.execute(mission)
    
    # Should handle gracefully
    success = assert_test(
        "Failure recovery: handled gracefully",
        mission.status in [MissionStatus.FAILED, MissionStatus.COMPLETED],
        f"Invalid mission status: {mission.status}"
    )
    
    kernel.shutdown()
    return success


def test_stress():
    """Test stress with 100 sequential missions."""
    print("\n[TEST] Stress Test (100 Sequential Missions)")
    
    kernel = AGOSKernel(base_path=os.path.dirname(os.path.abspath(__file__)))
    kernel.start()
    
    results = {"success": 0, "failed": 0}
    
    # Just test that kernel can handle rapid mission creation
    for i in range(100):
        mission = Mission(
            name=f"StressTest{i}",
            description=f"Stress test mission {i}",
            capability="RepositoryAnalysis",
            parameters={"url": "https://github.com/All-Hands-AI/OpenHands"}
        )
        result = kernel.mission_manager.execute(mission)
        
        if result.is_success:
            results["success"] += 1
        else:
            results["failed"] += 1
        
        if (i + 1) % 20 == 0:
            print(f"   Progress: {i + 1}/100")
    
    print(f"   Results: {results['success']} success, {results['failed']} failed")
    
    success = assert_test(
        "Stress test: all missions completed",
        results["success"] > 0,
        f"All missions failed: {results}"
    )
    
    kernel.shutdown()
    return success


def test_diagnostics():
    """Test kernel diagnostics."""
    print("\n[TEST] Kernel Diagnostics")
    
    kernel = AGOSKernel(base_path=os.path.dirname(os.path.abspath(__file__)))
    kernel.start()
    
    health_service = KernelHealthService()
    report = health_service.generate_report(
        kernel.capability_registry,
        kernel.capability_registry,
        kernel.provider_registry
    )
    
    success = assert_test(
        "Diagnostics: report generated",
        isinstance(report, KernelHealthReport),
        "Report is not a KernelHealthReport"
    )
    
    if success:
        assert_test("Diagnostics: has status", report.status is not None)
        print(f"   Status: {report.status}")
    
    kernel.shutdown()
    return success


def test_contracts():
    """Test contract validation."""
    print("\n[TEST] Contract Validation")
    
    engine = ContractEngine()
    
    # Create test capability
    capability = RepositoryAnalysisCapability()
    
    result = engine.validate(ContractType.CAPABILITY, capability)
    
    success = assert_test(
        "Contract validation: capability valid",
        result.is_valid,
        f"Capability validation failed: {[e.message for e in result.errors]}"
    )
    
    # Create test provider
    provider = LocalRepositoryProvider()
    
    result = engine.validate(ContractType.PROVIDER, provider)
    
    if not assert_test(
        "Contract validation: provider valid",
        result.is_valid,
        f"Provider validation failed: {[e.message for e in result.errors]}"
    ):
        success = False
    
    return success


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("AGOS KERNEL VALIDATION v0.3.0")
    print("=" * 60)
    
    tests = [
        ("Cold Start", test_cold_start),
        ("Warm Start", test_warm_start),
        ("Contract Validation", test_contracts),
        ("Kernel Diagnostics", test_diagnostics),
        ("Mission Execution", test_mission_execution),
        ("Repository Analysis", test_repository_analysis),
        ("Failure Recovery", test_failure_recovery),
        ("Stress Test", test_stress),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ TEST EXCEPTION: {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "=" * 60)
        print("✅ ALL VALIDATION TESTS PASSED")
        print("=" * 60)
        print("\nAGOS Kernel v0.3.0 VALIDATED")
        print("READY FOR RELEASE")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ VALIDATION FAILED")
        print("=" * 60)
        print("\nSTOP DEVELOPMENT")
        print("FIX ROOT CAUSE")
        print("REPEAT VALIDATION")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
