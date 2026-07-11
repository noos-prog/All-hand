"""Repository Fetcher."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class FetchStatus(Enum):
    """Fetch status."""
    PENDING = "pending"
    FETCHING = "fetching"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class FetcherResult:
    """Result of fetching a repository."""
    fetch_id: str
    repo_url: str
    status: FetchStatus
    local_path: Optional[str] = None
    files: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    fetched_at: Optional[datetime] = None


class Fetcher:
    """Base fetcher."""
    
    def fetch(self, repo_url: str) -> FetcherResult:
        """Fetch a repository."""
        pass


class RepositoryFetcher:
    """Repository Fetcher."""
    
    def __init__(self):
        self.fetchers: Dict[str, Fetcher] = {}
    
    def register_fetcher(self, source: str, fetcher: Fetcher) -> None:
        self.fetchers[source] = fetcher
    
    def fetch(self, repo_url: str) -> FetcherResult:
        """Fetch a repository."""
        result = FetcherResult(
            fetch_id=str(uuid.uuid4()),
            repo_url=repo_url,
            status=FetchStatus.PENDING,
        )
        
        if "github.com" in repo_url:
            result.status = FetchStatus.COMPLETED
            result.local_path = f"/tmp/{uuid.uuid4()}"
        elif "gitlab.com" in repo_url:
            result.status = FetchStatus.COMPLETED
            result.local_path = f"/tmp/{uuid.uuid4()}"
        else:
            result.status = FetchStatus.COMPLETED
            result.local_path = repo_url
        
        result.fetched_at = datetime.utcnow()
        return result
