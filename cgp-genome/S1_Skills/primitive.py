#!/usr/bin/env python3
"""
CGP - Primitive Skills
=====================

The smallest unit of capability.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class SkillDifficulty(Enum):
    """Skill difficulty levels."""
    TRIVIAL = "trivial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class SkillCategory(Enum):
    """Categories of skills."""
    FILE_OPERATIONS = "file_operations"
    CODE_OPERATIONS = "code_operations"
    GIT_OPERATIONS = "git_operations"
    EXECUTION = "execution"
    WEB = "web"
    API = "api"
    DATA = "data"
    SECURITY = "security"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    COMMUNICATION = "communication"
    DOCUMENTATION = "documentation"
    ANALYSIS = "analysis"
    GENERATION = "generation"


class ImplementationType(Enum):
    """How a skill is implemented."""
    CODE = "code"
    API = "api"
    TOOL = "tool"
    EXTERNAL = "external"


@dataclass
class SkillSchema:
    """Input/output schema for a skill."""
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Skill:
    """
    A primitive skill - the smallest unit of capability.
    
    Examples:
    - Read File
    - Write File
    - Search Code
    - Execute Command
    """
    skill_id: str
    name: str
    category: SkillCategory
    
    # Description
    description: str = ""
    
    # Schema
    input_schema: Dict[str, Any] = field(default_factory=SkillSchema)
    output_schema: Dict[str, Any] = field(default_factory=SkillSchema)
    
    # Implementation
    implementation_type: ImplementationType = ImplementationType.CODE
    implementation_ref: str = ""  # Reference to implementation
    
    # Metrics
    difficulty: SkillDifficulty = SkillDifficulty.MEDIUM
    estimated_time_seconds: int = 10
    estimated_cost: float = 0.01
    
    # Relationships
    requires: Tuple[str, ...] = ()    # Prerequisite skills
    provides: Tuple[str, ...] = ()    # Skills this enables
    related_skills: Tuple[str, ...] = ()
    
    # Metadata
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: Tuple[str, ...] = ()
    
    def get_complexity_score(self) -> float:
        """Calculate complexity score."""
        difficulty_scores = {
            SkillDifficulty.TRIVIAL: 0.1,
            SkillDifficulty.EASY: 0.3,
            SkillDifficulty.MEDIUM: 0.5,
            SkillDifficulty.HARD: 0.7,
            SkillDifficulty.EXPERT: 0.9,
        }
        return difficulty_scores.get(self.difficulty, 0.5)


@dataclass
class SkillExecution:
    """Execution record of a skill."""
    execution_id: str
    skill_id: str
    success: bool
    duration_ms: int
    cost: float
    timestamp: str
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class SkillRegistry:
    """
    Registry of all skills.
    """
    
    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._by_category: Dict[SkillCategory, List[str]] = {}
        self._by_tag: Dict[str, List[str]] = {}
        self._executions: List[SkillExecution] = []
        
        # Register default skills
        self._register_default_skills()
    
    def _register_default_skills(self) -> None:
        """Register default skills."""
        default_skills = [
            # File Operations
            Skill(skill_id="read_file", name="Read File", category=SkillCategory.FILE_OPERATIONS, description="Read contents of a file"),
            Skill(skill_id="write_file", name="Write File", category=SkillCategory.FILE_OPERATIONS, description="Write contents to a file"),
            Skill(skill_id="delete_file", name="Delete File", category=SkillCategory.FILE_OPERATIONS, description="Delete a file"),
            Skill(skill_id="move_file", name="Move File", category=SkillCategory.FILE_OPERATIONS, description="Move a file"),
            Skill(skill_id="copy_file", name="Copy File", category=SkillCategory.FILE_OPERATIONS, description="Copy a file"),
            Skill(skill_id="list_directory", name="List Directory", category=SkillCategory.FILE_OPERATIONS, description="List directory contents"),
            Skill(skill_id="create_directory", name="Create Directory", category=SkillCategory.FILE_OPERATIONS, description="Create a directory"),
            
            # Code Operations
            Skill(skill_id="search_code", name="Search Code", category=SkillCategory.CODE_OPERATIONS, description="Search for code patterns"),
            Skill(skill_id="replace_code", name="Replace Code", category=SkillCategory.CODE_OPERATIONS, description="Replace code patterns"),
            Skill(skill_id="format_code", name="Format Code", category=SkillCategory.CODE_OPERATIONS, description="Format code"),
            Skill(skill_id="lint_code", name="Lint Code", category=SkillCategory.CODE_OPERATIONS, description="Lint code"),
            Skill(skill_id="parse_code", name="Parse Code", category=SkillCategory.CODE_OPERATIONS, description="Parse code"),
            Skill(skill_id="generate_code", name="Generate Code", category=SkillCategory.CODE_OPERATIONS, description="Generate code"),
            
            # Git Operations
            Skill(skill_id="git_clone", name="Git Clone", category=SkillCategory.GIT_OPERATIONS, description="Clone a repository"),
            Skill(skill_id="git_commit", name="Git Commit", category=SkillCategory.GIT_OPERATIONS, description="Create a commit"),
            Skill(skill_id="git_push", name="Git Push", category=SkillCategory.GIT_OPERATIONS, description="Push to remote"),
            Skill(skill_id="git_pull", name="Git Pull", category=SkillCategory.GIT_OPERATIONS, description="Pull from remote"),
            Skill(skill_id="git_diff", name="Git Diff", category=SkillCategory.GIT_OPERATIONS, description="Show git diff"),
            Skill(skill_id="git_branch", name="Git Branch", category=SkillCategory.GIT_OPERATIONS, description="Manage branches"),
            
            # Execution
            Skill(skill_id="run_command", name="Run Command", category=SkillCategory.EXECUTION, description="Run a shell command"),
            Skill(skill_id="run_tests", name="Run Tests", category=SkillCategory.EXECUTION, description="Run test suite"),
            Skill(skill_id="run_build", name="Run Build", category=SkillCategory.EXECUTION, description="Run build process"),
            
            # Web
            Skill(skill_id="open_browser", name="Open Browser", category=SkillCategory.WEB, description="Open browser"),
            Skill(skill_id="take_screenshot", name="Take Screenshot", category=SkillCategory.WEB, description="Take screenshot"),
            Skill(skill_id="fill_form", name="Fill Form", category=SkillCategory.WEB, description="Fill web form"),
            Skill(skill_id="click_element", name="Click Element", category=SkillCategory.WEB, description="Click element"),
            
            # API
            Skill(skill_id="call_rest_api", name="Call REST API", category=SkillCategory.API, description="Call REST API"),
            Skill(skill_id="call_graphql", name="Call GraphQL", category=SkillCategory.API, description="Call GraphQL API"),
            Skill(skill_id="upload_file", name="Upload File", category=SkillCategory.API, description="Upload file"),
            
            # Data
            Skill(skill_id="parse_json", name="Parse JSON", category=SkillCategory.DATA, description="Parse JSON"),
            Skill(skill_id="parse_yaml", name="Parse YAML", category=SkillCategory.DATA, description="Parse YAML"),
            Skill(skill_id="parse_csv", name="Parse CSV", category=SkillCategory.DATA, description="Parse CSV"),
            
            # Generation
            Skill(skill_id="generate_text", name="Generate Text", category=SkillCategory.GENERATION, description="Generate text"),
            Skill(skill_id="generate_markdown", name="Generate Markdown", category=SkillCategory.GENERATION, description="Generate markdown"),
        ]
        
        for skill in default_skills:
            self.register(skill)
    
    def register(self, skill: Skill) -> str:
        """Register a skill."""
        self._skills[skill.skill_id] = skill
        
        # Index by category
        if skill.category not in self._by_category:
            self._by_category[skill.category] = []
        self._by_category[skill.category].append(skill.skill_id)
        
        # Index by tags
        for tag in skill.tags:
            if tag not in self._by_tag:
                self._by_tag[tag] = []
            self._by_tag[tag].append(skill.skill_id)
        
        return skill.skill_id
    
    def get(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID."""
        return self._skills.get(skill_id)
    
    def get_by_category(self, category: SkillCategory) -> List[Skill]:
        """Get all skills in a category."""
        skill_ids = self._by_category.get(category, [])
        return [self._skills[sid] for sid in skill_ids if sid in self._skills]
    
    def get_by_tag(self, tag: str) -> List[Skill]:
        """Get all skills with a tag."""
        skill_ids = self._by_tag.get(tag, [])
        return [self._skills[sid] for sid in skill_ids if sid in self._skills]
    
    def search(self, query: str, limit: int = 10) -> List[Skill]:
        """Search skills by name or description."""
        query_lower = query.lower()
        results = []
        
        for skill in self._skills.values():
            if query_lower in skill.name.lower() or query_lower in skill.description.lower():
                results.append(skill)
        
        return results[:limit]
    
    def record_execution(self, execution: SkillExecution) -> None:
        """Record a skill execution."""
        self._executions.append(execution)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        by_category = {cat.value: len(ids) for cat, ids in self._by_category.items()}
        
        return {
            "total_skills": len(self._skills),
            "by_category": by_category,
            "total_executions": len(self._executions),
            "successful_executions": sum(1 for e in self._executions if e.success),
        }


