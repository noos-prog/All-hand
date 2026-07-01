#!/usr/bin/env python3
"""
AGOS Kernel Integration Test v0.2.0

Tests:
- Auto-discovery of capabilities and providers
- Capability resolver
- Provider resolver
- Execution pipeline

ASSERTIONS:
- Kernel Started
- Auto-discovery worked
- Mission Completed
- Pipeline executed
- Events Published
- Exit Code Success

IF ANY ASSERTION FAILS:
BLOCK ALL FUTURE DEVELOPMENT
FIX KERNEL FIRST
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import AGOSKernel
from events import EventType
from mission import Mission


def assert_condition(condition: bool, message: str):
    """Assert a condition or fail the test."""
    if not condition:
        print(f"\n❌ ASSERTION FAILED: {message}")
        print("\n" + "=" * 60)
        print("KERNEL INTEGRATION TEST FAILED")
        print("BLOCK ALL FUTURE DEVELOPMENT")
        print("FIX KERNEL FIRST")
        print("=" * 60)
        sys.exit(1)
    print(f"✓ {message}")


def main():
    """Run integration test."""
    print("=" * 60)
    print("AGOS KERNEL INTEGRATION TEST v0.2.0")
    print("Auto-Discovery, Resolvers, Pipeline")
    print("=" * 60)
    print()
    
    assertions = {
        "kernel_started": False,
        "discovery_worked": False,
        "capability_registered": False,
        "provider_registered": False,
        "mission_created": False,
        "pipeline_executed": False,
        "dna_generated": False,
        "events_published": False,
        "mission_completed": False
    }
    
    test_url = "https://github.com/All-Hands-AI/OpenHands"
    
    try:
        # 1. Create Kernel with auto-discovery
        print("[1] Creating AGOS Kernel with auto-discovery...")
        kernel = AGOSKernel(base_path=os.path.dirname(os.path.abspath(__file__)))
        print("✓ Kernel created")
        
        # 2. Start kernel (triggers auto-discovery)
        print("\n[2] Starting Kernel (auto-discovery)...")
        kernel.start()
        assertions["kernel_started"] = True
        
        # 3. Check discovery results
        print("\n[3] Checking discovery results...")
        capabilities = kernel.capability_registry.list_all()
        providers = kernel.provider_registry.list_all()
        
        print(f"   Capabilities discovered: {len(capabilities)}")
        for cap in capabilities:
            print(f"   - {cap.name}")
            assertions["capability_registered"] = True
        
        print(f"   Providers discovered: {len(providers)}")
        for prov in providers:
            print(f"   - {prov.name}")
            assertions["provider_registered"] = True
        
        assertions["discovery_worked"] = len(capabilities) > 0 and len(providers) > 0
        
        # 4. Create Mission
        print("\n[4] Creating Mission...")
        mission = Mission(
            name="RepositoryAnalysis",
            description=f"Analyze {test_url}",
            capability="RepositoryAnalysis",
            parameters={"url": test_url, "branch": "main"}
        )
        assertions["mission_created"] = True
        print(f"✓ Mission created: {mission.id}")
        
        # 5. Execute Mission through pipeline
        print("\n[5] Executing Mission through pipeline...")
        result = kernel.mission_manager.execute(mission)
        assertions["pipeline_executed"] = True
        
        # 6. Check Events
        print("\n[6] Checking Events...")
        events = kernel.event_bus.get_events(mission.id)
        event_types = [e.type for e in events]
        
        if EventType.MISSION_STARTED in event_types:
            print("✓ MissionStarted event published")
        if EventType.CAPABILITY_SELECTED in event_types:
            print("✓ CapabilitySelected event published")
        if EventType.PROVIDER_SELECTED in event_types:
            print("✓ ProviderSelected event published")
        if EventType.EXECUTION_STARTED in event_types:
            print("✓ ExecutionStarted event published")
        if EventType.EXECUTION_COMPLETED in event_types:
            print("✓ ExecutionCompleted event published")
        if EventType.MISSION_COMPLETED in event_types:
            assertions["mission_completed"] = True
            print("✓ MissionCompleted event published")
        
        assertions["events_published"] = len(events) > 0
        
        # 7. Check Result
        print("\n[7] Checking Result...")
        if result.is_success:
            dna = result.data
            assertions["dna_generated"] = dna is not None
            print(f"✓ DNA Generated: {dna.name}")
            
            assert_condition(dna.name, "DNA has name")
            assert_condition(len(dna.languages) > 0, "DNA has languages")
            assert_condition(dna.primary_language, "DNA has primary language")
            print(f"✓ DNA Structure Valid")
            
            output_file = "test_output.json"
            with open(output_file, "w") as f:
                json.dump(dna.to_dict(), f, indent=2)
            print(f"✓ DNA saved to {output_file}")
        else:
            print(f"❌ Mission failed: {result.error}")
            sys.exit(1)
        
        # 8. Shutdown
        print("\n[8] Shutting down...")
        kernel.shutdown()
        print("✓ Kernel shutdown")
        
    except Exception as e:
        print(f"\n❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Final Assertions
    print("\n" + "=" * 60)
    print("FINAL ASSERTIONS")
    print("=" * 60)
    
    assert_condition(assertions["kernel_started"], "Kernel Started")
    assert_condition(assertions["discovery_worked"], "Auto-discovery Worked")
    assert_condition(assertions["capability_registered"], "Capability Registered")
    assert_condition(assertions["provider_registered"], "Provider Registered")
    assert_condition(assertions["mission_created"], "Mission Created")
    assert_condition(assertions["pipeline_executed"], "Pipeline Executed")
    assert_condition(assertions["dna_generated"], "DNA Generated")
    assert_condition(assertions["events_published"], "Events Published")
    assert_condition(assertions["mission_completed"], "Mission Completed")
    
    print("\n" + "=" * 60)
    print("✅ ALL ASSERTIONS PASSED")
    print("=" * 60)
    print()
    print("EXEC-000006 to EXEC-000010 COMPLETE")
    print("Auto-discovery, Resolvers, Pipeline working.")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
