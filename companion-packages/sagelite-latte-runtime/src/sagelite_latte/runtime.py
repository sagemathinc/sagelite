from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path(program: str) -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def bin_prefix() -> str:
    return os.fspath(Path(__file__).resolve().parent / "data" / "bin") + os.sep


def count_command() -> str:
    return os.fspath(executable_path("count"))


def integrate_command() -> str:
    return os.fspath(executable_path("integrate"))


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"LattE executable is missing from companion package: {program}")
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def count() -> int:
    return run_program("count")


def integrate() -> int:
    return run_program("integrate")


__all__ = [
    "bin_prefix",
    "count",
    "count_command",
    "integrate",
    "integrate_command",
]
