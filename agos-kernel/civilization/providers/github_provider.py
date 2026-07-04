"""
GitHub Provider
PHASE-02: Foundation Civilization

Provides GitHub API operations for the Foundation Civilization.
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GitHubRepo:
    """GitHub repository information."""
    name: str
    full_name: str
    description: str
    language: str
    stars: int
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    created_at: str
    updated_at: str
    url: str


@dataclass
class GitHubIssue:
    """GitHub issue information."""
    number: int
    title: str
    body: str
    state: str
    labels: List[str]
    author: str
    created_at: str
    updated_at: str


@dataclass
class GitHubPR:
    """GitHub pull request information."""
    number: int
    title: str
    body: str
    state: str
    author: str
    base: str
    head: str
    merged: bool
    created_at: str
    url: str


class GitHubProvider:
    """
    GitHub Provider.
    
    Provides GitHub API operations for repository analysis.
    """
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('GITHUB_TOKEN', '')
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make API request."""
        import urllib.request
        
        url = f"{self.api_base}{endpoint}"
        headers = self.headers.copy()
        
        if data:
            headers["Content-Type"] = "application/json"
            data = json.dumps(data).encode()
        else:
            data = None
        
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"GitHub API error: {e.code} - {e.read().decode()}")
    
    def get_repo(self, owner: str, repo: str) -> GitHubRepo:
        """Get repository information."""
        data = self._request("GET", f"/repos/{owner}/{repo}")
        
        return GitHubRepo(
            name=data['name'],
            full_name=data['full_name'],
            description=data.get('description', ''),
            language=data.get('language', ''),
            stars=data.get('stargazers_count', 0),
            forks=data.get('forks_count', 0),
            open_issues=data.get('open_issues_count', 0),
            watchers=data.get('watchers_count', 0),
            default_branch=data.get('default_branch', 'main'),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', ''),
            url=data.get('html_url', ''),
        )
    
    def get_issues(self, owner: str, repo: str, state: str = "open") -> List[GitHubIssue]:
        """Get repository issues."""
        data = self._request("GET", f"/repos/{owner}/{repo}/issues?state={state}&per_page=100")
        
        issues = []
        for item in data:
            if 'pull_request' not in item:  # Skip PRs
                issues.append(GitHubIssue(
                    number=item['number'],
                    title=item['title'],
                    body=item.get('body', ''),
                    state=item['state'],
                    labels=[l['name'] for l in item.get('labels', [])],
                    author=item['user']['login'],
                    created_at=item['created_at'],
                    updated_at=item['updated_at'],
                ))
        
        return issues
    
    def get_pull_requests(self, owner: str, repo: str, state: str = "open") -> List[GitHubPR]:
        """Get repository pull requests."""
        data = self._request("GET", f"/repos/{owner}/{repo}/pulls?state={state}&per_page=100")
        
        prs = []
        for item in data:
            prs.append(GitHubPR(
                number=item['number'],
                title=item['title'],
                body=item.get('body', ''),
                state=item['state'],
                author=item['user']['login'],
                base=item['base']['ref'],
                head=item['head']['ref'],
                merged=item.get('merged', False),
                created_at=item['created_at'],
                url=item['html_url'],
            ))
        
        return prs
    
    def get_contributors(self, owner: str, repo: str) -> List[Dict]:
        """Get repository contributors."""
        data = self._request("GET", f"/repos/{owner}/{repo}/contributors?per_page=100")
        
        return [
            {
                'login': c['login'],
                'contributions': c['contributions'],
                'avatar': c['avatar_url'],
            }
            for c in data
        ]
    
    def get_commits(self, owner: str, repo: str, per_page: int = 100) -> List[Dict]:
        """Get repository commits."""
        data = self._request("GET", f"/repos/{owner}/{repo}/commits?per_page={per_page}")
        
        return [
            {
                'sha': c['sha'][:8],
                'message': c['commit']['message'].split('\n')[0],
                'author': c['commit']['author']['name'],
                'date': c['commit']['author']['date'],
                'url': c['html_url'],
            }
            for c in data
        ]
    
    def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Get language statistics."""
        return self._request("GET", f"/repos/{owner}/{repo}/languages")
    
    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """Get repository README."""
        try:
            data = self._request("GET", f"/repos/{owner}/{repo}/readme")
            import base64
            return base64.b64decode(data['content']).decode('utf-8')
        except RuntimeError:
            return None
    
    def get_branches(self, owner: str, repo: str) -> List[Dict]:
        """Get repository branches."""
        data = self._request("GET", f"/repos/{owner}/{repo}/branches")
        
        return [
            {
                'name': b['name'],
                'protected': b.get('protected', False),
                'commit': b['commit']['sha'][:8],
            }
            for b in data
        ]
    
    def analyze_repo(self, owner: str, repo: str) -> Dict[str, Any]:
        """Perform complete GitHub analysis."""
        print(f"Analyzing GitHub repository: {owner}/{repo}")
        
        analysis = {
            'repository': {},
            'issues': [],
            'pull_requests': [],
            'contributors': [],
            'languages': {},
            'commits': [],
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        # Get repository info
        try:
            repo_info = self.get_repo(owner, repo)
            analysis['repository'] = {
                'name': repo_info.name,
                'full_name': repo_info.full_name,
                'description': repo_info.description,
                'language': repo_info.language,
                'stars': repo_info.stars,
                'forks': repo_info.forks,
                'open_issues': repo_info.open_issues,
                'default_branch': repo_info.default_branch,
                'created_at': repo_info.created_at,
            }
            print(f"  ✓ Repository: {repo_info.name}")
        except Exception as e:
            print(f"  ✗ Repository: {e}")
        
        # Get languages
        try:
            analysis['languages'] = self.get_languages(owner, repo)
            print(f"  ✓ Languages: {len(analysis['languages'])}")
        except Exception as e:
            print(f"  ✗ Languages: {e}")
        
        # Get contributors
        try:
            analysis['contributors'] = self.get_contributors(owner, repo)
            print(f"  ✓ Contributors: {len(analysis['contributors'])}")
        except Exception as e:
            print(f"  ✗ Contributors: {e}")
        
        # Get open issues
        try:
            analysis['issues'] = self.get_issues(owner, repo, "open")
            print(f"  ✓ Open Issues: {len(analysis['issues'])}")
        except Exception as e:
            print(f"  ✗ Issues: {e}")
        
        # Get pull requests
        try:
            analysis['pull_requests'] = self.get_pull_requests(owner, repo, "open")
            print(f"  ✓ Open PRs: {len(analysis['pull_requests'])}")
        except Exception as e:
            print(f"  ✗ PRs: {e}")
        
        return analysis
