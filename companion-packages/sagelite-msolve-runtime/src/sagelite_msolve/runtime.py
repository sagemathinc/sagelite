from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "msolve"


def run_msolve() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("msolve executable is missing from companion package")
    os.execv(os.fspath(executable), ["msolve", *sys.argv[1:]])
    return 127


def msolve() -> int:
    return run_msolve()
