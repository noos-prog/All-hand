"""ConstitutionValidator: mechanical enforcement of the constitution.

Scans a project tree and reports violations that CI can gate on.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

from .articles import ARTICLES, Article, KERNEL_BLACKLIST, ViolationSeverity


@dataclass(frozen=True)
class Violation:
    article: Article
    path: Path
    line: int
    message: str

    @property
    def severity(self) -> ViolationSeverity:
        return self.article.severity


_BLACKLIST_TOKEN_PATTERNS = {
    token: re.compile(rf"\b{re.escape(token.replace('-', '_'))}\b", re.IGNORECASE)
    for token in KERNEL_BLACKLIST
}


class ConstitutionValidator:
    """Scan Python sources for constitutional violations.

    The current rules:
      - Article 3 (Kernel Blacklist): files under ``kernel_roots`` may not
        import or reference blacklist tokens as top-level identifiers.
      - Article 6 (Observability): files under ``kernel_roots`` should not
        use bare ``print`` statements; use structured logging instead.
    """

    def __init__(
        self,
        kernel_roots: Sequence[str] = ("agos-kernel", "kernel"),
        excluded_dirs: Sequence[str] = ("tests", "__pycache__", ".git", "node_modules"),
    ) -> None:
        self.kernel_roots = tuple(kernel_roots)
        self.excluded_dirs = set(excluded_dirs)

    # ------------------------------------------------------------------ scan
    def scan(self, project_root: str | Path) -> List[Violation]:
        root = Path(project_root).resolve()
        violations: List[Violation] = []
        for path in self._iter_python(root):
            rel = path.relative_to(root)
            if self._is_kernel(rel):
                violations.extend(self._scan_kernel_file(path))
        return violations

    # ---------------------------------------------------------------- helpers
    def _iter_python(self, root: Path) -> Iterable[Path]:
        for p in root.rglob("*.py"):
            if any(part in self.excluded_dirs for part in p.parts):
                continue
            yield p

    def _is_kernel(self, rel: Path) -> bool:
        parts = rel.parts
        return bool(parts) and parts[0] in self.kernel_roots

    def _scan_kernel_file(self, path: Path) -> List[Violation]:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []
        out: List[Violation] = []
        art3 = next(a for a in ARTICLES if a.number == 3)
        art6 = next(a for a in ARTICLES if a.number == 6)
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            for token, pattern in _BLACKLIST_TOKEN_PATTERNS.items():
                if pattern.search(line):
                    out.append(
                        Violation(
                            article=art3,
                            path=path,
                            line=lineno,
                            message=f"kernel references blacklisted token {token!r}",
                        )
                    )

            if stripped.startswith("print(") or " print(" in stripped:
                out.append(
                    Violation(
                        article=art6,
                        path=path,
                        line=lineno,
                        message="kernel uses print(); use structured logging",
                    )
                )
        return out

    # -------------------------------------------------------------- reporting
    @staticmethod
    def format_report(violations: Sequence[Violation]) -> str:
        if not violations:
            return "Constitution: 0 violations"
        lines = [f"Constitution: {len(violations)} violation(s)"]
        for v in violations:
            lines.append(
                f"  [{v.severity.value.upper()}] Article {v.article.number} "
                f"({v.article.title}): {v.path}:{v.line} — {v.message}"
            )
        return "\n".join(lines)
