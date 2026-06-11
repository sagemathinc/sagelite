from __future__ import annotations

import bz2
import gzip
import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = (
    Path(__file__).resolve().parent / "src" / "sagelite_database_sloane"
)
BUNDLED_SOURCE = PACKAGE_ROOT / "_sloane"


def _candidate_source_pairs() -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []

    stripped_gz = os.environ.get("SAGELITE_SLOANE_STRIPPED_GZ")
    names_gz = os.environ.get("SAGELITE_SLOANE_NAMES_GZ")
    if stripped_gz and names_gz:
        pairs.append((Path(stripped_gz), Path(names_gz)))

    for variable in ("SAGELITE_SLOANE_DATA_DIR", "SLOANE_DATA_DIR"):
        value = os.environ.get(variable)
        if value:
            pairs.extend(_directory_pairs(Path(value)))

    dot_sage = os.environ.get("DOT_SAGE")
    if dot_sage:
        pairs.extend(_directory_pairs(Path(dot_sage) / "db" / "sloane"))

    pairs.extend(_directory_pairs(BUNDLED_SOURCE))
    pairs.extend(_directory_pairs(REPO_ROOT / "local" / "share" / "sloane"))
    pairs.extend(_directory_pairs(Path.home() / ".sage" / "db" / "sloane"))
    return pairs


def _directory_pairs(directory: Path) -> list[tuple[Path, Path]]:
    return [
        (directory / "stripped.gz", directory / "names.gz"),
        (directory / "sloane-oeis.bz2", directory / "sloane-names.bz2"),
    ]


def _find_source_pair() -> tuple[Path, Path]:
    for stripped, names in _candidate_source_pairs():
        if stripped.is_file() and names.is_file():
            return stripped.resolve(), names.resolve()
    searched = "\n  ".join(
        f"{stripped} and {names}" for stripped, names in _candidate_source_pairs()
    )
    raise RuntimeError(
        "could not find Sloane/OEIS stripped and names data files. "
        "Set SAGELITE_SLOANE_STRIPPED_GZ and SAGELITE_SLOANE_NAMES_GZ.\n"
        f"Searched:\n  {searched}"
    )


def _copy_or_convert(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix == ".bz2":
        shutil.copy2(source, target)
        return

    if source.suffix != ".gz":
        raise RuntimeError(f"unsupported Sloane/OEIS source format: {source}")

    with gzip.open(source, "rb") as source_file:
        data = source_file.read()
    with bz2.open(target, "wb") as target_file:
        target_file.write(data)


def _copy_database(stripped: Path, names: Path, target: Path) -> None:
    shutil.rmtree(target, ignore_errors=True)
    _copy_or_convert(stripped, target / "sloane-oeis.bz2")
    _copy_or_convert(names, target / "sloane-names.bz2")
    for filename in ("sloane-oeis.bz2", "sloane-names.bz2"):
        path = target / filename
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Sloane/OEIS data file was not copied: {filename}")


class build_py(_build_py):
    def run(self):
        super().run()

        stripped, names = _find_source_pair()
        target = Path(self.build_lib) / "sagelite_database_sloane" / "data" / "sloane"
        _copy_database(stripped, names, target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        stripped, names = _find_source_pair()
        target = Path(base_dir) / "src" / "sagelite_database_sloane" / "_sloane"
        _copy_database(stripped, names, target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
