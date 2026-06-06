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
    "hilbert",
    "markov",
    "graver",
    "zsolve",
    "qsolve",
    "rays",
    "ppi",
    "circuits",
    "groebner",
]
REQUIRED_PROGRAMS = ["hilbert", "zsolve", "qsolve", "groebner"]


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_4TI2_BINDIR", "FOURTITWO_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_bindir() -> Path:
    for bindir in _candidate_bindirs():
        if all(_program_path(bindir, program) for program in REQUIRED_PROGRAMS):
            return bindir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a 4ti2 executable directory containing "
        f"{', '.join(REQUIRED_PROGRAMS)}. Set SAGELITE_4TI2_BINDIR to the "
        f"Sage-built bin directory.\nSearched:\n  {searched}"
    )


def _program_path(bindir: Path, program: str) -> Path | None:
    for candidate in (bindir / program, bindir / f"4ti2-{program}"):
        if candidate.is_file():
            return candidate
    return None


class build_py(_build_py):
    def run(self):
        super().run()

        bindir = _find_bindir()
        target = Path(self.build_lib) / "sagelite_four_ti_2" / "data" / "bin"
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        for program in PROGRAMS:
            source = _program_path(bindir, program)
            if source is not None:
                shutil.copy2(source, target / program)


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_4TI2_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
