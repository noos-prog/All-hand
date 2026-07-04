"""
Dependency Analysis Capability
PHASE-02: Foundation Civilization

Analyzes software dependencies and their relationships.
"""

import json
import ast
from pathlib import Path
from typing import Dict, List, Any, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DependencyInfo:
    """Dependency information."""
    name: str = ""
    version: str = ""
    source: str = ""  # requirements.txt, package.json, etc.
    

@dataclass
class DependencyMetrics:
    """Dependency metrics."""
    internal_deps: int = 0
    external_deps: int = 0
    direct_deps: int = 0
    transitive_deps: int = 0
    outdated_deps: int = 0


class DependencyAnalyzer:
    """
    Dependency Analyzer.
    
    Analyzes software dependencies from various package managers.
    """
    
    def __init__(self):
        self.dependency_files = {
            'requirements.txt': self._parse_requirements,
            'Pipfile': self._parse_pipfile,
            'pyproject.toml': self._parse_pyproject,
            'package.json': self._parse_package_json,
            'package-lock.json': self._parse_package_lock,
            'Cargo.toml': self._parse_cargo,
            'go.mod': self._parse_go_mod,
            'pom.xml': self._parse_maven,
            'build.gradle': self._parse_gradle,
        }
    
    def analyze(self, repo_path: str) -> Dict[str, Any]:
        """Analyze dependencies."""
        repo_path = Path(repo_path).resolve()
        
        metrics = DependencyMetrics()
        dependencies = []
        sources = []
        
        # Find dependency files
        for dep_file, parser in self.dependency_files.items():
            for file_path in repo_path.rglob(dep_file):
                try:
                    deps = parser(file_path)
                    dependencies.extend(deps)
                    sources.append({
                        'file': str(file_path.relative_to(repo_path)),
                        'count': len(deps),
                        'type': dep_file,
                    })
                    
                    for dep in deps:
                        if dep.get('is_dev', False):
                            metrics.external_deps += 1
                        else:
                            metrics.direct_deps += 1
                except Exception:
                    pass
        
        # Analyze internal dependencies (Python imports)
        internal_deps = self._find_internal_deps(repo_path)
        metrics.internal_deps = len(internal_deps)
        
        result = {
            'total_dependencies': len(dependencies),
            'internal_dependencies': internal_deps,
            'dependency_sources': sources,
            'metrics': {
                'internal_deps': metrics.internal_deps,
                'external_deps': metrics.external_deps,
                'direct_deps': metrics.direct_deps,
                'transitive_deps': metrics.transitive_deps,
            },
            'dependencies': dependencies[:50],  # Limit for report size
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        return result
    
    def _find_internal_deps(self, repo_path: Path) -> List[str]:
        """Find internal module dependencies."""
        internal = set()
        modules = self._find_modules(repo_path)
        
        for py_file in repo_path.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module:
                            module = node.module.split('.')[0]
                            if module in modules:
                                internal.add(module)
            except Exception:
                pass
        
        return sorted(list(internal))
    
    def _find_modules(self, repo_path: Path) -> Set[str]:
        """Find all Python modules in repository."""
        modules = set()
        
        for py_file in repo_path.rglob('__init__.py'):
            try:
                module_path = py_file.parent.relative_to(repo_path)
                module = str(module_path).replace('/', '.').replace('\\', '.')
                modules.add(module.split('.')[0])
            except Exception:
                pass
        
        return modules
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = ['__pycache__', '.git', 'venv', 'test_', '_test.py']
        return any(ex in str(path) for ex in excluded)
    
    def _parse_requirements(self, file_path: Path) -> List[Dict]:
        """Parse requirements.txt."""
        deps = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '==' in line:
                            name, version = line.split('==', 1)
                            deps.append({'name': name.strip(), 'version': version.strip(), 'source': 'requirements.txt'})
                        elif '>=' in line:
                            name, version = line.split('>=', 1)
                            deps.append({'name': name.strip(), 'version': f'>={version.strip()}', 'source': 'requirements.txt'})
                        else:
                            deps.append({'name': line, 'version': '*', 'source': 'requirements.txt'})
        except Exception:
            pass
        return deps
    
    def _parse_pipfile(self, file_path: Path) -> List[Dict]:
        """Parse Pipfile."""
        return []  # Simplified - full TOML parsing would be needed
    
    def _parse_pyproject(self, file_path: Path) -> List[Dict]:
        """Parse pyproject.toml."""
        return []  # Simplified
    
    def _parse_package_json(self, file_path: Path) -> List[Dict]:
        """Parse package.json."""
        deps = []
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for key in ['dependencies', 'devDependencies']:
                if key in data:
                    for name, version in data[key].items():
                        deps.append({
                            'name': name,
                            'version': version,
                            'source': 'package.json',
                            'is_dev': key == 'devDependencies'
                        })
        except Exception:
            pass
        return deps
    
    def _parse_package_lock(self, file_path: Path) -> List[Dict]:
        """Parse package-lock.json."""
        return self._parse_package_json(file_path)
    
    def _parse_cargo(self, file_path: Path) -> List[Dict]:
        """Parse Cargo.toml."""
        return []
    
    def _parse_go_mod(self, file_path: Path) -> List[Dict]:
        """Parse go.mod."""
        deps = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('require'):
                        continue
                    if line and not line.startswith('module') and not line.startswith('go '):
                        parts = line.split(' ')
                        if len(parts) >= 2:
                            deps.append({'name': parts[0], 'version': parts[1], 'source': 'go.mod'})
        except Exception:
            pass
        return deps
    
    def _parse_maven(self, file_path: Path) -> List[Dict]:
        """Parse pom.xml."""
        return []
    
    def _parse_gradle(self, file_path: Path) -> List[Dict]:
        """Parse build.gradle."""
        return []
