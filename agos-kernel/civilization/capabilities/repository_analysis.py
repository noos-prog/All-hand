"""
Repository Analysis Capability
PHASE-02: Foundation Civilization

Analyzes software repositories to understand their structure and content.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RepositoryInfo:
    """Repository information."""
    name: str = ""
    path: str = ""
    size_bytes: int = 0
    file_count: int = 0
    directory_count: int = 0
    language: str = ""
    languages: Dict[str, int] = field(default_factory=dict)
    files: List[Dict] = field(default_factory=list)
    structure: Dict[str, Any] = field(default_factory=dict)
    
    
class RepositoryAnalyzer:
    """
    Repository Analyzer.
    
    Analyzes software repositories and produces comprehensive information.
    """
    
    def __init__(self):
        self.excluded_patterns = [
            '__pycache__', '.git', '.svn', '.hg',
            'node_modules', 'venv', '.venv', 'env',
            'dist', 'build', '.egg-info', '__pycache__',
            '*.pyc', '*.pyo', '.pytest_cache', '.tox',
            '.coverage', 'htmlcov', '.mypy_cache',
            '.DS_Store', 'Thumbs.db', '.idea', '.vscode'
        ]
        
        self.language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.hpp': 'C++ Header',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.less': 'Less',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.bash': 'Bash',
            '.zsh': 'Zsh',
            '.ps1': 'PowerShell',
            '.dockerfile': 'Dockerfile',
            '.toml': 'TOML',
            '.cfg': 'Config',
            '.ini': 'INI',
            '.conf': 'Config',
        }
    
    def analyze(self, repo_path: str) -> Dict[str, Any]:
        """
        Analyze a repository.
        
        Returns comprehensive repository information.
        """
        repo_path = Path(repo_path).resolve()
        
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        info = RepositoryInfo(
            name=repo_path.name,
            path=str(repo_path),
        )
        
        # Scan repository
        self._scan_directory(repo_path, info)
        
        # Detect primary language
        info.language = self._detect_primary_language(info.languages)
        
        # Generate structure
        info.structure = self._generate_structure(repo_path)
        
        # Calculate hash
        info.size_bytes = self._calculate_size(repo_path)
        
        return self._to_dict(info)
    
    def _scan_directory(self, path: Path, info: RepositoryInfo) -> None:
        """Scan directory and collect file information."""
        try:
            for item in path.iterdir():
                # Skip excluded patterns
                if self._should_exclude(item):
                    continue
                
                if item.is_dir():
                    info.directory_count += 1
                    self._scan_directory(item, info)
                elif item.is_file():
                    info.file_count += 1
                    
                    # Track language
                    ext = item.suffix.lower()
                    if ext in self.language_extensions:
                        lang = self.language_extensions[ext]
                        info.languages[lang] = info.languages.get(lang, 0) + 1
                    
                    # Record file info
                    try:
                        file_size = item.stat().st_size
                        info.files.append({
                            'path': str(item.relative_to(path)),
                            'name': item.name,
                            'extension': item.suffix,
                            'size': file_size,
                            'language': self.language_extensions.get(item.suffix.lower(), 'Unknown'),
                        })
                    except Exception:
                        pass
        except PermissionError:
            pass
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        name = path.name
        for pattern in self.excluded_patterns:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
        return False
    
    def _detect_primary_language(self, languages: Dict[str, int]) -> str:
        """Detect primary language based on file count."""
        if not languages:
            return "Unknown"
        return max(languages.items(), key=lambda x: x[1])[0]
    
    def _generate_structure(self, path: Path, max_depth: int = 3, current_depth: int = 0) -> Dict:
        """Generate repository structure."""
        if current_depth >= max_depth:
            return {'truncated': True}
        
        structure = {'name': path.name, 'type': 'directory', 'children': []}
        
        try:
            for item in sorted(path.iterdir()):
                if self._should_exclude(item):
                    continue
                    
                if item.is_dir():
                    structure['children'].append(
                        self._generate_structure(item, max_depth, current_depth + 1)
                    )
                else:
                    structure['children'].append({
                        'name': item.name,
                        'type': 'file',
                        'extension': item.suffix,
                    })
        except PermissionError:
            pass
        
        return structure
    
    def _calculate_size(self, path: Path) -> int:
        """Calculate total repository size."""
        total = 0
        try:
            for item in path.rglob('*'):
                if item.is_file() and not self._should_exclude(item):
                    try:
                        total += item.stat().st_size
                    except Exception:
                        pass
        except Exception:
            pass
        return total
    
    def _to_dict(self, info: RepositoryInfo) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': info.name,
            'path': info.path,
            'size_bytes': info.size_bytes,
            'size_mb': round(info.size_bytes / (1024 * 1024), 2),
            'file_count': info.file_count,
            'directory_count': info.directory_count,
            'primary_language': info.language,
            'languages': info.languages,
            'structure': info.structure,
            'timestamp': datetime.utcnow().isoformat(),
        }
