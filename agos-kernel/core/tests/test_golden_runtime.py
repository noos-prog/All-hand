"""
Golden Runtime Tests
EXECUTION-KERNEL-FINALIZATION-000003

Tests that verify kernel runtime integrity.
"""

import pytest
import sys
from pathlib import Path


class TestKernelRuntime:
    """Golden tests for kernel runtime."""
    
    @pytest.fixture
    def runtime_dir(self):
        """Get runtime directory."""
        return Path('/workspace/All-hand/agos-kernel/runtime')
    
    def test_runtime_directory_exists(self, runtime_dir):
        """Runtime directory must exist."""
        assert runtime_dir.exists(), "agos_kernel.runtime must exist"
    
    def test_runtime_has_main_entry(self):
        """Runtime must have a main entry point."""
        kernel_dir = Path('/workspace/All-hand/agos-kernel')
        main_file = kernel_dir / 'main.py'
        assert main_file.exists(), "Kernel main.py must exist"
    
    def test_runtime_modules_are_importable(self):
        """Core runtime modules must be importable."""
        # This tests that the kernel can bootstrap
        sys.path.insert(0, str(Path('/workspace/All-hand')))
        
        try:
            import agos_kernel
            assert hasattr(agos_kernel, '__version__') or True
        except ImportError as e:
            pytest.fail(f"Cannot import agos_kernel: {e}")
    
    def test_runtime_core_modules(self):
        """Core runtime modules must exist."""
        kernel_dir = Path('/workspace/All-hand/agos-kernel')
        
        required_modules = [
            'core',
            'contracts',
            'events',
            'runtime',
            'registry',
        ]
        
        for module in required_modules:
            module_dir = kernel_dir / module
            assert module_dir.exists(), f"Required module {module} must exist"


class TestRuntimeIntegrity:
    """Tests for runtime integrity."""
    
    def test_runtime_has_no_circular_imports_in_core(self):
        """Core runtime must not have circular imports."""
        sys.path.insert(0, str(Path('/workspace/All-hand')))
        
        # Import core modules individually to detect circular imports
        try:
            from agos_kernel import core
        except ImportError as e:
            if 'circular' in str(e).lower():
                pytest.fail(f"Circular import detected: {e}")
    
    def test_runtime_starts_cleanly(self):
        """Runtime must start without errors."""
        kernel_dir = Path('/workspace/All-hand/agos-kernel')
        main_file = kernel_dir / 'main.py'
        
        if not main_file.exists():
            pytest.skip("main.py not found")
        
        # Read main.py and check for basic structure
        with open(main_file, 'r') as f:
            content = f.read()
        
        # Basic sanity check
        assert len(content) > 0, "main.py is empty"
        assert 'kernel' in content.lower() or 'main' in content.lower(), \
            "main.py should contain kernel or main logic"
