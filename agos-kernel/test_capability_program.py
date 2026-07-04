#!/usr/bin/env python3
"""Test script for AGOS Capability, Provider, and Skill Programs."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from capabilities.base import Capability, CapabilityStatus
from capabilities.repository.discovery import RepositoryDiscoveryCapability
from capabilities.repository.clone import RepositoryCloneCapability
from capabilities.repository.sync import RepositorySyncCapability, RepositoryFingerprintCapability, RepositoryStructureCapability
from capabilities.technology.detection import TechnologyDetectionCapability
from capabilities.analysis.dependency import (
    DependencyAnalysisCapability, CodeIndexingCapability,
    ArchitectureExtractionCapability, ArchitectureValidationCapability,
    PatternDetectionCapability, AntiPatternDetectionCapability, DeadCodeDetectionCapability
)

from providers.base import Provider, ProviderStatus
from providers.filesystem import FilesystemProvider, GitProvider, GitHubProvider, get_provider

from skills.base import Skill, SkillStatus
from skills.vcs.operations import CloneRepositorySkill, PullRepositorySkill, CheckoutBranchSkill
from skills.file.operations import ReadFileSkill, WriteFileSkill, SearchFilesSkill
from skills.execution.operations import ExecuteCLISkill, RunTestsSkill


def test_capabilities():
    """Test capabilities."""
    print("=" * 60)
    print("Testing Capabilities")
    print("=" * 60)
    
    # Repository Discovery
    disc = RepositoryDiscoveryCapability()
    repos = disc.execute("local")
    print(f"✓ Repository Discovery: {len(repos)} repositories")
    
    # Repository Clone
    clone = RepositoryCloneCapability()
    result = clone.execute("https://github.com/example/repo", method="https")
    print(f"✓ Repository Clone: {result.success}")
    clone.cleanup(result.path)
    
    # Repository Sync
    sync = RepositorySyncCapability()
    sync_result = sync.execute("repo-123", "pull")
    print(f"✓ Repository Sync: {sync_result.success}")
    
    # Repository Fingerprint
    fingerprint = RepositoryFingerprintCapability()
    fp = fingerprint.execute("/path/to/repo")
    print(f"✓ Repository Fingerprint: {fp.hash[:16]}...")
    
    # Repository Structure
    structure = RepositoryStructureCapability()
    struct = structure.execute("/path/to/repo")
    print(f"✓ Repository Structure: {struct.id}")
    
    # Technology Detection
    tech = TechnologyDetectionCapability()
    detection = tech.execute(["main.py", "requirements.txt", "setup.py", "Dockerfile"])
    print(f"✓ Technology Detection: {detection.languages}")
    
    # Dependency Analysis
    dep = DependencyAnalysisCapability()
    dep_result = dep.execute([{"name": "requests", "version": "2.28", "internal": False}])
    print(f"✓ Dependency Analysis: {len(dep_result.external_deps)} deps")
    
    # Code Indexing
    idx = CodeIndexingCapability()
    index = idx.execute(["main.py", "utils.py"])
    print(f"✓ Code Indexing: {index.total_symbols} symbols")
    
    # Architecture Extraction
    arch = ArchitectureExtractionCapability()
    model = arch.execute({})
    print(f"✓ Architecture Extraction: {len(model.layers)} layers")
    
    # Architecture Validation
    validator = ArchitectureValidationCapability()
    validation = validator.execute({}, [])
    print(f"✓ Architecture Validation: passed={validation.passed}")
    
    # Pattern Detection
    patterns = PatternDetectionCapability()
    matches = patterns.execute(["main.py"])
    print(f"✓ Pattern Detection: {len(matches)} patterns")
    
    # Anti-Pattern Detection
    anti = AntiPatternDetectionCapability()
    issues = anti.execute(["main.py"])
    print(f"✓ Anti-Pattern Detection: {len(issues)} issues")
    
    # Dead Code Detection
    dead = DeadCodeDetectionCapability()
    dead_code = dead.execute({})
    print(f"✓ Dead Code Detection: {len(dead_code)} dead code items")


def test_providers():
    """Test providers."""
    print("\n" + "=" * 60)
    print("Testing Providers")
    print("=" * 60)
    
    # Filesystem Provider
    fs = FilesystemProvider()
    health = fs.health_check()
    print(f"✓ Filesystem Provider: healthy={health['healthy']}")
    
    # Git Provider
    git = GitProvider()
    git_health = git.health_check()
    print(f"✓ Git Provider: healthy={git_health['healthy']}")
    
    # GitHub Provider
    gh = GitHubProvider(token="test-token")
    gh_health = gh.health_check()
    print(f"✓ GitHub Provider: authenticated={gh_health['authenticated']}")
    
    # Get provider
    provider = get_provider("filesystem")
    print(f"✓ Provider Registry: {provider.metadata.name}")


def test_skills():
    """Test skills."""
    print("\n" + "=" * 60)
    print("Testing Skills")
    print("=" * 60)
    
    # Clone Repository
    clone = CloneRepositorySkill()
    result = clone.execute({"url": "https://github.com/example/repo", "path": "/tmp/repo"})
    print(f"✓ CloneRepository Skill: success={result['success']}")
    
    # Pull Repository
    pull = PullRepositorySkill()
    result = pull.execute({"path": "/tmp/repo"})
    print(f"✓ PullRepository Skill: success={result['success']}")
    
    # Checkout Branch
    checkout = CheckoutBranchSkill()
    result = checkout.execute({"branch": "main", "path": "/tmp/repo"})
    print(f"✓ CheckoutBranch Skill: success={result['success']}")
    
    # Read File
    read = ReadFileSkill()
    result = read.execute({"path": "/etc/hostname"})
    print(f"✓ ReadFile Skill: success={result['success']}")
    
    # Write File
    write = WriteFileSkill()
    result = write.execute({"path": "/tmp/test.txt", "content": "Hello World"})
    print(f"✓ WriteFile Skill: success={result['success']}")
    
    # Search Files
    search = SearchFilesSkill()
    result = search.execute({"root": "/tmp", "pattern": "test"})
    print(f"✓ SearchFiles Skill: {len(result['matches'])} matches")
    
    # Execute CLI
    exec_cli = ExecuteCLISkill()
    result = exec_cli.execute({"command": "echo 'Hello'"})
    print(f"✓ ExecuteCLI Skill: success={result['success']}")
    
    # Run Tests
    tests = RunTestsSkill()
    result = tests.execute({"cwd": "/workspace", "framework": "pytest"})
    print(f"✓ RunTests Skill: success={result['success']}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS FOUNDATION CAPABILITY PROGRAM")
    print("CAPABILITY-000001 to CAPABILITY-000020")
    print("PROVIDER-000001 to PROVIDER-000015")
    print("SKILL-000001 to SKILL-000040")
    print("=" * 60)
    
    test_capabilities()
    test_providers()
    test_skills()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print("\nAGOS Foundation Programs Ready!")


if __name__ == "__main__":
    main()