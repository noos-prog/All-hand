#!/usr/bin/env python3
"""
AGOS System Registry & Integrity Checker
========================================

Performs full integrity reconciliation of the AGOS civilization blueprint.
Builds authoritative registry of all components.
"""

import os
import re
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from enum import Enum


class ComponentStatus(Enum):
    IMPLEMENTED = "IMPLEMENTED"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    DUPLICATE = "DUPLICATE"
    CONFLICTING = "CONFLICTING"
    UNKNOWN = "UNKNOWN"
    DEFINED_ONLY = "DEFINED_ONLY"
    SIMULATED = "SIMULATED"
    BROKEN = "BROKEN"


class ComponentCategory(Enum):
    RUNTIME = "Runtime"
    ENGINE = "Engine"
    DOCUMENT = "Document"
    GOVERNANCE = "Governance"
    CAPABILITY = "Capability"
    PROVIDER = "Provider"
    ADAPTER = "Adapter"
    SKILL = "Skill"
    MODEL = "Model"
    ORCHESTRATOR = "Orchestrator"
    KNOWLEDGE = "Knowledge"
    EVIDENCE = "Evidence"
    ORCHESTRATION = "Orchestration"
    FOUNDATION = "Foundation"


@dataclass
class Component:
    """A component in the AGOS system."""
    name: str
    canonical_name: str
    category: str
    declared_purpose: str
    expected_interfaces: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: str = ComponentStatus.UNKNOWN.value
    file_path: str = ""
    line_count: int = 0
    is_executable: bool = False
    is_registry: bool = False
    has_tests: bool = False
    duplicates: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RegistryReport:
    """System registry report."""
    components: Dict[str, Component] = field(default_factory=dict)
    duplicates: Dict[str, List[str]] = field(default_factory=dict)
    missing: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    orphans: List[str] = field(default_factory=list)
    integrity_score: float = 0.0
    generated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "components": {k: v.to_dict() for k, v in self.components.items()},
            "duplicates": self.duplicates,
            "missing": self.missing,
            "conflicts": self.conflicts,
            "orphans": self.orphans,
            "integrity_score": self.integrity_score,
            "generated_at": self.generated_at.isoformat(),
        }


