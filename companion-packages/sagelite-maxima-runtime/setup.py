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
    roots = []
    if os.environ.get("SAGELITE_MAXIMA_PREFIX"):
        roots.append(Path(os.environ["SAGELITE_MAXIMA_PREFIX"]))
    if os.environ.get("MAXIMA_PREFIX"):
        roots.append(Path(os.environ["MAXIMA_PREFIX"]))
    roots.extend(Path("/usr/share").glob("maxima-sage/*"))
    roots.extend(Path("/usr/share").glob("maxima/*"))
    roots.extend(Path("/usr/local/share").glob("maxima/*"))
    return roots


def _candidate_fas_files() -> list[Path]:
    files = []
    if os.environ.get("SAGELITE_MAXIMA_FAS"):
        files.append(Path(os.environ["SAGELITE_MAXIMA_FAS"]))
    if os.environ.get("MAXIMA_FAS"):
        files.append(Path(os.environ["MAXIMA_FAS"]))
    files.extend(
        [
            Path("/usr/lib/ecl/maxima.fas"),
            Path("/usr/local/lib/ecl/maxima.fas"),
        ]
    )
    return files


def _candidate_images_dirs(maxima_prefix: Path) -> list[Path]:
    dirs = []
    if os.environ.get("SAGELITE_MAXIMA_IMAGESDIR"):
        dirs.append(Path(os.environ["SAGELITE_MAXIMA_IMAGESDIR"]))
    version = maxima_prefix.name
    dirs.extend(Path("/usr/lib").glob(f"maxima/{version}"))
    dirs.extend(Path("/usr/local/lib").glob(f"maxima/{version}"))
    return dirs


def _candidate_ecl_dirs() -> list[Path]:
    dirs = []
    if os.environ.get("SAGELITE_MAXIMA_ECLDIR"):
        dirs.append(Path(os.environ["SAGELITE_MAXIMA_ECLDIR"]))
    dirs.extend(Path("/usr/lib").glob("ecl-*"))
    dirs.extend(Path("/usr/local/lib").glob("ecl-*"))
    return dirs


def _candidate_library_dirs() -> list[Path]:
    dirs = []
    if os.environ.get("SAGELITE_MAXIMA_LIBDIR"):
        dirs.append(Path(os.environ["SAGELITE_MAXIMA_LIBDIR"]))
    dirs.extend([Path("/usr/lib"), Path("/usr/local/lib")])
    return dirs


def _looks_like_maxima_prefix(path: Path) -> bool:
    return (path / "src").is_dir() and (path / "share").is_dir()


def _looks_like_images_dir(path: Path) -> bool:
    return (path / "binary-ecl" / "maxima").is_file()


def _find_maxima_prefix() -> Path:
    for prefix in _candidate_prefixes():
        if _looks_like_maxima_prefix(prefix):
            return prefix.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_prefixes())
    raise RuntimeError(
        "could not find a Maxima prefix containing src/ and share/. "
        "Set SAGELITE_MAXIMA_PREFIX to the Sage-built Maxima share directory.\n"
        f"Searched:\n  {searched}"
    )


def _find_maxima_images_dir(maxima_prefix: Path) -> Path:
    for images_dir in _candidate_images_dirs(maxima_prefix):
        if _looks_like_images_dir(images_dir):
            return images_dir.resolve()
    searched = "\n  ".join(
        os.fspath(path) for path in _candidate_images_dirs(maxima_prefix)
    )
    raise RuntimeError(
        "could not find the Maxima binary image directory containing "
        "binary-ecl/maxima. Set SAGELITE_MAXIMA_IMAGESDIR to the Sage-built "
        f"Maxima image directory.\nSearched:\n  {searched}"
    )


def _find_maxima_fas() -> Path:
    for fas in _candidate_fas_files():
        if fas.is_file():
            return fas.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_fas_files())
    raise RuntimeError(
        "could not find maxima.fas. Set SAGELITE_MAXIMA_FAS to the matching "
        f"Sage-built ECL Maxima image.\nSearched:\n  {searched}"
    )


def _find_ecl_dir() -> Path:
    for ecl_dir in _candidate_ecl_dirs():
        if (ecl_dir / "sockets.fas").is_file():
            return ecl_dir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_ecl_dirs())
    raise RuntimeError(
        "could not find the ECL runtime directory containing sockets.fas. "
        f"Set SAGELITE_MAXIMA_ECLDIR.\nSearched:\n  {searched}"
    )


def _find_library(soname: str) -> Path:
    candidates = []
    for directory in _candidate_library_dirs():
        candidates.extend(directory.glob(f"{soname}*"))
        candidates.append(directory / soname)
    for candidate in candidates:
        if candidate.is_file() or candidate.is_symlink():
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in candidates)
    raise RuntimeError(
        f"could not find runtime library {soname}. Set SAGELITE_MAXIMA_LIBDIR.\n"
        f"Searched:\n  {searched}"
    )


def _ignore_maxima_files(directory: str, names: list[str]) -> set[str]:
    ignored = {
        "__pycache__",
        "doc",
        "html",
        "locale",
        "tests",
        "xmaxima",
    }
    ignored.update(
        name
        for name in names
        if name.endswith((".pyc", ".pyo", ".pdf", ".html", ".htm", ".css", ".js"))
    )
    return ignored


def _write_maxima_command(path: Path, version: str, ecl_dir_name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""#!/bin/sh
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PREFIX=$(dirname "$HERE")
export MAXIMA_PREFIX="${{MAXIMA_PREFIX:-$PREFIX/share/maxima/{version}}}"
export MAXIMA_LAYOUT_AUTOTOOLS=true
export MAXIMA_IMAGESDIR="$PREFIX/lib/maxima/{version}"
export ECLDIR="$PREFIX/lib/{ecl_dir_name}/"
export LD_LIBRARY_PATH="$PREFIX/lib/runtime${{LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}}"
exec "$PREFIX/lib/maxima/{version}/binary-ecl/maxima" \\
  --frame-stack 4096 --lisp-stack 65536 -- "$@"
""",
    )
    path.chmod(0o755)


class build_py(_build_py):
    def run(self):
        super().run()

        maxima_prefix = _find_maxima_prefix()
        maxima_images_dir = _find_maxima_images_dir(maxima_prefix)
        maxima_fas = _find_maxima_fas()
        ecl_dir = _find_ecl_dir()
        libecl = _find_library("libecl.so.24.5")
        libgmp = _find_library("libgmp.so.10")
        target = Path(self.build_lib) / "sagelite_maxima" / "data"
        shutil.rmtree(target, ignore_errors=True)

        share_target = target / "share" / "maxima" / maxima_prefix.name
        share_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            maxima_prefix,
            share_target,
            ignore=_ignore_maxima_files,
            ignore_dangling_symlinks=True,
        )

        fas_target = target / "lib" / "ecl" / "maxima.fas"
        fas_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(maxima_fas, fas_target)

        images_target = target / "lib" / "maxima" / maxima_prefix.name
        shutil.copytree(maxima_images_dir, images_target, ignore_dangling_symlinks=True)

        ecl_target = target / "lib" / ecl_dir.name
        shutil.copytree(ecl_dir, ecl_target, ignore_dangling_symlinks=True)

        runtime_target = target / "lib" / "runtime"
        runtime_target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(libecl, runtime_target / "libecl.so.24.5")
        shutil.copy2(libgmp, runtime_target / "libgmp.so.10")

        _write_maxima_command(
            target / "bin" / "maxima", maxima_prefix.name, ecl_dir.name
        )


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_MAXIMA_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
