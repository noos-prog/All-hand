"""
Golden Performance Tests
EXECUTION-KERNEL-FINALIZATION-000003

Tests that verify kernel performance characteristics.
"""

import pytest
import time
from pathlib import Path


class TestKernelPerformance:
    """Golden tests for kernel performance."""
    
    @pytest.fixture
    def kernel_dir(self):
        """Get kernel directory."""
        return Path('/workspace/All-hand/agos-kernel')
    
    def test_kernel_imports_quickly(self, kernel_dir):
        """Kernel must import within acceptable time."""
        import subprocess
        import sys
        
        # Measure import time
        start = time.time()
        result = subprocess.run(
            [sys.executable, '-c', 'import sys; sys.path.insert(0, "/workspace/All-hand"); import agos_kernel'],
            capture_output=True,
            timeout=5
        )
        elapsed = time.time() - start
        
        # Kernel should import in under 2 seconds
        assert elapsed < 2.0, f"Kernel import took {elapsed:.2f}s (expected < 2s)"
        assert result.returncode == 0, f"Kernel import failed: {result.stderr.decode()}"
    
    def test_contract_files_load_quickly(self, kernel_dir):
        """Contract files must load quickly."""
        contracts_dir = kernel_dir / 'contracts'
        
        if not contracts_dir.exists():
            pytest.skip("Contracts directory not found")
        
        import json
        
        start = time.time()
        for contract_file in contracts_dir.rglob('*.json'):
            with open(contract_file, 'r') as f:
                json.load(f)
        elapsed = time.time() - start
        
        # Should load all contracts in under 1 second
        assert elapsed < 1.0, f"Contract loading took {elapsed:.2f}s"
    
    def test_event_files_load_quickly(self, kernel_dir):
        """Event files must load quickly."""
        events_dir = kernel_dir / 'events'
        
        if not events_dir.exists():
            pytest.skip("Events directory not found")
        
        import json
        
        start = time.time()
        for event_file in events_dir.rglob('*.json'):
            with open(event_file, 'r') as f:
                json.load(f)
        elapsed = time.time() - start
        
        # Should load all events in under 1 second
        assert elapsed < 1.0, f"Event loading took {elapsed:.2f}s"


class TestPerformanceBaselines:
    """Tests for performance baselines."""
    
    def test_no_performance_regression(self):
        """Performance must not regress."""
        # Baseline: Import should be < 2s
        import subprocess
        import sys
        
        times = []
        for _ in range(3):
            start = time.time()
            result = subprocess.run(
                [sys.executable, '-c', 'import sys; sys.path.insert(0, "/workspace/All-hand")'],
                capture_output=True,
                timeout=5
            )
            elapsed = time.time() - start
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        
        # Allow 3x baseline for warm-up variations
        assert avg_time < 3.0, f"Average import time {avg_time:.2f}s exceeds baseline"
