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
    "libmpfr.so",
)


def _linked_libraries(path: Path) -> list[Path]:
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


def _runtime_libraries(executable: Path) -> list[Path]:
    libraries: dict[str, Path] = {}
    pending = [executable]
    seen: set[Path] = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        for library in _linked_libraries(path):
            previous = libraries.setdefault(library.name, library)
            if previous == library:
                pending.append(library)
    return sorted(libraries.values())


class build_py(_build_py):
    def run(self):
        source = _find_executable()
        target = Path(self.build_lib) / "sagelite_msolve" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_msolve" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source, target / "msolve-real")
        wrapper = target / "msolve"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            "export LD_LIBRARY_PATH\n"
            'exec "$HERE/msolve-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        for library in _runtime_libraries(source):
            shutil.copy2(library, lib_target / library.name)

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
