#!/usr/bin/env python3
"""
Install Sage source sidecars that are not Python modules.

Meson-python handles Python extension modules and ordinary Python package
sources well, but Sage also needs Cython include files, C/C++ helper sources,
headers, and small text sidecars available in installed wheels.  These files
are used by doctests, cythonized examples, and downstream packages that compile
against the installed ``sage`` namespace.
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


SIDECAR_SUFFIXES = {
    ".avi",
    ".c",
    ".cc",
    ".canvas3d",
    ".cpp",
    ".css",
    ".csv",
    ".dat",
    ".dvi",
    ".flv",
    ".g",
    ".gap",
    ".gif",
    ".gp",
    ".h",
    ".hh",
    ".html",
    ".htm",
    ".hpp",
    ".ini",
    ".jpg",
    ".jpeg",
    ".js",
    ".json",
    ".lib",
    ".lisp",
    ".m",
    ".md",
    ".mkv",
    ".mov",
    ".mp4",
    ".mtl",
    ".obj",
    ".ogv",
    ".pdf",
    ".png",
    ".pxd",
    ".pxi",
    ".pyi",
    ".pyx",
    ".rst",
    ".sage",
    ".sobj",
    ".spyx",
    ".spad",
    ".spec",
    ".supp",
    ".svg",
    ".tachyon",
    ".template",
    ".tex",
    ".txt",
    ".tpl",
    ".webm",
    ".wmv",
    ".xz",
    ".zip",
}

SIDECAR_NAMES = {
    "README",
}

IGNORED_DIRS = {
    "__pycache__",
}


def resolve_install_dir(install_dir: Path) -> Path:
    """
    Resolve a Meson install dir inside DESTDIR when install scripts run.
    """
    destdir_prefix = os.environ.get("MESON_INSTALL_DESTDIR_PREFIX")
    install_prefix = os.environ.get("MESON_INSTALL_PREFIX")

    if destdir_prefix:
        destdir_prefix_path = Path(destdir_prefix)
        if install_dir.is_absolute():
            if install_prefix:
                prefix_path = Path(install_prefix)
                try:
                    return destdir_prefix_path / install_dir.relative_to(prefix_path)
                except ValueError:
                    pass
            destdir = os.environ.get("DESTDIR")
            if destdir:
                return Path(destdir) / install_dir.relative_to("/")
        else:
            return destdir_prefix_path / install_dir

    return install_dir


def is_sidecar(path: Path) -> bool:
    return path.name in SIDECAR_NAMES or path.suffix in SIDECAR_SUFFIXES


def install_sidecars(source_dir: Path, install_dir: Path) -> int:
    count = 0
    for source in source_dir.rglob("*"):
        if not source.is_file():
            continue
        if any(part in IGNORED_DIRS for part in source.relative_to(source_dir).parts):
            continue
        if not is_sidecar(source):
            continue

        relative = source.relative_to(source_dir)
        target = install_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("install_dir", type=Path)
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    install_dir = resolve_install_dir(args.install_dir)
    count = install_sidecars(source_dir, install_dir)
    print(f"Installed {count} Sage sidecar files into {install_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
