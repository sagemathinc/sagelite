from __future__ import annotations

import os
from pathlib import Path
import sys


def jmol_dir() -> Path:
    return Path(__file__).resolve().parent / "data" / "jmol"


def jmol_jar_path() -> Path:
    return jmol_dir() / "Jmol.jar"


def jmol_data_jar_path() -> Path:
    return jmol_dir() / "JmolData.jar"


def run_jmol() -> int:
    jar = jmol_jar_path()
    if not jar.is_file():
        raise RuntimeError("Jmol.jar is missing from companion package")
    if not jmol_data_jar_path().is_file():
        raise RuntimeError("JmolData.jar is missing from companion package")
    os.execvp("java", ["java", "-Xmx512m", "-jar", os.fspath(jar), *sys.argv[1:]])
    return 127


def jmol() -> int:
    return run_jmol()
