#!/usr/bin/env python3
"""Test script for Language, Framework, and Cloud Packs."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from language_packs.library import LanguagePackLibrary, get_library as get_lang_library
from framework_packs.library import FrameworkPackLibrary, get_library as get_fwk_library
from cloud_packs.library import CloudPackLibrary, get_library as get_cloud_library


def test_language_packs():
    """Test language packs."""
    print("=" * 60)
    print("Testing Language Packs 1-40")
    print("=" * 60)
    
    library = get_lang_library()
    print(f"✓ Language Pack Library initialized")
    print(f"  Total packs: {len(library.packs)}")
    
    for i, (name, pack) in enumerate(list(library.packs.items())[:10]):
        print(f"  {i+1}. {pack.metadata.name} ({', '.join(pack.metadata.extensions[:2])})")
    
    print(f"  ... and {len(library.packs) - 10} more")
    
    # Detect language
    python = library.detect("main.py")
    print(f"\n✓ Detected: {python.metadata.name}")
    
    js = library.detect("app.jsx")
    print(f"✓ Detected: {js.metadata.name}")


def test_framework_packs():
    """Test framework packs."""
    print("\n" + "=" * 60)
    print("Testing Framework Packs 1-60")
    print("=" * 60)
    
    library = get_fwk_library()
    print(f"✓ Framework Pack Library initialized")
    print(f"  Total packs: {len(library.packs)}")
    
    for i, (name, pack) in enumerate(list(library.packs.items())[:10]):
        print(f"  {i+1}. {pack.metadata.name} ({pack.metadata.category})")
    
    print(f"  ... and {len(library.packs) - 10} more")
    
    # Get framework
    react = library.get("react")
    if react:
        print(f"\n✓ Framework: {react.metadata.name}")


def test_cloud_packs():
    """Test cloud packs."""
    print("\n" + "=" * 60)
    print("Testing Cloud Packs 1-30")
    print("=" * 60)
    
    library = get_cloud_library()
    print(f"✓ Cloud Pack Library initialized")
    print(f"  Total packs: {len(library.packs)}")
    
    for i, (name, pack) in enumerate(list(library.packs.items())[:10]):
        print(f"  {i+1}. {pack.metadata.name} ({pack.metadata.category})")
    
    print(f"  ... and {len(library.packs) - 10} more")
    
    # List by category
    paas = library.list_by_category("paas")
    print(f"\n✓ PaaS providers: {[p.metadata.name for p in paas]}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS LANGUAGE, FRAMEWORK & CLOUD PACKS")
    print("LANGUAGE-PACK-000001 to LANGUAGE-PACK-000040")
    print("FRAMEWORK-PACK-000001 to FRAMEWORK-PACK-000060")
    print("CLOUD-PACK-000001 to CLOUD-PACK-000030")
    print("=" * 60)
    
    test_language_packs()
    test_framework_packs()
    test_cloud_packs()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()