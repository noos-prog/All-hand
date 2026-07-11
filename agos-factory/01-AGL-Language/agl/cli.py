#!/usr/bin/env python3
"""
Command-line interface for the AGL compiler.

Usage:
    python -m agl.cli compile path/to/Mission.agl -o /tmp/out
"""

from __future__ import annotations

import argparse
import sys

from .compiler import AGLCompiler
from .parser import AGLParseError


def main() -> None:
    parser = argparse.ArgumentParser(description="AGOS Language (AGL) compiler")
    sub = parser.add_subparsers(dest="command", required=True)

    compile_cmd = sub.add_parser("compile", help="compile a .agl file to Python + JSON Schema")
    compile_cmd.add_argument("source", help="path to a .agl file")
    compile_cmd.add_argument("-o", "--out", default=".", help="output directory")

    args = parser.parse_args()
    if args.command == "compile":
        try:
            compiler = AGLCompiler()
            compiled = compiler.compile_file(args.source, args.out)
        except AGLParseError as exc:
            print(f"AGL syntax error: {exc}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print(f"no such file: {args.source}", file=sys.stderr)
            sys.exit(1)
        print(f"compiled '{compiled.object_def.name}' -> {args.out}/"
              f"{compiled.object_def.name}.py, {args.out}/{compiled.object_def.name}.schema.json")


if __name__ == "__main__":
    main()
