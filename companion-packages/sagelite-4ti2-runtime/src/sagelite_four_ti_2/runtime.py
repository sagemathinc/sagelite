from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = [
    "hilbert",
    "markov",
    "graver",
    "zsolve",
    "qsolve",
    "rays",
    "ppi",
    "circuits",
    "groebner",
]


def executable_path(program: str) -> str:
    return os.fspath(Path(__file__).resolve().parent / "data" / "bin" / program)


def executable_paths() -> dict[str, str]:
    return {program: executable_path(program) for program in PROGRAMS}


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not Path(executable).is_file():
        raise RuntimeError(f"4ti2 executable is missing from companion package: {program}")
    os.execv(executable, [program, *sys.argv[1:]])
    return 127


def _make_main(program: str):
    def main() -> int:
        return run_program(program)

    return main


for _program in PROGRAMS:
    globals()[_program] = _make_main(_program)
    globals()[f"{_program}_command"] = (lambda program: lambda: executable_path(program))(
        _program
    )
