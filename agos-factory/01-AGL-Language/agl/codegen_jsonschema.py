#!/usr/bin/env python3
"""JSON Schema codegen — turns an `ObjectDef` into a real Draft-07 JSON Schema."""

from __future__ import annotations

from typing import Any, Dict, List

from .ast_nodes import Field, ObjectDef

_PRIMITIVE_TO_JSONSCHEMA: Dict[str, Dict[str, Any]] = {
    "String": {"type": "string"},
    "Int": {"type": "integer"},
    "Decimal": {"type": "number"},
    "Float": {"type": "number"},
    "Boolean": {"type": "boolean"},
    "UUID": {"type": "string", "format": "uuid"},
    "DateTime": {"type": "string", "format": "date-time"},
    "Binary": {"type": "string", "contentEncoding": "base64"},
    "JSON": {"type": "object"},
}


def _schema_for_field(f: Field) -> Dict[str, Any]:
    if f.enum is not None:
        schema: Dict[str, Any] = {"type": "string", "enum": list(f.enum.values)}
    elif f.type_name in _PRIMITIVE_TO_JSONSCHEMA:
        schema = dict(_PRIMITIVE_TO_JSONSCHEMA[f.type_name])
    else:
        # Reference to another AGL object: JSON Schema $ref by convention.
        schema = {"$ref": f"#/definitions/{f.type_name}"}

    if f.is_list:
        schema = {"type": "array", "items": schema}
    return schema


def _required_fields(object_def: ObjectDef) -> List[str]:
    required_names = set()
    for rule in object_def.validations:
        if "required" in rule.rules:
            required_names.add(rule.field)
    # Non-optional, non-list scalar fields without an explicit "required"
    # rule are still required by AGL's own semantics (`?` is what opts out).
    for f in object_def.fields:
        if not f.optional:
            required_names.add(f.name)
    return sorted(required_names)


def generate_json_schema(object_def: ObjectDef) -> Dict[str, Any]:
    """Render a Draft-07 JSON Schema document for `object_def`."""
    properties = {f.name: _schema_for_field(f) for f in object_def.fields}
    schema: Dict[str, Any] = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": object_def.name,
        "type": "object",
        "properties": properties,
        "required": _required_fields(object_def),
        "additionalProperties": False,
    }
    if object_def.version:
        schema["version"] = object_def.version
    return schema
