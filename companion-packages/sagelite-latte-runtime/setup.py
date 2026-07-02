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


PROGRAMS = {
    "count": ("count", "latte-count"),
    "integrate": ("integrate", "latte-integrate"),
}
RUNTIME_LIBRARY_PREFIXES = (
    "libLiDIA",
    "lib4ti2",
    "libcdd",
    "libflint",
    "libgf2x",
    "libglpk",
    "libgmp",
    "liblatte",
    "libmpfr",
    "libntl",
    "libzsolve",
)


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_LATTE_BINDIR", "LATTE_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _program_path(bindir: Path, program: str) -> Path | None:
    for executable_name in PROGRAMS[program]:
        candidate = bindir / executable_name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def _find_bindir() -> Path:
    for bindir in _candidate_bindirs():
        if all(_program_path(bindir, program) for program in PROGRAMS):
            return bindir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a LattE executable directory containing count and "
        "integrate, or the distro-prefixed latte-count and latte-integrate. "
        "Set SAGELITE_LATTE_BINDIR to the Sage-built or system package bin "
        f"directory.\nSearched:\n  {searched}"
    )


def _runtime_libraries(executable: Path) -> list[Path]:
    output = subprocess.run(
        ["ldd", os.fspath(executable)],
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


def _fix_macos_install_names(executables: list[Path], libraries: dict[Path, Path]) -> None:
    if sys.platform != "darwin":
        return

    for executable in executables:
        _add_rpath(executable, "@loader_path/../lib")
    for library in libraries.values():
        _install_name_tool("-id", f"@rpath/{library.name}", os.fspath(library))
        _add_rpath(library, "@loader_path")

    machos = [*executables, *libraries.values()]
    for mach_o in machos:
        for original, bundled in libraries.items():
            _install_name_tool(
                "-change",
                os.fspath(original),
                f"@rpath/{bundled.name}",
                os.fspath(mach_o),
            )
        _codesign_darwin(mach_o)


class build_py(_build_py):
    def run(self):
        bindir = _find_bindir()
        target = Path(self.build_lib) / "sagelite_latte" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_latte" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        executables = []
        libraries = {}
        for program in PROGRAMS:
            source = _program_path(bindir, program)
            if source is None:
                raise RuntimeError(f"{program} executable disappeared from {bindir}")

            real = target / f"{program}-real"
            shutil.copy2(source.resolve(), real)
            real.chmod(real.stat().st_mode | 0o200)
            executables.append(real)
            for library in _runtime_libraries(source.resolve()):
                libraries.setdefault(library, lib_target / library.name)

            wrapper = target / program
            wrapper.write_text(
                "#!/usr/bin/env bash\n"
                'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
                'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
                'DYLD_LIBRARY_PATH="$HERE/../lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"\n'
                "export LD_LIBRARY_PATH\n"
                "export DYLD_LIBRARY_PATH\n"
                f'exec -a {program} "$HERE/{program}-real" "$@"\n'
            )
            wrapper.chmod(0o755)

        for library, destination in libraries.items():
            shutil.copy2(library, destination)
            destination.chmod(destination.stat().st_mode | 0o200)

        _fix_macos_install_names(executables, libraries)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_LATTE_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
