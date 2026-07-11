#!/usr/bin/env python3
"""
Python codegen — turns an `ObjectDef` into a real, importable `dataclass`.

Generates: the primary dataclass, one `Enum` class per inline `Enum [...]`
field, a `validate()` method that enforces the AGL `validate {}` block, and
`EVENTS` / `PERMISSIONS` / `VERSION` class-level metadata so all information
in the `.agl` source survives into the generated Python.
"""

from __future__ import annotations

from typing import Dict, List

from .ast_nodes import EventDef, Field, ObjectDef, PermissionRule, ValidationRule

_PRIMITIVE_TO_PYTHON = {
    "String": "str",
    "Int": "int",
    "Decimal": "decimal.Decimal",
    "Float": "float",
    "Boolean": "bool",
    "UUID": "uuid.UUID",
    "DateTime": "datetime.datetime",
    "Binary": "bytes",
    "JSON": "Dict[str, Any]",
}


def _enum_class_name(object_name: str, field_name: str) -> str:
    return f"{object_name}{field_name.capitalize()}"


def _python_type_for_field(object_name: str, f: Field) -> str:
    if f.enum is not None:
        base = _enum_class_name(object_name, f.name)
    elif f.type_name in _PRIMITIVE_TO_PYTHON:
        base = _PRIMITIVE_TO_PYTHON[f.type_name]
    else:
        # Reference to another AGL object — forward-reference by name since
        # that object may be compiled in a separate module.
        base = f'"{f.type_name}"'

    if f.is_list:
        base = f"List[{base}]"
    if f.optional:
        base = f"Optional[{base}]"
    return base


def _default_for_field(f: Field) -> str:
    if f.is_list:
        return " = field(default_factory=list)"
    if f.optional:
        return " = None"
    return ""


def _render_enum_classes(object_def: ObjectDef) -> List[str]:
    blocks = []
    for f in object_def.fields:
        if f.enum is not None:
            class_name = _enum_class_name(object_def.name, f.name)
            members = "\n".join(f'    {v} = "{v}"' for v in f.enum.values)
            blocks.append(f"class {class_name}(enum.Enum):\n{members}\n")
    return blocks


def _render_validate_method(object_def: ObjectDef) -> str:
    if not object_def.validations:
        return (
            "    def validate(self) -> List[str]:\n"
            "        \"\"\"No validate {} block in the source AGL — always valid.\"\"\"\n"
            "        return []\n"
        )

    lines = [
        "    def validate(self) -> List[str]:",
        '        """Run the rules declared in the AGL `validate {}` block.',
        "",
        "        Returns a list of human-readable error strings; empty means valid.",
        '        """',
        "        errors: List[str] = []",
    ]
    for rule in object_def.validations:
        for r in rule.rules:
            lines.extend(_render_single_rule(rule.field, r))
    lines.append("        return errors")
    return "\n".join(lines) + "\n"


def _render_single_rule(field_name: str, rule_text: str) -> List[str]:
    value_expr = f"self.{field_name}"
    if rule_text == "required":
        return [
            f"        if {value_expr} is None or {value_expr} == '':",
            f'            errors.append("{field_name} is required")',
        ]
    if rule_text.startswith("min(") and rule_text.endswith(")"):
        n = rule_text[4:-1]
        return [
            f"        if {value_expr} is not None and hasattr({value_expr}, '__len__') and len({value_expr}) < {n}:",
            f'            errors.append("{field_name} must have length >= {n}")',
        ]
    if rule_text.startswith("max(") and rule_text.endswith(")"):
        n = rule_text[4:-1]
        return [
            f"        if {value_expr} is not None and hasattr({value_expr}, '__len__') and len({value_expr}) > {n}:",
            f'            errors.append("{field_name} must have length <= {n}")',
        ]
    # Unknown rule keyword: recorded, not silently dropped, so authors notice
    # unsupported rules instead of getting a validator that quietly no-ops.
    return [
        f"        # unsupported validation rule '{rule_text}' for field '{field_name}' — add support in codegen_python.py",
    ]


def _render_events_metadata(events: List[EventDef]) -> str:
    # ClassVar so these are shared class-level metadata, not per-instance
    # dataclass fields (dataclasses reject mutable dict/list defaults).
    if not events:
        return "    EVENTS: ClassVar[Dict[str, str]] = {}\n"
    entries = ", ".join(f'"{e.name}": "{e.payload_type}"' for e in events)
    return f"    EVENTS: ClassVar[Dict[str, str]] = {{{entries}}}\n"


def _render_permissions_metadata(permissions: List[PermissionRule]) -> str:
    if not permissions:
        return "    PERMISSIONS: ClassVar[Dict[str, Any]] = {}\n"
    parts = []
    for rule in permissions:
        if rule.roles is not None:
            roles = ", ".join(f'"{r}"' for r in rule.roles)
            parts.append(f'"{rule.action}": [{roles}]')
        else:
            entries = []
            for fname, roles in (rule.field_roles or {}).items():
                role_list = ", ".join(f'"{r}"' for r in roles)
                entries.append(f'"{fname}": [{role_list}]')
            field_entries = ", ".join(entries)
            parts.append(f'"{rule.action}": {{{field_entries}}}')
    return f"    PERMISSIONS: ClassVar[Dict[str, Any]] = {{{', '.join(parts)}}}\n"


def generate_python(object_def: ObjectDef) -> str:
    """Render a complete, importable Python module for `object_def`."""
    header = (
        '"""Auto-generated by agos-factory AGL compiler. Do not edit by hand —\n'
        "edit the .agl source and recompile."
        '"""\n\n'
        # Deliberately NOT using `from __future__ import annotations`: with
        # postponed evaluation, `ClassVar[...]` annotations become plain
        # strings and the dataclasses module can fail to recognize them as
        # ClassVar when the module isn't registered in sys.modules under its
        # own name (e.g. when exec()'d dynamically) — treating EVENTS /
        # PERMISSIONS as real mutable dataclass fields and raising at class
        # definition time. Real typing objects avoid that entirely.
        "import datetime\n"
        "import decimal\n"
        "import enum\n"
        "import uuid\n"
        "from dataclasses import dataclass, field\n"
        "from typing import Any, ClassVar, Dict, List, Optional\n\n\n"
    )

    body_parts: List[str] = _render_enum_classes(object_def)

    field_lines = []
    for f in object_def.fields:
        py_type = _python_type_for_field(object_def.name, f)
        field_lines.append(f"    {f.name}: {py_type}{_default_for_field(f)}")
    fields_block = "\n".join(field_lines) if field_lines else "    pass"

    class_lines = [
        "@dataclass",
        f"class {object_def.name}:",
        f'    """Generated from {object_def.name}.agl by the AGL compiler."""',
        "",
        fields_block,
        "",
        f'    VERSION: str = "{object_def.version or "0.0.0"}"',
        "",
        _render_events_metadata(object_def.events).rstrip("\n"),
        _render_permissions_metadata(object_def.permissions).rstrip("\n"),
        "",
        _render_validate_method(object_def).rstrip("\n"),
    ]
    body_parts.append("\n".join(class_lines) + "\n")

    return header + "\n\n".join(body_parts)
