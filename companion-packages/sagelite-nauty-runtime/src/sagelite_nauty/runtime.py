from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = [
    "addedgeg",
    "addptg",
    "amtog",
    "ancestorg",
    "assembleg",
    "biplabg",
    "catg",
    "complg",
    "converseg",
    "copyg",
    "countg",
    "countneg",
    "cubhamg",
    "deledgeg",
    "delptg",
    "dimacs2g",
    "directg",
    "dreadnaut",
    "dretodot",
    "dretog",
    "edgetransg",
    "genbg",
    "genbgL",
    "geng",
    "gengL",
    "genktreeg",
    "genposetg",
    "genquarticg",
    "genrang",
    "genspecialg",
    "gentourng",
    "gentreeg",
    "hamheuristic",
    "labelg",
    "linegraphg",
    "listg",
    "multig",
    "nbrhoodg",
    "newedgeg",
    "NRswitchg",
    "pickg",
    "planarg",
    "productg",
    "ranlabg",
    "ransubg",
    "shortg",
    "showg",
    "subdivideg",
    "twohamg",
    "underlyingg",
    "uniqg",
    "vcolg",
    "watercluster2",
]


def executable_path(program: str) -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"nauty executable is missing from companion package: {program}")
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def _make_main(program: str):
    def main() -> int:
        return run_program(program)

    return main


for _program in PROGRAMS:
    globals()[_program] = _make_main(_program)
