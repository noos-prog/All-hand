#!/usr/bin/env python3
"""
ARI - Reports
=============

Report generation and publishing.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import json


class ReportType(Enum):
    """Types of reports."""
    PROVIDER_REPORT = "provider_report"
    MODEL_REPORT = "model_report"
    CAPABILITY_REPORT = "capability_report"
    BENCHMARK_REPORT = "benchmark_report"
    COMPARISON_REPORT = "comparison_report"
    TREND_REPORT = "trend_report"
    SUMMARY_REPORT = "summary_report"


class ReportFormat(Enum):
    """Report formats."""
    JSON = "json"
    HTML = "html"
    MARKDOWN = "markdown"
    PDF = "pdf"


@dataclass
class ReportSection:
    """A section in a report."""
    section_id: str
    title: str
    content: str
    
    # Data
    data: Dict[str, Any] = field(default_factory=dict)
    
    # Visualization
    chart_type: Optional[str] = None
    
    # Metadata
    order: int = 0


@dataclass
class Report:
    """An ARI report."""
    report_id: str
    report_type: ReportType
    title: str
    
    # Sections
    sections: Tuple[ReportSection, ...] = ()
    
    # Summary
    summary: str = ""
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    generated_by: str = "ari"
    
    # Filters
    filters: Dict[str, Any] = field(default_factory=dict)
    
    # Statistics
    total_entities: int = 0
    total_benchmarks: int = 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get report summary."""
        return {
            "report_id": self.report_id,
            "title": self.title,
            "type": self.report_type.value,
            "sections": len(self.sections),
            "created_at": self.created_at,
        }


