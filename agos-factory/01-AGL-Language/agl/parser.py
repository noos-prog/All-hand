#!/usr/bin/env python3
"""
Recursive-descent parser for the AGL DSL.

Implements the grammar documented in `01-AGL-Language/README.md`:
`object Name { fields... validate {} events {} permissions {} version "x" }`.
"""

from __future__ import annotations

from typing import List, Optional

from .ast_nodes import EnumType, EventDef, Field, ObjectDef, PermissionRule, ValidationRule
from .lexer import Token, TokenType, tokenize


class AGLParseError(SyntaxError):
    """Raised on any AGL source that does not match the grammar."""


class _Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    # -- token stream helpers -------------------------------------------------

    @property
    def _current(self) -> Token:
        return self._tokens[self._pos]

    def _advance(self) -> Token:
        tok = self._tokens[self._pos]
        if tok.type != TokenType.EOF:
            self._pos += 1
        return tok

    def _check(self, type_: TokenType, value: Optional[str] = None) -> bool:
        tok = self._current
        if tok.type != type_:
            return False
        return value is None or tok.value == value

    def _expect(self, type_: TokenType, value: Optional[str] = None) -> Token:
        if not self._check(type_, value):
            tok = self._current
            expected = value if value is not None else type_.name
            raise AGLParseError(
                f"expected {expected!r} but got {tok.value!r} ({tok.type.name}) at {tok.line}:{tok.col}"
            )
        return self._advance()

    def _match_ident(self, *values: str) -> bool:
        return self._current.type == TokenType.IDENT and self._current.value in values

    # -- grammar ---------------------------------------------------------------

    def parse_object(self) -> ObjectDef:
        self._expect(TokenType.IDENT, "object")
        name = self._expect(TokenType.IDENT).value
        self._expect(TokenType.LBRACE)

        fields: List[Field] = []
        validations: List[ValidationRule] = []
        events: List[EventDef] = []
        permissions: List[PermissionRule] = []
        version: Optional[str] = None

        while not self._check(TokenType.RBRACE):
            if self._match_ident("validate"):
                self._advance()
                validations.extend(self._parse_validate_block())
            elif self._match_ident("events"):
                self._advance()
                events.extend(self._parse_events_block())
            elif self._match_ident("permissions"):
                self._advance()
                permissions.extend(self._parse_permissions_block())
            elif self._match_ident("version"):
                self._advance()
                version = self._expect(TokenType.STRING).value
            elif self._current.type == TokenType.IDENT:
                fields.append(self._parse_field())
            else:
                tok = self._current
                raise AGLParseError(f"unexpected token {tok.value!r} at {tok.line}:{tok.col}")

        self._expect(TokenType.RBRACE)
        return ObjectDef(
            name=name, fields=fields, validations=validations,
            events=events, permissions=permissions, version=version,
        )

    def _parse_field(self) -> Field:
        field_name = self._expect(TokenType.IDENT).value
        self._expect(TokenType.COLON)
        return self._parse_type(field_name)

    def _parse_type(self, field_name: str) -> Field:
        if self._match_ident("Enum"):
            self._advance()
            self._expect(TokenType.LBRACKET)
            values = [self._expect(TokenType.IDENT).value]
            while self._check(TokenType.COMMA):
                self._advance()
                values.append(self._expect(TokenType.IDENT).value)
            self._expect(TokenType.RBRACKET)
            optional = self._consume_optional_marker()
            return Field(name=field_name, type_name=None, enum=EnumType(values), optional=optional)

        type_name = self._expect(TokenType.IDENT).value
        is_list = False
        if self._check(TokenType.LBRACKET):
            self._advance()
            self._expect(TokenType.RBRACKET)
            is_list = True
        optional = self._consume_optional_marker()
        return Field(name=field_name, type_name=type_name, is_list=is_list, optional=optional)

    def _consume_optional_marker(self) -> bool:
        if self._check(TokenType.QUESTION):
            self._advance()
            return True
        return False

    def _parse_validate_block(self) -> List[ValidationRule]:
        self._expect(TokenType.LBRACE)
        rules: List[ValidationRule] = []
        while not self._check(TokenType.RBRACE):
            field_name = self._expect(TokenType.IDENT).value
            self._expect(TokenType.COLON)
            rule_texts = [self._parse_rule_expr()]
            while self._check(TokenType.COMMA):
                self._advance()
                rule_texts.append(self._parse_rule_expr())
            rules.append(ValidationRule(field=field_name, rules=rule_texts))
        self._expect(TokenType.RBRACE)
        return rules

    def _parse_rule_expr(self) -> str:
        name = self._expect(TokenType.IDENT).value
        if self._check(TokenType.LPAREN):
            self._advance()
            args = []
            if not self._check(TokenType.RPAREN):
                args.append(self._parse_rule_arg())
                while self._check(TokenType.COMMA):
                    self._advance()
                    args.append(self._parse_rule_arg())
            self._expect(TokenType.RPAREN)
            return f"{name}({', '.join(args)})"
        return name

    def _parse_rule_arg(self) -> str:
        if self._check(TokenType.NUMBER):
            return self._advance().value
        if self._check(TokenType.STRING):
            return repr(self._advance().value)
        return self._expect(TokenType.IDENT).value

    def _parse_events_block(self) -> List[EventDef]:
        self._expect(TokenType.LBRACE)
        events: List[EventDef] = []
        while not self._check(TokenType.RBRACE):
            event_name = self._expect(TokenType.IDENT).value
            self._expect(TokenType.COLON)
            payload_type = self._expect(TokenType.IDENT).value
            payload_fields: List[Field] = []
            if self._check(TokenType.LBRACE):
                self._advance()
                while not self._check(TokenType.RBRACE):
                    payload_fields.append(self._parse_field())
                self._expect(TokenType.RBRACE)
            events.append(EventDef(name=event_name, payload_type=payload_type, payload_fields=payload_fields))
        self._expect(TokenType.RBRACE)
        return events

    def _parse_permissions_block(self) -> List[PermissionRule]:
        self._expect(TokenType.LBRACE)
        rules: List[PermissionRule] = []
        while not self._check(TokenType.RBRACE):
            action = self._expect(TokenType.IDENT).value
            self._expect(TokenType.COLON)
            if self._check(TokenType.LBRACKET):
                roles = self._parse_role_list()
                rules.append(PermissionRule(action=action, roles=roles))
            elif self._check(TokenType.LBRACE):
                self._advance()
                field_roles = {}
                while not self._check(TokenType.RBRACE):
                    fname = self._expect(TokenType.IDENT).value
                    self._expect(TokenType.COLON)
                    field_roles[fname] = self._parse_role_list()
                self._expect(TokenType.RBRACE)
                rules.append(PermissionRule(action=action, field_roles=field_roles))
            else:
                tok = self._current
                raise AGLParseError(f"expected '[' or '{{' after '{action}:' at {tok.line}:{tok.col}")
        self._expect(TokenType.RBRACE)
        return rules

    def _parse_role_list(self) -> List[str]:
        self._expect(TokenType.LBRACKET)
        roles = [self._expect(TokenType.IDENT).value]
        while self._check(TokenType.COMMA):
            self._advance()
            roles.append(self._expect(TokenType.IDENT).value)
        self._expect(TokenType.RBRACKET)
        return roles


def parse(source: str) -> ObjectDef:
    """Parse one `.agl` source string containing a single `object` definition."""
    tokens = tokenize(source)
    parser = _Parser(tokens)
    obj = parser.parse_object()
    if not parser._check(TokenType.EOF):  # noqa: SLF001 - internal consistency check
        tok = parser._current  # noqa: SLF001
        raise AGLParseError(f"unexpected trailing content at {tok.line}:{tok.col}")
    return obj
