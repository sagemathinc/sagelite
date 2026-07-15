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
    for variable in ("SAGELITE_LIE_BINDIR", "LIE_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _candidate_info_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_LIE_INFO_DIR", "LIE_INFO_DIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "lib" / "LiE")
    dirs.extend(
        [
            Path("/usr/lib/LiE"),
            Path("/usr/lib/lie"),
            Path("/usr/local/lib/LiE"),
            Path("/usr/local/lib/lie"),
        ]
    )
    return dirs


def _looks_like_info_dir(path: Path) -> bool:
    return (path / "INFO.0").is_file() and (path / "INFO.3").is_file()


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        command = bindir / "lie"
        if command.is_file() and os.access(command, os.X_OK):
            return command.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a lie executable. Set SAGELITE_LIE_BINDIR to the "
        f"Sage-built bin directory.\nSearched:\n  {searched}"
    )


def _find_info_dir() -> Path:
    for path in _candidate_info_dirs():
        if _looks_like_info_dir(path):
            return path.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_info_dirs())
    raise RuntimeError(
        "could not find a LiE info directory containing INFO.0 and INFO.3. "
        f"Set SAGELITE_LIE_INFO_DIR.\nSearched:\n  {searched}"
    )


def _write_lie_command(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """#!/bin/sh
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PREFIX=$(dirname "$HERE")
LD="${LIE_INFO_DIR:-$PREFIX/LiE}"
exec "$LD/Lie.exe" initfile "$LD" "$@"
""",
    )
    path.chmod(0o755)


def _macos_runtime_libraries(executable: Path) -> list[Path]:
    if sys.platform != "darwin":
        return []

    output = subprocess.run(
        ["otool", "-L", os.fspath(executable)],
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


def _bundle_macos_runtime(executable: Path, target: Path) -> None:
    libraries = _macos_runtime_libraries(executable)
    if not libraries:
        return

    target.mkdir(parents=True, exist_ok=True)
    bundled = {}
    for library in libraries:
        destination = target / library.name
        shutil.copy2(library, destination)
        destination.chmod(destination.stat().st_mode | 0o200)
        bundled[library] = destination

    executable.chmod(executable.stat().st_mode | 0o200)
    for library, destination in bundled.items():
        subprocess.run(
            [
                "install_name_tool",
                "-change",
                os.fspath(library),
                f"@loader_path/lib/{destination.name}",
                os.fspath(executable),
            ],
            check=True,
        )
        subprocess.run(
            [
                "install_name_tool",
                "-id",
                f"@loader_path/{destination.name}",
                os.fspath(destination),
            ],
            check=True,
        )

    if shutil.which("codesign") is not None:
        for path in [*bundled.values(), executable]:
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(path)],
                check=True,
            )


class build_py(_build_py):
    def run(self):
        command = _find_executable()
        info_dir = _find_info_dir()
        target = Path(self.build_lib) / "sagelite_lie" / "data"
        bin_target = target / "bin"
        info_target = target / "LiE"
        shutil.rmtree(target, ignore_errors=True)
        bin_target.mkdir(parents=True, exist_ok=True)

        shutil.copytree(info_dir, info_target, ignore_dangling_symlinks=True)
        lie_executable = info_target / "Lie.exe"
        if not lie_executable.is_file():
            shutil.copy2(command, lie_executable)
        lie_executable.chmod(lie_executable.stat().st_mode | 0o111)
        _bundle_macos_runtime(lie_executable, info_target / "lib")
        _write_lie_command(bin_target / "lie")

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_LIE_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
