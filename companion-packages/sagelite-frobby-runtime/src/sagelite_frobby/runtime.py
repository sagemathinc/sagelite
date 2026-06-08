from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "frobby"


def frobby() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("frobby executable is missing from companion package")
    os.execv(os.fspath(executable), ["frobby", *sys.argv[1:]])
    return 127
