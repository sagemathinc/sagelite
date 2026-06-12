from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist

REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_cremona_databases() -> list[Path]:
    databases = []
    for variable in (
        "SAGELITE_CREMONA_ELLCURVE_DB",
        "CREMONA_ELLCURVE_DB",
        "CREMONA_LARGE_DATA_DIR",
    ):
        value = os.environ.get(variable)
        if value:
            path = Path(value)
            databases.append(path / "cremona.db" if path.is_dir() else path)
    for variable in ("SAGELITE_CREMONA_ELLCURVE_DIR", "CREMONA_ELLCURVE_DIR"):
        value = os.environ.get(variable)
        if value:
            databases.append(Path(value) / "cremona.db")
    if os.environ.get("SAGE_SHARE"):
        databases.append(Path(os.environ["SAGE_SHARE"]) / "cremona" / "cremona.db")
    if os.environ.get("SAGE_LOCAL"):
        databases.append(
            Path(os.environ["SAGE_LOCAL"]) / "share" / "cremona" / "cremona.db"
        )
    databases.extend(
        [
            REPO_ROOT / "local" / "share" / "cremona" / "cremona.db",
            Path("/usr/share/cremona/cremona.db"),
            Path("/usr/local/share/cremona/cremona.db"),
        ]
    )
    return databases


def _find_cremona_database() -> Path:
    for database in _candidate_cremona_databases():
        if database.is_file():
            return database.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_cremona_databases())
    raise RuntimeError(
        "could not find the full Cremona elliptic-curve database cremona.db. "
        "Set SAGELITE_CREMONA_ELLCURVE_DB.\n"
        f"Searched:\n  {searched}"
    )


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_cremona_ellcurve"
            / "data"
            / "cremona"
            / "cremona.db"
        )
        _copy_database(_find_cremona_database(), target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_cremona_ellcurve"
            / "data"
            / "cremona"
            / "cremona.db"
        )
        _copy_database(_find_cremona_database(), target)


def _copy_database(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    if not target.is_file():
        raise RuntimeError("full Cremona database was not copied into the package")


setup(cmdclass={"build_py": build_py, "sdist": sdist})
