"""AGOS Language Packs Library."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class LanguagePackMetadata:
    """Language pack metadata."""
    id: str
    name: str
    version: str = "1.0.0"
    extensions: List[str] = field(default_factory=list)
    description: str = ""


class LanguagePack:
    """A programming language pack."""
    
    def __init__(self, name: str, extensions: List[str], description: str = ""):
        """Initialize language pack."""
        self.metadata = LanguagePackMetadata(
            id=f"lang-{uuid.uuid4().hex[:8]}",
            name=name,
            extensions=extensions,
            description=description,
        )
        self.grammar = ""
        self.best_practices: List[str] = []
        self.anti_patterns: List[str] = []
        self.security_rules: List[str] = []
        self.templates: List[Dict] = []


# Language Packs
LANGUAGE_PACKS = {
    "typescript": LanguagePack("TypeScript", [".ts", ".tsx"], "TypeScript language pack"),
    "javascript": LanguagePack("JavaScript", [".js", ".jsx"], "JavaScript language pack"),
    "python": LanguagePack("Python", [".py"], "Python language pack"),
    "java": LanguagePack("Java", [".java"], "Java language pack"),
    "kotlin": LanguagePack("Kotlin", [".kt", ".kts"], "Kotlin language pack"),
    "scala": LanguagePack("Scala", [".scala"], "Scala language pack"),
    "go": LanguagePack("Go", [".go"], "Go language pack"),
    "rust": LanguagePack("Rust", [".rs"], "Rust language pack"),
    "c": LanguagePack("C", [".c", ".h"], "C language pack"),
    "cpp": LanguagePack("C++", [".cpp", ".hpp", ".cc"], "C++ language pack"),
    "csharp": LanguagePack("C#", [".cs"], "C# language pack"),
    "fsharp": LanguagePack("F#", [".fs"], "F# language pack"),
    "swift": LanguagePack("Swift", [".swift"], "Swift language pack"),
    "objectivec": LanguagePack("Objective-C", [".m", ".h"], "Objective-C language pack"),
    "dart": LanguagePack("Dart", [".dart"], "Dart language pack"),
    "php": LanguagePack("PHP", [".php"], "PHP language pack"),
    "ruby": LanguagePack("Ruby", [".rb"], "Ruby language pack"),
    "elixir": LanguagePack("Elixir", [".ex", ".exs"], "Elixir language pack"),
    "erlang": LanguagePack("Erlang", [".erl"], "Erlang language pack"),
    "lua": LanguagePack("Lua", [".lua"], "Lua language pack"),
    "zig": LanguagePack("Zig", [".zig"], "Zig language pack"),
    "nim": LanguagePack("Nim", [".nim"], "Nim language pack"),
    "haskell": LanguagePack("Haskell", [".hs"], "Haskell language pack"),
    "ocaml": LanguagePack("OCaml", [".ml", ".mli"], "OCaml language pack"),
    "r": LanguagePack("R", [".r", ".R"], "R language pack"),
    "julia": LanguagePack("Julia", [".jl"], "Julia language pack"),
    "matlab": LanguagePack("MATLAB", [".m"], "MATLAB language pack"),
    "bash": LanguagePack("Bash", [".sh"], "Bash shell language pack"),
    "powershell": LanguagePack("PowerShell", [".ps1"], "PowerShell language pack"),
    "sql": LanguagePack("SQL", [".sql"], "SQL language pack"),
    "graphql": LanguagePack("GraphQL", [".graphql", ".gql"], "GraphQL language pack"),
    "html": LanguagePack("HTML", [".html", ".htm"], "HTML language pack"),
    "css": LanguagePack("CSS", [".css"], "CSS language pack"),
    "solidity": LanguagePack("Solidity", [".sol"], "Solidity language pack"),
    "move": LanguagePack("Move", [".move"], "Move language pack"),
    "assembly": LanguagePack("Assembly", [".asm"], "Assembly language pack"),
    "wasm": LanguagePack("WebAssembly", [".wasm"], "WebAssembly language pack"),
    "yaml": LanguagePack("YAML", [".yaml", ".yml"], "YAML language pack"),
    "json": LanguagePack("JSON", [".json"], "JSON language pack"),
    "xml": LanguagePack("XML", [".xml"], "XML language pack"),
}


class LanguagePackLibrary:
    """Library of language packs."""
    
    def __init__(self):
        self.packs = LANGUAGE_PACKS
    
    def get(self, name: str) -> LanguagePack:
        return self.packs.get(name)
    
    def list_all(self) -> List[LanguagePack]:
        return list(self.packs.values())
    
    def detect(self, file_path: str) -> LanguagePack:
        """Detect language from file path."""
        ext = file_path.split(".")[-1].lower() if "." in file_path else ""
        for pack in self.packs.values():
            for e in pack.metadata.extensions:
                if file_path.lower().endswith(e.lower()):
                    return pack
        return self.packs.get("javascript")  # Default fallback


_library = LanguagePackLibrary()


def get_library() -> LanguagePackLibrary:
    return _library