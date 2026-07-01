"""RIE Infrastructure - Git operations, file system operations."""
import os
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List, Optional

from domain import FileNode, Repository


class GitFetcher:
    """Fetches repositories from git."""
    
    def fetch(self, url: str, branch: str = "main", depth: int = 1) -> str:
        """Clone repository and return local path."""
        temp_dir = tempfile.mkdtemp(prefix="rie_repo_")
        repo_path = os.path.join(temp_dir, "repo")
        
        subprocess.run(
            ["git", "clone", "--branch", branch, "--depth", str(depth), url, repo_path],
            check=True,
            capture_output=True
        )
        
        return repo_path
    
    def get_metadata(self, repo_path: str) -> Dict[str, Any]:
        """Get repository metadata."""
        # Get remote URL
        result = subprocess.run(
            ["git", "-C", repo_path, "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        
        # Get branch
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        branch = result.stdout.strip()
        
        # Get commit
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True
        )
        commit = result.stdout.strip()
        
        # Get name and owner
        name = os.path.basename(url).replace(".git", "")
        parts = url.replace(".git", "").split("/")
        owner = parts[-2] if len(parts) >= 2 else ""
        
        return {
            "url": url,
            "name": name,
            "owner": owner,
            "branch": branch,
            "commit": commit
        }
    
    def cleanup(self, repo_path: str) -> None:
        """Clean up cloned repository."""
        parent = os.path.dirname(repo_path)
        if os.path.exists(parent):
            shutil.rmtree(parent, ignore_errors=True)


class FileSystemReader:
    """Reads files from filesystem."""
    
    def __init__(self, max_file_size: int = 1024 * 1024):  # 1MB
        self.max_file_size = max_file_size
    
    def read_repository(self, repo_path: str) -> List[FileNode]:
        """Read all files in repository."""
        files = []
        
        for dirpath, dirnames, filenames in os.walk(repo_path):
            # Skip .git
            if ".git" in dirpath:
                continue
            
            rel_dir = os.path.relpath(dirpath, repo_path)
            
            # Directories
            for dirname in dirnames:
                if dirname.startswith("."):
                    continue
                dir_path = os.path.join(rel_dir, dirname) if rel_dir != "." else dirname
                files.append(FileNode(path=dir_path, is_dir=True))
            
            # Files
            for filename in filenames:
                if filename.startswith("."):
                    continue
                file_path = os.path.join(rel_dir, filename) if rel_dir != "." else filename
                full_path = os.path.join(dirpath, filename)
                
                try:
                    size = os.path.getsize(full_path)
                    content = None
                    
                    if size < self.max_file_size:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                    
                    ext = os.path.splitext(filename)[1]
                    
                    files.append(FileNode(
                        path=file_path,
                        is_dir=False,
                        size=size,
                        content=content,
                        extension=ext
                    ))
                except:
                    pass
        
        return files


class RepositoryNormalizer:
    """Normalizes repositories to universal format."""
    
    def __init__(self, fetcher: GitFetcher, reader: FileSystemReader):
        self.fetcher = fetcher
        self.reader = reader
    
    def normalize(self, url: str, branch: str = "main") -> Dict[str, Any]:
        """Normalize a repository."""
        # Fetch
        repo_path = self.fetcher.fetch(url, branch)
        
        try:
            # Get metadata
            metadata = self.fetcher.get_metadata(repo_path)
            
            # Read files
            files = self.reader.read_repository(repo_path)
            
            # Normalize
            directories = list(set(f.path for f in files if f.is_dir))
            file_data = {
                f.path: {
                    "size": f.size,
                    "extension": f.extension,
                    "has_content": f.content is not None
                }
                for f in files if not f.is_dir
            }
            
            return {
                "url": metadata["url"],
                "name": metadata["name"],
                "owner": metadata["owner"],
                "branch": metadata["branch"],
                "commit": metadata["commit"],
                "directories": sorted(directories),
                "files": file_data,
                "total_files": len([f for f in files if not f.is_dir]),
                "total_directories": len(directories)
            }
        finally:
            self.fetcher.cleanup(repo_path)
