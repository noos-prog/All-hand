"""
Filesystem Provider
PHASE-02: Foundation Civilization

Provides filesystem access for the Foundation Civilization.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileInfo:
    """File information."""
    path: str
    name: str
    size: int
    is_dir: bool
    is_file: bool
    modified: float
    created: float


class FilesystemProvider:
    """
    Filesystem Provider.
    
    Provides standardized access to filesystem operations.
    """
    
    def __init__(self, root: Optional[str] = None):
        self.root = Path(root) if root else Path.cwd()
        self.excluded_patterns = [
            '__pycache__', '.git', '.svn', '.hg',
            'node_modules', 'venv', '.venv',
            '.DS_Store', 'Thumbs.db',
        ]
    
    def list_directory(self, path: str = ".") -> List[FileInfo]:
        """List directory contents."""
        dir_path = self.root / path if path != "." else self.root
        
        if not dir_path.exists():
            raise ValueError(f"Directory does not exist: {dir_path}")
        
        files = []
        for item in dir_path.iterdir():
            if self._should_exclude(item.name):
                continue
            
            stat = item.stat()
            files.append(FileInfo(
                path=str(item.relative_to(self.root)),
                name=item.name,
                size=stat.st_size if item.is_file() else 0,
                is_dir=item.is_dir(),
                is_file=item.is_file(),
                modified=stat.st_mtime,
                created=stat.st_ctime,
            ))
        
        return sorted(files, key=lambda x: (not x.is_dir, x.name))
    
    def read_file(self, path: str) -> str:
        """Read file contents."""
        file_path = self.root / path
        
        if not file_path.exists():
            raise ValueError(f"File does not exist: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def read_file_bytes(self, path: str) -> bytes:
        """Read file as bytes."""
        file_path = self.root / path
        
        if not file_path.exists():
            raise ValueError(f"File does not exist: {file_path}")
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    def write_file(self, path: str, content: str) -> bool:
        """Write content to file."""
        file_path = self.root / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    def copy_file(self, src: str, dst: str) -> bool:
        """Copy file."""
        src_path = self.root / src
        dst_path = self.root / dst
        
        if not src_path.exists():
            raise ValueError(f"Source does not exist: {src_path}")
        
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        
        return True
    
    def delete_file(self, path: str) -> bool:
        """Delete file."""
        file_path = self.root / path
        
        if not file_path.exists():
            return False
        
        if file_path.is_dir():
            shutil.rmtree(file_path)
        else:
            file_path.unlink()
        
        return True
    
    def exists(self, path: str) -> bool:
        """Check if path exists."""
        return (self.root / path).exists()
    
    def is_file(self, path: str) -> bool:
        """Check if path is a file."""
        return (self.root / path).is_file()
    
    def is_dir(self, path: str) -> bool:
        """Check if path is a directory."""
        return (self.root / path).is_dir()
    
    def get_stats(self, path: str) -> Dict[str, Any]:
        """Get file/directory statistics."""
        file_path = self.root / path
        
        if not file_path.exists():
            raise ValueError(f"Path does not exist: {file_path}")
        
        stat = file_path.stat()
        
        return {
            'path': str(file_path.relative_to(self.root)),
            'size': stat.st_size,
            'is_file': file_path.is_file(),
            'is_dir': file_path.is_dir(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'permissions': oct(stat.st_mode)[-3:],
        }
    
    def find_files(self, pattern: str, path: str = ".") -> List[str]:
        """Find files matching pattern."""
        dir_path = self.root / path
        
        matches = []
        for item in dir_path.rglob(pattern):
            if self._should_exclude(item.name):
                continue
            matches.append(str(item.relative_to(self.root)))
        
        return matches
    
    def _should_exclude(self, name: str) -> bool:
        """Check if name should be excluded."""
        return name in self.excluded_patterns or name.startswith('.')
