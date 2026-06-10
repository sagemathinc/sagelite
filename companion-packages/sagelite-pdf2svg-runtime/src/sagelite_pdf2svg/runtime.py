from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "pdf2svg"


def run_pdf2svg() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("pdf2svg executable is missing from companion package")
    os.execv(os.fspath(executable), ["pdf2svg", *sys.argv[1:]])
    return 127


def pdf2svg() -> int:
    return run_pdf2svg()
