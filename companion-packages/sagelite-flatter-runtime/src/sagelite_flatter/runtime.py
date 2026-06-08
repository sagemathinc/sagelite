from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "flatter"


def run_flatter() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("flatter executable is missing from companion package")
    os.execv(os.fspath(executable), ["flatter", *sys.argv[1:]])
    return 127


def flatter() -> int:
    return run_flatter()
