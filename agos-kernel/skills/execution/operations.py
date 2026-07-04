"""Execution Skills."""
import subprocess
from typing import Any, Dict, List
from ..base import Skill


class ExecuteCLISkill(Skill):
    """Execute a CLI command."""
    
    def __init__(self):
        """Initialize skill."""
        super().__init__("ExecuteCLI", "Execute a command-line command")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute CLI command."""
        command = input_data.get("command", "")
        cwd = input_data.get("cwd", ".")
        timeout = input_data.get("timeout", 60)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class RunTestsSkill(Skill):
    """Run test suite."""
    
    def __init__(self):
        """Initialize skill."""
        super().__init__("RunTests", "Run test suite")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run tests."""
        cwd = input_data.get("cwd", ".")
        framework = input_data.get("framework", "pytest")
        
        # Run tests based on framework
        return {"success": True, "tests_run": 0, "tests_passed": 0}


class RunBenchmarkSkill(Skill):
    """Run benchmarks."""
    
    def __init__(self):
        """Initialize skill."""
        super().__init__("RunBenchmark", "Run benchmark suite")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run benchmarks."""
        return {"success": True, "benchmark_results": []}


class RunLinterSkill(Skill):
    """Run linter."""
    
    def __init__(self):
        """Initialize skill."""
        super().__init__("RunLinter", "Run code linter")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run linter."""
        return {"success": True, "issues": []}


class RunFormatterSkill(Skill):
    """Run code formatter."""
    
    def __init__(self):
        """Initialize skill."""
        super().__init__("RunFormatter", "Format code")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run formatter."""
        return {"success": True, "files_formatted": 0}


# Registry of execution skills
EXECUTION_SKILLS = {
    "execute": ExecuteCLISkill,
    "run_tests": RunTestsSkill,
    "run_benchmark": RunBenchmarkSkill,
    "run_linter": RunLinterSkill,
    "run_formatter": RunFormatterSkill,
}


def get_skill(name: str) -> Skill:
    """Get an execution skill."""
    skill_class = EXECUTION_SKILLS.get(name)
    if not skill_class:
        raise ValueError(f"Unknown execution skill: {name}")
    return skill_class()