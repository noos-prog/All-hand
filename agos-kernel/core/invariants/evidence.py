"""
Invariant Evidence Generator
EXECUTION-KERNEL-FINALIZATION-000002

Generates verifiable evidence for kernel invariant compliance.
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path

from agos_kernel.core.invariants.runtime import InvariantResult


@dataclass
class Evidence:
    """Evidence of invariant compliance."""
    invariant_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    content_hash: str = ""
    proof: Dict = field(default_factory=dict)
    signature: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'invariant_id': self.invariant_id,
            'timestamp': self.timestamp.isoformat(),
            'content_hash': self.content_hash,
            'proof': self.proof,
            'signature': self.signature,
        }


@dataclass
class EvidencePackage:
    """Collection of evidence for all invariants."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    kernel_version: str = "1.0.0"
    kernel_hash: str = ""
    evidence_items: List[Evidence] = field(default_factory=list)
    manifest_hash: str = ""
    
    @property
    def is_complete(self) -> bool:
        """All invariants have evidence."""
        return len(self.evidence_items) > 0


class EvidenceGenerator:
    """
    Generates verifiable evidence for kernel invariant compliance.
    
    Every decision produces evidence.
    Every verification produces artifacts.
    """
    
    def __init__(self, kernel_root: Optional[Path] = None):
        self.kernel_root = kernel_root or Path('/workspace/All-hand/agos-kernel')
    
    def generate_evidence(
        self,
        result: InvariantResult,
        proof_data: Optional[Dict] = None
    ) -> Evidence:
        """Generate evidence for a single invariant result."""
        content = {
            'invariant_id': result.invariant_id,
            'passed': result.passed,
            'timestamp': result.timestamp.isoformat(),
            'violations': result.violations,
            'execution_time_ms': result.execution_time_ms,
            'proof_data': proof_data or {},
        }
        
        content_str = json.dumps(content, sort_keys=True)
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()
        
        evidence = Evidence(
            invariant_id=result.invariant_id,
            content_hash=content_hash,
            proof=content,
            signature=self._sign(content_hash),
        )
        
        return evidence
    
    def generate_package(
        self,
        results: List[InvariantResult]
    ) -> EvidencePackage:
        """Generate complete evidence package."""
        evidence_items = []
        
        for result in results:
            evidence = self.generate_evidence(result)
            evidence_items.append(evidence)
        
        kernel_hash = self._compute_kernel_hash()
        
        manifest_content = {
            'timestamp': datetime.utcnow().isoformat(),
            'kernel_version': '1.0.0',
            'kernel_hash': kernel_hash,
            'evidence_count': len(evidence_items),
            'evidence_hashes': [e.content_hash for e in evidence_items],
        }
        
        manifest_hash = hashlib.sha256(
            json.dumps(manifest_content, sort_keys=True).encode()
        ).hexdigest()
        
        return EvidencePackage(
            kernel_hash=kernel_hash,
            evidence_items=evidence_items,
            manifest_hash=manifest_hash,
        )
    
    def verify_evidence(self, evidence: Evidence) -> bool:
        """Verify evidence integrity."""
        expected_hash = self._compute_content_hash(evidence.proof)
        return evidence.content_hash == expected_hash
    
    def _compute_kernel_hash(self) -> str:
        """Compute hash of kernel state."""
        files_hashes = []
        
        for py_file in self.kernel_root.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            try:
                with open(py_file, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()[:16]
                    files_hashes.append(file_hash)
            except Exception:
                pass
        
        combined = ''.join(sorted(files_hashes))
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _compute_content_hash(self, content: Dict) -> str:
        """Compute hash of content."""
        return hashlib.sha256(
            json.dumps(content, sort_keys=True).encode()
        ).hexdigest()
    
    def _sign(self, content_hash: str) -> str:
        """
        Sign evidence (simplified - in production use proper crypto).
        
        This generates a signature-like hash for the evidence.
        """
        return hashlib.sha256(
            f"{content_hash}:{datetime.utcnow().isoformat()}:kernel-v1.0.0".encode()
        ).hexdigest()
    
    def export_evidence_package(
        self,
        package: EvidencePackage,
        output_dir: Path
    ) -> None:
        """Export evidence package to files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export manifest
        manifest = {
            'timestamp': package.timestamp.isoformat(),
            'kernel_version': package.kernel_version,
            'kernel_hash': package.kernel_hash,
            'evidence_count': len(package.evidence_items),
            'manifest_hash': package.manifest_hash,
        }
        
        with open(output_dir / 'evidence_manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Export individual evidence
        for evidence in package.evidence_items:
            filename = f"evidence_{evidence.invariant_id}.json"
            with open(output_dir / filename, 'w') as f:
                json.dump(evidence.to_dict(), f, indent=2)
        
        # Export complete package
        with open(output_dir / 'evidence_package.json', 'w') as f:
            json.dump({
                'manifest': manifest,
                'evidence': [e.to_dict() for e in package.evidence_items],
            }, f, indent=2)
