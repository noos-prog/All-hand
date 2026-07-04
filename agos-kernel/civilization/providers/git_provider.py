"""
Git Provider
PHASE-02: Foundation Civilization

Provides Git operations for the Foundation Civilization.
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GitCommit:
    """Git commit information."""
    sha: str
    message: str
    author: str
    author_email: str
    date: str
    files_changed: int
    insertions: int
    deletions: int


@dataclass
class GitBranch:
    """Git branch information."""
    name: str
    is_current: bool
    is_remote: bool


class GitProvider:
    """
    Git Provider.
    
    Provides Git operations for repository analysis.
    """
    
    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
    
    def _run_git(self, *args) -> str:
        """Run a git command."""
        try:
            result = subprocess.run(
                ['git'] + list(args),
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {e.stderr}")
    
    def is_git_repo(self) -> bool:
        """Check if path is a git repository."""
        try:
            self._run_git('rev-parse', '--git-dir')
            return True
        except RuntimeError:
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get repository status."""
        output = self._run_git('status', '--porcelain')
        
        modified = []
        untracked = []
        
        for line in output.split('\n'):
            if not line:
                continue
            
            status = line[:2]
            file = line[3:]
            
            if status[0] == '?' or status[1] == '?':
                untracked.append(file)
            else:
                modified.append(file)
        
        return {
            'is_dirty': len(modified) > 0 or len(untracked) > 0,
            'modified': modified,
            'untracked': untracked,
            'branch': self.get_current_branch(),
        }
    
    def get_current_branch(self) -> str:
        """Get current branch name."""
        return self._run_git('rev-parse', '--abbrev-ref', 'HEAD')
    
    def get_branches(self) -> List[GitBranch]:
        """Get all branches."""
        output = self._run_git('branch', '-a')
        
        branches = []
        current = self.get_current_branch()
        
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            is_remote = line.startswith('remotes/')
            name = line.replace('remotes/', '').replace('* ', '')
            
            branches.append(GitBranch(
                name=name,
                is_current=name == current or f'remotes/origin/{current}' == name,
                is_remote=is_remote,
            ))
        
        return branches
    
    def get_commits(self, max_count: int = 50) -> List[GitCommit]:
        """Get commit history."""
        output = self._run_git(
            'log', f'--max-count={max_count}',
            '--pretty=format:%H|%s|%an|%ae|%aI',
        )
        
        commits = []
        stats_output = self._run_git(
            'log', f'--max-count={max_count}',
            '--numstat', '--pretty=format:',
        )
        
        # Parse stats
        stats = {}
        for line in stats_output.split('\n'):
            if line and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    insertions = parts[1] if parts[1] != '-' else 0
                    deletions = parts[2] if parts[2] != '-' else 0
                    stats[line] = (int(insertions), int(deletions))
        
        # Parse commits
        for i, line in enumerate(output.split('\n')):
            if not line or '|' not in line:
                continue
            
            parts = line.split('|')
            if len(parts) >= 5:
                commits.append(GitCommit(
                    sha=parts[0][:8],
                    message=parts[1],
                    author=parts[2],
                    author_email=parts[3],
                    date=parts[4],
                    files_changed=0,
                    insertions=0,
                    deletions=0,
                ))
        
        return commits
    
    def get_diff(self, ref: str = "HEAD") -> str:
        """Get diff for a reference."""
        return self._run_git('diff', ref)
    
    def get_file_history(self, file_path: str) -> List[Dict]:
        """Get file change history."""
        output = self._run_git(
            'log', '--follow', '--pretty=format:%H|%s|%an|%aI',
            '--', file_path,
        )
        
        history = []
        for line in output.split('\n'):
            if not line or '|' not in line:
                continue
            
            parts = line.split('|')
            if len(parts) >= 4:
                history.append({
                    'sha': parts[0][:8],
                    'message': parts[1],
                    'author': parts[2],
                    'date': parts[3],
                })
        
        return history
    
    def get_remote_url(self) -> Optional[str]:
        """Get remote URL."""
        try:
            return self._run_git('remote', 'get-url', 'origin')
        except RuntimeError:
            return None
    
    def get_contributors(self) -> List[Dict]:
        """Get contributor statistics."""
        output = self._run_git(
            'shortlog', '-sne', '--all',
        )
        
        contributors = []
        for line in output.split('\n'):
            if not line:
                continue
            
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                count = int(parts[0].strip())
                name_email = parts[1].strip()
                
                if '<' in name_email:
                    name = name_email.split('<')[0].strip()
                    email = name_email.split('<')[1].replace('>', '').strip()
                else:
                    name = name_email
                    email = ""
                
                contributors.append({
                    'commits': count,
                    'name': name,
                    'email': email,
                })
        
        return sorted(contributors, key=lambda x: x['commits'], reverse=True)
