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


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_MSOLVE_BINDIR", "MSOLVE_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        candidate = bindir / "msolve"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find an msolve executable. Set SAGELITE_MSOLVE_BINDIR to "
        f"the Sage-built bin directory.\nSearched:\n  {searched}"
    )


RUNTIME_LIBRARY_PREFIXES = (
    "libmsolve.so",
    "libneogb.so",
    "libflint.so",
    "libgmp.so",
    "libgomp.so",
    "libmpfr.so",
)


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


def _runtime_libraries(executable: Path) -> list[Path]:
    libraries: dict[str, Path] = {}
    pending = [executable]
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
    executable: Path, libraries: dict[Path, Path]
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

    for binary in [executable, *libraries.values()]:
        linked = set(_darwin_load_paths(binary))
        relative_libdir = "../lib" if binary == executable else "."
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
        for binary in [*libraries.values(), executable]:
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(binary)],
                check=True,
            )


class build_py(_build_py):
    def run(self):
        source = _find_executable()
        target = Path(self.build_lib) / "sagelite_msolve" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_msolve" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        real = target / "msolve-real"
        shutil.copy2(source, real)
        real.chmod(real.stat().st_mode | 0o200)
        wrapper = target / "msolve"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            'DYLD_LIBRARY_PATH="$HERE/../lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"\n'
            "export LD_LIBRARY_PATH DYLD_LIBRARY_PATH\n"
            'exec "$HERE/msolve-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        libraries: dict[Path, Path] = {}
        for library in _runtime_libraries(source):
            destination = lib_target / library.name
            shutil.copy2(library, destination)
            destination.chmod(destination.stat().st_mode | 0o200)
            libraries[library] = destination

        _repair_macos_install_names(real, libraries)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_MSOLVE_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
