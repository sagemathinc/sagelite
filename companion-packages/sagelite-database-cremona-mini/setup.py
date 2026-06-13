from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DATA_FILE = (
    Path(__file__).resolve().parent
    / "src"
    / "sagelite_database_cremona_mini"
    / "data"
    / "cremona"
    / "cremona_mini.db"
)
PACKAGE_DATA_RELATIVE = os.fspath(
    Path("src")
    / "sagelite_database_cremona_mini"
    / "data"
    / "cremona"
    / "cremona_mini.db"
)


def _candidate_cremona_mini_databases() -> list[Path]:
    databases = []
    for variable in (
        "SAGELITE_CREMONA_MINI_DB",
        "CREMONA_MINI_DB",
        "CREMONA_MINI_DATA_DIR",
    ):
        value = os.environ.get(variable)
        if value:
            path = Path(value)
            databases.append(path / "cremona_mini.db" if path.is_dir() else path)
    for variable in ("SAGELITE_CREMONA_MINI_DIR", "CREMONA_MINI_DIR"):
        value = os.environ.get(variable)
        if value:
            databases.append(Path(value) / "cremona_mini.db")
    if os.environ.get("SAGE_SHARE"):
        databases.append(
            Path(os.environ["SAGE_SHARE"]) / "cremona" / "cremona_mini.db"
        )
    if os.environ.get("SAGE_LOCAL"):
        databases.append(
            Path(os.environ["SAGE_LOCAL"])
            / "share"
            / "cremona"
            / "cremona_mini.db"
        )
    databases.extend(
        [
            PACKAGE_DATA_FILE,
            REPO_ROOT / "local" / "share" / "cremona" / "cremona_mini.db",
            Path("/usr/share/cremona/cremona_mini.db"),
            Path("/usr/local/share/cremona/cremona_mini.db"),
        ]
    )
    return databases


def _find_cremona_mini_database() -> Path:
    for database in _candidate_cremona_mini_databases():
        if database.is_file():
            return database.resolve()
    searched = "\n  ".join(
        os.fspath(path) for path in _candidate_cremona_mini_databases()
    )
    raise RuntimeError(
        "could not find the mini Cremona elliptic-curve database "
        "cremona_mini.db. Set SAGELITE_CREMONA_MINI_DB.\n"
        f"Searched:\n  {searched}"
    )


def _copy_database(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    if not target.is_file():
        raise RuntimeError("mini Cremona database was not copied into the wheel")


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_cremona_mini"
            / "data"
            / "cremona"
            / "cremona_mini.db"
        )
        _copy_database(_find_cremona_mini_database(), target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_cremona_mini"
            / "data"
            / "cremona"
            / "cremona_mini.db"
        )
        _copy_database(_find_cremona_mini_database(), target)


setup(
    cmdclass={"build_py": build_py, "sdist": sdist},
    data_files=[("share/cremona", [PACKAGE_DATA_RELATIVE])],
)
