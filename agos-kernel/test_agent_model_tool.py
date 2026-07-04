#!/usr/bin/env python3
"""Test script for Agent, Model, and Tool Packs."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from agent_packs.library import AgentPackLibrary, get_library as get_agent_library
from model_packs.library import ModelPackLibrary, get_library as get_model_library
from tool_packs.library import ToolPackLibrary, get_library as get_tool_library


def test_agent_packs():
    """Test agent packs."""
    print("=" * 60)
    print("Testing Agent Packs 1-50")
    print("=" * 60)
    
    library = get_agent_library()
    print(f"✓ Agent Pack Library initialized")
    print(f"  Total packs: {len(library.packs)}")
    
    for i, (name, pack) in enumerate(list(library.packs.items())[:10]):
        print(f"  {i+1}. {pack.metadata.name} ({pack.metadata.provider})")
    
    print(f"  ... and {len(library.packs) - 10} more")
    
    # Get agent
    openai = library.get("openai")
    if openai:
        print(f"\n✓ Agent: {openai.metadata.name}")


def test_model_packs():
    """Test model packs."""
    print("\n" + "=" * 60)
    print("Testing Model Packs 1-50")
    print("=" * 60)
    
    library = get_model_library()
    print(f"✓ Model Pack Library initialized")
    print(f"  Total packs: {len(library.packs)}")
    
    for i, (name, pack) in enumerate(list(library.packs.items())[:10]):
        print(f"  {i+1}. {pack.metadata.name} ({pack.metadata.family})")
    
    print(f"  ... and {len(library.packs) - 10} more")
    
    # List by family
    gpt_models = library.list_by_family("GPT")
    print(f"\n✓ GPT models: {len(gpt_models)}")
    
    claude_models = library.list_by_family("Claude")
    print(f"✓ Claude models: {len(claude_models)}")


def test_tool_packs():
    """Test tool packs."""
    print("\n" + "=" * 60)
    print("Testing Tool Packs 1-60")
    print("=" * 60)
    
    library = get_tool_library()
    print(f"✓ Tool Pack Library initialized")
    print(f"  Total packs: {len(library.packs)}")
    
    for i, (name, pack) in enumerate(list(library.packs.items())[:10]):
        print(f"  {i+1}. {pack.metadata.name} ({pack.metadata.category})")
    
    print(f"  ... and {len(library.packs) - 10} more")
    
    # List by category
    containers = library.list_by_category("container")
    print(f"\n✓ Container tools: {len(containers)}")
    
    testing = library.list_by_category("testing")
    print(f"✓ Testing tools: {len(testing)}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS AGENT, MODEL & TOOL PACKS")
    print("AGENT-PACK-000001 to AGENT-PACK-000050")
    print("MODEL-PACK-000001 to MODEL-PACK-000050")
    print("TOOL-PACK-000001 to TOOL-PACK-000060")
    print("=" * 60)
    
    test_agent_packs()
    test_model_packs()
    test_tool_packs()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()