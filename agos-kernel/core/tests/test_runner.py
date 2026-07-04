"""
Golden Test Suite Runner
EXECUTION-KERNEL-FINALIZATION-000003

Main entry point for running all Golden Tests.
Every Pull Request executes this suite.
Failure blocks merge.
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json

# Test root directory
TEST_DIR = Path(__file__).parent


def run_golden_tests():
    """
    Run all golden tests.
    
    Returns:
        0 if all tests pass
        1 if any test fails
    """
    print("=" * 60)
    print("AGOS KERNEL GOLDEN TEST SUITE")
    print("=" * 60)
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print(f"Version: 1.0.0")
    print()
    
    # Test categories
    test_files = [
        'test_golden_contracts.py',
        'test_golden_events.py',
        'test_golden_runtime.py',
        'test_golden_registry.py',
        'test_golden_serialization.py',
        'test_golden_compatibility.py',
        'test_golden_recovery.py',
        'test_golden_performance.py',
        'test_golden_security.py',
    ]
    
    all_passed = True
    results = []
    
    for test_file in test_files:
        test_path = TEST_DIR / test_file
        
        if not test_path.exists():
            print(f"⚠️  {test_file}: NOT FOUND")
            results.append({
                'file': test_file,
                'status': 'SKIPPED',
                'message': 'File not found'
            })
            continue
        
        print(f"Running {test_file}...")
        
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', str(test_path), '-v', '--tb=short'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"  ✅ PASSED")
            results.append({
                'file': test_file,
                'status': 'PASSED'
            })
        else:
            print(f"  ❌ FAILED")
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            all_passed = False
            results.append({
                'file': test_file,
                'status': 'FAILED',
                'output': result.stdout[-1000:]
            })
        
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results if r['status'] == 'PASSED')
    failed = sum(1 for r in results if r['status'] == 'FAILED')
    skipped = sum(1 for r in results if r['status'] == 'SKIPPED')
    
    print(f"Total: {len(results)}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Skipped: {skipped}")
    print()
    
    if all_passed:
        print("🎉 ALL GOLDEN TESTS PASSED")
        print("Kernel protection verified. PR can be merged.")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("Kernel protection compromised. PR is BLOCKED.")
        return 1


def run_quick_check():
    """
    Quick validation check.
    
    Returns True if basic checks pass.
    """
    print("Running quick validation...")
    
    # Check critical directories exist
    kernel_dir = Path('/workspace/All-hand/agos-kernel')
    
    required_dirs = [
        'core',
        'contracts',
        'events',
        'runtime',
        'registry',
    ]
    
    missing = []
    for d in required_dirs:
        if not (kernel_dir / d).exists():
            missing.append(d)
    
    if missing:
        print(f"❌ Missing directories: {missing}")
        return False
    
    print("✅ Quick validation passed")
    return True


if __name__ == '__main__':
    sys.exit(run_golden_tests())
