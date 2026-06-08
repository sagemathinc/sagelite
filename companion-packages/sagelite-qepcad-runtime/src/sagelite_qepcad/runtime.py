from __future__ import annotations

import os
from pathlib import Path
import sys


def root_dir() -> Path:
    return Path(__file__).resolve().parent / "data" / "root"


def executable_path() -> Path:
    return root_dir() / "bin" / "qepcad"


def help_path() -> Path:
    return root_dir() / "share" / "qepcad" / "qepcad.help"


def default_qepcadrc_path() -> Path:
    return root_dir() / "etc" / "default.qepcadrc"


def run_qepcad() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("QEPCAD executable is missing from companion package")
    os.environ.setdefault("qe", os.fspath(root_dir()))
    os.execv(os.fspath(executable), ["qepcad", *sys.argv[1:]])
    return 127


def qepcad() -> int:
    return run_qepcad()
