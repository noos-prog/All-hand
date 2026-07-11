#!/usr/bin/env python3
"""AST node types produced by the AGL parser."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

PRIMITIVE_TYPES = {"String", "Int", "Decimal", "Float", "Boolean", "UUID", "DateTime", "Binary", "JSON"}


@dataclass(frozen=True)
class EnumType:
    """Inline enum type, e.g. `Enum [ACTIVE, INACTIVE]`."""

    values: List[str]


@dataclass(frozen=True)
class Field:
    """One field of an `object` or event payload.

    `type_name` is either a primitive (see `PRIMITIVE_TYPES`), a reference
    to another `object` name (for relationships), or `None` when `enum` is
    set instead.
    """

    name: str
    type_name: Optional[str]
    enum: Optional[EnumType] = None
    is_list: bool = False
    optional: bool = False


@dataclass(frozen=True)
class ValidationRule:
    """One field's validation rules, e.g. `name: required, min(3), max(100)`."""

    field: str
    rules: List[str]  # each rule rendered back as source text, e.g. "min(3)"


@dataclass(frozen=True)
class EventDef:
    """One domain event, optionally with its own payload fields."""

    name: str
    payload_type: str
    payload_fields: List[Field] = field(default_factory=list)


@dataclass(frozen=True)
class PermissionRule:
    """One permission action, either role-scoped or field-scoped.

    `roles` is set for `read: [owner, admin]`.
    `field_roles` is set for `write: { status: [admin], name: [owner] }`.
    """

    action: str
    roles: Optional[List[str]] = None
    field_roles: Optional[Dict[str, List[str]]] = None


@dataclass(frozen=True)
class ObjectDef:
    """A complete `object Name { ... }` definition — the AGL compilation unit."""

    name: str
    fields: List[Field] = field(default_factory=list)
    validations: List[ValidationRule] = field(default_factory=list)
    events: List[EventDef] = field(default_factory=list)
    permissions: List[PermissionRule] = field(default_factory=list)
    version: Optional[str] = None
