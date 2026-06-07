from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "buckygen"


def buckygen() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("buckygen executable is missing from companion package")
    os.execv(os.fspath(executable), ["buckygen", *sys.argv[1:]])
    return 127
