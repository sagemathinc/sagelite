from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "plantri"


def run_plantri() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("plantri executable is missing from companion package")
    os.execv(os.fspath(executable), ["plantri", *sys.argv[1:]])
    return 127


def plantri() -> int:
    return run_plantri()
