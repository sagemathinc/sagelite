from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "tachyon"


def run_tachyon() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("tachyon executable is missing from companion package")
    os.execv(os.fspath(executable), ["tachyon", *sys.argv[1:]])
    return 127


def tachyon() -> int:
    return run_tachyon()
