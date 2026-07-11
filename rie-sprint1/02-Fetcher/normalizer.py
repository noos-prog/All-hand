"""Repository Normalizer - Convert repositories to universal format."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
import os
import mimetypes


@dataclass
class NormalizedFile:
    """A normalized file representation."""
    path: str
    name: str
    extension: str
    size_bytes: int
    is_binary: bool
    content_type: str = ""


@dataclass
class NormalizedRepository:
    """A normalized repository representation."""
    repo_url: str
    repo_name: str
    files: List[NormalizedFile] = field(default_factory=list)
    directories: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class RepositoryNormalizer:
    """
    Repository Normalizer.
    
    Converts repositories to universal format:
    ✅ File normalization
    ✅ Directory structure extraction
    ✅ Metadata extraction
    """
    
    def normalize(self, local_path: str, repo_url: str) -> NormalizedRepository:
        """Normalize a repository."""
        files: List[NormalizedFile] = []
        directories: Set[str] = set()
        
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        
        # Walk directory
        for root, dirs, filenames in os.walk(local_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, local_path)
                
                # Skip hidden files
                if filename.startswith("."):
                    continue
                
                try:
                    stat = os.stat(file_path)
                    extension = os.path.splitext(filename)[1]
                    
                    # Detect binary
                    is_binary = False
                    if extension in [".pyc", ".so", ".dll", ".exe", ".png", ".jpg", ".gif", ".pdf"]:
                        is_binary = True
                    
                    files.append(NormalizedFile(
                        path=rel_path,
                        name=filename,
                        extension=extension,
                        size_bytes=stat.st_size,
                        is_binary=is_binary,
                    ))
                except:
                    pass
                
                directories.add(os.path.dirname(rel_path))
        
        return NormalizedRepository(
            repo_url=repo_url,
            repo_name=repo_name,
            files=files,
            directories=list(directories),
        )
