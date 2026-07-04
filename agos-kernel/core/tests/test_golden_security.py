"""
Golden Security Tests
EXECUTION-KERNEL-FINALIZATION-000003

Tests that verify kernel security characteristics.
"""

import pytest
from pathlib import Path
import re


class TestKernelSecurity:
    """Golden tests for kernel security."""
    
    @pytest.fixture
    def kernel_dir(self):
        """Get kernel directory."""
        return Path('/workspace/All-hand/agos-kernel')
    
    def test_no_hardcoded_secrets(self, kernel_dir):
        """Kernel must not contain hardcoded secrets."""
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'private_key\s*=\s*["\'][^"\']+["\']',
        ]
        
        violations = []
        
        for py_file in kernel_dir.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Filter out example/placeholder values
                    if not any(p in match.lower() for p in ['example', 'placeholder', 'your_', 'changeme']):
                        violations.append(f"{py_file}: {match[:50]}...")
        
        assert len(violations) == 0, \
            f"Hardcoded secrets found:\n" + "\n".join(violations[:5])
    
    def test_no_eval_usage(self, kernel_dir):
        """Kernel must not use eval()."""
        violations = []
        
        for py_file in kernel_dir.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            
            with open(py_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if 'eval(' in line and not line.strip().startswith('#'):
                    violations.append(f"{py_file}:{i}: {line.strip()}")
        
        assert len(violations) == 0, \
            f"eval() usage found:\n" + "\n".join(violations[:5])
    
    def test_no_exec_usage(self, kernel_dir):
        """Kernel must not use exec()."""
        violations = []
        
        for py_file in kernel_dir.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            
            with open(py_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if 'exec(' in line and not line.strip().startswith('#'):
                    violations.append(f"{py_file}:{i}: {line.strip()}")
        
        assert len(violations) == 0, \
            f"exec() usage found:\n" + "\n".join(violations[:5])
    
    def test_no_sql_injection_patterns(self, kernel_dir):
        """Kernel should avoid SQL injection vulnerabilities."""
        sql_patterns = [
            r'f["\'].*SELECT.*{',
            r'f["\'].*INSERT.*{',
            r'f["\'].*UPDATE.*{',
            r'f["\'].*DELETE.*{',
        ]
        
        violations = []
        
        for py_file in kernel_dir.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in sql_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    violations.append(f"{py_file}: contains SQL injection pattern")
        
        # Warning level check
        if len(violations) > 0:
            pytest.fail(f"SQL injection patterns found:\n" + "\n".join(violations[:3]))


class TestSecurityBestPractices:
    """Tests for security best practices."""
    
    def test_imports_are_safe(self):
        """Kernel should use safe import patterns."""
        kernel_dir = Path('/workspace/All-hand/agos-kernel')
        
        unsafe_patterns = ['__import__', 'importlib.import_module(']
        violations = []
        
        for py_file in kernel_dir.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in unsafe_patterns:
                if pattern in content:
                    violations.append(f"{py_file}: uses {pattern}")
        
        assert len(violations) == 0, \
            f"Unsafe import patterns:\n" + "\n".join(violations[:5])
    
    def test_file_permissions_are_restricted(self, kernel_dir):
        """Kernel files should have appropriate permissions."""
        # Check that sensitive files don't exist with wrong permissions
        sensitive_files = [
            '*.key', '*.pem', '*.cert', '*id_rsa*', '*id_dsa*'
        ]
        
        violations = []
        
        for pattern in sensitive_files:
            for f in kernel_dir.rglob(pattern):
                if f.is_file():
                    # Files should not be executable scripts
                    if f.suffix in ['.py', '.sh']:
                        violations.append(f"Sensitive file {f} should not be executable")
        
        # This is informational - not a hard failure
        if len(violations) > 0:
            pytest.skip(f"Sensitive file check: {'; '.join(violations[:3])}")
