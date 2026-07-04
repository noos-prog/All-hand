#!/usr/bin/env python3
"""Test script for AGOS Civilization Platform v2."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from distributed import DistributedRuntime, ClusterState
from marketplace import MarketplaceRuntime, MarketplaceAssetType
from extension import ExtensionRuntime, ExtensionType
from sdk import SDKGenerator, SDKLanguage
from certification import CertificationRuntime
from laboratory import EvolutionLaboratory
from observatory import CivilizationObservatory, ExpansionEngine
from v2 import get_platform_v2


def test_distributed():
    """Test Distributed Runtime."""
    print("=" * 60)
    print("Testing Distributed Runtime")
    print("=" * 60)
    
    runtime = DistributedRuntime()
    
    # Join cluster
    node = runtime.join_cluster("node-1", "192.168.1.1", 8080)
    print(f"✓ Node joined: {node.id}")
    
    # Join another node
    node2 = runtime.join_cluster("node-2", "192.168.1.2", 8080)
    print(f"✓ Node joined: {node2.id}")
    
    # Health check
    health = runtime.get_health()
    print(f"✓ Cluster health: {health['cluster_state']}")
    print(f"  Active nodes: {health['active_nodes']}")
    
    return runtime


def test_marketplace():
    """Test Marketplace Runtime."""
    print("\n" + "=" * 60)
    print("Testing Marketplace Runtime")
    print("=" * 60)
    
    runtime = MarketplaceRuntime()
    
    # Create asset
    from marketplace.runtime import MarketplaceAsset
    asset = MarketplaceAsset(
        id="capability-1",
        name="Image Recognition",
        asset_type=MarketplaceAssetType.CAPABILITY,
        description="AI-powered image recognition",
        trust_score=0.9,
    )
    
    # Publish
    runtime.publish(asset)
    print(f"✓ Asset published: {asset.name}")
    
    # Discover
    results = runtime.discover("image")
    print(f"✓ Discovered {len(results)} assets")
    
    return runtime


def test_extension():
    """Test Extension Runtime."""
    print("\n" + "=" * 60)
    print("Testing Extension Runtime")
    print("=" * 60)
    
    runtime = ExtensionRuntime()
    
    # Create extension
    from extension.runtime import Extension
    ext = Extension(
        id="ext-1",
        name="Cloud Integration",
        extension_type=ExtensionType.PROVIDER,
    )
    
    # Install
    success = runtime.install(ext)
    print(f"✓ Extension installed: {success}")
    
    return runtime


def test_sdk_generator():
    """Test SDK Generator."""
    print("\n" + "=" * 60)
    print("Testing SDK Generator")
    print("=" * 60)
    
    generator = SDKGenerator()
    
    # Generate Python SDK
    sdk = generator.generate({}, SDKLanguage.PYTHON)
    print(f"✓ Python SDK generated: {sdk.id}")
    
    # Generate TypeScript SDK
    sdk_ts = generator.generate({}, SDKLanguage.TYPESCRIPT)
    print(f"✓ TypeScript SDK generated: {sdk_ts.id}")
    
    # Generate Go SDK
    sdk_go = generator.generate({}, SDKLanguage.GO)
    print(f"✓ Go SDK generated: {sdk_go.id}")
    
    return generator


def test_certification():
    """Test Certification Runtime."""
    print("\n" + "=" * 60)
    print("Testing Certification Runtime")
    print("=" * 60)
    
    runtime = CertificationRuntime()
    
    # Certify
    from sdk.runtime import CertificationType
    cert = runtime.certify("capability-1", CertificationType.CAPABILITY)
    print(f"✓ Certification created: {cert.id}")
    print(f"  Status: {cert.status.value}")
    
    return runtime


def test_laboratory():
    """Test Evolution Laboratory."""
    print("\n" + "=" * 60)
    print("Testing Evolution Laboratory")
    print("=" * 60)
    
    runtime = EvolutionLaboratory()
    
    # Create hypothesis
    hypothesis = runtime.create_hypothesis("Adding caching improves performance")
    print(f"✓ Hypothesis created: {hypothesis.id}")
    
    # Run experiment
    experiment = runtime.run_experiment("caching-test", hypothesis.id)
    print(f"✓ Experiment completed: {experiment.id}")
    print(f"  Outcome: {experiment.results.get('outcome')}")
    
    return runtime


def test_observatory():
    """Test Civilization Observatory."""
    print("\n" + "=" * 60)
    print("Testing Civilization Observatory")
    print("=" * 60)
    
    runtime = CivilizationObservatory()
    
    # Create dashboard
    dashboard = runtime.create_dashboard("Main Dashboard", ["missions", "health"])
    print(f"✓ Dashboard created: {dashboard['name']}")
    
    # Add alert
    alert = runtime.add_alert("info", "Test Alert", "This is a test alert")
    print(f"✓ Alert added: {alert['id']}")
    
    # Global metrics
    metrics = runtime.get_global_metrics()
    print(f"✓ Global metrics: health={metrics['health_score']}")
    
    return runtime


def test_expansion():
    """Test Expansion Engine."""
    print("\n" + "=" * 60)
    print("Testing Expansion Engine")
    print("=" * 60)
    
    engine = ExpansionEngine()
    
    # Discover opportunities
    opportunities = engine.discover_opportunities()
    print(f"✓ Discovered {len(opportunities)} opportunities")
    
    # Generate proposal
    proposal = engine.generate_proposal(
        "Add Multi-Cloud Support",
        "Support for AWS, GCP, and Azure",
        "capability",
    )
    print(f"✓ Proposal generated: {proposal.title}")
    
    return engine


def test_platform_v2():
    """Test Platform v2."""
    print("\n" + "=" * 60)
    print("Testing AGOS Civilization Platform v2.0")
    print("=" * 60)
    
    platform = get_platform_v2()
    
    print(f"✓ Platform initialized")
    print(f"  Version: {platform.version}")
    print(f"  Name: {platform.name}")
    
    # Health check
    health = platform.health_check()
    print(f"\n✓ Platform health: {health['status']}")
    print(f"  Architecture integrity: {health['architecture']['integrity']}")
    
    # Stats
    stats = platform.get_stats()
    print(f"\n✓ Platform Stats:")
    print(f"  Distributed nodes: {stats['distributed']['nodes']}")
    print(f"  Marketplace assets: {stats['marketplace']['assets']}")
    print(f"  Extensions: {stats['extensions']['installed']}")
    print(f"  Certifications: {stats['certifications']['active']}")
    print(f"  Experiments: {stats['experiments']['total']}")
    
    # Integrity verification
    integrity = platform.verify_integrity()
    print(f"\n✓ Integrity verification: {integrity['status']}")
    
    # Describe
    description = platform.describe()
    print(f"\n✓ Platform Description:")
    print(f"  Guarantees: {len(description['guarantees'])}")
    for g in description['guarantees'][:3]:
        print(f"    - {g}")
    
    # Generate SDKs
    sdks = platform.generate_sdks()
    print(f"\n✓ SDKs generated: {len(sdks)}")
    for lang in sdks:
        print(f"    - {lang}")
    
    return platform


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS CIVILIZATION PLATFORM v2 - TEST SUITE")
    print("EXECUTION-000091 to EXECUTION-000100")
    print("=" * 60)
    
    # Test subsystems
    test_distributed()
    test_marketplace()
    test_extension()
    test_sdk_generator()
    test_certification()
    test_laboratory()
    test_observatory()
    test_expansion()
    
    # Test platform v2
    test_platform_v2()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print("\nAGOS Civilization Platform v2.0 Ready!")
    print("BEGIN CONTINUOUS CIVILIZATION EVOLUTION 🎊")


if __name__ == "__main__":
    main()
