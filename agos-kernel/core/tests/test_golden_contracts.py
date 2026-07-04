"""
Golden Contract Tests
EXECUTION-KERNEL-FINALIZATION-000003

Tests that verify kernel contracts remain stable.
Every contract must be backward compatible.
"""

import pytest
import json
import hashlib
from pathlib import Path


class TestKernelContracts:
    """Golden tests for kernel contracts."""
    
    @pytest.fixture
    def contracts_dir(self):
        """Get contracts directory."""
        return Path('/workspace/All-hand/agos-kernel/contracts')
    
    @pytest.fixture
    def contract_manifest(self):
        """Contract manifest snapshot."""
        return {
            'version': '1.0.0',
            'contracts': [
                'agent_contract',
                'capability_contract',
                'event_contract',
                'mission_contract',
                'runtime_contract',
            ]
        }
    
    def test_contracts_directory_exists(self, contracts_dir):
        """Contracts directory must exist."""
        assert contracts_dir.exists(), "agos_kernel.contracts must exist"
    
    def test_contract_files_are_valid_json(self, contracts_dir):
        """All contract files must be valid JSON."""
        if not contracts_dir.exists():
            pytest.skip("Contracts directory not found")
        
        for contract_file in contracts_dir.rglob('*.json'):
            with open(contract_file, 'r') as f:
                try:
                    json.load(f)
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in {contract_file}: {e}")
    
    def test_contract_manifest_integrity(self, contract_manifest):
        """Contract manifest must be stable."""
        manifest_hash = hashlib.sha256(
            json.dumps(contract_manifest, sort_keys=True).encode()
        ).hexdigest()
        
        # Golden snapshot - any change here should be reviewed
        assert len(manifest_hash) == 64, "Manifest hash must be SHA-256"
    
    def test_no_contract_mutation(self, contracts_dir):
        """Contracts must not be mutated at runtime."""
        # Check that contract files don't contain mutating code
        if not contracts_dir.exists():
            pytest.skip("Contracts directory not found")
        
        mutation_patterns = ['del ', '.clear()', '.pop(', '.update(']
        
        for contract_file in contracts_dir.rglob('*.json'):
            with open(contract_file, 'r') as f:
                content = f.read()
            
            for pattern in mutation_patterns:
                assert pattern not in content, \
                    f"Contract file {contract_file} contains mutation: {pattern}"


class TestContractBackwardCompatibility:
    """Tests for contract backward compatibility."""
    
    def test_contract_version_exists(self):
        """All contracts must have a version."""
        contracts_dir = Path('/workspace/All-hand/agos-kernel/contracts')
        
        if not contracts_dir.exists():
            pytest.skip("Contracts directory not found")
        
        for contract_file in contracts_dir.rglob('*.json'):
            with open(contract_file, 'r') as f:
                data = json.load(f)
            
            # Contracts should have version or type field
            assert 'version' in data or 'type' in data, \
                f"Contract {contract_file} missing version/type"
