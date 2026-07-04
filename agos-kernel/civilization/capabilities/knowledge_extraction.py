"""
Knowledge Extraction Capability
PHASE-02: Foundation Civilization

Extracts engineering knowledge from repositories.
"""

import ast
from pathlib import Path
from typing import Dict, List, Any, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class KnowledgeEntry:
    """A piece of extracted knowledge."""
    type: str  # module, class, function, pattern, convention
    name: str
    description: str = ""
    location: str = ""
    tags: List[str] = field(default_factory=list)


class KnowledgeExtractor:
    """
    Knowledge Extractor.
    
    Extracts engineering knowledge from software repositories.
    """
    
    def extract(self, repo_path: str) -> Dict[str, Any]:
        """Extract knowledge from repository."""
        repo_path = Path(repo_path).resolve()
        
        knowledge = {
            'modules': [],
            'classes': [],
            'functions': [],
            'patterns': [],
            'conventions': [],
            'technologies': [],
            'apis': [],
        }
        
        # Extract from Python files
        for py_file in repo_path.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content, filename=str(py_file))
                
                self._extract_from_tree(tree, py_file, knowledge)
            except Exception:
                pass
        
        # Extract technologies
        knowledge['technologies'] = self._detect_technologies(repo_path)
        
        # Extract conventions
        knowledge['conventions'] = self._detect_conventions(repo_path)
        
        return {
            'modules': knowledge['modules'][:50],
            'classes': knowledge['classes'][:50],
            'functions': knowledge['functions'][:50],
            'patterns': list(set(knowledge['patterns'])),
            'conventions': knowledge['conventions'],
            'technologies': knowledge['technologies'],
            'api_count': len(knowledge['apis']),
            'total_entries': (
                len(knowledge['modules']) + 
                len(knowledge['classes']) + 
                len(knowledge['functions'])
            ),
            'timestamp': datetime.utcnow().isoformat(),
        }
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = ['__pycache__', '.git', 'venv', 'test_', '_test.py', '.venv']
        return any(ex in str(path) for ex in excluded)
    
    def _extract_from_tree(self, tree: ast.AST, file_path: Path, knowledge: Dict) -> None:
        """Extract knowledge from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Module):
                if node.name:
                    knowledge['modules'].append({
                        'name': node.name,
                        'file': str(file_path.relative_to(file_path.parent.parent)),
                    })
            
            elif isinstance(node, ast.ClassDef):
                knowledge['classes'].append({
                    'name': node.name,
                    'bases': [base.attr if isinstance(base, ast.Attribute) else getattr(base, 'id', str(base)) 
                              for base in node.bases],
                    'file': str(file_path.relative_to(file_path.parent.parent)),
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                })
                
                # Detect patterns
                self._detect_class_pattern(node, knowledge)
            
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                knowledge['functions'].append({
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'file': str(file_path.relative_to(file_path.parent.parent)),
                    'is_public': not node.name.startswith('_'),
                })
                
                # Detect APIs (public functions)
                if not node.name.startswith('_'):
                    knowledge['apis'].append({
                        'name': node.name,
                        'file': str(file_path.relative_to(file_path.parent.parent)),
                    })
    
    def _detect_class_pattern(self, node: ast.ClassDef, knowledge: Dict) -> None:
        """Detect class patterns."""
        name_lower = node.name.lower()
        
        patterns = {
            'adapter': ['adapter', 'wrapper'],
            'factory': ['factory', 'creator'],
            'singleton': ['singleton', 'instance'],
            'strategy': ['strategy', 'policy'],
            'observer': ['observer', 'listener', 'subscriber'],
            'builder': ['builder', 'builder'],
            'decorator': ['decorator'],
            'facade': ['facade', 'service'],
            'repository': ['repository', 'repo'],
            'service': ['service', 'manager'],
        }
        
        for pattern, keywords in patterns.items():
            if any(kw in name_lower for kw in keywords):
                knowledge['patterns'].append(f"{pattern}:{node.name}")
    
    def _detect_technologies(self, repo_path: Path) -> List[str]:
        """Detect technologies used."""
        technologies = set()
        
        # Check for files
        files = [f.name for f in repo_path.rglob('*') if f.is_file()]
        
        tech_markers = {
            'python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
            'javascript': ['package.json', 'yarn.lock', 'pnpm-lock.yaml'],
            'typescript': ['tsconfig.json'],
            'docker': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'],
            'rust': ['Cargo.toml', 'Cargo.lock'],
            'go': ['go.mod', 'go.sum'],
            'java': ['pom.xml', 'build.gradle', 'settings.gradle'],
            'kotlin': ['build.gradle.kts'],
            'swift': ['Package.swift'],
            'dotnet': ['*.csproj', '*.sln'],
            'terraform': ['*.tf'],
            'ansible': ['ansible.cfg', 'playbook.yml'],
        }
        
        for tech, markers in tech_markers.items():
            for marker in markers:
                if marker in files or any(marker in f for f in files):
                    technologies.add(tech)
        
        return sorted(list(technologies))
    
    def _detect_conventions(self, repo_path: Path) -> List[Dict]:
        """Detect code conventions."""
        conventions = []
        
        # Check naming conventions
        snake_case_count = 0
        camel_case_count = 0
        pascal_case_count = 0
        
        for py_file in repo_path.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        name = node.name
                        if '_' in name and not name.startswith('_'):
                            snake_case_count += 1
                        elif name[0].isupper():
                            pascal_case_count += 1
                        elif name[0].islower():
                            camel_case_count += 1
            except Exception:
                pass
        
        if snake_case_count > 0:
            conventions.append({
                'type': 'naming',
                'style': 'snake_case',
                'usage': f'{snake_case_count} occurrences',
            })
        
        return conventions
