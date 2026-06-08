from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = Path(__file__).resolve().parent / "src" / "sagelite_database_kohel"
BUNDLED_SOURCE = PACKAGE_ROOT / "data" / "kohel"


def _candidate_database_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_KOHEL_DATA_DIR", "DATABASE_KOHEL_DATA_DIR"):
        value = os.environ.get(variable)
        if value:
            path = Path(value)
            dirs.append(path / "kohel" if (path / "kohel").is_dir() else path)
    if os.environ.get("SAGE_SHARE"):
        dirs.append(Path(os.environ["SAGE_SHARE"]) / "kohel")
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "kohel")
    dirs.extend(
        [
            BUNDLED_SOURCE,
            REPO_ROOT / "local" / "share" / "kohel",
            Path("/usr/share/kohel"),
            Path("/usr/local/share/kohel"),
        ]
    )
    return dirs


def _has_kohel_payload(path: Path) -> bool:
    return (
        (path / "PolMod" / "Cls" / "pol.029.dbz").is_file()
        and (path / "PolMod" / "Atk" / "pol.002.dbz").is_file()
        and (
            path
            / "PolHeeg"
            / "Cls"
            / "0000001-0005000"
            / "pol.0000023.dbz"
        ).is_file()
    )


def _find_database_dir() -> Path:
    for directory in _candidate_database_dirs():
        if directory.is_dir() and _has_kohel_payload(directory):
            return directory.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_database_dirs())
    raise RuntimeError(
        "could not find the Kohel modular and Hilbert polynomial database. "
        "Set SAGELITE_KOHEL_DATA_DIR.\n"
        f"Searched:\n  {searched}"
    )


def _copy_database(source: Path, target: Path) -> None:
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target, ignore_dangling_symlinks=True)
    if not _has_kohel_payload(target):
        raise RuntimeError("Kohel database was not copied into the wheel")


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib) / "sagelite_database_kohel" / "data" / "kohel"
        )
        _copy_database(_find_database_dir(), target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir) / "src" / "sagelite_database_kohel" / "data" / "kohel"
        )
        _copy_database(_find_database_dir(), target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