class AGOSSystemRegistry:
    """Authoritative registry of all AGOS components."""
    
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.components: Dict[str, Component] = {}
        self.category_patterns = {
            ComponentCategory.RUNTIME: [r"runtime\.py$", r"Runtime", r"runtime"],
            ComponentCategory.ENGINE: [r"engine\.py$", r"Engine"],
            ComponentCategory.CAPABILITY: [r"capabilities/", r"Capability"],
            ComponentCategory.PROVIDER: [r"providers/", r"Provider"],
            ComponentCategory.ADAPTER: [r"adapters/", r"Adapter"],
            ComponentCategory.SKILL: [r"skills/", r"Skill"],
            ComponentCategory.MODEL: [r"models\.py$", r"@dataclass", r"class.*Model"],
            ComponentCategory.DOCUMENT: [r"\.md$", r"README"],
            ComponentCategory.GOVERNANCE: [r"governance/", r"policy", r"Policy"],
            ComponentCategory.KNOWLEDGE: [r"knowledge/", r"Knowledge"],
            ComponentCategory.EVIDENCE: [r"evidence", r"Evidence"],
        }
        
    def scan_repository(self) -> None:
        """Scan entire repository and build registry."""
        print("=" * 70)
        print("PHASE 1: SCANNING REPOSITORY")
        print("=" * 70)
        
        for root, dirs, files in os.walk(self.root_path):
            # Skip .git and __pycache__
            if ".git" in root or "__pycache__" in root:
                continue
                
            for filename in files:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, self.root_path)
                
                if filename.endswith(".py"):
                    self._scan_python_file(filepath, rel_path)
                elif filename.endswith(".md"):
                    self._scan_markdown_file(filepath, rel_path)
        
        print(f"\nTotal components scanned: {len(self.components)}")
    
    def _scan_python_file(self, filepath: str, rel_path: str) -> None:
        """Scan a Python file for components."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")
            
            line_count = len(lines)
            
            # Find classes and functions
            classes = re.findall(r'^class (\w+)', content, re.MULTILINE)
            functions = re.findall(r'^def (\w+)', content, re.MULTILINE)
            
            # Find component categories
            category = self._detect_category(filepath, content)
            
            # Determine status
            status = self._determine_status(content, classes, functions)
            
            # Check for registry patterns
            is_registry = any(x in content.lower() for x in ["registry", "_registry", "REGISTRY"])
            has_tests = self._has_associated_tests(rel_path)
            
            # Process each class as a component
            for class_name in classes:
                canonical = self._canonicalize_name(class_name)
                
                # Skip private classes
                if class_name.startswith("_"):
                    continue
                
                component = Component(
                    name=class_name,
                    canonical_name=canonical,
                    category=category,
                    declared_purpose=self._extract_purpose(content, class_name),
                    file_path=rel_path,
                    line_count=line_count,
                    is_executable=status in [ComponentStatus.IMPLEMENTED.value, ComponentStatus.PARTIAL.value],
                    is_registry=is_registry,
                    has_tests=has_tests,
                    status=status,
                )
                
                self.components[canonical] = component
            
            # Check for duplicate names across files
            for class_name in classes:
                canonical = self._canonicalize_name(class_name)
                if canonical in self.components:
                    existing = self.components[canonical]
                    if existing.file_path != rel_path:
                        if rel_path not in existing.duplicates:
                            existing.duplicates.append(rel_path)
                            existing.status = ComponentStatus.DUPLICATE.value
                            
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
    
    def _scan_markdown_file(self, filepath: str, rel_path: str) -> None:
        """Scan a Markdown file for documentation components."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Extract title
            title_match = re.search(r'^#+\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else os.path.basename(filepath)
            
            # Determine document type
            if any(x in rel_path.lower() for x in ["adr", "decision", "constitution", "canon"]):
                category = ComponentCategory.DOCUMENT.value
                status = ComponentStatus.DEFINED_ONLY.value
            else:
                category = ComponentCategory.DOCUMENT.value
                status = ComponentStatus.DEFINED_ONLY.value
            
            canonical = self._canonicalize_name(title)
            
            component = Component(
                name=title,
                canonical_name=canonical,
                category=category,
                declared_purpose=self._extract_doc_purpose(content),
                file_path=rel_path,
                line_count=len(content.split("\n")),
                is_executable=False,
                status=status,
            )
            
            self.components[canonical] = component
            
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
    
    def _detect_category(self, filepath: str, content: str) -> str:
        """Detect the category of a component."""
        filepath_lower = filepath.lower()
        
        for category, patterns in self.category_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filepath_lower) or re.search(pattern, content):
                    return category.value
        
        return ComponentCategory.FOUNDATION.value
    
    def _determine_status(self, content: str, classes: List[str], functions: List[str]) -> str:
        """Determine if a component is implemented or just defined."""
        # Check for pass statements (empty implementation)
        pass_count = content.count("pass")
        
        # Check for NotImplementedError
        not_impl_count = content.count("NotImplementedError")
        
        # Check for actual implementation patterns
        has_logic = any([
            "return " in content,
            "for " in content and " in " in content,
            "if " in content,
            "try:" in content,
            "raise " in content,
            len(classes) > 0 and len(functions) > 1,
        ])
        
        # Check for stubs
        is_stub = pass_count > 2 and not_impl_count > 0
        
        if is_stub:
            return ComponentStatus.PARTIAL.value
        elif has_logic:
            return ComponentStatus.IMPLEMENTED.value
        elif classes or functions:
            return ComponentStatus.PARTIAL.value
        else:
            return ComponentStatus.UNKNOWN.value
    
    def _has_associated_tests(self, filepath: str) -> bool:
        """Check if component has associated tests."""
        test_patterns = [
            filepath.replace(".py", "_test.py"),
            "test_" + os.path.basename(filepath),
            os.path.dirname(filepath) + "/tests/" + os.path.basename(filepath),
        ]
        
        for pattern in test_patterns:
            full_path = os.path.join(self.root_path, pattern)
            if os.path.exists(full_path):
                return True
        
        return False
    
    def _canonicalize_name(self, name: str) -> str:
        """Create canonical name for deduplication."""
        # Remove common prefixes/suffixes
        name = re.sub(r'^(Runtime|Engine|Capability|Provider|Adapter|Skill)$', '', name)
        return name.upper().replace(" ", "_").replace("-", "_")
    
    def _extract_purpose(self, content: str, class_name: str) -> str:
        """Extract declared purpose from docstring."""
        docstring_match = re.search(
            rf'class {class_name}.*?"""(.*?)"""',
            content,
            re.DOTALL
        )
        if docstring_match:
            docstring = docstring_match.group(1).strip()
            first_line = docstring.split("\n")[0].strip()
            return first_line[:200]
        return ""
    
    def _extract_doc_purpose(self, content: str) -> str:
        """Extract purpose from markdown document."""
        lines = content.split("\n")
        for line in lines:
            if line.startswith("##"):
                return line.replace("##", "").strip()[:200]
        return content[:200]
    
    def detect_duplicates(self) -> Dict[str, List[str]]:
        """Detect duplicate components."""
        print("\n" + "=" * 70)
        print("PHASE 2: DUPLICATE DETECTION")
        print("=" * 70)
        
        duplicates = {}
        name_map: Dict[str, List[str]] = {}
        
        for canonical, component in self.components.items():
            # Use base name for comparison
            base_name = re.sub(r'^(RUNTIME|ENGINE|CAPABILITY|PROVIDER|ADAPTER|SKILL)_*', '', canonical)
            
            if base_name not in name_map:
                name_map[base_name] = []
            name_map[base_name].append(canonical)
        
        for base_name, canons in name_map.items():
            if len(canons) > 1:
                duplicates[base_name] = canons
                for c in canons:
                    if c in self.components:
                        self.components[c].status = ComponentStatus.DUPLICATE.value
        
        print(f"Duplicate groups found: {len(duplicates)}")
        for base, canons in list(duplicates.items())[:10]:
            print(f"  {base}: {canons}")
        
        return duplicates
    
    def detect_gaps(self) -> List[str]:
        """Detect missing implementations."""
        print("\n" + "=" * 70)
        print("PHASE 3: GAP DETECTION")
        print("=" * 70)
        
        missing = []
        
        # Required components based on architecture
        required = {
            "KERNEL": "agos-kernel/kernel or main.py",
            "CORE": "agos-kernel/core/__init__.py",
            "BRAIN": "agos-kernel/brain/engine.py",
            "PROVIDER_REGISTRY": "agos-kernel/providers/base.py",
            "CAPABILITY_REGISTRY": "agos-kernel/capabilities/base.py",
            "KNOWLEDGE_RUNTIME": "agos-kernel/knowledge/runtime.py",
            "MEMORY_RUNTIME": "agos-kernel/memory/runtime.py",
            "MISSION_MANAGER": "agos-kernel/mission/__init__.py",
            "EVENT_BUS": "agos-kernel/events/__init__.py",
            "GOVERNANCE_RUNTIME": "agos-kernel/governance/runtime.py",
        }
        
        for req, expected_path in required.items():
            found = False
            for canonical, component in self.components.items():
                if req in canonical or req.replace("_", "") in canonical.replace("_", ""):
                    if component.status == ComponentStatus.IMPLEMENTED.value:
                        found = True
                        break
            
            if not found:
                missing.append(f"{req} -> Expected: {expected_path}")
        
        print(f"Missing required components: {len(missing)}")
        for m in missing[:10]:
            print(f"  - {m}")
        
        return missing
    
    def calculate_integrity_score(self) -> float:
        """Calculate system integrity score (0-100)."""
        total = len(self.components)
        if total == 0:
            return 0.0
        
        implemented = sum(1 for c in self.components.values() 
                         if c.status == ComponentStatus.IMPLEMENTED.value)
        partial = sum(1 for c in self.components.values() 
                     if c.status == ComponentStatus.PARTIAL.value)
        defined = sum(1 for c in self.components.values() 
                     if c.status == ComponentStatus.DEFINED_ONLY.value)
        duplicates = sum(1 for c in self.components.values() 
                        if c.status == ComponentStatus.DUPLICATE.value)
        
        # Weighted score
        score = (implemented * 1.0 + partial * 0.5 + defined * 0.3) / total * 100
        score -= duplicates * 0.5  # Penalty for duplicates
        
        return max(0.0, min(100.0, score))
    
    def generate_report(self) -> RegistryReport:
        """Generate full integrity report."""
        report = RegistryReport()
        report.duplicates = self.detect_duplicates()
        report.missing = self.detect_gaps()
        report.integrity_score = self.calculate_integrity_score()
        
        for canonical, component in self.components.items():
            if component.status == ComponentStatus.DUPLICATE.value:
                report.components[f"[DUP] {canonical}"] = component
            elif component.status == ComponentStatus.UNKNOWN.value:
                report.components[f"[UNK] {canonical}"] = component
        
        return report
    
    def print_summary(self) -> None:
        """Print registry summary."""
        print("\n" + "=" * 70)
        print("SYSTEM REGISTRY SUMMARY")
        print("=" * 70)
        
        by_category: Dict[str, int] = {}
        by_status: Dict[str, int] = {}
        
        for component in self.components.values():
            by_category[component.category] = by_category.get(component.category, 0) + 1
            by_status[component.status] = by_status.get(component.status, 0) + 1
        
        print("\nBy Category:")
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")
        
        print("\nBy Status:")
        for status, count in sorted(by_status.items(), key=lambda x: -x[1]):
            print(f"  {status}: {count}")


def main():
    """Run AGOS system registry."""
    root = "/workspace/project/All-hand"
    
    print("AGOS SYSTEM REGISTRY")
    print("Full Integrity Reconciliation")
    print("=" * 70)
    
    registry = AGOSSystemRegistry(root)
    registry.scan_repository()
    report = registry.generate_report()
    
    registry.print_summary()
    
    # Save report
    report_path = os.path.join(root, "agos_system_registry_report.json")
    with open(report_path, "w") as f:
        json.dump(report.to_dict(), f, indent=2, default=str)
    
    print(f"\nFull report saved to: {report_path}")
    print(f"\nIntegrity Score: {report.integrity_score:.1f}/100")
    
    return report


if __name__ == "__main__":
    main()
