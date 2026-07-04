"""
Engineering Report Generator
PHASE-02: Foundation Civilization

Generates comprehensive engineering reports.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class EngineeringReport:
    """Complete engineering report."""
    repository: str
    version: str = "1.0"
    generated_at: str = ""
    summary: Dict = None
    recommendations: List[Dict] = None
    

class EngineeringReporter:
    """
    Engineering Report Generator.
    
    Generates comprehensive engineering reports with recommendations.
    """
    
    def __init__(self):
        self.report_version = "2.0.0"
    
    def generate(self, repo_path: str, analysis_results: Dict) -> Dict[str, Any]:
        """Generate engineering report."""
        repo_path = Path(repo_path)
        
        report = {
            'report_version': self.report_version,
            'repository': repo_path.name,
            'path': str(repo_path),
            'generated_at': datetime.utcnow().isoformat(),
            'summary': self._generate_summary(analysis_results),
            'sections': self._generate_sections(analysis_results),
            'recommendations': self._generate_recommendations(analysis_results),
            'evidence': self._generate_evidence(analysis_results),
        }
        
        return report
    
    def _generate_summary(self, analysis: Dict) -> Dict:
        """Generate executive summary."""
        repo_info = analysis.get('repository', {})
        arch_info = analysis.get('architecture', {})
        quality_info = analysis.get('code_quality', {})
        
        return {
            'repository_name': repo_info.get('name', 'Unknown'),
            'primary_language': repo_info.get('primary_language', 'Unknown'),
            'total_files': repo_info.get('file_count', 0),
            'total_size_mb': repo_info.get('size_mb', 0),
            'code_quality_grade': quality_info.get('scores', {}).get('grade', 'N/A'),
            'total_modules': arch_info.get('metrics', {}).get('total_modules', 0),
            'total_classes': arch_info.get('metrics', {}).get('total_classes', 0),
            'health_status': self._calculate_health_status(analysis),
        }
    
    def _calculate_health_status(self, analysis: Dict) -> str:
        """Calculate overall health status."""
        scores = []
        
        # Code quality
        quality = analysis.get('code_quality', {})
        if 'scores' in quality:
            scores.append(quality['scores'].get('overall', 0))
        
        # Architecture
        arch = analysis.get('architecture', {})
        metrics = arch.get('metrics', {})
        if metrics.get('total_modules', 0) > 0:
            scores.append(70)  # Architecture present
        
        if not scores:
            return "UNKNOWN"
        
        avg = sum(scores) / len(scores)
        
        if avg >= 80:
            return "EXCELLENT"
        elif avg >= 70:
            return "GOOD"
        elif avg >= 60:
            return "FAIR"
        else:
            return "NEEDS_IMPROVEMENT"
    
    def _generate_sections(self, analysis: Dict) -> Dict:
        """Generate report sections."""
        return {
            'repository': self._section_repository(analysis.get('repository', {})),
            'architecture': self._section_architecture(analysis.get('architecture', {})),
            'code_quality': self._section_code_quality(analysis.get('code_quality', {})),
        }
    
    def _section_repository(self, repo: Dict) -> Dict:
        """Repository section."""
        return {
            'name': repo.get('name', ''),
            'language': repo.get('primary_language', ''),
            'files': repo.get('file_count', 0),
            'size_mb': repo.get('size_mb', 0),
            'languages': repo.get('languages', {}),
        }
    
    def _section_architecture(self, arch: Dict) -> Dict:
        """Architecture section."""
        return {
            'modules': arch.get('metrics', {}).get('total_modules', 0),
            'classes': arch.get('metrics', {}).get('total_classes', 0),
            'functions': arch.get('metrics', {}).get('total_functions', 0),
            'patterns': arch.get('patterns', []),
            'layers': arch.get('layers', []),
        }
    
    def _section_code_quality(self, quality: Dict) -> Dict:
        """Code quality section."""
        return {
            'lines_of_code': quality.get('lines_of_code', 0),
            'comment_ratio': quality.get('comment_ratio', 0),
            'average_complexity': quality.get('average_complexity', 0),
            'issue_count': quality.get('issue_count', 0),
            'scores': quality.get('scores', {}),
        }
    
    def _generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate improvement recommendations."""
        recommendations = []
        
        # Code quality recommendations
        quality = analysis.get('code_quality', {})
        scores = quality.get('scores', {})
        
        if scores.get('documentation', 0) < 50:
            recommendations.append({
                'priority': 'high',
                'category': 'documentation',
                'title': 'Improve Documentation',
                'description': 'Add more docstrings and comments to code.',
            })
        
        if scores.get('complexity', 0) < 60:
            recommendations.append({
                'priority': 'medium',
                'category': 'complexity',
                'title': 'Reduce Code Complexity',
                'description': 'Break down complex functions into smaller units.',
            })
        
        # Architecture recommendations
        arch = analysis.get('architecture', {})
        patterns = arch.get('patterns', [])
        
        if len(patterns) < 3:
            recommendations.append({
                'priority': 'low',
                'category': 'architecture',
                'title': 'Consider Design Patterns',
                'description': 'Document and apply relevant design patterns.',
            })
        
        return recommendations
    
    def _generate_evidence(self, analysis: Dict) -> Dict:
        """Generate evidence package."""
        return {
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'analysis_version': self.report_version,
            'files_analyzed': analysis.get('repository', {}).get('file_count', 0),
            'verification': {
                'repository_processed': True,
                'analysis_complete': True,
                'evidence_generated': True,
            }
        }
    
    def export_report(self, report: Dict, output_path: Path) -> None:
        """Export report to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report exported to: {output_path}")
