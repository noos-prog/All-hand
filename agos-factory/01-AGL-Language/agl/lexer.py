#!/usr/bin/env python3
"""
Lexer for the AGL (AGOS Language) DSL.

Converts raw `.agl` source text into a flat list of `Token`s, stripping
line (`//`) and block (`/* */`) comments and tracking line/column for
useful parser error messages.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class TokenType(Enum):
    IDENT = auto()
    STRING = auto()
    NUMBER = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LPAREN = auto()
    RPAREN = auto()
    COLON = auto()
    COMMA = auto()
    QUESTION = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str
    line: int
    col: int

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.col})"


_SINGLE_CHAR = {
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    "?": TokenType.QUESTION,
}


class AGLLexError(SyntaxError):
    """Raised when the AGL source contains a character the lexer cannot tokenize."""


def tokenize(source: str) -> List[Token]:
    tokens: List[Token] = []
    line = 1
    col = 1
    i = 0
    n = len(source)

    def advance(count: int = 1) -> None:
        nonlocal i, line, col
        for _ in range(count):
            if i < n and source[i] == "\n":
                line += 1
                col = 1
            else:
                col += 1
            i += 1

    while i < n:
        ch = source[i]

        if ch in " \t\r\n":
            advance()
            continue

        if ch == "/" and i + 1 < n and source[i + 1] == "/":
            while i < n and source[i] != "\n":
                advance()
            continue

        if ch == "/" and i + 1 < n and source[i + 1] == "*":
            start_line, start_col = line, col
            advance(2)
            while i < n and not (source[i] == "*" and i + 1 < n and source[i + 1] == "/"):
                advance()
            if i >= n:
                raise AGLLexError(f"unterminated block comment starting at {start_line}:{start_col}")
            advance(2)
            continue

        if ch == '"':
            start_line, start_col = line, col
            advance()
            start = i
            while i < n and source[i] != '"':
                advance()
            if i >= n:
                raise AGLLexError(f"unterminated string starting at {start_line}:{start_col}")
            value = source[start:i]
            advance()
            tokens.append(Token(TokenType.STRING, value, start_line, start_col))
            continue

        if ch.isdigit() or (ch == "-" and i + 1 < n and source[i + 1].isdigit()):
            start_line, start_col = line, col
            start = i
            advance()
            while i < n and (source[i].isdigit() or source[i] == "."):
                advance()
            tokens.append(Token(TokenType.NUMBER, source[start:i], start_line, start_col))
            continue

        if ch.isalpha() or ch == "_":
            start_line, start_col = line, col
            start = i
            while i < n and (source[i].isalnum() or source[i] == "_"):
                advance()
            tokens.append(Token(TokenType.IDENT, source[start:i], start_line, start_col))
            continue

        if ch in _SINGLE_CHAR:
            tokens.append(Token(_SINGLE_CHAR[ch], ch, line, col))
            advance()
            continue

        raise AGLLexError(f"unexpected character {ch!r} at {line}:{col}")

    tokens.append(Token(TokenType.EOF, "", line, col))
    return tokens
