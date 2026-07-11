"""
AGL (AGOS Language) — a real lexer/parser/compiler for the `.agl` DSL
documented in `01-AGL-Language/README.md`.

Public API:
    tokenize(source)                 -> List[Token]
    parse(source)                    -> ObjectDef
    AGLCompiler().compile_source(s)  -> {"python": str, "json_schema": dict}
    AGLCompiler().compile_file(path) -> writes <Name>.py + <Name>.schema.json
"""

from .lexer import Token, TokenType, tokenize
from .ast_nodes import EventDef, Field, ObjectDef, ValidationRule
from .parser import AGLParseError, parse
from .compiler import AGLCompiler

__all__ = [
    "Token",
    "TokenType",
    "tokenize",
    "Field",
    "EventDef",
    "ObjectDef",
    "ValidationRule",
    "AGLParseError",
    "parse",
    "AGLCompiler",
]
