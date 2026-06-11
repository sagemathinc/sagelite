from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "pdftocairo"


def run_pdftocairo() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("pdftocairo executable is missing from companion package")
    os.execv(os.fspath(executable), ["pdftocairo", *sys.argv[1:]])
    return 127


def pdftocairo() -> int:
    return run_pdftocairo()
