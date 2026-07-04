"""
Repository DNA Generator
PHASE-02: Foundation Civilization

Generates unique DNA fingerprints for repositories.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DNAFragment:
    """A fragment of repository DNA."""
    type: str  # structure, code, config, dependency
    hash: str
    value: Any


class RepositoryDNA:
    """
    Repository DNA Generator.
    
    Generates unique DNA fingerprints for software repositories.
    DNA can be used to identify, compare, and track repositories.
    """
    
    VERSION = "1.0"
    
    def generate(self, repo_path: str) -> Dict[str, Any]:
        """Generate Repository DNA."""
        repo_path = Path(repo_path).resolve()
        
        fragments = {
            'structure': self._generate_structure_dna(repo_path),
            'code': self._generate_code_dna(repo_path),
            'config': self._generate_config_dna(repo_path),
            'dependency': self._generate_dependency_dna(repo_path),
        }
        
        # Combine all fragments
        combined = self._combine_fragments(fragments)
        
        return {
            'version': self.VERSION,
            'repository': repo_path.name,
            'path': str(repo_path),
            'generated_at': datetime.utcnow().isoformat(),
            'fragments': fragments,
            'dna': combined,
            'signature': hashlib.sha256(combined.encode()).hexdigest()[:32],
        }
    
    def _generate_structure_dna(self, repo_path: Path) -> str:
        """Generate DNA from repository structure."""
        structure_elements = []
        
        for item in sorted(repo_path.rglob('*')):
            if self._should_exclude(item):
                continue
            
            rel_path = str(item.relative_to(repo_path))
            
            if item.is_dir():
                structure_elements.append(f"DIR:{rel_path}")
            else:
                structure_elements.append(f"FILE:{rel_path}")
        
        structure_str = "\n".join(structure_elements)
        return hashlib.sha256(structure_str.encode()).hexdigest()[:16]
    
    def _generate_code_dna(self, repo_path: Path) -> str:
        """Generate DNA from code content."""
        code_hashes = []
        
        for py_file in repo_path.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Hash function/class names
                code_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
                code_hashes.append(code_hash)
            except Exception:
                pass
        
        combined = "".join(sorted(code_hashes))
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _generate_config_dna(self, repo_path: Path) -> str:
        """Generate DNA from configuration files."""
        config_files = [
            'package.json', 'setup.py', 'pyproject.toml', 'requirements.txt',
            'Dockerfile', 'docker-compose.yml', '.gitignore', '.dockerignore',
            'tsconfig.json', 'jest.config.js', 'pytest.ini', 'tox.ini',
        ]
        
        config_hashes = []
        
        for config_file in config_files:
            for file_path in repo_path.rglob(config_file):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    config_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
                    config_hashes.append(config_hash)
                except Exception:
                    pass
        
        if not config_hashes:
            return "NO_CONFIG"
        
        combined = "".join(sorted(config_hashes))
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _generate_dependency_dna(self, repo_path: Path) -> str:
        """Generate DNA from dependencies."""
        dep_hashes = []
        
        dep_files = [
            'requirements.txt', 'package.json', 'package-lock.json',
            'Pipfile', 'Pipfile.lock', 'go.mod', 'Cargo.toml',
        ]
        
        for dep_file in dep_files:
            for file_path in repo_path.rglob(dep_file):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    dep_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
                    dep_hashes.append(dep_hash)
                except Exception:
                    pass
        
        if not dep_hashes:
            return "NO_DEPS"
        
        combined = "".join(sorted(dep_hashes))
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _combine_fragments(self, fragments: Dict[str, str]) -> str:
        """Combine all fragments into single DNA."""
        combined = "|".join([
            f"{k}:{v}" for k, v in sorted(fragments.items())
        ])
        return combined
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = [
            '__pycache__', '.git', '.svn', '.hg',
            'node_modules', 'venv', '.venv', 'env',
            'dist', 'build', '.egg-info',
            '*.pyc', '*.pyo', '.pytest_cache',
            '.mypy_cache', '.tox', '.coverage',
            '.DS_Store', 'Thumbs.db',
        ]
        
        name = path.name
        for ex in excluded:
            if ex.startswith('*'):
                if name.endswith(ex[1:]):
                    return True
            elif name == ex:
                return True
        
        return False
    
    def compare(self, dna1: Dict, dna2: Dict) -> Dict[str, Any]:
        """Compare two repository DNAs."""
        similarity = 0
        differences = []
        
        for fragment in ['structure', 'code', 'config', 'dependency']:
            if dna1['fragments'].get(fragment) == dna2['fragments'].get(fragment):
                similarity += 25
            else:
                differences.append(fragment)
        
        return {
            'similarity_percent': similarity,
            'differences': differences,
            'same_repository': similarity == 100,
        }
