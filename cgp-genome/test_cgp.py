#!/usr/bin/env python3
"""
CGP - Test Suite
===============

Tests for the Capability Genome Project.
Run with: python test_cgp.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
# Add in reverse order (most specific first)
sys.path.insert(0, os.path.join(base_dir, 'S10_Marketplace'))
sys.path.insert(0, os.path.join(base_dir, 'S9_Evolution'))
sys.path.insert(0, os.path.join(base_dir, 'S8_Overlap'))
sys.path.insert(0, os.path.join(base_dir, 'S7_Reuse'))
sys.path.insert(0, os.path.join(base_dir, 'S6_Capability_Graph'))
sys.path.insert(0, os.path.join(base_dir, 'S5_Missions'))
sys.path.insert(0, os.path.join(base_dir, 'S4_Departments'))
sys.path.insert(0, os.path.join(base_dir, 'S3_Services'))
sys.path.insert(0, os.path.join(base_dir, 'S2_Capabilities'))
sys.path.insert(0, os.path.join(base_dir, 'S1_Skills'))

# Skills
from primitive import (
    Skill, SkillCategory, SkillDifficulty,
    SkillRegistry, SkillExtractor
)

# Capabilities
from composer import (
    Capability, CapabilityCategory, CapabilityComposer,
    CapabilityRegistry
)

# Services
from aggregator import (
    Service, ServiceCategory, ServiceAggregator,
    ServiceRegistry
)

# Departments
from organizer import (
    Department, DepartmentDomain, DepartmentOrganizer,
    DepartmentRegistry
)

# Missions
from builder import (
    Mission, MissionStatus, MissionBuilder,
    MissionRegistry, MissionExecutor
)

# Genome
from analyzer import (
    CapabilityGenome, GenomeAnalyzer,
    GenomeGenerator
)

# Reuse
from engine import (
    ReuseEngine, ReuseAnalyzer,
    ReuseStatus
)

# Overlap
from overlap_analyzer import OverlapAnalyzer, OverlapMatrix, SimilarityCalculator

# Evolution
from tracker import (
    EvolutionTracker, EvolutionAnalyzer,
    EvolutionTrend, EvolutionEvent
)

# Marketplace
from marketplace import (
    CapabilityListing, ListingType,
    Marketplace, QualityLevel, PricingModel
)


def test_skills():
    """Test skills module."""
    print("\n=== Testing Skills Module ===")
    
    registry = SkillRegistry()
    print(f"  Total skills: {len(registry._skills)}")
    
    # Get by category
    file_ops = registry.get_by_category(SkillCategory.FILE_OPERATIONS)
    print(f"  File operations: {len(file_ops)}")
    
    # Search
    results = registry.search("read")
    print(f"  Search 'read': {len(results)}")
    
    # Get statistics
    stats = registry.get_statistics()
    print(f"  Categories: {len(stats['by_category'])}")
    
    print("  ✓ Skills module tests passed")


def test_capabilities():
    """Test capabilities module."""
    print("\n=== Testing Capabilities Module ===")
    
    registry = CapabilityRegistry()
    print(f"  Total capabilities: {len(registry._capabilities)}")
    
    # Get by category
    coding_caps = registry.get_by_category(CapabilityCategory.CODING)
    print(f"  Coding capabilities: {len(coding_caps)}")
    
    # Find by skills
    found = registry.find_by_skills(["read_file", "generate_code"])
    print(f"  Found by skills: {len(found)}")
    
    print("  ✓ Capabilities module tests passed")


def test_services():
    """Test services module."""
    print("\n=== Testing Services Module ===")
    
    aggregator = ServiceAggregator()
    registry = ServiceRegistry()
    
    # Create a service
    service = aggregator.aggregate(
        service_id="backend_dev",
        name="Backend Development",
        category=ServiceCategory.BACKEND,
        capability_ids=["api_design", "code_generation", "testing", "deployment"],
    )
    registry.register(service)
    
    print(f"  Service: {service.name}")
    print(f"  Capabilities: {service.get_capability_count()}")
    
    print("  ✓ Services module tests passed")


def test_departments():
    """Test departments module."""
    print("\n=== Testing Departments Module ===")
    
    organizer = DepartmentOrganizer()
    registry = DepartmentRegistry()
    
    # Create a department
    dept = organizer.organize(
        department_id="qa_dept",
        name="QA Department",
        domain=DepartmentDomain.QA,
        service_ids=["testing", "security", "reporting"],
    )
    registry.register(dept)
    
    print(f"  Department: {dept.name}")
    print(f"  Services: {dept.get_service_count()}")
    
    print("  ✓ Departments module tests passed")


def test_missions():
    """Test missions module."""
    print("\n=== Testing Missions Module ===")
    
    builder = MissionBuilder()
    registry = MissionRegistry()
    
    # Create a mission
    mission = builder.build(
        mission_id="build_saas",
        name="Build SaaS",
        department_ids=["backend_dept", "frontend_dept", "qa_dept"],
    )
    registry.register(mission)
    
    print(f"  Mission: {mission.name}")
    print(f"  Departments: {mission.get_department_count()}")
    print(f"  Status: {mission.status.value}")
    
    print("  ✓ Missions module tests passed")


def test_genome():
    """Test genome module."""
    print("\n=== Testing Genome Module ===")
    
    generator = GenomeGenerator()
    analyzer = GenomeAnalyzer()
    
    # Generate genome
    genome = generator.generate(
        project_id="test_project",
        project_name="Test Project",
        skill_ids=["skill_1", "skill_2", "skill_3"],
        capability_ids=["code_generation", "testing"],
    )
    
    print(f"  Genome: {genome.genome_id}")
    print(f"  Skills: {genome.skill_count}")
    print(f"  Capabilities: {genome.capability_count}")
    
    # Analyze
    analysis = analyzer.analyze_quality(genome)
    print(f"  Quality scores: {len(analysis['scores'])}")
    
    print("  ✓ Genome module tests passed")


def test_reuse():
    """Test reuse module."""
    print("\n=== Testing Reuse Module ===")
    
    engine = ReuseEngine()
    analyzer = ReuseAnalyzer(engine)
    
    # Record usage
    engine.record_usage("openhands", "code_generation")
    engine.record_usage("goose", "code_generation")
    engine.record_usage("cline", "code_generation")
    engine.record_usage("openhands", "bug_fix")
    
    # Analyze
    analysis = analyzer.analyze("code_generation")
    print(f"  Capability: {analysis.capability_id}")
    print(f"  Projects: {analysis.project_count}")
    print(f"  Status: {analysis.status.value}")
    
    # Find most reused
    most_reused = analyzer.find_most_reused()
    print(f"  Most reused: {len(most_reused)}")
    
    print("  ✓ Reuse module tests passed")


def test_overlap():
    """Test overlap module."""
    print("\n=== Testing Overlap Module ===")
    
    analyzer = OverlapAnalyzer()
    
    # Register projects
    analyzer.register_project("openhands", ["code_gen", "bug_fix", "testing", "review"])
    analyzer.register_project("goose", ["code_gen", "bug_fix", "deployment"])
    analyzer.register_project("cline", ["code_gen", "testing", "security"])
    
    # Analyze overlap
    overlap = analyzer.analyze_pair("openhands", "goose")
    print(f"  Shared: {len(overlap.shared_capabilities)}")
    print(f"  Unique to OpenHands: {len(overlap.unique_to_a)}")
    print(f"  Jaccard: {overlap.jaccard_index:.2f}")
    
    # Find similar
    similar = analyzer.find_most_similar("openhands")
    print(f"  Most similar: {similar[0] if similar else 'None'}")
    
    print("  ✓ Overlap module tests passed")


def test_evolution():
    """Test evolution module."""
    print("\n=== Testing Evolution Module ===")
    
    tracker = EvolutionTracker()
    analyzer = EvolutionAnalyzer(tracker)
    
    # Record events
    tracker.record_event(EvolutionEvent(
        event_id="e1",
        capability_id="code_generation",
        event_type="added",
        description="First implementation",
        timestamp="2024-01-01",
        project_id="openhands",
    ))
    
    tracker.record_event(EvolutionEvent(
        event_id="e2",
        capability_id="code_generation",
        event_type="added",
        description="Second implementation",
        timestamp="2024-02-01",
        project_id="goose",
    ))
    
    # Analyze
    evolution = analyzer.analyze("code_generation")
    print(f"  Capability: {evolution.capability_id}")
    print(f"  Trend: {evolution.trend.value}")
    print(f"  Adoptions: {evolution.adoption_count}")
    
    print("  ✓ Evolution module tests passed")


def test_marketplace():
    """Test marketplace module."""
    print("\n=== Testing Marketplace Module ===")
    
    marketplace = Marketplace()
    
    # Publish a listing
    listing = CapabilityListing(
        listing_id="list_1",
        capability_id="code_generation",
        name="Advanced Code Generation",
        version="1.0",
        listing_type=ListingType.OFFICIAL,
        quality_level=QualityLevel.CERTIFIED,
        provider_name="AGOS",
        provider_id="agos",
        description="Advanced code generation capability",
        pricing_model=PricingModel.FREE,
    )
    marketplace.publish(listing)
    
    print(f"  Listing: {listing.name}")
    print(f"  Type: {listing.listing_type.value}")
    print(f"  Quality: {listing.quality_level.value}")
    
    # Search
    results = marketplace.search("code")
    print(f"  Search results: {results.total_count}")
    
    print("  ✓ Marketplace module tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CGP - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_skills()
        test_capabilities()
        test_services()
        test_departments()
        test_missions()
        test_genome()
        test_reuse()
        test_overlap()
        test_evolution()
        test_marketplace()
        
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
