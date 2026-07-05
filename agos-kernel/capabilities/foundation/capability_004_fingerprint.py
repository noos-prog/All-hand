"""
CAPABILITY-000004: Repository Fingerprinting

PURPOSE: Generate immutable repository identity.

OUTPUT:
- Repository Fingerprint
- Repository Signature
- Repository Hash Profile

VERSION: 1.0.0
"""
import hashlib
import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class RepositoryFingerprint:
    """Immutable repository identity."""
    fingerprint: str
    signature: str
    hash_profile: Dict[str, str]
    computed_at: datetime = field(default_factory=datetime.utcnow)
    commit_hash: str = ""
    branch: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fingerprint": self.fingerprint,
            "signature": self.signature,
            "hash_profile": self.hash_profile,
            "computed_at": self.computed_at.isoformat(),
            "commit_hash": self.commit_hash,
            "branch": self.branch,
        }


class RepositoryFingerprintCapability:
    """
    CAPABILITY-000004: Repository Fingerprinting
    
    Generates immutable repository identity using multiple hash algorithms.
    
    VERSION: 1.0.0
    """
    
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000004"
    
    def __init__(self):
        self.hash_algorithms = ["sha256", "sha1", "md5", "blake2b"]
    
    @property
    def name(self) -> str:
        return "RepositoryFingerprint"
    
    @property
    def description(self) -> str:
        return "Generates immutable repository identity"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> RepositoryFingerprint:
        """
        Execute fingerprinting.
        
        Args:
            input_data: Dict with 'path' key containing repository path
            
        Returns:
            RepositoryFingerprint with identity data
        """
        path = input_data.get("path", "")
        if not path:
            raise ValueError("Path is required")
        
        if not os.path.isdir(path):
            raise ValueError(f"Not a directory: {path}")
        
        # Get git info
        commit_hash = self._get_commit_hash(path)
        branch = self._get_branch(path)
        
        # Compute hashes
        hash_profile = self._compute_hashes(path)
        
        # Generate fingerprint (combined hash of all files)
        fingerprint = self._generate_fingerprint(hash_profile)
        
        # Generate signature
        signature = self._generate_signature(fingerprint, commit_hash)
        
        return RepositoryFingerprint(
            fingerprint=fingerprint,
            signature=signature,
            hash_profile=hash_profile,
            commit_hash=commit_hash,
            branch=branch,
        )
    
    def _get_commit_hash(self, path: str) -> str:
        """Get current commit hash."""
        try:
            result = subprocess.run(
                ["git", "-C", path, "rev-parse", "HEAD"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except:
            return ""
    
    def _get_branch(self, path: str) -> str:
        """Get current branch."""
        try:
            result = subprocess.run(
                ["git", "-C", path, "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except:
            return ""
    
    def _compute_hashes(self, path: str) -> Dict[str, str]:
        """Compute multiple hash algorithms."""
        hashes = {alg: hashlib.new(alg) for alg in self.hash_algorithms}
        file_hashes = []
        
        for root, dirs, files in os.walk(path):
            # Skip .git
            if ".git" in root:
                continue
            
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            
            for filename in sorted(files):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, path)
                
                try:
                    with open(filepath, "rb") as f:
                        content = f.read()
                        
                    # Update all hashes with content
                    for h in hashes.values():
                        h.update(content)
                    
                    # Also hash the relative path
                    h_path = hashlib.sha256()
                    h_path.update(rel_path.encode())
                    h_path.update(content)
                    file_hashes.append(h_path.hexdigest())
                    
                except Exception:
                    pass
        
        # Add file list hash
        file_list_hash = hashlib.sha256()
        for fh in sorted(file_hashes):
            file_list_hash.update(fh.encode())
        
        result = {alg: h.hexdigest() for alg, h in hashes.items()}
        result["file_tree"] = file_list_hash.hexdigest()
        
        return result
    
    def _generate_fingerprint(self, hash_profile: Dict[str, str]) -> str:
        """Generate combined fingerprint."""
        # Combine all hashes
        combined = ""
        for alg in sorted(hash_profile.keys()):
            combined += hash_profile[alg]
        
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _generate_signature(self, fingerprint: str, commit_hash: str) -> str:
        """Generate repository signature."""
        data = f"{fingerprint}:{commit_hash}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def verify(self, path: str, fingerprint: RepositoryFingerprint) -> bool:
        """Verify if repository matches fingerprint."""
        current = self.execute({"path": path})
        return current.fingerprint == fingerprint.fingerprint
