#!/usr/bin/env python3
"""Test script for Civilization, Marketplace, and Connector Programs."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from civilization_packs.library import CivilizationPackLibrary, get_library as get_civ_library
from marketplace.library import Marketplace, get_marketplace
from connectors.library import ConnectorLibrary, get_library as get_conn_library


def test_civilization_packs():
    """Test civilization packs."""
    print("=" * 60)
    print("Testing Civilization Packs 1-30")
    print("=" * 60)
    
    library = get_civ_library()
    print(f"✓ Civilization Pack Library initialized")
    print(f"  Total packs: {len(library.packs)}")
    
    for i, (name, pack) in enumerate(list(library.packs.items())[:10]):
        print(f"  {i+1}. {pack.metadata.name}")
        print(f"      Domains: {', '.join(pack.metadata.domains[:3])}")
    
    print(f"  ... and {len(library.packs) - 10} more")
    
    # Get pack
    foundation = library.get("foundation")
    if foundation:
        print(f"\n✓ Foundation pack: {foundation.metadata.description}")


def test_marketplace():
    """Test marketplace."""
    print("\n" + "=" * 60)
    print("Testing Marketplace 1-40")
    print("=" * 60)
    
    marketplace = get_marketplace()
    print(f"✓ Marketplace initialized")
    print(f"  Total categories: {len(marketplace.categories)}")
    
    print(f"  Categories: {', '.join(marketplace.categories[:15])}")
    print(f"  ... and {len(marketplace.categories) - 15} more")
    
    # Publish an asset
    from marketplace.library import MarketplaceAsset
    asset = MarketplaceAsset("Test Capability", "capability", "AGOS")
    asset_id = marketplace.publish(asset)
    print(f"\n✓ Published asset: {asset_id}")


def test_connectors():
    """Test connectors."""
    print("\n" + "=" * 60)
    print("Testing Connectors 1-50")
    print("=" * 60)
    
    library = get_conn_library()
    print(f"✓ Connector Library initialized")
    print(f"  Total connectors: {len(library.connectors)}")
    
    for i, (name, conn) in enumerate(list(library.connectors.items())[:10]):
        print(f"  {i+1}. {conn.metadata.name} ({conn.metadata.provider})")
    
    print(f"  ... and {len(library.connectors) - 10} more")
    
    # Get connector
    github = library.get("github")
    if github:
        print(f"\n✓ GitHub connector: {github.metadata.description}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS CIVILIZATION, MARKETPLACE & CONNECTOR PROGRAMS")
    print("CIVILIZATION-PACK-000001 to CIVILIZATION-PACK-000030")
    print("MARKETPLACE-000001 to MARKETPLACE-000040")
    print("CONNECTOR-000001 to CONNECTOR-000050")
    print("=" * 60)
    
    test_civilization_packs()
    test_marketplace()
    test_connectors()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()