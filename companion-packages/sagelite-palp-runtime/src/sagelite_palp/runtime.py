from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = [
    f"{program}{suffix}.x"
    for program in ("poly", "class", "nef", "cws")
    for suffix in ("", "-4d", "-5d", "-6d", "-11d")
]


def bin_prefix() -> str:
    """
    Return the bundled PALP executable directory with a trailing separator.
    """
    return os.fspath(Path(__file__).resolve().parent / "data" / "bin") + os.sep


def executable_path(program: str) -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"PALP executable is missing from companion package: {program}")
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def _entry_point_name(program: str) -> str:
    return program.replace("-", "_").replace(".", "_")


def _make_main(program: str):
    def main() -> int:
        return run_program(program)

    return main


for _program in PROGRAMS:
    globals()[_entry_point_name(_program)] = _make_main(_program)
