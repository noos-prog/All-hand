"""AGOS Reports."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ReportFormat(Enum):
    """Report format."""
    JSON = "json"
    HTML = "html"
    PDF = "pdf"
    MARKDOWN = "markdown"


class ReportType(Enum):
    """Report type."""
    SUMMARY = "summary"
    DETAILED = "detailed"
    METRICS = "metrics"
    AUDIT = "audit"


@dataclass
class ReportSection:
    """A report section."""
    title: str
    content: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Report:
    """A report."""
    id: str
    title: str
    report_type: ReportType
    sections: List[ReportSection] = field(default_factory=list)
    format: ReportFormat = ReportFormat.JSON
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "type": self.report_type.value,
            "format": self.format.value,
            "sections": [{"title": s.title, "content": s.content} for s in self.sections],
            "created_at": self.created_at.isoformat(),
        }


class ReportGenerator:
    """
    Report Generator.
    
    Generates reports in various formats.
    
    Usage:
        generator = ReportGenerator()
        report = generator.generate(
            title="Mission Report",
            report_type=ReportType.SUMMARY,
            sections=[ReportSection("Overview", "Mission completed")],
        )
    """
    
    def __init__(self):
        """Initialize report generator."""
        self._templates: Dict[str, Report] = {}
    
    def generate(
        self,
        title: str,
        report_type: ReportType,
        sections: Optional[List[ReportSection]] = None,
        format: ReportFormat = ReportFormat.JSON,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Report:
        """Generate a report."""
        report = Report(
            id=f"report-{uuid.uuid4().hex[:8]}",
            title=title,
            report_type=report_type,
            sections=sections or [],
            format=format,
            metadata=metadata or {},
        )
        return report
    
    def add_section(
        self,
        report: Report,
        title: str,
        content: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a section to a report."""
        report.sections.append(
            ReportSection(title=title, content=content, data=data or {})
        )
    
    def render(self, report: Report) -> str:
        """Render a report in its format."""
        if report.format == ReportFormat.JSON:
            import json
            return json.dumps(report.to_dict(), indent=2)
        elif report.format == ReportFormat.MARKDOWN:
            return self._render_markdown(report)
        elif report.format == ReportFormat.HTML:
            return self._render_html(report)
        return str(report.to_dict())
    
    def _render_markdown(self, report: Report) -> str:
        """Render as Markdown."""
        md = f"# {report.title}\n\n"
        md += f"*Generated: {report.created_at.isoformat()}*\n\n"
        for section in report.sections:
            md += f"## {section.title}\n\n{section.content}\n\n"
        return md
    
    def _render_html(self, report: Report) -> str:
        """Render as HTML."""
        html = f"<html><head><title>{report.title}</title></head><body>"
        html += f"<h1>{report.title}</h1>"
        html += f"<p><em>Generated: {report.created_at.isoformat()}</em></p>"
        for section in report.sections:
            html += f"<h2>{section.title}</h2><p>{section.content}</p>"
        html += "</body></html>"
        return html


_report_generator: Optional[ReportGenerator] = None


def get_report_generator() -> ReportGenerator:
    """Get the global report generator."""
    global _report_generator
    if _report_generator is None:
        _report_generator = ReportGenerator()
    return _report_generator
