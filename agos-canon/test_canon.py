#!/usr/bin/env python3
"""
AGOS Canon - Test Suite
========================

Tests for canon and constitution compliance.
Run with: python -m pytest test_canon.py -v
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vocabulary import Vocabulary, get_vocabulary, TermCategory, CanonicalTerm
from rules import CanonRules, CanonType, ViolationSeverity, CanonRule
from constitution import Constitution, ArticleType, ArticleStatus, ConstitutionalArticle
from validator import CanonValidator, ComplianceLevel, Violation, ValidationResult
from registry import CanonRegistry, get_registry, RegistryStatus, ComponentRecord, ViolationRecord


def test_vocabulary():
    """Test vocabulary module."""
    print("\n=== Testing Vocabulary ===")
    
    vocab = get_vocabulary()
    assert vocab is not None
    
    # Test get term
    agos_term = vocab.get("AGOS")
    assert agos_term is not None
    assert agos_term.term == "AGOS"
    assert "Autonomous General Orchestration System" in agos_term.definition
    
    # Test validate usage
    is_valid, reason = vocab.validate_usage("kernel")
    assert is_valid, reason
    
    # Test stats
    stats = vocab.get_stats()
    assert stats["total_terms"] > 0
    print(f"  Vocabulary: {stats['total_terms']} terms")
    print(f"  Hash: {stats['hash']}")
    
    # Test by category
    core_terms = vocab.get_by_category(TermCategory.CORE)
    assert len(core_terms) > 0
    print(f"  Core terms: {len(core_terms)}")
    
    print("  ✓ Vocabulary tests passed")


def test_rules():
    """Test canon rules module."""
    print("\n=== Testing Canon Rules ===")
    
    # Test get all rules
    rules = CanonRules.get_all_rules()
    assert len(rules) == 10, f"Expected 10 rules, got {len(rules)}"
    print(f"  Total rules: {len(rules)}")
    
    # Test get specific rule
    canon_001 = CanonRules.get_rule("CANON-001")
    assert canon_001 is not None
    assert canon_001.id == "CANON-001"
    assert canon_001.name == "Vocabulary"
    print(f"  CANON-001: {canon_001.name}")
    
    # Test rule hash
    rule_hash = CanonRules.get_rule_hash()
    assert len(rule_hash) == 16
    print(f"  Rule hash: {rule_hash}")
    
    # Test all rules have required fields
    for rule in rules:
        assert hasattr(rule, 'id')
        assert hasattr(rule, 'name')
        assert hasattr(rule, 'rule_text')
        assert hasattr(rule, 'examples_valid')
        assert hasattr(rule, 'examples_invalid')
        assert hasattr(rule, 'severity')
    
    print("  ✓ Rules tests passed")


def test_constitution():
    """Test constitution module."""
    print("\n=== Testing Constitution ===")
    
    # Test get all articles
    articles = Constitution.get_all_articles()
    assert len(articles) == 15, f"Expected 15 articles, got {len(articles)}"
    print(f"  Total articles: {len(articles)}")
    
    # Test get specific article
    article_1 = Constitution.get_article(1)
    assert article_1 is not None
    assert article_1.roman_numeral == "I"
    assert article_1.title == "The One Brain"
    print(f"  Article I: {article_1.title}")
    
    # Test constitution hash
    const_hash = Constitution.compute_hash()
    assert len(const_hash) == 16
    print(f"  Constitution hash: {const_hash}")
    
    # Test summary
    summary = Constitution.get_summary()
    assert summary["version"] == "1.0"
    assert summary["articles"] == 15
    print(f"  Version: {summary['version']}")
    
    # Test article types
    for article in articles:
        assert hasattr(article, 'number')
        assert hasattr(article, 'statement')
        assert hasattr(article, 'rules')
        assert hasattr(article, 'requirements')
        assert hasattr(article, 'forbidden')
    
    print("  ✓ Constitution tests passed")


def test_validator():
    """Test validator module."""
    print("\n=== Testing Validator ===")
    
    validator = CanonValidator()
    
    # Test vocabulary validation
    code_with_forbidden = """
    def get_ai_decision():
        # The AI decided this is best
        return magic_number()
    """
    
    validator.reset()
    validator.validate_vocabulary_usage(code_with_forbidden, "test.py")
    violations = validator._violations
    assert len(violations) > 0, "Should find forbidden words"
    print(f"  Found {len(violations)} vocabulary violations")
    
    # Test naming validation
    code_with_bad_naming = """
    class myClass:  # Should be MyClass
        def MyFunction(self):  # Should be my_function
            pass
    """
    
    validator.reset()
    validator.validate_naming(code_with_bad_naming, "test.py")
    violations = validator._violations
    print(f"  Found {len(violations)} naming violations")
    
    # Test kernel ownership validation
    code_with_violation = """
    external_ai.plan_next_move()
    """
    
    validator.reset()
    validator.validate_kernel_ownership(code_with_violation, "test.py")
    violations = validator._violations
    assert len(violations) > 0, "Should find kernel ownership violations"
    print(f"  Found {len(violations)} kernel ownership violations")
    
    # Test contract versioning
    contracts = [
        {"name": "valid_contract", "version": "v1_0"},
        {"name": "invalid_contract", "version": "1.0"},  # Missing v prefix
        {"name": "no_version"},  # Missing version
    ]
    
    validator.reset()
    result = validator.validate_contracts(contracts)
    assert len(result.violations) >= 2
    print(f"  Contract validation: {len(result.violations)} violations")
    
    # Test knowledge evidence validation
    entries = [
        {
            "source": "https://example.com",
            "evidence": "test evidence",
            "confidence": 0.9,
            "lineage": "created by test"
        },
        {
            "source": "https://example.com",
            # Missing evidence, confidence, lineage
        }
    ]
    
    validator.reset()
    result = validator.validate_knowledge_base(entries)
    assert len(result.violations) > 0
    print(f"  Knowledge validation: {len(result.violations)} violations")
    
    print("  ✓ Validator tests passed")


def test_registry():
    """Test registry module."""
    print("\n=== Testing Registry ===")
    
    # Get fresh registry
    registry = get_registry()
    
    # Test register component
    component = registry.register_component(
        component_id="test_component",
        component_type="module",
        name="Test Component",
        version="1.0",
        metadata={"author": "test"}
    )
    assert component is not None
    assert component.name == "Test Component"
    print(f"  Registered: {component.name}")
    
    # Test get component
    retrieved = registry.get_component("test_component")
    assert retrieved is not None
    assert retrieved.component_id == "test_component"
    
    # Test list components
    components = registry.list_components()
    assert len(components) > 0
    print(f"  Total components: {len(components)}")
    
    # Test record violation
    violation = registry.record_violation(
        violation_id="V0001",
        component_id="test_component",
        rule_id="CANON-001",
        severity="high",
        description="Test violation"
    )
    assert violation is not None
    print(f"  Recorded violation: {violation.violation_id}")
    
    # Test get violations
    violations = registry.get_violations(component_id="test_component")
    assert len(violations) > 0
    
    # Test statistics
    stats = registry.get_statistics()
    assert stats["total_components"] > 0
    print(f"  Statistics: {stats['total_components']} components, {stats['total_violations']} violations")
    
    # Test compliance score
    score = registry.get_compliance_score()
    assert 0 <= score <= 100
    print(f"  Compliance score: {score}%")
    
    # Test export/import
    state = registry.export_state()
    assert "components" in state
    assert "violations" in state
    print(f"  Exported state: {len(state['components'])} components")
    
    print("  ✓ Registry tests passed")


def test_validation_flow():
    """Test full validation flow."""
    print("\n=== Testing Full Validation Flow ===")
    
    # Sample Python code with various issues
    sample_code = '''
# This code has canon violations
from vocabulary import get_vocabulary  # OK

def MyFunction(data):  # Violation: naming
    """Process data."""
    # The AI will decide what to do  # Violation: forbidden word
    result = {}
    if data:  # TODO: fix this later  # Violation: TODO
        result["status"] = "ok"
    return result

class MyClass:  # Violation: PascalCase
    pass
'''
    
    validator = CanonValidator()
    result = validator.validate_python_file("sample_code.py", sample_code)
    
    print(f"  Validation result: {result.level.value}")
    print(f"  Violations found: {len(result.violations)}")
    
    # Generate report
    report = validator.generate_report([result])
    assert "AGOS CANON" in report
    assert "FAIL" in report  # Should fail due to violations
    print(f"  Report generated ({len(report)} chars)")
    
    print("  ✓ Full validation flow tests passed")


def test_integration():
    """Test integration between modules."""
    print("\n=== Testing Integration ===")
    
    # Get vocabulary
    vocab = get_vocabulary()
    
    # Get constitution
    const = Constitution()
    
    # Get registry
    registry = get_registry()
    
    # Register a component
    registry.register_component(
        component_id="integration_test",
        component_type="module",
        name="Integration Test Component",
        version="1.0"
    )
    
    # Validate it
    validator = CanonValidator()
    sample_code = '''
def test_function():
    """A test function."""
    return True
'''
    
    result = validator.validate_python_file("integration_test.py", sample_code)
    
    # Record validation
    registry.record_validation(
        component_id="integration_test",
        is_compliant=result.is_compliant(),
        violation_count=len(result.violations),
        hash=result.hash
    )
    
    # Check stats
    stats = registry.get_statistics()
    score = registry.get_compliance_score()
    
    print(f"  Integration test completed")
    print(f"  Registry stats: {stats}")
    print(f"  Compliance score: {score}%")
    
    print("  ✓ Integration tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("AGOS CANON - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_vocabulary()
        test_rules()
        test_constitution()
        test_validator()
        test_registry()
        test_validation_flow()
        test_integration()
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
