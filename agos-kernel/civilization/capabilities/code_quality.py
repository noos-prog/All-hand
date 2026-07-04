"""
Code Quality Analysis Capability
PHASE-02: Foundation Civilization

Analyzes code quality metrics and produces quality scores.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class QualityMetrics:
    """Quality metrics."""
    files_analyzed: int = 0
    lines_of_code: int = 0
    lines_of_comments: int = 0
    blank_lines: int = 0
    complexity_total: int = 0
    issues: List[Dict] = field(default_factory=list)


class CodeQualityAnalyzer:
    """
    Code Quality Analyzer.
    
    Analyzes code quality and produces quality scores.
    """
    
    def __init__(self):
        self.max_line_length = 120
        self.max_function_length = 50
        self.max_complexity = 10
    
    def analyze(self, repo_path: str) -> Dict[str, Any]:
        """Analyze code quality."""
        repo_path = Path(repo_path).resolve()
        
        metrics = QualityMetrics()
        
        # Analyze Python files
        for py_file in repo_path.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                self._analyze_file(py_file, metrics)
            except Exception:
                pass
        
        # Calculate scores
        scores = self._calculate_scores(metrics)
        
        result = {
            'files_analyzed': metrics.files_analyzed,
            'lines_of_code': metrics.lines_of_code,
            'lines_of_comments': metrics.lines_of_comments,
            'blank_lines': metrics.blank_lines,
            'comment_ratio': round(metrics.lines_of_comments / max(metrics.lines_of_code, 1) * 100, 2),
            'average_complexity': round(metrics.complexity_total / max(metrics.files_analyzed, 1), 2),
            'scores': scores,
            'issues': metrics.issues[:20],  # Top 20 issues
            'issue_count': len(metrics.issues),
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        return result
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = ['__pycache__', '.git', 'venv', 'test_', '_test.py', '.venv']
        return any(ex in str(path) for ex in excluded)
    
    def _analyze_file(self, file_path: Path, metrics: QualityMetrics) -> None:
        """Analyze a single file."""
        metrics.files_analyzed += 1
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Count lines
        for line in lines:
            stripped = line.strip()
            if not stripped:
                metrics.blank_lines += 1
            elif stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                metrics.lines_of_comments += 1
            else:
                metrics.lines_of_code += 1
                
                # Check line length
                if len(line) > self.max_line_length:
                    metrics.issues.append({
                        'file': str(file_path.relative_to(file_path.parent.parent)),
                        'type': 'line_length',
                        'message': f'Line too long ({len(line)} chars)',
                        'severity': 'warning',
                    })
        
        # Analyze AST for complexity
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity = self._calculate_complexity(node)
                    metrics.complexity_total += complexity
                    
                    if complexity > self.max_complexity:
                        metrics.issues.append({
                            'file': str(file_path.relative_to(file_path.parent.parent)),
                            'type': 'complexity',
                            'message': f'Function {node.name} has complexity {complexity}',
                            'severity': 'warning',
                            'function': node.name,
                        })
        except Exception:
            pass
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_scores(self, metrics: QualityMetrics) -> Dict[str, float]:
        """Calculate quality scores."""
        # Documentation score
        doc_score = min(100, metrics.lines_of_comments / max(metrics.lines_of_code, 1) * 100 * 10)
        
        # Complexity score (inverse)
        avg_complexity = metrics.complexity_total / max(metrics.files_analyzed, 1)
        complexity_score = max(0, 100 - avg_complexity * 5)
        
        # Issue score (inverse)
        issue_penalty = min(50, len(metrics.issues) * 2)
        issue_score = 100 - issue_penalty
        
        # Overall score
        overall = (doc_score * 0.3 + complexity_score * 0.4 + issue_score * 0.3)
        
        return {
            'documentation': round(doc_score, 2),
            'complexity': round(complexity_score, 2),
            'issues': round(issue_score, 2),
            'overall': round(overall, 2),
            'grade': self._get_grade(overall),
        }
    
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
