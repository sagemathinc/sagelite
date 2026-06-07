from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover - wheel is a build requirement
    _bdist_wheel = None


PROGRAMS = [
    f"{program}{suffix}.x"
    for program in ("poly", "class", "nef", "cws")
    for suffix in ("", "-4d", "-5d", "-6d", "-11d")
]
REQUIRED_PROGRAMS = PROGRAMS


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_PALP_BINDIR", "PALP_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_bindir() -> Path:
    for bindir in _candidate_bindirs():
        if all((bindir / program).is_file() for program in REQUIRED_PROGRAMS):
            return bindir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a PALP executable directory containing "
        f"{', '.join(REQUIRED_PROGRAMS)}. Set SAGELITE_PALP_BINDIR to the "
        f"Sage-built bin directory.\nSearched:\n  {searched}"
    )


class build_py(_build_py):
    def run(self):
        bindir = _find_bindir()
        target = Path(self.build_lib) / "sagelite_palp" / "data" / "bin"
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        for program in PROGRAMS:
            shutil.copy2(bindir / program, target / program)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_PALP_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