class SkillExtractor:
    """
    Extracts skills from code.
    """
    
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self._extractors: Dict[str, Callable] = {}
    
    def register_extractor(
        self,
        name: str,
        extractor: Callable[[str], List[str]]
    ) -> None:
        """Register an extractor."""
        self._extractors[name] = extractor
    
    def extract_from_code(self, code: str, language: str = "python") -> List[Skill]:
        """Extract skills from code."""
        skill_ids = []
        
        # Check for file operations
        if "open(" in code or "read(" in code:
            skill_ids.append("read_file")
        if "write(" in code or "create" in code:
            skill_ids.append("write_file")
        
        # Check for git operations
        if "git" in code.lower():
            if "clone" in code.lower():
                skill_ids.append("git_clone")
            if "commit" in code.lower():
                skill_ids.append("git_commit")
        
        # Check for API calls
        if "requests" in code or "fetch" in code:
            skill_ids.append("call_rest_api")
        
        # Get skill objects
        skills = []
        for sid in set(skill_ids):
            skill = self.registry.get(sid)
            if skill:
                skills.append(skill)
        
        return skills
    
    def extract_from_structure(self, structure: Dict[str, Any]) -> List[Skill]:
        """Extract skills from project structure."""
        skills = []
        
        # Check file types
        files = structure.get("files", [])
        for file in files:
            if file.endswith(".py"):
                skills.append(self.registry.get("parse_code"))
            elif file.endswith(".json"):
                skills.append(self.registry.get("parse_json"))
            elif file.endswith(".yaml") or file.endswith(".yml"):
                skills.append(self.registry.get("parse_yaml"))
        
        return list(set(skills))
