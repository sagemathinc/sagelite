from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = ["dot", "neato", "twopi"]


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def executable_path(program: str = "dot") -> Path:
    if program not in PROGRAMS:
        raise ValueError(f"unknown Graphviz program: {program}")
    return data_dir() / "bin" / program


def plugin_dir() -> Path:
    return data_dir() / "lib" / "graphviz"


def run_program(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"Graphviz executable is missing from companion package: {program}")

    env = os.environ.copy()
    libdir = data_dir() / "lib"
    old_library_path = env.get("LD_LIBRARY_PATH")
    env["LD_LIBRARY_PATH"] = (
        os.fspath(libdir)
        if not old_library_path
        else f"{libdir}{os.pathsep}{old_library_path}"
    )
    env["GV_PLUGIN_PATH"] = os.fspath(plugin_dir())

    os.execve(os.fspath(executable), [program, *sys.argv[1:]], env)
    return 127


def dot() -> int:
    return run_program("dot")


def neato() -> int:
    return run_program("neato")


def twopi() -> int:
    return run_program("twopi")


__all__ = [
    "dot",
    "executable_path",
    "neato",
    "plugin_dir",
    "run_program",
    "twopi",
]
