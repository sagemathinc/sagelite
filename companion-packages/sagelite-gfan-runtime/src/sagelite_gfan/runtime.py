from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = [
    "gfan",
    "gfan_bases",
    "gfan_buchberger",
    "gfan_combinerays",
    "gfan_doesidealcontain",
    "gfan_fancommonrefinement",
    "gfan_fanhomology",
    "gfan_fanisbalanced",
    "gfan_fanlink",
    "gfan_fanproduct",
    "gfan_fansubfan",
    "gfan_genericlinearchange",
    "gfan_groebnercone",
    "gfan_groebnerfan",
    "gfan_homogeneityspace",
    "gfan_homogenize",
    "gfan_initialforms",
    "gfan_interactive",
    "gfan_ismarkedgroebnerbasis",
    "gfan_krulldimension",
    "gfan_latticeideal",
    "gfan_leadingterms",
    "gfan_list",
    "gfan_markpolynomialset",
    "gfan_minkowskisum",
    "gfan_minors",
    "gfan_mixedvolume",
    "gfan_overintegers",
    "gfan_padic",
    "gfan_polynomialsetunion",
    "gfan_render",
    "gfan_renderstaircase",
    "gfan_resultantfan",
    "gfan_saturation",
    "gfan_secondaryfan",
    "gfan_stats",
    "gfan_substitute",
    "gfan_symmetries",
    "gfan_tolatex",
    "gfan_topolyhedralfan",
    "gfan_tropicalbasis",
    "gfan_tropicalbruteforce",
    "gfan_tropicalcurve",
    "gfan_tropicalevaluation",
    "gfan_tropicalfunction",
    "gfan_tropicalhypersurface",
    "gfan_tropicalintersection",
    "gfan_tropicallifting",
    "gfan_tropicallinearspace",
    "gfan_tropicalmultiplicity",
    "gfan_tropicalprevariety",
    "gfan_tropicalrank",
    "gfan_tropicalstartingcone",
    "gfan_tropicaltraverse",
    "gfan_tropicalweildivisor",
    "gfan_version",
]


def executable_path(program: str = "gfan") -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / program


def bin_prefix() -> str:
    return os.fspath(Path(__file__).resolve().parent / "data" / "bin") + os.sep


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"gfan executable is missing from companion package: {program}")
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def _make_main(program: str):
    def main() -> int:
        return run_program(program)

    return main


for _program in PROGRAMS:
    globals()[_program] = _make_main(_program)
