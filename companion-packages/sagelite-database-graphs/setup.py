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
    / "sagelite_database_graphs"
    / "data"
    / "graphs"
)
GRAPH_DATABASE_FILES = (
    "brouwer_srg_database.json",
    "graphs.db",
    "isgci_sage.xml",
    "smallgraphs.txt",
)


def _candidate_graphs_dirs() -> list[Path]:
    directories = []
    for variable in ("SAGELITE_GRAPHS_DATA_DIR", "GRAPHS_DATA_DIR"):
        value = os.environ.get(variable)
        if value:
            directories.append(Path(value))
    if os.environ.get("SAGE_SHARE"):
        directories.append(Path(os.environ["SAGE_SHARE"]) / "graphs")
    if os.environ.get("SAGE_LOCAL"):
        directories.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "graphs")
    directories.extend(
        [
            REPO_ROOT / "local" / "share" / "graphs",
            PACKAGE_DATA_DIR,
            Path("/usr/share/graphs"),
            Path("/usr/local/share/graphs"),
        ]
    )
    return directories


def _looks_like_graphs_dir(path: Path) -> bool:
    return path.is_dir() and all(
        (path / filename).is_file() for filename in GRAPH_DATABASE_FILES
    )


def _find_graphs_dir() -> Path:
    for directory in _candidate_graphs_dirs():
        if _looks_like_graphs_dir(directory):
            return directory.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_graphs_dirs())
    raise RuntimeError(
        "could not find the graph database directory containing "
        f"{', '.join(GRAPH_DATABASE_FILES)}. Set SAGELITE_GRAPHS_DATA_DIR.\n"
        f"Searched:\n  {searched}"
    )


def _copy_graph_database(source: Path, target: Path) -> None:
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)
    for filename in GRAPH_DATABASE_FILES:
        shutil.copy2(source / filename, target / filename)
    if not _looks_like_graphs_dir(target):
        raise RuntimeError(f"graph database files were not copied from {source}")


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_graphs"
            / "data"
            / "graphs"
        )
        _copy_graph_database(_find_graphs_dir(), target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_graphs"
            / "data"
            / "graphs"
        )
        _copy_graph_database(_find_graphs_dir(), target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