@dataclass
class ReportTemplate:
    """A report template."""
    template_id: str
    name: str
    report_type: ReportType
    
    # Sections to include
    sections: Tuple[str, ...] = ()  # Section IDs
    
    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class ReportGenerator:
    """
    Generates ARI reports.
    """
    
    def __init__(self):
        self._templates: Dict[str, ReportTemplate] = {}
        self._reports: Dict[str, Report] = {}
        self._formatters: Dict[ReportFormat, Callable] = {}
        
        # Register default formatters
        self._register_default_formatters()
        self._register_default_templates()
    
    def _register_default_formatters(self) -> None:
        """Register default formatters."""
        def format_json(report: Report) -> str:
            return json.dumps(report.__dict__, indent=2, default=str)
        
        def format_markdown(report: Report) -> str:
            lines = [f"# {report.title}\n"]
            lines.append(f"**Generated:** {report.created_at}\n")
            lines.append(f"**Type:** {report.report_type.value}\n\n")
            
            if report.summary:
                lines.append(f"## Summary\n{report.summary}\n\n")
            
            for section in report.sections:
                lines.append(f"## {section.title}\n")
                lines.append(f"{section.content}\n\n")
            
            return "\n".join(lines)
        
        self._formatters[ReportFormat.JSON] = format_json
        self._formatters[ReportFormat.MARKDOWN] = format_markdown
    
    def _register_default_templates(self) -> None:
        """Register default report templates."""
        self.register_template(ReportTemplate(
            template_id="provider_summary",
            name="Provider Summary Report",
            report_type=ReportType.PROVIDER_REPORT,
            sections=("overview", "metrics", "benchmarks", "recommendations"),
        ))
    
    def register_template(self, template: ReportTemplate) -> None:
        """Register a report template."""
        self._templates[template.template_id] = template
    
    def generate_report(
        self,
        report_type: ReportType,
        title: str,
        sections: List[Dict[str, Any]],
        summary: str = "",
        filters: Dict[str, Any] = None
    ) -> Report:
        """Generate a report."""
        report_id = f"report_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        report_sections = [
            ReportSection(
                section_id=s.get("section_id", f"section_{i}"),
                title=s.get("title", f"Section {i}"),
                content=s.get("content", ""),
                data=s.get("data", {}),
                chart_type=s.get("chart_type"),
                order=s.get("order", i),
            )
            for i, s in enumerate(sections)
        ]
        
        report = Report(
            report_id=report_id,
            report_type=report_type,
            title=title,
            sections=tuple(report_sections),
            summary=summary,
            filters=filters or {},
            total_entities=len(sections),
        )
        
        self._reports[report_id] = report
        return report
    
    def generate_provider_report(
        self,
        provider_id: str,
        provider_data: Dict[str, Any],
        benchmark_results: List[Dict[str, Any]]
    ) -> Report:
        """Generate a provider report."""
        sections = [
            {
                "section_id": "overview",
                "title": "Provider Overview",
                "content": f"**Name:** {provider_data.get('name', 'Unknown')}\n"
                           f"**Type:** {provider_data.get('type', 'Unknown')}\n"
                           f"**Status:** {provider_data.get('status', 'Unknown')}",
            },
            {
                "section_id": "metrics",
                "title": "Performance Metrics",
                "content": self._format_metrics(provider_data),
                "data": provider_data,
            },
            {
                "section_id": "benchmarks",
                "title": "Benchmark Results",
                "content": self._format_benchmarks(benchmark_results),
                "data": {"results": benchmark_results},
            },
            {
                "section_id": "recommendations",
                "title": "Recommendations",
                "content": self._generate_recommendations(provider_data, benchmark_results),
            },
        ]
        
        return self.generate_report(
            report_type=ReportType.PROVIDER_REPORT,
            title=f"Provider Report: {provider_data.get('name', provider_id)}",
            sections=sections,
            summary=f"This report covers the performance of {provider_data.get('name', provider_id)} "
                   f"across {len(benchmark_results)} benchmarks.",
            filters={"provider_id": provider_id},
        )
    
    def generate_summary_report(
        self,
        providers: List[Dict[str, Any]],
        models: List[Dict[str, Any]],
        benchmarks: List[Dict[str, Any]]
    ) -> Report:
        """Generate a summary report."""
        sections = [
            {
                "section_id": "executive",
                "title": "Executive Summary",
                "content": f"ARI Research Infrastructure Report\n\n"
                           f"**Providers Analyzed:** {len(providers)}\n"
                           f"**Models Evaluated:** {len(models)}\n"
                           f"**Benchmarks Run:** {len(benchmarks)}",
            },
            {
                "section_id": "top_performers",
                "title": "Top Performers",
                "content": self._format_top_performers(providers, models),
                "data": {"providers": providers, "models": models},
            },
            {
                "section_id": "trends",
                "title": "Trends",
                "content": "Analysis of trends over the reporting period.",
            },
        ]
        
        return self.generate_report(
            report_type=ReportType.SUMMARY_REPORT,
            title="ARI Summary Report",
            sections=sections,
            summary=f"Summary of {len(providers)} providers and {len(models)} models.",
        )
    
    def _format_metrics(self, data: Dict[str, Any]) -> str:
        """Format metrics as text."""
        lines = []
        
        if "success_rate" in data:
            lines.append(f"- **Success Rate:** {data['success_rate']:.1%}")
        if "avg_latency_ms" in data:
            lines.append(f"- **Avg Latency:** {data['avg_latency_ms']:.0f}ms")
        if "cost" in data:
            lines.append(f"- **Cost:** ${data['cost']:.4f}")
        
        return "\n".join(lines) if lines else "No metrics available."
    
    def _format_benchmarks(self, results: List[Dict[str, Any]]) -> str:
        """Format benchmark results."""
        if not results:
            return "No benchmark results available."
        
        lines = []
        for result in results[:10]:
            lines.append(f"- **{result.get('name', 'Unknown')}:** "
                        f"{result.get('score', 0):.1%}")
        
        return "\n".join(lines)
    
    def _generate_recommendations(
        self,
        provider: Dict[str, Any],
        results: List[Dict[str, Any]]
    ) -> str:
        """Generate recommendations."""
        recommendations = []
        
        # Check success rate
        success_rate = provider.get("success_rate", 0)
        if success_rate < 0.8:
            recommendations.append("- Consider improving test coverage to increase success rate")
        
        # Check latency
        latency = provider.get("avg_latency_ms", 0)
        if latency > 5000:
            recommendations.append("- Optimize for faster response times")
        
        # Check cost
        cost = provider.get("cost", 0)
        if cost > 1.0:
            recommendations.append("- Consider cost optimization strategies")
        
        return "\n".join(recommendations) if recommendations else "No specific recommendations."
    
    def _format_top_performers(
        self,
        providers: List[Dict[str, Any]],
        models: List[Dict[str, Any]]
    ) -> str:
        """Format top performers."""
        lines = ["## Top Providers\n"]
        
        sorted_providers = sorted(
            providers,
            key=lambda p: p.get("score", 0),
            reverse=True
        )[:5]
        
        for i, p in enumerate(sorted_providers):
            lines.append(f"{i+1}. **{p.get('name', 'Unknown')}** - {p.get('score', 0):.1%}")
        
        lines.append("\n## Top Models\n")
        
        sorted_models = sorted(
            models,
            key=lambda m: m.get("score", 0),
            reverse=True
        )[:5]
        
        for i, m in enumerate(sorted_models):
            lines.append(f"{i+1}. **{m.get('name', 'Unknown')}** - {m.get('score', 0):.1%}")
        
        return "\n".join(lines)
    
    def format_report(
        self,
        report: Report,
        format: ReportFormat = ReportFormat.JSON
    ) -> str:
        """Format a report."""
        if format not in self._formatters:
            raise ValueError(f"Unknown format: {format}")
        
        return self._formatters[format](report)
    
    def get_report(self, report_id: str) -> Optional[Report]:
        """Get a report by ID."""
        return self._reports.get(report_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get generator statistics."""
        by_type = {}
        for report in self._reports.values():
            rtype = report.report_type.value
            by_type[rtype] = by_type.get(rtype, 0) + 1
        
        return {
            "total_reports": len(self._reports),
            "by_type": by_type,
            "templates": len(self._templates),
        }


class ReportPublisher:
    """
    Publishes reports to various destinations.
    """
    
    def __init__(self):
        self._publishers: Dict[str, Callable] = {}
    
    def register_publisher(
        self,
        name: str,
        publisher: Callable[[Report], bool]
    ) -> None:
        """Register a publisher."""
        self._publishers[name] = publisher
    
    def publish(
        self,
        report: Report,
        destinations: List[str]
    ) -> Dict[str, bool]:
        """Publish a report to destinations."""
        results = {}
        
        for dest in destinations:
            if dest not in self._publishers:
                results[dest] = False
                continue
            
            try:
                results[dest] = self._publishers[dest](report)
            except Exception as e:
                results[dest] = False
        
        return results
