#!/usr/bin/env python3
"""
AGOS Kernel Integration Test

Tests the complete mission flow:
1. Receive Mission
2. Create Context
3. Select Capability
4. Select Provider
5. Clone Repository
6. Analyze Repository
7. Generate DNA
8. Publish Events
9. Complete Mission

ASSERTIONS:
- Kernel Started
- Mission Completed
- Capability Selected
- Provider Selected
- DNA Generated
- Events Published
- Exit Code Success

IF ANY ASSERTION FAILS:
BLOCK ALL FUTURE DEVELOPMENT
FIX KERNEL FIRST
"""
import json
import sys
import os

# Add kernel to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from capabilities import RepositoryAnalysisCapability
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
    print("AGOS KERNEL INTEGRATION TEST")
    print("=" * 60)
    print()
    
    # Track assertions
    assertions = {
        "kernel_started": False,
        "mission_created": False,
        "capability_selected": False,
        "provider_selected": False,
        "dna_generated": False,
        "events_published": False,
        "mission_completed": False
    }
    
    test_url = "https://github.com/All-Hands-AI/OpenHands"
    
    try:
        # 1. Create Kernel
        print("[1] Creating AGOS Kernel...")
        kernel = AGOSKernel()
        assertions["kernel_started"] = True
        print("✓ Kernel created")
        
        # 2. Register components
        print("\n[2] Registering components...")
        capability = RepositoryAnalysisCapability()
        kernel.capability_registry.register(capability)
        print(f"✓ Capability registered: {capability.name}")
        
        from providers import LocalRepositoryProvider
        provider = LocalRepositoryProvider()
        kernel.provider_registry.register(provider)
        print(f"✓ Provider registered: {provider.name}")
        
        # 3. Start kernel
        print("\n[3] Starting Kernel...")
        kernel.start()
        assertions["kernel_started"] = True
        
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
        
        # 5. Execute Mission
        print("\n[5] Executing Mission...")
        result = kernel.mission_manager.execute(mission)
        
        # 6. Check Events
        print("\n[6] Checking Events...")
        events = kernel.event_bus.get_events(mission.id)
        
        event_types = [e.type for e in events]
        
        if EventType.MISSION_STARTED in event_types:
            print("✓ MissionStarted event published")
        if EventType.CAPABILITY_SELECTED in event_types:
            assertions["capability_selected"] = True
            print("✓ CapabilitySelected event published")
        if EventType.PROVIDER_SELECTED in event_types:
            assertions["provider_selected"] = True
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
            
            # Validate DNA structure
            assert_condition(dna.name, "DNA has name")
            assert_condition(len(dna.languages) > 0, "DNA has languages")
            assert_condition(dna.primary_language, "DNA has primary language")
            print(f"✓ DNA Structure Valid")
            
            # Save DNA
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
    assert_condition(assertions["mission_created"], "Mission Created")
    assert_condition(assertions["capability_selected"], "Capability Selected")
    assert_condition(assertions["provider_selected"], "Provider Selected")
    assert_condition(assertions["dna_generated"], "DNA Generated")
    assert_condition(assertions["events_published"], "Events Published")
    assert_condition(assertions["mission_completed"], "Mission Completed")
    
    print("\n" + "=" * 60)
    print("✅ ALL ASSERTIONS PASSED")
    print("=" * 60)
    print()
    print("AGOS Kernel is working correctly.")
    print("Proceed with EXEC-000002.")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
