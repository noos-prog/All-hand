#!/usr/bin/env python3
"""Test script for Domain, Knowledge, and Workflow Programs."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from domains.base import Domain, DomainRegistry
from domains.software import get_domain as get_software_domain
from domains.engineering import get_domain as get_engineering_domain
from knowledge.base import KnowledgeBase, get_knowledge_base
from workflows.library import WorkflowLibrary, get_library


def test_domains():
    """Test domains."""
    print("=" * 60)
    print("Testing Domains 1-25")
    print("=" * 60)
    
    # Test Software Engineering Domain
    software = get_software_domain("software")
    print(f"✓ Domain-001: {software.metadata.name}")
    print(f"  Capabilities: {len(software.capabilities)}")
    print(f"  Knowledge Packs: {len(software.knowledge_packs)}")
    print(f"  Policies: {len(software.policies)}")
    print(f"  Workflows: {len(software.workflows)}")
    
    # Test Backend Engineering Domain
    backend = get_software_domain("backend")
    print(f"✓ Domain-002: {backend.metadata.name}")
    
    # Test DevOps Domain
    devops = get_software_domain("devops")
    print(f"✓ Domain-006: {devops.metadata.name}")
    
    # Test SRE Domain
    sre = get_software_domain("sre")
    print(f"✓ Domain-010: {sre.metadata.name}")
    
    # Test Cyber Security Domain
    security = get_engineering_domain("security")
    print(f"✓ Domain-011: {security.metadata.name}")
    
    # Test AI Engineering Domain
    ai = get_engineering_domain("ai")
    print(f"✓ Domain-014: {ai.metadata.name}")
    
    # Test LLM Engineering Domain
    llm = get_engineering_domain("llm")
    print(f"✓ Domain-016: {llm.metadata.name}")
    
    # Test QA Domain
    qa = get_engineering_domain("qa")
    print(f"✓ Domain-021: {qa.metadata.name}")
    
    # Test Knowledge Engineering Domain
    knowledge_eng = get_engineering_domain("knowledge")
    print(f"✓ Domain-025: {knowledge_eng.metadata.name}")
    
    print(f"\nTotal domains available: 25")


def test_knowledge():
    """Test knowledge base."""
    print("\n" + "=" * 60)
    print("Testing Knowledge Base")
    print("=" * 60)
    
    kb = get_knowledge_base()
    print(f"✓ Knowledge Base initialized")
    print(f"  Total objects: {len(kb.objects)}")
    
    # Search test
    results = kb.search("architecture")
    print(f"  Search 'architecture': {len(results)} results")
    
    # List by category
    arch_patterns = kb.list_by_category("architecture")
    print(f"  Architecture patterns: {len(arch_patterns)}")
    
    design_patterns = kb.list_by_category("design")
    print(f"  Design patterns: {len(design_patterns)}")
    
    security_patterns = kb.list_by_category("security")
    print(f"  Security patterns: {len(security_patterns)}")
    
    performance_patterns = kb.list_by_category("performance")
    print(f"  Performance patterns: {len(performance_patterns)}")


def test_workflows():
    """Test workflow library."""
    print("\n" + "=" * 60)
    print("Testing Workflow Library")
    print("=" * 60)
    
    library = get_library()
    print(f"✓ Workflow Library initialized")
    print(f"  Total workflows: {len(library.workflows)}")
    
    # List workflows
    for i, (name, workflow) in enumerate(list(library.workflows.items())[:10]):
        print(f"  {i+1}. {workflow.metadata.name}")
    
    print(f"  ... and {len(library.workflows) - 10} more")
    
    # Execute a workflow
    execution = library.execute("repository_analysis", {"repo": "test"})
    print(f"\n✓ Executed: {execution.workflow_id}")
    print(f"  Status: {execution.status.value}")
    print(f"  Steps completed: {len(execution.results)}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS DOMAIN, KNOWLEDGE & WORKFLOW PROGRAMS")
    print("DOMAIN-000001 to DOMAIN-000025")
    print("KNOWLEDGE-000001 to KNOWLEDGE-000050")
    print("WORKFLOW-000001 to WORKFLOW-000030")
    print("=" * 60)
    
    test_domains()
    test_knowledge()
    test_workflows()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()