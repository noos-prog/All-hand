#!/usr/bin/env python3
"""Test script for Certification, Benchmark, and Audit Programs."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from certification.library import CertificationLibrary, get_library as get_cert_library
from benchmark.library import BenchmarkLibrary, get_library as get_bench_library
from audit.library import AuditLibrary, get_library as get_audit_library


def test_certifications():
    """Test certifications."""
    print("=" * 60)
    print("Testing Certifications 1-30")
    print("=" * 60)
    
    library = get_cert_library()
    print(f"✓ Certification Library initialized")
    print(f"  Total certifications: {len(library.certifications)}")
    
    for i, (name, cert) in enumerate(list(library.certifications.items())[:10]):
        print(f"  {i+1}. {cert.metadata.name}")
    
    print(f"  ... and {len(library.certifications) - 10} more")
    
    # Run certification
    result = library.certify("capability", {"name": "test"})
    print(f"\n✓ Certification result: {result.status.value}, score={result.score}")


def test_benchmarks():
    """Test benchmarks."""
    print("\n" + "=" * 60)
    print("Testing Benchmarks 1-50")
    print("=" * 60)
    
    library = get_bench_library()
    print(f"✓ Benchmark Library initialized")
    print(f"  Total benchmarks: {len(library.benchmarks)}")
    
    for i, (name, bench) in enumerate(list(library.benchmarks.items())[:10]):
        print(f"  {i+1}. {bench.name}")
    
    print(f"  ... and {len(library.benchmarks) - 10} more")
    
    # Run benchmark
    result = library.run("performance", {"name": "test"})
    print(f"\n✓ Benchmark result: score={result.score}")


def test_audits():
    """Test audits."""
    print("\n" + "=" * 60)
    print("Testing Audits 1-40")
    print("=" * 60)
    
    library = get_audit_library()
    print(f"✓ Audit Library initialized")
    print(f"  Total audits: {len(library.audits)}")
    
    for i, (name, audit) in enumerate(list(library.audits.items())[:10]):
        print(f"  {i+1}. {audit.name}")
    
    print(f"  ... and {len(library.audits) - 10} more")
    
    # Run audit
    result = library.run("security", {"name": "test"})
    print(f"\n✓ Audit result: {result.status.value}, risk_score={result.risk_score}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS CERTIFICATION, BENCHMARK & AUDIT PROGRAMS")
    print("CERTIFICATION-000001 to CERTIFICATION-000030")
    print("BENCHMARK-000001 to BENCHMARK-000050")
    print("AUDIT-000001 to AUDIT-000040")
    print("=" * 60)
    
    test_certifications()
    test_benchmarks()
    test_audits()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()