from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover - wheel is a build requirement
    _bdist_wheel = None


PROGRAMS = ("lrs", "lrsnash")


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_LRSLIB_BINDIR", "LRSLIB_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_programs() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for bindir in _candidate_bindirs():
        for program in PROGRAMS:
            candidate = bindir / program
            if candidate.is_file() and os.access(candidate, os.X_OK):
                found.setdefault(program, candidate.resolve())

    missing = [program for program in PROGRAMS if program not in found]
    if missing:
        searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
        raise RuntimeError(
            "could not find required lrslib executables "
            f"{', '.join(missing)}. Set SAGELITE_LRSLIB_BINDIR to the "
            f"Sage-built bin directory.\nSearched:\n  {searched}"
        )
    return found


RUNTIME_LIBRARY_PREFIXES = ("liblrs.so", "libflint.so", "libgmp.so", "libmpfr.so")


def _ldd_linked_libraries(path: Path) -> list[Path]:
    output = subprocess.run(
        ["ldd", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

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


def _darwin_load_paths(path: Path) -> list[str]:
    output = subprocess.run(
        ["otool", "-L", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [
        line.strip().split(" (", 1)[0]
        for line in output.splitlines()[1:]
    ]


def _darwin_linked_libraries(path: Path) -> list[Path]:
    libraries = []
    for dependency in _darwin_load_paths(path):
        if dependency.startswith(("@loader_path/", "@rpath/")):
            candidate = path.parent / dependency.split("/", 1)[1]
            if candidate.is_file():
                libraries.append(candidate)
            continue
        if not dependency.startswith("/"):
            continue
        if dependency.startswith(("/System/Library/", "/usr/lib/")):
            continue
        libraries.append(Path(dependency))
    return libraries


def _runtime_libraries(executables: list[Path]) -> list[Path]:
    libraries: dict[str, Path] = {}
    pending = list(executables)
    seen: set[Path] = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        linked = (
            _darwin_linked_libraries(path)
            if sys.platform == "darwin"
            else _ldd_linked_libraries(path)
        )
        for library in linked:
            if not library.is_file():
                raise RuntimeError(f"linked library does not exist: {library}")
            previous = libraries.setdefault(library.name, library)
            if previous.resolve() != library.resolve():
                raise RuntimeError(
                    "distinct linked libraries have the same basename: "
                    f"{previous}, {library}"
                )
            if previous.resolve() == library.resolve():
                pending.append(library)
    return sorted(libraries.values())


def _repair_macos_install_names(
    executables: list[Path], libraries: dict[Path, Path]
) -> None:
    if sys.platform != "darwin":
        return

    for bundled in libraries.values():
        subprocess.run(
            [
                "install_name_tool",
                "-id",
                f"@loader_path/{bundled.name}",
                os.fspath(bundled),
            ],
            check=True,
        )

    for binary in [*executables, *libraries.values()]:
        linked = set(_darwin_load_paths(binary))
        relative_libdir = "../lib" if binary in executables else "."
        for source, bundled in libraries.items():
            original = os.fspath(source)
            candidates = (
                original,
                f"@rpath/{source.name}",
                f"@loader_path/{source.name}",
            )
            load_path = next((item for item in candidates if item in linked), None)
            if load_path is None:
                continue
            replacement = f"@loader_path/{relative_libdir}/{bundled.name}"
            subprocess.run(
                [
                    "install_name_tool",
                    "-change",
                    load_path,
                    replacement,
                    os.fspath(binary),
                ],
                check=True,
            )

    if shutil.which("codesign") is not None:
        for binary in [*libraries.values(), *executables]:
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(binary)],
                check=True,
            )


class build_py(_build_py):
    def run(self):
        programs = _find_programs()
        target = Path(self.build_lib) / "sagelite_lrslib" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_lrslib" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        copied_programs = []
        for program, source in programs.items():
            real = target / f"{program}-real"
            shutil.copy2(source, real)
            real.chmod(real.stat().st_mode | 0o200)
            copied_programs.append(real)
            wrapper = target / program
            wrapper.write_text(
                "#!/bin/sh\n"
                'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
                'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
                'DYLD_LIBRARY_PATH="$HERE/../lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"\n'
                "export LD_LIBRARY_PATH DYLD_LIBRARY_PATH\n"
                f'exec "$HERE/{program}-real" "$@"\n'
            )
            wrapper.chmod(0o755)

        libraries: dict[Path, Path] = {}
        for library in _runtime_libraries(list(programs.values())):
            destination = lib_target / library.name
            shutil.copy2(library, destination)
            destination.chmod(destination.stat().st_mode | 0o200)
            libraries[library] = destination

        _repair_macos_install_names(copied_programs, libraries)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_LRSLIB_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
