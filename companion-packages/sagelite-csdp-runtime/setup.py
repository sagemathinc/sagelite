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


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_CSDP_BINDIR", "CSDP_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _candidate_libdirs(executable: Path) -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_CSDP_LIBDIR", "CSDP_LIBDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "lib")
    dirs.append(executable.parent.parent / "lib")
    dirs.extend([Path("/usr/lib"), Path("/usr/local/lib")])
    dirs.extend(Path("/usr/lib").glob("*-linux-gnu"))
    return dirs


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        for executable in ("theta", "csdp-theta"):
            candidate = bindir / executable
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find the CSDP theta executable. "
        "Set SAGELITE_CSDP_BINDIR to the Sage-built bin directory.\n"
        f"Searched:\n  {searched}"
    )


def _ldd_libraries(path: Path) -> list[tuple[str, Path | None]]:
    output = subprocess.run(
        ["ldd", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries: list[tuple[str, Path | None]] = []
    for line in output.splitlines():
        if "=>" not in line:
            continue
        name, rest = line.split("=>", 1)
        name = name.strip()
        path = rest.strip().split(maxsplit=1)[0]
        if path == "not":
            libraries.append((name, None))
        else:
            libraries.append((name, Path(path)))
    return libraries


def _find_library(name: str, executable: Path) -> Path:
    for directory in _candidate_libdirs(executable):
        for candidate in (directory / name, *directory.glob(f"{name}*")):
            if candidate.is_file() or candidate.is_symlink():
                return candidate
    searched = "\n  ".join(
        os.fspath(directory / name) for directory in _candidate_libdirs(executable)
    )
    raise RuntimeError(
        f"could not find CSDP runtime library {name}. "
        "Set SAGELITE_CSDP_LIBDIR to the Sage-built lib directory.\n"
        f"Searched:\n  {searched}"
    )


def _runtime_libraries(executable: Path) -> list[Path]:
    prefixes = (
        "libsdp",
        "libgmp",
        "libblas",
        "liblapack",
        "libopenblas",
        "libgfortran",
        "libquadmath",
    )
    libraries: dict[str, Path] = {}
    pending = [executable]
    seen = set()
    while pending:
        path = pending.pop()
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        for name, library in _ldd_libraries(resolved):
            if not name.startswith(prefixes):
                continue
            if library is None:
                library = _find_library(name, executable)
            if library.name not in libraries:
                libraries[library.name] = library
                pending.append(library)
    return sorted(libraries.values())


class build_py(_build_py):
    def run(self):
        source = _find_executable()
        target = Path(self.build_lib) / "sagelite_csdp" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_csdp" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source, target / "theta-real")
        wrapper = target / "theta"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            "export LD_LIBRARY_PATH\n"
            'exec "$HERE/theta-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        libraries: dict[str, Path] = {}
        for library in _runtime_libraries(source):
            libraries.setdefault(library.name, library)
        for library in libraries.values():
            shutil.copy2(library, lib_target / library.name)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_CSDP_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
