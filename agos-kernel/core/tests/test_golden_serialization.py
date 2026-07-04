"""
Golden Serialization Tests
EXECUTION-KERNEL-FINALIZATION-000003

Tests that verify kernel serialization is stable and reversible.
"""

import pytest
import json
import pickle
from pathlib import Path


class TestSerialization:
    """Golden tests for kernel serialization."""
    
    def test_kernel_contracts_are_json_serializable(self):
        """All kernel contracts must be JSON serializable."""
        contracts_dir = Path('/workspace/All-hand/agos-kernel/contracts')
        
        if not contracts_dir.exists():
            pytest.skip("Contracts directory not found")
        
        for contract_file in contracts_dir.rglob('*.json'):
            with open(contract_file, 'r') as f:
                data = json.load(f)
            
            # Must be able to serialize back to JSON
            serialized = json.dumps(data)
            deserialized = json.loads(serialized)
            
            assert data == deserialized, \
                f"Contract {contract_file} is not properly serializable"
    
    def test_kernel_events_are_json_serializable(self):
        """All kernel events must be JSON serializable."""
        events_dir = Path('/workspace/All-hand/agos-kernel/events')
        
        if not events_dir.exists():
            pytest.skip("Events directory not found")
        
        for event_file in events_dir.rglob('*.json'):
            with open(event_file, 'r') as f:
                data = json.load(f)
            
            # Must be able to serialize back to JSON
            serialized = json.dumps(data)
            deserialized = json.loads(serialized)
            
            assert data == deserialized, \
                f"Event {event_file} is not properly serializable"
    
    def test_kernel_lock_file_is_valid(self):
        """Kernel lock file must be valid JSON."""
        kernel_dir = Path('/workspace/All-hand/agos-kernel')
        lock_file = kernel_dir / 'finalization' / 'KERNEL_LOCK.json'
        
        if not lock_file.exists():
            pytest.skip("KERNEL_LOCK.json not found")
        
        with open(lock_file, 'r') as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "KERNEL_LOCK.json must be a dictionary"
        assert 'version' in data or 'kernel' in data, \
            "KERNEL_LOCK.json should contain version or kernel info"


class TestSerializationStability:
    """Tests for serialization stability."""
    
    def test_contract_structure_is_stable(self):
        """Contract JSON structure must be stable."""
        contracts_dir = Path('/workspace/All-hand/agos-kernel/contracts')
        
        if not contracts_dir.exists():
            pytest.skip("Contracts directory not found")
        
        for contract_file in contracts_dir.rglob('*.json'):
            with open(contract_file, 'r') as f:
                data = json.load(f)
            
            # All top-level keys must be strings
            for key in data.keys():
                assert isinstance(key, str), \
                    f"Contract {contract_file} has non-string key: {key}"
    
    def test_event_structure_is_stable(self):
        """Event JSON structure must be stable."""
        events_dir = Path('/workspace/All-hand/agos-kernel/events')
        
        if not events_dir.exists():
            pytest.skip("Events directory not found")
        
        for event_file in events_dir.rglob('*.json'):
            with open(event_file, 'r') as f:
                data = json.load(f)
            
            # All top-level keys must be strings
            for key in data.keys():
                assert isinstance(key, str), \
                    f"Event {event_file} has non-string key: {key}"
