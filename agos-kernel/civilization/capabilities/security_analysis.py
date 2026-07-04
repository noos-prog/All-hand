"""
Security Analysis Capability
PHASE-02: Foundation Civilization

Analyzes security patterns and vulnerabilities.
"""

import re
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SecurityFinding:
    """A security finding."""
    severity: str  # critical, high, medium, low
    type: str
    file: str
    line: int
    description: str


class SecurityAnalyzer:
    """
    Security Analyzer.
    
    Analyzes code for security issues.
    """
    
    def __init__(self):
        self.patterns = [
            # Critical
            (r'password\s*=\s*["\'][^"\']+["\']', 'hardcoded_password', 'critical'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'hardcoded_api_key', 'critical'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'hardcoded_secret', 'critical'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'hardcoded_token', 'critical'),
            (r'private_key\s*=\s*["\'][^"\']+["\']', 'hardcoded_private_key', 'critical'),
            
            # High
            (r'eval\s*\(', 'dangerous_eval', 'high'),
            (r'exec\s*\(', 'dangerous_exec', 'high'),
            (r'subprocess\s*\.\s*(call|run|Popen)\s*\(\s*shell\s*=\s*True', 'shell_injection', 'high'),
            (r'os\s*\.\s*system\s*\(', 'os_system', 'high'),
            
            # Medium
            (r'SQL\s*\(\s*["\']\s*SELECT', 'sql_injection_risk', 'medium'),
            (r'f["\'][^"\']*SELECT.*{', 'sql_injection_risk', 'medium'),
            (r'random\s*\.\s*random\s*\(\s*\)', 'weak_random', 'medium'),
            
            # Low
            (r'print\s*\(\s*.*password', 'info_disclosure', 'low'),
            (r'passw\s*=', 'potential_password', 'low'),
        ]
    
    def analyze(self, repo_path: str) -> Dict[str, Any]:
        """Analyze security."""
        repo_path = Path(repo_path).resolve()
        
        findings = []
        files_scanned = 0
        
        # Scan Python files
        for py_file in repo_path.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            files_scanned += 1
            findings.extend(self._scan_file(py_file))
        
        # Categorize findings
        by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
        }
        
        for finding in findings:
            by_severity[finding.severity].append({
                'type': finding.type,
                'file': finding.file,
                'line': finding.line,
                'description': finding.description,
            })
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(by_severity)
        
        return {
            'files_scanned': files_scanned,
            'total_findings': len(findings),
            'by_severity': {
                'critical': len(by_severity['critical']),
                'high': len(by_severity['high']),
                'medium': len(by_severity['medium']),
                'low': len(by_severity['low']),
            },
            'findings': findings[:20],  # Top 20
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'timestamp': datetime.utcnow().isoformat(),
        }
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = ['__pycache__', '.git', 'venv', 'test_', '_test.py']
        return any(ex in str(path) for ex in excluded)
    
    def _scan_file(self, file_path: Path) -> List[SecurityFinding]:
        """Scan a file for security issues."""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                for pattern, issue_type, severity in self.patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Filter out examples/placeholders
                        if not any(p in line.lower() for p in ['example', 'placeholder', 'your_', 'changeme', '#']):
                            findings.append(SecurityFinding(
                                severity=severity,
                                type=issue_type,
                                file=str(file_path.relative_to(file_path.parent.parent)),
                                line=i,
                                description=line.strip()[:100],
                            ))
        except Exception:
            pass
        
        return findings
    
    def _calculate_risk_score(self, by_severity: Dict) -> float:
        """Calculate overall risk score."""
        weights = {
            'critical': 40,
            'high': 25,
            'medium': 10,
            'low': 2,
        }
        
        score = 100
        for severity, weight in weights.items():
            score -= len(by_severity[severity]) * weight
        
        return max(0, min(100, score))
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level from score."""
        if score >= 80:
            return 'LOW'
        elif score >= 60:
            return 'MEDIUM'
        elif score >= 40:
            return 'HIGH'
        else:
            return 'CRITICAL'
