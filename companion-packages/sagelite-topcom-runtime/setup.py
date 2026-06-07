from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover - wheel is a build requirement
    _bdist_wheel = None


PROGRAMS = [
    "B_A",
    "B_A_center",
    "B_D",
    "checkregularity",
    "chiro2allfinetriangs",
    "chiro2alltriangs",
    "chiro2circuits",
    "chiro2cocircuits",
    "chiro2dual",
    "chiro2finetriang",
    "chiro2finetriangs",
    "chiro2mintriang",
    "chiro2nallfinetriangs",
    "chiro2nalltriangs",
    "chiro2nfinetriangs",
    "chiro2ntriangs",
    "chiro2placingtriang",
    "chiro2triangs",
    "cocircuits2facets",
    "cross",
    "cube",
    "cyclic",
    "hypersimplex",
    "lattice",
    "points2allfinetriangs",
    "points2alltriangs",
    "points2chiro",
    "points2facets",
    "points2finetriang",
    "points2finetriangs",
    "points2flips",
    "points2nallfinetriangs",
    "points2nalltriangs",
    "points2nfinetriangs",
    "points2nflips",
    "points2ntriangs",
    "points2placingtriang",
    "points2triangs",
    "points2volume",
    "santos_22_triang",
    "santos_dim4_triang",
    "santos_triang",
]
REQUIRED_PROGRAMS = ["points2allfinetriangs", "points2placingtriang"]


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_TOPCOM_BINDIR", "TOPCOM_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _program_path(bindir: Path, program: str) -> Path | None:
    for candidate in (bindir / program, bindir / f"topcom-{program}"):
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def _find_bindir() -> Path:
    for bindir in _candidate_bindirs():
        if all(_program_path(bindir, program) for program in REQUIRED_PROGRAMS):
            return bindir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a TOPCOM executable directory containing "
        f"{', '.join(REQUIRED_PROGRAMS)}. Set SAGELITE_TOPCOM_BINDIR to the "
        f"Sage-built bin directory.\nSearched:\n  {searched}"
    )


def _runtime_libraries(executables: list[Path]) -> list[Path]:
    prefixes = (
        "libCHECKREG",
        "libTOPCOM",
        "libcddgmp",
        "libgmp",
        "libgmpxx",
    )
    libraries: dict[str, Path] = {}
    for executable in executables:
        output = subprocess.run(
            ["ldd", os.fspath(executable)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        for line in output.splitlines():
            if "=>" not in line:
                continue
            name, rest = line.split("=>", 1)
            name = name.strip()
            path = rest.strip().split(maxsplit=1)[0]
            if name.startswith(prefixes) and path != "not":
                libraries[name] = Path(path)
    return list(libraries.values())


class build_py(_build_py):
    def run(self):
        super().run()

        bindir = _find_bindir()
        target = Path(self.build_lib) / "sagelite_topcom" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_topcom" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        copied = []
        for program in PROGRAMS:
            source = _program_path(bindir, program)
            if source is None:
                continue
            resolved = source.resolve()
            shutil.copy2(resolved, target / program)
            copied.append(resolved)

        for library in _runtime_libraries(copied):
            shutil.copy2(library, lib_target / library.name)


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_TOPCOM_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
