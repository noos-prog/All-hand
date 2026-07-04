"""
Golden Registry Tests
EXECUTION-KERNEL-FINALIZATION-000003

Tests that verify kernel registry integrity.
"""

import pytest
from pathlib import Path


class TestKernelRegistry:
    """Golden tests for kernel registry."""
    
    @pytest.fixture
    def registry_dir(self):
        """Get registry directory."""
        return Path('/workspace/All-hand/agos-kernel/registry')
    
    def test_registry_directory_exists(self, registry_dir):
        """Registry directory must exist."""
        assert registry_dir.exists(), "agos_kernel.registry must exist"
    
    def test_registry_has_required_components(self):
        """Registry must have required components."""
        registry_dir = Path('/workspace/All-hand/agos-kernel/registry')
        
        if not registry_dir.exists():
            pytest.skip("Registry directory not found")
        
        # Check for typical registry components
        components = list(registry_dir.iterdir())
        assert len(components) > 0, "Registry should have components"


class TestRegistryIntegrity:
    """Tests for registry integrity."""
    
    def test_registry_entries_are_valid(self):
        """Registry entries must be valid."""
        registry_dir = Path('/workspace/All-hand/agos-kernel/registry')
        
        if not registry_dir.exists():
            pytest.skip("Registry directory not found")
        
        for entry in registry_dir.rglob('*.json'):
            import json
            with open(entry, 'r') as f:
                try:
                    data = json.load(f)
                    assert data is not None, f"Registry entry {entry} is invalid"
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON in registry entry: {entry}")
    
    def test_registry_has_version(self):
        """Registry must track versions."""
        registry_dir = Path('/workspace/All-hand/agos-kernel/registry')
        
        if not registry_dir.exists():
            pytest.skip("Registry directory not found")
        
        # At least one registry entry should have version info
        found_version = False
        import json
        
        for entry in registry_dir.rglob('*.json'):
            with open(entry, 'r') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict) and 'version' in data:
                        found_version = True
                        break
                except:
                    pass
        
        assert found_version, "At least one registry entry should have version"
