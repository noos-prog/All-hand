#!/usr/bin/env python3
"""
Real, executable tests for the AGL lexer/parser/compiler.

Run with:
    python -m pytest agos-factory/01-AGL-Language/tests/test_agl.py -q
or, dependency-free:
    python agos-factory/01-AGL-Language/tests/test_agl.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agl.compiler import AGLCompiler  # noqa: E402
from agl.parser import AGLParseError, parse  # noqa: E402

_EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "examples", "mission.agl")


def _load_example() -> str:
    with open(_EXAMPLE_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


def test_parses_mission_example() -> None:
    obj = parse(_load_example())
    assert obj.name == "Mission"
    field_names = [f.name for f in obj.fields]
    assert field_names == ["id", "name", "type", "tasks", "parent"]
    assert obj.version == "1.0.0"


def test_enum_field_parsed() -> None:
    obj = parse(_load_example())
    type_field = next(f for f in obj.fields if f.name == "type")
    assert type_field.enum is not None
    assert type_field.enum.values == ["BUILD", "FIX", "REFACTOR"]


def test_list_and_optional_markers() -> None:
    obj = parse(_load_example())
    tasks_field = next(f for f in obj.fields if f.name == "tasks")
    parent_field = next(f for f in obj.fields if f.name == "parent")
    assert tasks_field.is_list is True
    assert parent_field.optional is True


def test_validate_block_parsed() -> None:
    obj = parse(_load_example())
    assert len(obj.validations) == 1
    rule = obj.validations[0]
    assert rule.field == "name"
    assert rule.rules == ["required", "min(3)", "max(100)"]


def test_events_block_with_payload_parsed() -> None:
    obj = parse(_load_example())
    assert len(obj.events) == 2
    created = obj.events[0]
    assert created.name == "created"
    assert created.payload_type == "MissionCreated"
    assert [f.name for f in created.payload_fields] == [
        "mission_id", "name", "created_by", "timestamp",
    ]


def test_permissions_block_parsed() -> None:
    obj = parse(_load_example())
    read_rule = next(p for p in obj.permissions if p.action == "read")
    write_rule = next(p for p in obj.permissions if p.action == "write")
    assert read_rule.roles == ["owner", "admin", "viewer"]
    assert write_rule.field_roles == {"status": ["admin"], "name": ["owner", "admin"]}


def test_syntax_error_reports_location() -> None:
    broken = "object Broken {\n  name String\n}"  # missing ':'
    try:
        parse(broken)
        raise AssertionError("expected AGLParseError")
    except AGLParseError as exc:
        assert "2:" in str(exc)


def test_compile_source_generates_valid_python() -> None:
    compiled = AGLCompiler().compile_source(_load_example())
    namespace: dict = {}
    exec(compiled.python_source, namespace)  # noqa: S102 - compiling our own trusted codegen output
    mission_cls = namespace["Mission"]
    assert mission_cls.VERSION == "1.0.0"
    assert "created" in mission_cls.EVENTS


def test_compile_source_generates_valid_json_schema() -> None:
    compiled = AGLCompiler().compile_source(_load_example())
    schema = compiled.json_schema
    assert schema["title"] == "Mission"
    assert schema["properties"]["type"]["enum"] == ["BUILD", "FIX", "REFACTOR"]
    assert "name" in schema["required"]


def test_compile_file_writes_outputs(tmp_path_str: str = "") -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as out_dir:
        compiled = AGLCompiler().compile_file(_EXAMPLE_PATH, out_dir)
        assert os.path.exists(os.path.join(out_dir, "Mission.py"))
        assert os.path.exists(os.path.join(out_dir, "Mission.schema.json"))
        assert compiled.object_def.name == "Mission"


def _run_all() -> None:
    failures = 0
    tests = [obj for name, obj in globals().items() if name.startswith("test_") and callable(obj)]
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:  # noqa: BLE001 - test runner surfaces every failure
            failures += 1
            print(f"FAIL {test.__name__}: {exc}")
    if failures:
        raise SystemExit(f"{failures} test(s) failed")
    print(f"all {len(tests)} tests passed")


if __name__ == "__main__":
    _run_all()
