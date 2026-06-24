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
RUNTIME_LIBRARY_PREFIXES = (
    "lib4ti2",
    "libcircuits",
    "libgmp",
    "libgmpxx",
    "libgraver",
    "libgroebner",
    "libhilbert",
    "libmarkov",
    "libppi",
    "libqsolve",
    "librays",
    "libzsolve",
)


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_4TI2_BINDIR", "FOURTITWO_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _candidate_libexecdirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_4TI2_LIBEXECDIR", "FOURTITWO_LIBEXECDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "libexec" / "4ti2" / "bin")
    dirs.extend(
        [
            Path("/usr/libexec/x86_64-linux-gnu/4ti2/bin"),
            Path("/usr/libexec/aarch64-linux-gnu/4ti2/bin"),
            Path("/usr/libexec/4ti2/bin"),
            Path("/usr/local/libexec/4ti2/bin"),
        ]
    )
    return dirs


def _candidate_libdirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_4TI2_LIBDIR", "FOURTITWO_LIBDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "lib")
    for bindir in _candidate_bindirs():
        dirs.append(bindir.parent / "lib")
        dirs.append(bindir.parent / "lib64")
    dirs.extend([Path("/usr/lib64"), Path("/usr/lib"), Path("/usr/local/lib")])
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


def _find_libexecdir() -> Path | None:
    for libexecdir in _candidate_libexecdirs():
        if (libexecdir / "4ti2gmp").is_file() or (libexecdir / "4ti2int64").is_file():
            return libexecdir.resolve()
    return None


def _linked_libraries(path: Path) -> list[Path]:
    try:
        output = subprocess.run(
            ["ldd", os.fspath(path)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except subprocess.CalledProcessError:
        return []

    libraries = []
    for line in output.splitlines():
        if "=>" not in line:
            continue
        name, rest = line.split("=>", 1)
        name = name.strip()
        path = rest.strip().split(maxsplit=1)[0]
        if name.startswith(RUNTIME_LIBRARY_PREFIXES) and path != "not":
            libraries.append(Path(path))
    return libraries


def _runtime_libraries(executables: list[Path]) -> list[Path]:
    libraries: dict[str, Path] = {}
    pending = list(executables)
    seen: set[Path] = set()
    for libdir in _candidate_libdirs():
        if not libdir.is_dir():
            continue
        for prefix in RUNTIME_LIBRARY_PREFIXES:
            for library in libdir.glob(f"{prefix}*.so*"):
                if library.is_file() or library.is_symlink():
                    pending.append(library.resolve())

    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        if path.name.startswith(RUNTIME_LIBRARY_PREFIXES):
            libraries.setdefault(path.name, path)
        for library in _linked_libraries(path):
            previous = libraries.setdefault(library.name, library)
            if previous == library:
                pending.append(library)
    return sorted(libraries.values())


class build_py(_build_py):
    def run(self):
        bindir = _find_bindir()
        target = Path(self.build_lib) / "sagelite_four_ti_2" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_four_ti_2" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)
        executables = []
        for program in PROGRAMS:
            source = _program_path(bindir, program)
            if source is not None:
                shutil.copy2(source, target / program)
                executables.append(source.resolve())
        for source in bindir.glob("4ti2-*"):
            if source.is_file():
                shutil.copy2(source, target / source.name)
                executables.append(source.resolve())
        libexecdir = _find_libexecdir()
        if libexecdir is not None:
            for source in libexecdir.glob("4ti2*"):
                if source.is_file():
                    shutil.copy2(source, target / source.name)
                    executables.append(source.resolve())
        for library in _runtime_libraries(executables):
            shutil.copy2(library, lib_target / library.name)

        super().run()


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
