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
    for variable in ("SAGELITE_FLATTER_BINDIR", "FLATTER_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        candidate = bindir / "flatter"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a flatter executable. Set SAGELITE_FLATTER_BINDIR to "
        f"the Sage-built bin directory.\nSearched:\n  {searched}"
    )


def _runtime_libraries(executable: Path) -> list[Path]:
    if sys.platform == "darwin":
        return _darwin_runtime_libraries(executable)

    output = subprocess.run(
        ["ldd", os.fspath(executable)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries = []
    prefixes = (
        "libflatter.so",
        "libflatter.dylib",
        "libfplll.so",
        "libfplll.",
        "libgfortran.so",
        "libgfortran.",
        "libgomp.so",
        "libgomp.",
        "libopenblas.so",
        "libopenblas.",
        "libgmp.so",
        "libgmp.",
        "libmpfr.so",
        "libmpfr.",
        "libquadmath.so",
        "libquadmath.",
        "libqd.so",
        "libqd.",
        "libomp.dylib",
    )
    for line in output.splitlines():
        if "=>" not in line:
            continue
        name, rest = line.split("=>", 1)
        name = name.strip()
        path = rest.strip().split(maxsplit=1)[0]
        if name.startswith(prefixes) and path != "not":
            libraries.append(Path(path))
    return libraries


def _darwin_linked_libraries(path: Path) -> list[Path]:
    output = subprocess.run(
        ["otool", "-L", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries = []
    for line in output.splitlines()[1:]:
        dependency = line.strip().split(" (", 1)[0]
        if not dependency.startswith("/"):
            continue
        if dependency.startswith(("/System/Library/", "/usr/lib/")):
            continue
        libraries.append(Path(dependency))
    return libraries


def _darwin_runtime_libraries(executable: Path) -> list[Path]:
    """Return the complete non-system dylib closure for *executable*."""
    pending = _darwin_linked_libraries(executable)
    libraries: dict[Path, None] = {}
    while pending:
        library = pending.pop()
        if library in libraries:
            continue
        if not library.is_file():
            raise RuntimeError(f"linked library does not exist: {library}")
        libraries[library] = None
        pending.extend(_darwin_linked_libraries(library))
    return list(libraries)


def _install_name_tool(*args: str) -> None:
    subprocess.run(["install_name_tool", *args], check=True)


def _add_rpath(binary: Path, rpath: str) -> None:
    result = subprocess.run(
        ["install_name_tool", "-add_rpath", rpath, os.fspath(binary)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 and "would duplicate path" not in result.stderr:
        result.check_returncode()


def _codesign_darwin(path: Path) -> None:
    if sys.platform != "darwin" or shutil.which("codesign") is None:
        return
    subprocess.run(["codesign", "--force", "--sign", "-", os.fspath(path)], check=True)


def _fix_macos_install_names(executable: Path, libraries: dict[Path, Path]) -> None:
    if sys.platform != "darwin":
        return

    _add_rpath(executable, "@loader_path/../lib")
    for library in libraries.values():
        _install_name_tool("-id", f"@rpath/{library.name}", os.fspath(library))
        _add_rpath(library, "@loader_path")

    machos = [executable, *libraries.values()]
    for mach_o in machos:
        for original, bundled in libraries.items():
            if os.fspath(original) in {
                os.fspath(path) for path in _darwin_linked_libraries(mach_o)
            }:
                _install_name_tool(
                    "-change",
                    os.fspath(original),
                    f"@rpath/{bundled.name}",
                    os.fspath(mach_o),
                )
        _codesign_darwin(mach_o)


class build_py(_build_py):
    def run(self):
        source = _find_executable()
        target = Path(self.build_lib) / "sagelite_flatter" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_flatter" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        real = target / "flatter-real"
        shutil.copy2(source, real)
        real.chmod(real.stat().st_mode | 0o200)
        wrapper = target / "flatter"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            'DYLD_LIBRARY_PATH="$HERE/../lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"\n'
            "export LD_LIBRARY_PATH\n"
            "export DYLD_LIBRARY_PATH\n"
            'exec "$HERE/flatter-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        libraries = {}
        for library in _runtime_libraries(source):
            libraries.setdefault(library, lib_target / library.name)

        for library, destination in libraries.items():
            shutil.copy2(library, destination)
            destination.chmod(destination.stat().st_mode | 0o200)

        _fix_macos_install_names(real, libraries)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_FLATTER_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
