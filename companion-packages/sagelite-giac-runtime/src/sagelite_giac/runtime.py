from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "giac"


def giac_command() -> Path:
    return executable_path()


def giac() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("giac executable is missing from companion package")
    os.execv(os.fspath(executable), ["giac", *sys.argv[1:]])
    return 127
