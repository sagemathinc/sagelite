from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = ["glucose", "glucose-syrup"]


def bin_prefix() -> str:
    """
    Return the bundled Glucose executable directory with a trailing separator.
    """
    return os.fspath(Path(__file__).resolve().parent / "data" / "bin") + os.sep


def executable_path(program: str = "glucose") -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(
            f"Glucose executable is missing from companion package: {program}"
        )
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def glucose() -> int:
    return run_program("glucose")


def glucose_syrup() -> int:
    return run_program("glucose-syrup")
