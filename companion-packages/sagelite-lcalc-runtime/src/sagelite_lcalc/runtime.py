from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "lcalc"


def lcalc_command() -> Path:
    return executable_path()


def lcalc() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("lcalc executable is missing from companion package")
    os.execv(os.fspath(executable), ["lcalc", *sys.argv[1:]])
    return 127
