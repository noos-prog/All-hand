"""CAPABILITY-000015: License Analysis - VERSION 1.0.0"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class LicenseInfo:
    name: str
    spdx_id: str
    permissions: List[str] = field(default_factory=list)

@dataclass
class LicenseAnalysisResult:
    licenses: List[LicenseInfo] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    def to_dict(self) -> Dict[str, Any]:
        return {"licenses": [{"name": l.name, "spdx_id": l.spdx_id} for l in self.licenses], "analyzed_at": self.analyzed_at.isoformat()}

class LicenseAnalysisCapability:
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000015"
    @property
    def name(self) -> str: return "LicenseAnalysis"
    @property
    def description(self) -> str: return "Analyzes repository licenses"
    @property
    def version(self) -> str: return self.VERSION
    def execute(self, input_data: Dict[str, Any]) -> LicenseAnalysisResult:
        return LicenseAnalysisResult(licenses=[])
