"""Local Repository Provider."""
import os
import subprocess
import tempfile
from typing import Generator

from contracts import FileNode, RepositoryMetadata, RepositorySnapshot
from interfaces import IProvider, SkillInput, SkillOutput


class CloneRepositoryInput(SkillInput):
    """Input for CloneRepository skill."""
    def __init__(self, url: str, branch: str = "main"):
        self.url = url
        self.branch = branch


class CloneRepositoryOutput(SkillOutput):
    """Output from CloneRepository skill."""
    def __init__(self, path: str, metadata: RepositoryMetadata):
        self.path = path
        self.metadata = metadata


class ReadRepositoryInput(SkillInput):
    """Input for ReadRepository skill."""
    def __init__(self, path: str):
        self.path = path


class ReadRepositoryOutput(SkillOutput):
    """Output from ReadRepository skill."""
    def __init__(self, snapshot: RepositorySnapshot):
        self.snapshot = snapshot


class LocalRepositoryProvider(IProvider):
    """
    Provider for local filesystem repository operations.
    Stateless, replaceable, no business logic.
    """
    
    @property
    def name(self) -> str:
        return "LocalRepositoryProvider"
    
    def supports_skill(self, skill_name: str) -> bool:
        return skill_name in ["CloneRepository", "ReadRepository"]
    
    def execute(self, skill_name: str, input_data: SkillInput) -> SkillOutput:
        if skill_name == "CloneRepository":
            return self._clone(input_data)
        elif skill_name == "ReadRepository":
            return self._read(input_data)
        else:
            raise ValueError(f"Unknown skill: {skill_name}")
    
    def Clone(self, url: str, branch: str = "main") -> str:
        """Clone a git repository."""
        temp_dir = tempfile.mkdtemp(prefix="agos_repo_")
        repo_path = os.path.join(temp_dir, "repo")
        subprocess.run(
            ["git", "clone", "--branch", branch, "--depth", "1", url, repo_path],
            check=True, capture_output=True
        )
        return repo_path
    
    def Open(self, path: str) -> str:
        """Open a repository."""
        if not os.path.isdir(path):
            raise ValueError(f"Not a directory: {path}")
        if not os.path.isdir(os.path.join(path, ".git")):
            raise ValueError(f"Not a git repository: {path}")
        return os.path.abspath(path)
    
    def Read(self, path: str) -> RepositorySnapshot:
        """Read an entire repository."""
        repo_path = self.Open(path)
        metadata = self.Metadata(repo_path)
        files = list(self._walk_files(repo_path))
        return RepositorySnapshot(metadata=metadata, files=files, root_path=repo_path)
    
    def Walk(self, path: str) -> Generator[FileNode, None, None]:
        """Walk through files."""
        repo_path = self.Open(path)
        yield from self._walk_files(repo_path)
    
    def Exists(self, path: str) -> bool:
        """Check if repository exists."""
        return os.path.isdir(os.path.join(path, ".git"))
    
    def Metadata(self, path: str) -> RepositoryMetadata:
        """Get repository metadata."""
        repo_path = self.Open(path)
        
        result = subprocess.run(
            ["git", "-C", repo_path, "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        branch = result.stdout.strip()
        
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True
        )
        commit = result.stdout.strip()
        
        name = os.path.basename(url).replace(".git", "")
        parts = url.replace(".git", "").split("/")
        owner = parts[-2] if len(parts) >= 2 else ""
        
        return RepositoryMetadata(
            url=url, name=name, owner=owner,
            branch=branch, commit=commit
        )
    
    def _clone(self, input_data: CloneRepositoryInput) -> CloneRepositoryOutput:
        path = self.Clone(input_data.url, input_data.branch)
        metadata = self.Metadata(path)
        return CloneRepositoryOutput(path=path, metadata=metadata)
    
    def _read(self, input_data: ReadRepositoryInput) -> ReadRepositoryOutput:
        snapshot = self.Read(input_data.path)
        return ReadRepositoryOutput(snapshot=snapshot)
    
    def _walk_files(self, root: str) -> Generator[FileNode, None, None]:
        """Walk through files in a directory."""
        for dirpath, dirnames, filenames in os.walk(root):
            if ".git" in dirpath:
                continue
            
            rel_dir = os.path.relpath(dirpath, root)
            
            for dirname in dirnames:
                if dirname.startswith("."):
                    continue
                dir_path = os.path.join(rel_dir, dirname) if rel_dir != "." else dirname
                yield FileNode(path=dir_path, is_dir=True)
            
            for filename in filenames:
                if filename.startswith("."):
                    continue
                file_path = os.path.join(rel_dir, filename) if rel_dir != "." else filename
                full_path = os.path.join(dirpath, filename)
                
                try:
                    size = os.path.getsize(full_path)
                    if size < 1024 * 1024:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                    else:
                        content = None
                except:
                    size = 0
                    content = None
                
                yield FileNode(path=file_path, is_dir=False, size=size, content=content)
