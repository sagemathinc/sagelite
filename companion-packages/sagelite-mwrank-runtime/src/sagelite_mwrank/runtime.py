from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "mwrank"


def mwrank_command() -> Path:
    return executable_path()


def run_mwrank() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("mwrank executable is missing from companion package")
    os.execv(os.fspath(executable), ["mwrank", *sys.argv[1:]])
    return 127


def mwrank() -> int:
    return run_mwrank()
