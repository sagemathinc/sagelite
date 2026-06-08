from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "theta"


def run_theta() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("CSDP theta executable is missing from companion package")
    os.execv(os.fspath(executable), ["theta", *sys.argv[1:]])
    return 127


def theta() -> int:
    return run_theta()
