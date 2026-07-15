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
    for variable in ("SAGELITE_PLANARITY_BINDIR", "PLANARITY_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        candidate = bindir / "planarity"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a planarity executable. "
        "Set SAGELITE_PLANARITY_BINDIR to the Sage-built bin directory.\n"
        f"Searched:\n  {searched}"
    )


def _runtime_libraries(executable: Path) -> list[Path]:
    if sys.platform == "darwin":
        output = subprocess.run(
            ["otool", "-L", os.fspath(executable)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        return [
            Path(line.strip().split(" (", 1)[0])
            for line in output.splitlines()[1:]
            if Path(line.strip().split(" (", 1)[0]).name.startswith(
                "libplanarity"
            )
        ]

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
        if name.startswith("libplanarity") and path != "not":
            libraries.append(Path(path))
    return libraries


def _repair_macos_install_names(
    executable: Path, libraries: dict[Path, Path]
) -> None:
    if sys.platform != "darwin":
        return

    for source, bundled in libraries.items():
        subprocess.run(
            [
                "install_name_tool",
                "-change",
                os.fspath(source),
                f"@loader_path/../lib/{bundled.name}",
                os.fspath(executable),
            ],
            check=True,
        )
        subprocess.run(
            [
                "install_name_tool",
                "-id",
                f"@loader_path/{bundled.name}",
                os.fspath(bundled),
            ],
            check=True,
        )
    if shutil.which("codesign") is not None:
        for path in [*libraries.values(), executable]:
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(path)],
                check=True,
            )


class build_py(_build_py):
    def run(self):
        source = _find_executable()
        target = Path(self.build_lib) / "sagelite_planarity" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_planarity" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        real = target / "planarity-real"
        shutil.copy2(source, real)
        real.chmod(real.stat().st_mode | 0o200)
        wrapper = target / "planarity"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            'DYLD_LIBRARY_PATH="$HERE/../lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"\n'
            "export LD_LIBRARY_PATH\n"
            "export DYLD_LIBRARY_PATH\n"
            'exec "$HERE/planarity-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        libraries = {
            library: lib_target / library.name
            for library in _runtime_libraries(source)
        }
        for library, destination in libraries.items():
            shutil.copy2(library, destination)
            destination.chmod(destination.stat().st_mode | 0o200)

        _repair_macos_install_names(real, libraries)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_PLANARITY_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
