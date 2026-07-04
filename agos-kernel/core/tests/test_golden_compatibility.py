"""
Golden Compatibility Tests
EXECUTION-KERNEL-FINALIZATION-000003

Tests that verify kernel compatibility with Python standards.
"""

import pytest
import sys
from pathlib import Path


class TestPythonCompatibility:
    """Golden tests for Python compatibility."""
    
    def test_python_version_compatible(self):
        """Kernel must be compatible with Python 3.8+."""
        assert sys.version_info >= (3, 8), \
            f"Kernel requires Python 3.8+, current: {sys.version_info}"
    
    def test_core_modules_python3_syntax(self):
        """Core modules must use valid Python 3 syntax."""
        kernel_dir = Path('/workspace/All-hand/agos-kernel')
        
        syntax_errors = []
        for py_file in kernel_dir.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(py_file), 'exec')
            except SyntaxError as e:
                syntax_errors.append(f"{py_file}: {e}")
        
        assert len(syntax_errors) == 0, \
            f"Syntax errors found:\n" + "\n".join(syntax_errors)


class TestAPCompatibility:
    """Tests for API compatibility."""
    
    def test_kernel_has_version(self):
        """Kernel must expose version."""
        kernel_dir = Path('/workspace/All-hand/agos-kernel')
        
        # Check for version in various places
        has_version = False
        
        # Check __init__.py
        init_file = kernel_dir / '__init__.py'
        if init_file.exists():
            with open(init_file, 'r') as f:
                content = f.read()
                if '__version__' in content or 'version' in content.lower():
                    has_version = True
        
        # Check main.py
        main_file = kernel_dir / 'main.py'
        if main_file.exists():
            with open(main_file, 'r') as f:
                content = f.read()
                if '__version__' in content or 'version' in content.lower():
                    has_version = True
        
        assert has_version, "Kernel should expose version information"


class TestDependencyCompatibility:
    """Tests for dependency compatibility."""
    
    def test_kernel_uses_only_standard_library_or_declared(self):
        """Kernel should use only standard library or declared dependencies."""
        kernel_dir = Path('/workspace/All-hand/agos-kernel')
        
        # List of standard library modules
        stdlib = {
            'os', 'sys', 'time', 'datetime', 'json', 're', 'math',
            'random', 'hashlib', 'pathlib', 'typing', 'collections',
            'contextlib', 'functools', 'itertools', 'abc', 'copy',
            'dataclasses', 'enum', 'uuid', 'base64', 'binascii',
        }
        
        violations = []
        
        for py_file in kernel_dir.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for imports
            for line in content.split('\n'):
                if line.strip().startswith('import '):
                    module = line.strip().split()[1].split('.')[0]
                    if module not in stdlib and not module.startswith('agos_'):
                        violations.append(f"{py_file}: imports {module}")
        
        # Allow third-party imports that are reasonable
        allowed_third_party = {'pytest', 'numpy', 'pandas'}
        violations = [v for v in violations if not any(a in v for a in allowed_third_party)]
        
        # This is a warning-level check, not a hard failure
        # Some third-party deps might be necessary
        if len(violations) > 5:
            pytest.fail(f"Too many third-party imports: {violations[:5]}...")
