from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DATA_DIR = (
    Path(__file__).resolve().parent
    / "src"
    / "sagelite_database_symbolic_data"
    / "data"
    / "symbolic_data"
)


def _candidate_symbolic_data_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_SYMBOLIC_DATA_DIR", "DATABASE_SYMBOLIC_DATA_DIR"):
        value = os.environ.get(variable)
        if value:
            path = Path(value)
            dirs.append(
                path / "symbolic_data" if (path / "symbolic_data").is_dir() else path
            )
    if os.environ.get("SAGE_SHARE"):
        dirs.append(Path(os.environ["SAGE_SHARE"]) / "symbolic_data")
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "symbolic_data")
    dirs.extend(
        [
            PACKAGE_DATA_DIR,
            REPO_ROOT / "local" / "share" / "symbolic_data",
            Path("/usr/share/symbolic_data"),
            Path("/usr/local/share/symbolic_data"),
        ]
    )
    return dirs


def _has_symbolic_data_payload(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "COPYING").is_file()
        and (path / "Data" / "XMLResources").is_dir()
    )


def _find_symbolic_data_dir() -> Path:
    for directory in _candidate_symbolic_data_dirs():
        if _has_symbolic_data_payload(directory):
            return directory.resolve()
    searched = "\n  ".join(
        os.fspath(path) for path in _candidate_symbolic_data_dirs()
    )
    raise RuntimeError(
        "could not find the SymbolicData database directory containing COPYING "
        "and Data/XMLResources. Set SAGELITE_SYMBOLIC_DATA_DIR.\n"
        f"Searched:\n  {searched}"
    )


def _copy_symbolic_data(source: Path, target: Path) -> None:
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target, ignore_dangling_symlinks=True)
    if not _has_symbolic_data_payload(target):
        raise RuntimeError("SymbolicData database was not copied into the wheel")


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_symbolic_data"
            / "data"
            / "symbolic_data"
        )
        _copy_symbolic_data(_find_symbolic_data_dir(), target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_symbolic_data"
            / "data"
            / "symbolic_data"
        )
        _copy_symbolic_data(_find_symbolic_data_dir(), target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
