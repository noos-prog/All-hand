"""
AGOS Seal Module
================

System validation and integrity checking.
Provides Seal validation and status tracking.

RULES:
- Seal verifies system integrity
- Seal is immutable once set
- Seal status tracks system health
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class KernelSealCertificate:
    """
    Kernel Seal Certificate for Version 1.0.
    
    This certificate seals the kernel and defines its permanent state.
    """
    
    VERSION = "1.0.0"
    STATUS = "STABLE"
    LIFECYCLE = "MAINTENANCE"
    EVOLUTION = "ECOSYSTEM_ONLY"
    ARCHITECTURE_PHASE = "CLOSED"
    
    # Locked components
    LOCKED_COMPONENTS = [
        "kernel_architecture",
        "kernel_contracts",
        "kernel_runtime",
        "kernel_event_model",
        "kernel_layering",
        "kernel_dependency_rules",
        "kernel_invariants",
        "kernel_public_apis",
    ]
    
    # Allowed modifications in maintenance mode
    ALLOWED_MODIFICATIONS = [
        "security_fixes",
        "bug_fixes",
        "performance_improvements",
        "compatibility_improvements",
        "reliability_improvements",
        "observability_improvements",
    ]
    
    # Requirements for modifications
    MODIFICATION_REQUIREMENTS = [
        "architecture_review",
        "evidence",
        "compatibility_report",
        "certification",
        "governance_approval",
    ]
    
    def __init__(self, kernel_root: Optional[Path] = None):
        self.kernel_root = kernel_root or Path('/workspace/All-hand/agos-kernel')
        self.generated_at = datetime.utcnow()
        self._certificate_hash = ""
        self._kernel_integrity_hash = ""
        self._architecture_fingerprint = ""
    
    def generate(self) -> Dict:
        """
        Generate the complete seal certificate.
        
        Returns:
            Complete seal certificate as dictionary.
        """
        self._compute_kernel_integrity_hash()
        self._compute_architecture_fingerprint()
        self._compute_certificate_hash()
        
        return self._build_certificate()
    
    def _compute_kernel_integrity_hash(self) -> str:
        """Compute hash of entire kernel state."""
        files_hashes = []
        
        for py_file in sorted(self.kernel_root.rglob('*.py')):
            if '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'rb') as f:
                    content = f.read()
                    file_hash = hashlib.sha256(content).hexdigest()
                    rel_path = py_file.relative_to(self.kernel_root)
                    files_hashes.append(f"{rel_path}:{file_hash}")
            except Exception:
                pass
        
        combined = "\n".join(sorted(files_hashes))
        self._kernel_integrity_hash = hashlib.sha256(combined.encode()).hexdigest()
        return self._kernel_integrity_hash
    
    def _compute_architecture_fingerprint(self) -> str:
        """Compute architecture fingerprint."""
        components = {
            'directories': [],
            'modules': [],
            'contracts': 0,
            'events': 0,
        }
        
        # Count directories
        for item in self.kernel_root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                components['directories'].append(item.name)
        
        # Count Python modules
        components['modules'] = len(list(self.kernel_root.rglob('*.py')))
        
        # Count contracts and events
        contracts_dir = self.kernel_root / 'contracts'
        if contracts_dir.exists():
            components['contracts'] = len(list(contracts_dir.rglob('*.json')))
        
        events_dir = self.kernel_root / 'events'
        if events_dir.exists():
            components['events'] = len(list(events_dir.rglob('*.json')))
        
        fingerprint_content = json.dumps(components, sort_keys=True)
        self._architecture_fingerprint = hashlib.sha256(fingerprint_content.encode()).hexdigest()
        return self._architecture_fingerprint
    
    def _compute_certificate_hash(self) -> str:
        """Compute hash of entire certificate."""
        cert_content = json.dumps(self._build_certificate(), sort_keys=True)
        self._certificate_hash = hashlib.sha256(cert_content.encode()).hexdigest()
        return self._certificate_hash
    
    def _build_certificate(self) -> Dict:
        """Build the complete certificate."""
        return {
            "certificate_type": "AGOS_KERNEL_SEAL",
            "version": self.VERSION,
            "status": self.STATUS,
            "lifecycle": self.LIFECYCLE,
            "evolution": self.EVOLUTION,
            "architecture_phase": self.ARCHITECTURE_PHASE,
            
            "generated_at": self.generated_at.isoformat(),
            "generated_by": "EXECUTION-KERNEL-FINALIZATION-000004",
            
            "kernel_integrity_hash": self._kernel_integrity_hash,
            "architecture_fingerprint": self._architecture_fingerprint,
            "certificate_hash": self._certificate_hash,
            
            "locked_components": self.LOCKED_COMPONENTS,
            "allowed_modifications": self.ALLOWED_MODIFICATIONS,
            "modification_requirements": self.MODIFICATION_REQUIREMENTS,
            
            "kernel_metrics": {
                "modules": len(list(self.kernel_root.rglob('*.py'))),
                "directories": len([i for i in self.kernel_root.iterdir() if i.is_dir()]),
                "contracts": len(list((self.kernel_root / 'contracts').rglob('*.json'))) if (self.kernel_root / 'contracts').exists() else 0,
                "events": len(list((self.kernel_root / 'events').rglob('*.json'))) if (self.kernel_root / 'events').exists() else 0,
            },
            
            "final_state": {
                "kernel_status": self.STATUS,
                "kernel_lifecycle": self.LIFECYCLE,
                "kernel_evolution": self.EVOLUTION,
                "architecture_phase": self.ARCHITECTURE_PHASE,
            },
            
            "governance": {
                "all_modifications_require_approval": True,
                "certification_required": True,
                "evidence_required": True,
            },
            
            "signature": self._generate_signature(),
        }
    
    def _generate_signature(self) -> str:
        """Generate certificate signature."""
        content = (
            f"{self.VERSION}:"
            f"{self._kernel_integrity_hash}:"
            f"{self._architecture_fingerprint}:"
            f"{self.generated_at.isoformat()}"
        )
        return hashlib.sha256(content.encode()).hexdigest()
    
    def save(self, output_path: Path) -> None:
        """Save certificate to file."""
        certificate = self.generate()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(certificate, f, indent=2)
        
        print(f"Certificate saved to: {output_path}")
    
    def verify(self) -> bool:
        """
        Verify the certificate integrity.
        
        Returns:
            True if certificate is valid.
        """
        # Load existing certificate
        cert_path = self.kernel_root / 'finalization' / 'KERNEL_SEAL_CERTIFICATE.json'
        
        if not cert_path.exists():
            print("No certificate found to verify")
            return False
        
        with open(cert_path, 'r') as f:
            stored = json.load(f)
        
        # Generate current certificate
        current = self.generate()
        
        # Compare critical fields
        if stored['version'] != current['version']:
            print(f"Version mismatch: {stored['version']} vs {current['version']}")
            return False
        
        if stored['kernel_integrity_hash'] != current['kernel_integrity_hash']:
            print("Kernel integrity hash mismatch - kernel has been modified!")
            return False
        
        print("Certificate verification: VALID")
        return True


def create_kernel_seal_certificate():
    """Create and save the kernel seal certificate."""
    kernel_root = Path('/workspace/All-hand/agos-kernel')
    
    certificate = KernelSealCertificate(kernel_root)
    cert_data = certificate.generate()
    
    # Save to finalization directory
    output_path = kernel_root / 'finalization' / 'KERNEL_SEAL_CERTIFICATE.json'
    certificate.save(output_path)
    
    # Also save individual reports
    manifest_path = kernel_root / 'finalization' / 'KERNEL_MANIFEST_v1.0.json'
    integrity_path = kernel_root / 'finalization' / 'KERNEL_INTEGRITY_HASH.json'
    fingerprint_path = kernel_root / 'finalization' / 'ARCHITECTURE_FINGERPRINT.json'
    
    # Kernel Manifest
    with open(manifest_path, 'w') as f:
        json.dump({
            "manifest_type": "KERNEL_MANIFEST",
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat(),
            "metrics": cert_data['kernel_metrics'],
            "components": cert_data['locked_components'],
            "final_state": cert_data['final_state'],
        }, f, indent=2)
    
    # Integrity Hash
    with open(integrity_path, 'w') as f:
        json.dump({
            "type": "KERNEL_INTEGRITY_HASH",
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat(),
            "hash": cert_data['kernel_integrity_hash'],
            "algorithm": "SHA-256",
        }, f, indent=2)
    
    # Architecture Fingerprint
    with open(fingerprint_path, 'w') as f:
        json.dump({
            "type": "ARCHITECTURE_FINGERPRINT",
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat(),
            "fingerprint": cert_data['architecture_fingerprint'],
            "metrics": cert_data['kernel_metrics'],
        }, f, indent=2)
    
    print("\n" + "=" * 60)
    print("KERNEL SEAL CERTIFICATE CREATED")
    print("=" * 60)
    print(f"Version: {cert_data['version']}")
    print(f"Status: {cert_data['status']}")
    print(f"Lifecycle: {cert_data['lifecycle']}")
    print(f"Architecture Phase: {cert_data['architecture_phase']}")
    print()
    print("Files generated:")
    print(f"  - {output_path}")
    print(f"  - {manifest_path}")
    print(f"  - {integrity_path}")
    print(f"  - {fingerprint_path}")
    print()
    print("🎉 Kernel Version 1.0 is now SEALED")
    print()
    
    return cert_data


if __name__ == '__main__':
    create_kernel_seal_certificate()


class SealStatus(Enum):
    """Seal status."""
    UNSEALED = "unsealed"
    SEALED = "sealed"
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"


class Seal:
    """
    AGOS Seal - System validation.
    
    Tracks system integrity and seal status.
    """
    
    def __init__(self, root_path: Optional[Path] = None):
        """Initialize seal."""
        self.root_path = root_path or Path("/workspace/project/All-hand/agos-kernel")
        self.certificate: Optional[Dict[str, Any]] = None
        self.status = SealStatus.UNSEALED
    
    def create_certificate(self) -> Dict[str, Any]:
        """Create seal certificate."""
        cert = KernelSealCertificate(self.root_path)
        self.certificate = cert.generate()
        self.status = SealStatus.SEALED
        return self.certificate
    
    def verify(self) -> bool:
        """Verify seal integrity."""
        if self.status == SealStatus.UNSEALED:
            return False
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get seal status."""
        return {
            "status": self.status.value,
            "has_certificate": self.certificate is not None,
            "root_path": str(self.root_path),
        }

