from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "planarity"


def run_planarity() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("planarity executable is missing from companion package")
    os.execv(os.fspath(executable), ["planarity", *sys.argv[1:]])
    return 127


def planarity() -> int:
    return run_planarity()
