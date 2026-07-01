#!/usr/bin/env python3
"""
AGOS Kernel - Main Entry Point

Usage:
    python main.py <github_url> [--branch <branch>]
    
Example:
    python main.py https://github.com/All-Hands-AI/OpenHands
"""
import json
import sys
from datetime import datetime

from capabilities import RepositoryAnalysisCapability
from core import AGOSKernel
from mission import Mission


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <github_url> [--branch <branch>]")
        sys.exit(1)
    
    url = sys.argv[1]
    branch = "main"
    
    # Parse arguments
    if len(sys.argv) > 3 and sys.argv[2] == "--branch":
        branch = sys.argv[3]
    
    print(f"[AGOS] Starting Kernel v0.1.0")
    print(f"[AGOS] Mission: Analyze {url}")
    print("=" * 60)
    
    # Create kernel
    kernel = AGOSKernel()
    
    # Register capability
    capability = RepositoryAnalysisCapability()
    kernel.capability_registry.register(capability)
    
    # Register provider
    from providers import LocalRepositoryProvider
    provider = LocalRepositoryProvider()
    kernel.provider_registry.register(provider)
    
    # Start kernel
    kernel.start()
    
    # Create mission
    mission = Mission(
        name="RepositoryAnalysis",
        description=f"Analyze repository {url}",
        capability="RepositoryAnalysis",
        parameters={"url": url, "branch": branch}
    )
    
    print(f"\n[MISSION] Created: {mission.id}")
    print(f"[MISSION] Capability: {mission.capability}")
    print("=" * 60)
    
    # Execute mission
    print("\n[EXECUTING] Starting mission execution...\n")
    result = kernel.mission_manager.execute(mission)
    
    # Output results
    print("\n" + "=" * 60)
    print("[RESULT]")
    
    if result.is_success:
        print("[SUCCESS] Mission completed!")
        dna = result.data
        
        # Save to file
        output_file = "RepositoryDNA.json"
        with open(output_file, "w") as f:
            json.dump(dna.to_dict(), f, indent=2)
        print(f"[OUTPUT] Saved to {output_file}")
        
        # Print summary
        print("\n[DNA SUMMARY]")
        print(f"  Name: {dna.name}")
        print(f"  Owner: {dna.owner}")
        print(f"  Primary Language: {dna.primary_language}")
        print(f"  Languages: {', '.join(dna.languages)}")
        print(f"  Frameworks: {', '.join(dna.frameworks) if dna.frameworks else 'None detected'}")
        print(f"  Package Managers: {', '.join(dna.package_managers) if dna.package_managers else 'None detected'}")
        print(f"  Config Files: {len(dna.config_files)}")
        print(f"  Directories: {len(dna.directory_tree)}")
        
    else:
        print(f"[FAILURE] Mission failed: {result.error}")
        sys.exit(1)
    
    # Print events
    print("\n" + "=" * 60)
    print("[EVENTS]")
    events = kernel.event_bus.get_events(mission.id)
    for event in events:
        print(f"  [{event.timestamp.strftime('%H:%M:%S')}] {event.type.value}")
    
    # Cleanup
    kernel.shutdown()
    print("\n[AGOS] Kernel stopped")


if __name__ == "__main__":
    main()
