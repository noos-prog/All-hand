"""
Civilization Engine
PHASE-02: Foundation Civilization

The main engine for the Foundation Civilization.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
import json

from agos_kernel.civilization.core.foundation import Foundation, FoundationConfig
from agos_kernel.civilization.providers.filesystem_provider import FilesystemProvider
from agos_kernel.civilization.providers.git_provider import GitProvider
from agos_kernel.civilization.providers.github_provider import GitHubProvider


@dataclass
class CivilizationEngineStats:
    """Civilization engine statistics."""
    repositories_processed: int = 0
    reports_generated: int = 0
    dna_generated: int = 0
    knowledge_extracted: int = 0
    errors: int = 0


class CivilizationEngine:
    """
    Civilization Engine.
    
    The main engine that orchestrates all Foundation Civilization operations.
    
    Foundation Goal:
    - A software repository enters AGOS
    - AGOS understands it
    - Produces Engineering Knowledge
    - Produces Repository DNA
    - Produces Evidence
    - Produces Reports
    - Produces Improvement Recommendations
    - Without human intervention
    """
    
    VERSION = "2.0.0"
    PHASE = "FOUNDATION"
    
    def __init__(self, config: Optional[FoundationConfig] = None):
        self.config = config or FoundationConfig()
        self.foundation = Foundation(self.config)
        self.stats = CivilizationEngineStats()
        self.started_at = datetime.utcnow()
        self._output_dir = Path("/workspace/All-hand/agos-kernel/civilization/output")
    
    def initialize(self) -> bool:
        """Initialize the civilization engine."""
        print("=" * 70)
        print("AGOS FOUNDATION CIVILIZATION ENGINE")
        print("=" * 70)
        print(f"Version: {self.VERSION}")
        print(f"Phase: {self.PHASE}")
        print(f"Started: {datetime.utcnow().isoformat()}")
        print("=" * 70)
        print()
        
        # Initialize foundation
        if not self.foundation.initialize():
            return False
        
        # Create output directory
        self._output_dir.mkdir(parents=True, exist_ok=True)
        
        return True
    
    def process_repository(self, repo_path: str) -> Dict[str, Any]:
        """
        Process a complete repository.
        
        This is the main entry point for the Foundation Civilization.
        """
        print()
        print("=" * 70)
        print(f"PROCESSING REPOSITORY: {repo_path}")
        print("=" * 70)
        
        results = {
            'status': 'pending',
            'repository': repo_path,
            'outputs': {},
            'errors': [],
        }
        
        try:
            # Initialize if not already
            if not self.foundation.initialize():
                raise RuntimeError("Foundation initialization failed")
            
            # Process through foundation
            process_result = self.foundation.process_repository(repo_path)
            results['outputs'] = process_result['outputs']
            
            if process_result['status'] == 'completed':
                results['status'] = 'completed'
                self.stats.repositories_processed += 1
                self.stats.reports_generated += 1
                self.stats.dna_generated += 1
                self.stats.knowledge_extracted += 1
            else:
                results['status'] = 'failed'
                results['errors'].append(process_result.get('error', 'Unknown error'))
                self.stats.errors += 1
            
            # Save results
            self._save_results(results)
            
        except Exception as e:
            results['status'] = 'error'
            results['errors'].append(str(e))
            self.stats.errors += 1
            print(f"Error: {e}")
        
        print()
        print("=" * 70)
        print(f"PROCESSING COMPLETE: {results['status'].upper()}")
        print("=" * 70)
        
        return results
    
    def analyze_github_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Analyze a GitHub repository.
        
        Clone the repo, then process it.
        """
        print()
        print("=" * 70)
        print(f"ANALYZING GITHUB REPOSITORY: {owner}/{repo}")
        print("=" * 70)
        
        # Create temp directory for the repo
        import tempfile
        import subprocess
        
        temp_dir = Path(tempfile.mkdtemp())
        repo_path = temp_dir / repo
        
        results = {
            'status': 'pending',
            'github': {'owner': owner, 'repo': repo},
            'outputs': {},
        }
        
        try:
            # Clone repository
            print(f"Cloning {owner}/{repo}...")
            result = subprocess.run(
                ['git', 'clone', f'https://github.com/{owner}/{repo}.git', str(repo_path)],
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Clone failed: {result.stderr}")
            
            print("  ✓ Clone successful")
            
            # Analyze with GitHub provider
            github = GitHubProvider()
            github_analysis = github.analyze_repo(owner, repo)
            results['github_analysis'] = github_analysis
            
            # Process repository
            results['repository_analysis'] = self.foundation.analyze_repository(str(repo_path))
            
            # Generate DNA
            results['dna'] = self.foundation.generate_dna(str(repo_path))
            
            # Extract knowledge
            results['knowledge'] = self.foundation.extract_knowledge(str(repo_path))
            
            # Generate report
            results['report'] = self.foundation.generate_report(str(repo_path), results['repository_analysis'])
            
            results['status'] = 'completed'
            self.stats.repositories_processed += 1
            
            # Save results
            self._save_results(results)
            
            print("  ✓ Analysis complete")
            
        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            self.stats.errors += 1
            print(f"  ✗ Error: {e}")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        print()
        return results
    
    def _save_results(self, results: Dict) -> None:
        """Save processing results."""
        repo_name = Path(results['repository']).name if 'repository' in results else 'unknown'
        output_file = self._output_dir / f"{repo_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        self._output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Results saved to: {output_file}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            'version': self.VERSION,
            'phase': self.PHASE,
            'uptime_seconds': (datetime.utcnow() - self.started_at).total_seconds(),
            'foundation_stats': self.foundation.get_stats(),
            'engine_stats': {
                'repositories_processed': self.stats.repositories_processed,
                'reports_generated': self.stats.reports_generated,
                'dna_generated': self.stats.dna_generated,
                'knowledge_extracted': self.stats.knowledge_extracted,
                'errors': self.stats.errors,
            },
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check engine health."""
        return {
            'status': 'healthy' if self.stats.errors == 0 else 'degraded',
            'version': self.VERSION,
            'phase': self.PHASE,
            'timestamp': datetime.utcnow().isoformat(),
            'uptime_seconds': (datetime.utcnow() - self.started_at).total_seconds(),
        }


def run_civilization():
    """Run the Foundation Civilization engine."""
    engine = CivilizationEngine()
    
    if not engine.initialize():
        print("Initialization failed!")
        return 1
    
    # Process the current repository (AGOS itself)
    print("\nProcessing AGOS Kernel repository...")
    results = engine.process_repository("/workspace/All-hand")
    
    print("\n" + "=" * 70)
    print("CIVILIZATION ENGINE STATS")
    print("=" * 70)
    stats = engine.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    return 0 if results['status'] == 'completed' else 1


if __name__ == '__main__':
    import sys
    sys.exit(run_civilization())
