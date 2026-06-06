from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = ["cu2", "cubex", "dikcube", "mcube", "optimal", "size222"]


def bin_prefix() -> str:
    return os.fspath(Path(__file__).resolve().parent / "data" / "bin") + os.sep


def executable_path(program: str) -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(
            f"Rubiks executable is missing from companion package: {program}"
        )
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def _make_main(program: str):
    def main() -> int:
        return run_program(program)

    return main


for _program in PROGRAMS:
    globals()[_program] = _make_main(_program)
