from __future__ import annotations

import os
import shutil
import tarfile
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = (
    Path(__file__).resolve().parent
    / "src"
    / "sagelite_database_jones_numfield"
)
BUNDLED_SOURCE = PACKAGE_ROOT / "data" / "jones"


def _candidate_database_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_JONES_NUMFIELD_DATA_DIR", "DATABASE_JONES_NUMFIELD_DIR"):
        value = os.environ.get(variable)
        if value:
            path = Path(value)
            dirs.append(path / "jones" if (path / "jones").is_dir() else path)
    if os.environ.get("SAGE_SHARE"):
        dirs.append(Path(os.environ["SAGE_SHARE"]) / "jones")
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "jones")
    dirs.extend(
        [
            BUNDLED_SOURCE,
            REPO_ROOT / "local" / "share" / "jones",
            Path("/usr/share/jones"),
            Path("/usr/local/share/jones"),
        ]
    )
    return dirs


def _candidate_spkg_tarballs() -> list[Path]:
    tarballs = []
    value = os.environ.get("SAGELITE_JONES_NUMFIELD_SPKG")
    if value:
        tarballs.append(Path(value))
    upstream = REPO_ROOT / "upstream"
    tarballs.extend(sorted(upstream.glob("database_jones_numfield-*.spkg")))
    tarballs.extend(sorted(upstream.glob("database_jones_numfield-*.tar.*")))
    return tarballs


def _has_jones_payload(path: Path) -> bool:
    return path.is_dir() and (path / "jones.sobj").is_file()


def _find_database_dir() -> Path | None:
    for directory in _candidate_database_dirs():
        if _has_jones_payload(directory):
            return directory.resolve()
    return None


def _extract_spkg(target: Path) -> bool:
    for tarball in _candidate_spkg_tarballs():
        if not tarball.is_file():
            continue
        with tarfile.open(tarball) as archive:
            member = next(
                (
                    item
                    for item in archive.getmembers()
                    if Path(item.name).name == "jones.sobj" and item.isfile()
                ),
                None,
            )
            if member is None:
                continue
            target.mkdir(parents=True, exist_ok=True)
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            with (target / "jones.sobj").open("wb") as output:
                shutil.copyfileobj(extracted, output)
            return True
    return False


def _copy_database(target: Path) -> None:
    shutil.rmtree(target, ignore_errors=True)
    source = _find_database_dir()
    if source is not None:
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / "jones.sobj", target / "jones.sobj")
    elif not _extract_spkg(target):
        searched = "\n  ".join(os.fspath(path) for path in _candidate_database_dirs())
        raise RuntimeError(
            "could not find the Jones number field database jones.sobj. "
            "Set SAGELITE_JONES_NUMFIELD_DATA_DIR or SAGELITE_JONES_NUMFIELD_SPKG.\n"
            f"Searched:\n  {searched}"
        )

    if not _has_jones_payload(target):
        raise RuntimeError("Jones number field database was not copied into the wheel")


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_jones_numfield"
            / "data"
            / "jones"
        )
        _copy_database(target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_jones_numfield"
            / "data"
            / "jones"
        )
        _copy_database(target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
