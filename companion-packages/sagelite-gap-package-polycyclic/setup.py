from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


GAP_PACKAGE_PREFIXES = ("alnuth", "autpgrp", "polycyclic")


def _split_roots(value: str | None) -> list[Path]:
    if not value:
        return []
    roots = []
    for root in value.replace(os.pathsep, ";").split(";"):
        root = root.strip()
        if root:
            roots.append(Path(root))
    return roots


def _candidate_gap_roots() -> list[Path]:
    roots = []
    roots.extend(_split_roots(os.environ.get("SAGELITE_GAP_POLYCYCLIC_ROOT")))
    roots.extend(_split_roots(os.environ.get("SAGELITE_GAP_ROOTS")))
    roots.extend(_split_roots(os.environ.get("SAGELITE_GAP_ROOT")))
    roots.extend(_split_roots(os.environ.get("GAP_ROOT_PATHS")))
    roots.extend([Path("/usr/share/gap"), Path("/usr/local/share/gap")])
    return roots


def _candidate_package_dirs() -> list[Path]:
    dirs = []
    for variable in (
        "SAGELITE_GAP_POLYCYCLIC_PACKAGE_DIR",
        "SAGELITE_GAP_PACKAGE_POLYCYCLIC_DIR",
        "SAGELITE_GAP_ALNUTH_PACKAGE_DIR",
        "SAGELITE_GAP_PACKAGE_ALNUTH_DIR",
        "SAGELITE_GAP_AUTPGRP_PACKAGE_DIR",
        "SAGELITE_GAP_PACKAGE_AUTPGRP_DIR",
    ):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))

    for root in _candidate_gap_roots():
        pkg = root / "pkg"
        if pkg.is_dir():
            dirs.extend(path for path in pkg.iterdir() if path.is_dir())
    return dirs


def _find_gap_package_dir(prefix: str) -> Path:
    for package_dir in _candidate_package_dirs():
        if (
            package_dir.name.lower().startswith(prefix)
            and (package_dir / "PackageInfo.g").is_file()
        ):
            return package_dir.resolve()

    searched = "\n  ".join(os.fspath(path) for path in _candidate_package_dirs())
    raise RuntimeError(
        f"could not find a GAP {prefix.upper()} package directory "
        "containing PackageInfo.g. "
        "Set SAGELITE_GAP_POLYCYCLIC_ROOT or the matching "
        "SAGELITE_GAP_*_PACKAGE_DIR variables.\n"
        f"Searched:\n  {searched}"
    )


def _ignore_gap_package_files(directory: str, names: list[str]) -> set[str]:
    ignored = {"__pycache__", "doc", "htm", "test", "tst"}
    ignored.update(
        name
        for name in names
        if name.endswith((".pyc", ".pyo", ".pdf", ".html", ".htm", ".css", ".js"))
    )
    return ignored


class build_py(_build_py):
    def run(self):
        package_root = (
            Path(self.build_lib)
            / "sagelite_gap_package_polycyclic"
            / "data"
            / "gaproot"
            / "pkg"
        )
        shutil.rmtree(package_root.parent, ignore_errors=True)
        package_root.mkdir(parents=True, exist_ok=True)
        for prefix in GAP_PACKAGE_PREFIXES:
            source = _find_gap_package_dir(prefix)
            shutil.copytree(
                source,
                package_root / source.name,
                ignore=_ignore_gap_package_files,
                ignore_dangling_symlinks=True,
            )
        super().run()


setup(cmdclass={"build_py": build_py})
