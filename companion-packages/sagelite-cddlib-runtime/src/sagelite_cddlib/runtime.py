from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path(program: str = "cddexec_gmp") -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"cddlib executable is missing from companion package: {program}")
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def cddexec() -> int:
    return run_program("cddexec")


def cddexec_gmp() -> int:
    return run_program("cddexec_gmp")


def redcheck_gmp() -> int:
    return run_program("redcheck_gmp")


def scdd() -> int:
    return run_program("scdd")


def scdd_gmp() -> int:
    return run_program("scdd_gmp")
