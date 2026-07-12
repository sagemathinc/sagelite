from __future__ import annotations

import os
from pathlib import Path
import sys


PROGRAMS = ["dot", "neato", "twopi", "fdp", "circo"]


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def bin_dir() -> Path:
    return data_dir() / "bin"


def _ensure_executable(path: Path) -> Path:
    """Restore execute bits stripped from wheel package data."""
    if path.is_file() and not os.access(path, os.X_OK):
        try:
            path.chmod(path.stat().st_mode | 0o111)
        except OSError:
            # A read-only installation will report the normal execution error
            # from ``run_program`` instead of failing during path discovery.
            pass
    return path


def executable_path(program: str = "dot") -> Path:
    if program not in PROGRAMS:
        raise ValueError(f"unknown Graphviz program: {program}")
    root = bin_dir()
    _ensure_executable(root / f"{program}-real")
    return _ensure_executable(root / program)


def library_dir() -> Path:
    return data_dir() / "lib"


def plugin_dir() -> Path:
    return library_dir() / "graphviz"


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


def fdp() -> int:
    return run_program("fdp")


def circo() -> int:
    return run_program("circo")


__all__ = [
    "circo",
    "dot",
    "bin_dir",
    "executable_path",
    "fdp",
    "library_dir",
    "neato",
    "plugin_dir",
    "run_program",
    "twopi",
]
