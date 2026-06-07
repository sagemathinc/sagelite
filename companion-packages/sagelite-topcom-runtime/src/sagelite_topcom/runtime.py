from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = [
    "B_A",
    "B_A_center",
    "B_D",
    "checkregularity",
    "chiro2allfinetriangs",
    "chiro2alltriangs",
    "chiro2circuits",
    "chiro2cocircuits",
    "chiro2dual",
    "chiro2finetriang",
    "chiro2finetriangs",
    "chiro2mintriang",
    "chiro2nallfinetriangs",
    "chiro2nalltriangs",
    "chiro2nfinetriangs",
    "chiro2ntriangs",
    "chiro2placingtriang",
    "chiro2triangs",
    "cocircuits2facets",
    "cross",
    "cube",
    "cyclic",
    "hypersimplex",
    "lattice",
    "points2allfinetriangs",
    "points2alltriangs",
    "points2chiro",
    "points2facets",
    "points2finetriang",
    "points2finetriangs",
    "points2flips",
    "points2nallfinetriangs",
    "points2nalltriangs",
    "points2nfinetriangs",
    "points2nflips",
    "points2ntriangs",
    "points2placingtriang",
    "points2triangs",
    "points2volume",
    "santos_22_triang",
    "santos_dim4_triang",
    "santos_triang",
]


def executable_path(program: str) -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def executable_paths() -> dict[str, str]:
    return {program: os.fspath(executable_path(program)) for program in PROGRAMS}


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"TOPCOM executable is missing from companion package: {program}")

    env = os.environ.copy()
    libdir = executable.parent.parent / "lib"
    if libdir.is_dir():
        old_path = env.get("LD_LIBRARY_PATH")
        env["LD_LIBRARY_PATH"] = (
            os.fspath(libdir) if not old_path else f"{libdir}{os.pathsep}{old_path}"
        )
    os.execve(executable, [program, *sys.argv[1:]], env)
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
