from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "lie"


def lie_command() -> Path:
    return executable_path()


def info_dir() -> Path:
    return Path(__file__).resolve().parent / "data" / "LiE"


def lie() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("lie executable is missing from companion package")
    os.execv(os.fspath(executable), ["lie", *sys.argv[1:]])
    return 127
