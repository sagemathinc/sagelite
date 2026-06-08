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
    / "sagelite_database_ellcurves"
    / "data"
    / "ellcurves"
)


def _candidate_ellcurves_dirs() -> list[Path]:
    directories = []
    for variable in (
        "SAGELITE_ELLCURVES_DATA_DIR",
        "SAGELITE_ELLIPTIC_CURVES_DATA_DIR",
        "ELLCURVE_DATA_DIR",
    ):
        value = os.environ.get(variable)
        if value:
            directories.append(Path(value))
    if os.environ.get("SAGE_SHARE"):
        directories.append(Path(os.environ["SAGE_SHARE"]) / "ellcurves")
    if os.environ.get("SAGE_LOCAL"):
        directories.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "ellcurves")
    directories.extend(
        [
            REPO_ROOT / "local" / "share" / "ellcurves",
            PACKAGE_DATA_DIR,
            Path("/usr/share/ellcurves"),
            Path("/usr/local/share/ellcurves"),
        ]
    )
    return directories


def _looks_like_ellcurves_dir(path: Path) -> bool:
    return path.is_dir() and (path / "rank0").is_file()


def _find_ellcurves_dir() -> Path:
    for directory in _candidate_ellcurves_dirs():
        if _looks_like_ellcurves_dir(directory):
            return directory.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_ellcurves_dirs())
    raise RuntimeError(
        "could not find the elliptic curves database directory containing rank0. "
        "Set SAGELITE_ELLCURVES_DATA_DIR.\n"
        f"Searched:\n  {searched}"
    )


def _copy_rank_files(source: Path, target: Path) -> int:
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)

    copied = 0
    for rank_file in sorted(source.glob("rank*")):
        if rank_file.is_file():
            shutil.copy2(rank_file, target / rank_file.name)
            copied += 1

    if not copied:
        raise RuntimeError(f"no rank files copied from {source}")
    return copied


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_ellcurves"
            / "data"
            / "ellcurves"
        )
        _copy_rank_files(_find_ellcurves_dir(), target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_ellcurves"
            / "data"
            / "ellcurves"
        )
        _copy_rank_files(_find_ellcurves_dir(), target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
