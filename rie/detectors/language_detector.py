"""Language Detector - Detect programming languages."""
from typing import Dict, List

from ..domain.repository import Repository, RepositoryLanguage, FileInfo
from .base_detector import BaseDetector, DetectionResult


LANGUAGE_EXTENSIONS: Dict[str, RepositoryLanguage] = {
    ".py": RepositoryLanguage.PYTHON,
    ".js": RepositoryLanguage.JAVASCRIPT,
    ".ts": RepositoryLanguage.TYPESCRIPT,
    ".jsx": RepositoryLanguage.JAVASCRIPT,
    ".tsx": RepositoryLanguage.TYPESCRIPT,
    ".java": RepositoryLanguage.JAVA,
    ".go": RepositoryLanguage.GO,
    ".rs": RepositoryLanguage.RUST,
    ".cs": RepositoryLanguage.C_SHARP,
    ".cpp": RepositoryLanguage.CPP,
    ".cc": RepositoryLanguage.CPP,
    ".cxx": RepositoryLanguage.CPP,
    ".c": RepositoryLanguage.C,
    ".h": RepositoryLanguage.C,
    ".hpp": RepositoryLanguage.CPP,
    ".rb": RepositoryLanguage.RUBY,
    ".swift": RepositoryLanguage.SWIFT,
    ".kt": RepositoryLanguage.KOTLIN,
    ".scala": RepositoryLanguage.SCALA,
    ".php": RepositoryLanguage.PHP,
}


class LanguageDetector(BaseDetector):
    """Detects programming languages in a repository."""
    
    def detect(self, repo: Repository) -> DetectionResult:
        """Detect languages by file extensions."""
        language_counts: Dict[str, int] = {}
        total_files = 0
        
        for file in repo.files:
            ext = file.extension.lower()
            if ext in LANGUAGE_EXTENSIONS:
                lang = LANGUAGE_EXTENSIONS[ext].value
                language_counts[lang] = language_counts.get(lang, 0) + 1
                total_files += 1
        
        # Calculate percentages
        language_percentages: Dict[str, float] = {}
        if total_files > 0:
            for lang, count in language_counts.items():
                language_percentages[lang] = (count / total_files) * 100
        
        # Determine primary language
        primary_language = max(language_percentages, key=language_percentages.get) if language_percentages else None
        confidence = 1.0 if primary_language else 0.0
        
        return DetectionResult(
            detector_name="LanguageDetector",
            detected=len(language_percentages) > 0,
            confidence=confidence,
            data={
                "languages": language_percentages,
                "primary_language": primary_language,
                "file_count": total_files,
            },
        )
