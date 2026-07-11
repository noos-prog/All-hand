#!/usr/bin/env python3
"""AGLCompiler — the single entry point for turning `.agl` source into code."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict

from .ast_nodes import ObjectDef
from .codegen_jsonschema import generate_json_schema
from .codegen_python import generate_python
from .parser import parse


@dataclass(frozen=True)
class CompiledObject:
    object_def: ObjectDef
    python_source: str
    json_schema: Dict


class AGLCompiler:
    """Compiles AGL source into Python dataclasses and JSON Schema documents."""

    def compile_source(self, source: str) -> CompiledObject:
        object_def = parse(source)
        return CompiledObject(
            object_def=object_def,
            python_source=generate_python(object_def),
            json_schema=generate_json_schema(object_def),
        )

    def compile_file(self, path: str, out_dir: str) -> CompiledObject:
        """Compile one `.agl` file and write `<Name>.py` + `<Name>.schema.json` to `out_dir`."""
        with open(path, "r", encoding="utf-8") as fh:
            source = fh.read()
        compiled = self.compile_source(source)

        os.makedirs(out_dir, exist_ok=True)
        py_path = os.path.join(out_dir, f"{compiled.object_def.name}.py")
        schema_path = os.path.join(out_dir, f"{compiled.object_def.name}.schema.json")

        with open(py_path, "w", encoding="utf-8") as fh:
            fh.write(compiled.python_source)
        with open(schema_path, "w", encoding="utf-8") as fh:
            json.dump(compiled.json_schema, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

        return compiled
