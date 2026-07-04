"""
Documentation Analysis Capability
PHASE-02: Foundation Civilization

Analyzes documentation quality and coverage.
"""

from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


class DocAnalyzer:
    """
    Documentation Analyzer.
    
    Analyzes documentation quality and coverage.
    """
    
    def __init__(self):
        self.doc_files = [
            'README.md', 'README.txt', 'README.rst',
            'CONTRIBUTING.md', 'CONTRIBUTING.txt',
            'LICENSE', 'LICENSE.txt', 'LICENSE.md',
            'CHANGELOG.md', 'CHANGELOG.txt',
            'docs/README.md', 'docs/index.md',
            'API.md', 'API.rst',
        ]
    
    def analyze(self, repo_path: str) -> Dict[str, Any]:
        """Analyze documentation."""
        repo_path = Path(repo_path).resolve()
        
        docs_found = []
        docs_missing = []
        coverage = {}
        
        # Check for documentation files
        for doc_pattern in self.doc_files:
            for doc_file in repo_path.rglob(doc_pattern):
                rel_path = str(doc_file.relative_to(repo_path))
                docs_found.append({
                    'file': rel_path,
                    'size': doc_file.stat().st_size,
                })
        
        # Check for required documentation
        required = ['README', 'LICENSE']
        for req in required:
            found = any(req.lower() in d['file'].lower() for d in docs_found)
            coverage[req] = found
        
        # Analyze README quality
        readme_quality = self._analyze_readme(repo_path)
        
        # Calculate scores
        score = self._calculate_doc_score(coverage, readme_quality)
        
        return {
            'documentation_files': docs_found,
            'total_docs': len(docs_found),
            'total_size_bytes': sum(d['size'] for d in docs_found),
            'coverage': coverage,
            'readme_quality': readme_quality,
            'score': score,
            'grade': self._get_grade(score),
            'timestamp': datetime.utcnow().isoformat(),
        }
    
    def _analyze_readme(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze README quality."""
        readme_files = [
            repo_path / 'README.md',
            repo_path / 'README.txt',
            repo_path / 'README.rst',
        ]
        
        for readme in readme_files:
            if readme.exists():
                with open(readme, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return {
                    'exists': True,
                    'file': readme.name,
                    'size': len(content),
                    'lines': content.count('\n'),
                    'has_installation': 'install' in content.lower(),
                    'has_usage': 'usage' in content.lower() or 'example' in content.lower(),
                    'has_license': 'license' in content.lower(),
                    'has_contributing': 'contribut' in content.lower(),
                }
        
        return {
            'exists': False,
            'file': None,
            'size': 0,
            'lines': 0,
        }
    
    def _calculate_doc_score(self, coverage: Dict, readme_quality: Dict) -> float:
        """Calculate documentation score."""
        score = 0
        
        # Coverage (50%)
        coverage_score = sum(1 for v in coverage.values() if v) / max(len(coverage), 1) * 50
        score += coverage_score
        
        # README quality (50%)
        if readme_quality['exists']:
            score += 20  # Base for having README
            if readme_quality.get('has_installation'):
                score += 10
            if readme_quality.get('has_usage'):
                score += 10
            if readme_quality.get('has_license'):
                score += 5
            if readme_quality.get('has_contributing'):
                score += 5
        
        return min(100, score)
    
    def _get_grade(self, score: float) -> str:
        """Convert score to grade."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
