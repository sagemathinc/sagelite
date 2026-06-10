from __future__ import annotations

import os
from pathlib import Path
import sys


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def executable_path() -> Path:
    return data_dir() / "bin" / "info"


def info_dir() -> Path:
    return data_dir() / "share" / "info"


def info() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("info executable is missing from companion package")
    os.execv(os.fspath(executable), ["info", *sys.argv[1:]])
    return 127
