from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover - wheel is a build requirement
    _bdist_wheel = None


def _candidate_prefixes() -> list[Path]:
    prefixes = []
    for variable in ("SAGELITE_FRICAS_PREFIX", "FRICAS_PREFIX", "SAGE_LOCAL"):
        if os.environ.get(variable):
            prefixes.append(Path(os.environ[variable]))
    prefixes.extend([Path("/usr"), Path("/usr/local")])
    return prefixes


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_FRICAS_BINDIR", "FRICAS_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    dirs.extend(prefix / "bin" for prefix in _candidate_prefixes())
    return dirs


def _candidate_libdirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_FRICAS_LIBDIR", "FRICAS_LIBDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    dirs.extend(prefix / "lib" / "fricas" for prefix in _candidate_prefixes())
    return dirs


def _candidate_sharedirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_FRICAS_SHAREDIR", "FRICAS_SHAREDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    dirs.extend(prefix / "share" / "fricas" for prefix in _candidate_prefixes())
    return dirs


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        candidate = bindir / "fricas"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a fricas executable. Set SAGELITE_FRICAS_BINDIR "
        f"to the Sage-built bin directory.\nSearched:\n  {searched}"
    )


def _find_libdir() -> Path:
    for libdir in _candidate_libdirs():
        if libdir.is_dir():
            return libdir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_libdirs())
    raise RuntimeError(
        "could not find a FriCAS lib directory. Set SAGELITE_FRICAS_LIBDIR.\n"
        f"Searched:\n  {searched}"
    )


def _find_sharedir() -> Path | None:
    for sharedir in _candidate_sharedirs():
        if sharedir.is_dir():
            return sharedir.resolve()
    return None


def _write_relocatable_command(source: Path, target: Path) -> None:
    try:
        script = source.read_text()
    except UnicodeDecodeError:
        shutil.copy2(source, target.with_name("fricas-real"))
        target.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'FRICAS_PREFIX="$(CDPATH= cd -- "$HERE/.." && pwd)"\n'
            'export FRICAS_PREFIX\n'
            'exec "$HERE/fricas-real" "$@"\n'
        )
    else:
        lines = script.splitlines()
        injected = False
        patched = []
        for line in lines:
            if not injected and line.startswith("exec_prefix="):
                patched.extend(
                    [
                        'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"',
                        'FRICAS_PREFIX="$(CDPATH= cd -- "$HERE/.." && pwd)"',
                        "export FRICAS_PREFIX",
                    ]
                )
                injected = True
            patched.append(line)
        if not injected:
            shutil.copy2(source, target.with_name("fricas-real"))
            patched = [
                "#!/bin/sh",
                'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"',
                'FRICAS_PREFIX="$(CDPATH= cd -- "$HERE/.." && pwd)"',
                "export FRICAS_PREFIX",
                'exec "$HERE/fricas-real" "$@"',
            ]
        target.write_text("\n".join(patched) + "\n")

    target.chmod(0o755)


class build_py(_build_py):
    def run(self):
        source = _find_executable()
        libdir = _find_libdir()
        sharedir = _find_sharedir()
        target = Path(self.build_lib) / "sagelite_fricas" / "data"
        bin_target = target / "bin"
        lib_target = target / "lib" / "fricas"
        share_target = target / "share" / "fricas"
        shutil.rmtree(target, ignore_errors=True)
        bin_target.mkdir(parents=True, exist_ok=True)

        _write_relocatable_command(source, bin_target / "fricas")
        shutil.copytree(libdir, lib_target, ignore_dangling_symlinks=True)
        if sharedir is not None:
            shutil.copytree(sharedir, share_target, ignore_dangling_symlinks=True)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_FRICAS_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
