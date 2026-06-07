from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "sympow"


def sympow_command() -> Path:
    return executable_path()


def run_sympow() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("sympow executable is missing from companion package")
    os.execv(os.fspath(executable), ["sympow", *sys.argv[1:]])
    return 127


def sympow() -> int:
    return run_sympow()
