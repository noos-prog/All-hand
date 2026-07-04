"""
Architecture Analysis Capability
PHASE-02: Foundation Civilization

Analyzes software architecture patterns and structures.
"""

import ast
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ArchitectureMetrics:
    """Architecture metrics."""
    modules: int = 0
    classes: int = 0
    functions: int = 0
    interfaces: int = 0
    patterns_found: List[str] = field(default_factory=list)
    layers: List[str] = field(default_factory=list)
    dependencies: List[Dict] = field(default_factory=list)


class ArchitectureAnalyzer:
    """
    Architecture Analyzer.
    
    Analyzes software architecture patterns and produces insights.
    """
    
    PATTERNS = [
        'singleton', 'factory', 'observer', 'strategy', 'adapter',
        'decorator', 'facade', 'proxy', 'builder', 'prototype',
        'mvc', 'mvvm', 'repository', 'service', 'dao',
    ]
    
    LAYER_PATTERNS = [
        'presentation', 'ui', 'view', 'controller',
        'business', 'service', 'domain', 'logic',
        'data', 'repository', 'dao', 'dal',
        'infrastructure', 'adapter', 'provider',
    ]
    
    def analyze(self, repo_path: str) -> Dict[str, Any]:
        """Analyze architecture."""
        repo_path = Path(repo_path).resolve()
        
        metrics = ArchitectureMetrics()
        architecture = {
            'metrics': {},
            'patterns': [],
            'layers': [],
            'dependencies': [],
            'structure': {},
        }
        
        # Analyze Python files
        for py_file in repo_path.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(py_file))
                
                self._analyze_file(tree, py_file, metrics)
            except Exception:
                pass
        
        # Analyze patterns
        architecture['patterns'] = metrics.patterns_found
        architecture['layers'] = list(set(metrics.layers))
        architecture['dependencies'] = metrics.dependencies
        
        # Calculate metrics
        architecture['metrics'] = {
            'total_modules': metrics.modules,
            'total_classes': metrics.classes,
            'total_functions': metrics.functions,
            'total_interfaces': metrics.interfaces,
            'pattern_count': len(metrics.patterns_found),
            'layer_count': len(architecture['layers']),
        }
        
        architecture['timestamp'] = datetime.utcnow().isoformat()
        
        return architecture
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = ['__pycache__', '.git', 'venv', '.venv', 'test_', '_test.py']
        return any(ex in str(path) for ex in excluded)
    
    def _analyze_file(self, tree: ast.AST, file_path: Path, metrics: ArchitectureMetrics) -> None:
        """Analyze a single file."""
        metrics.modules += 1
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                metrics.classes += 1
                self._detect_patterns(node, metrics)
                
            elif isinstance(node, ast.FunctionDef):
                metrics.functions += 1
                self._detect_layer(node.name, metrics)
    
    def _detect_patterns(self, node: ast.ClassDef, metrics: ArchitectureMetrics) -> None:
        """Detect architectural patterns."""
        class_name = node.name.lower()
        
        for pattern in self.PATTERNS:
            if pattern in class_name:
                metrics.patterns_found.append(f"{pattern}: {node.name}")
    
    def _detect_layer(self, name: str, metrics: ArchitectureMetrics) -> None:
        """Detect architectural layers."""
        name_lower = name.lower()
        
        for layer in self.LAYER_PATTERNS:
            if layer in name_lower:
                metrics.layers.append(layer)
