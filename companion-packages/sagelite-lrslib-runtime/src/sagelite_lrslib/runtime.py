from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path(program: str = "lrs") -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def lrs_command() -> Path:
    return executable_path("lrs")


def lrsnash_command() -> Path:
    return executable_path("lrsnash")


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"lrslib executable is missing from companion package: {program}")
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def lrs() -> int:
    return run_program("lrs")


def lrsnash() -> int:
    return run_program("lrsnash")
