from __future__ import annotations

import os
import sys
from pathlib import Path


def executable_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin" / "ecm"


def ecm_command() -> Path:
    return executable_path()


def run_ecm() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("ecm executable is missing from companion package")
    os.execv(os.fspath(executable), ["ecm", *sys.argv[1:]])
    return 127


def ecm() -> int:
    return run_ecm()
