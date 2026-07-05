#!/usr/bin/env python3
"""
AGOS Kernel - Main Entry Point

Usage:
    python main.py <github_url> [--branch <branch>]
    
Example:
    python main.py https://github.com/All-Hands-AI/OpenHands
"""
import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from capabilities import RepositoryAnalysisCapability
from core import AutonomousCore
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
    
    print(f"[AGOS] Starting Kernel v1.0.0")
    print(f"[AGOS] Mission: Analyze {url}")
    print("=" * 60)
    
    # Create kernel
    kernel = AutonomousCore()
    kernel.initialize()
    
    # Register capability
    capability = RepositoryAnalysisCapability()
    
    # Create mission
    mission = kernel.create_mission(
        objective=f"Analyze repository {url}",
        context={"url": url, "branch": branch}
    )
    
    print(f"\n[MISSION] Created: {mission.id}")
    print(f"[MISSION] Objective: {mission.objective}")
    print("=" * 60)
    
    # Execute capability directly for now
    print("\n[EXECUTING] Running capability...\n")
    try:
        result = capability.execute({"url": url, "branch": branch})
        
        # Output results
        print("\n" + "=" * 60)
        print("[RESULT]")
        print("[SUCCESS] Mission completed!")
        
        # Save to file
        output_file = "RepositoryDNA.json"
        with open(output_file, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"[OUTPUT] Saved to {output_file}")
        
        # Print summary
        print("\n[DNA SUMMARY]")
        print(f"  Name: {result.name}")
        print(f"  Owner: {result.owner}")
        print(f"  Primary Language: {result.primary_language}")
        print(f"  Languages: {', '.join(result.languages)}")
        print(f"  Frameworks: {', '.join(result.frameworks) if result.frameworks else 'None detected'}")
        print(f"  Package Managers: {', '.join(result.package_managers) if result.package_managers else 'None detected'}")
        print(f"  Config Files: {len(result.config_files)}")
        print(f"  Directories: {len(result.directory_tree)}")
        
    except Exception as e:
        print(f"\n[FAILURE] Mission failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n[AGOS] Kernel stopped")


if __name__ == "__main__":
    main()
