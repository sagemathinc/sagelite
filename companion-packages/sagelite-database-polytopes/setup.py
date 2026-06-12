from __future__ import annotations

import os
import shutil
import tarfile
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = Path(__file__).resolve().parent / "src" / "sagelite_database_polytopes"
BUNDLED_SOURCE = PACKAGE_ROOT / "data" / "reflexive_polytopes"


def _candidate_database_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_POLYTOPES_DATA_DIR", "POLYTOPES_DB_DIR"):
        value = os.environ.get(variable)
        if value:
            path = Path(value)
            dirs.append(
                path / "reflexive_polytopes"
                if (path / "reflexive_polytopes").is_dir()
                else path
            )
    if os.environ.get("SAGE_SHARE"):
        dirs.append(Path(os.environ["SAGE_SHARE"]) / "reflexive_polytopes")
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "reflexive_polytopes")
    dirs.extend(
        [
            BUNDLED_SOURCE,
            REPO_ROOT / "local" / "share" / "reflexive_polytopes",
            Path("/usr/share/reflexive_polytopes"),
            Path("/usr/local/share/reflexive_polytopes"),
        ]
    )
    return dirs


def _candidate_spkg_tarballs() -> list[Path]:
    tarballs = []
    value = os.environ.get("SAGELITE_POLYTOPES_SPKG")
    if value:
        tarballs.append(Path(value))
    upstream = REPO_ROOT / "upstream"
    tarballs.extend(sorted(upstream.glob("polytopes_db-*.spkg")))
    tarballs.extend(sorted(upstream.glob("polytopes_db-*.tar.*")))
    return tarballs


def _has_polytopes_payload(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "Full2d" / "zzdb.info").is_file()
        and (path / "Full3d" / "zzdb.info").is_file()
        and (path / "reflexive_polytopes_2d").is_file()
        and (path / "reflexive_polytopes_3d").is_file()
    )


def _find_database_dir() -> Path | None:
    for directory in _candidate_database_dirs():
        if _has_polytopes_payload(directory):
            return directory.resolve()
    return None


def _extract_spkg(target: Path) -> bool:
    for tarball in _candidate_spkg_tarballs():
        if not tarball.is_file():
            continue
        copied = False
        with tarfile.open(tarball) as archive:
            for member in archive.getmembers():
                parts = Path(member.name).parts
                if not parts or parts[0].startswith("."):
                    continue
                names = {
                    "Full2d",
                    "Full3d",
                    "reflexive_polytopes_2d",
                    "reflexive_polytopes_3d",
                }
                index = next(
                    (i for i, part in enumerate(parts) if part in names),
                    None,
                )
                if index is None:
                    continue
                relative = Path(*parts[index:])
                destination = target / relative
                if member.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                    continue
                if not member.isfile():
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                extracted = archive.extractfile(member)
                if extracted is None:
                    continue
                with destination.open("wb") as output:
                    shutil.copyfileobj(extracted, output)
                copied = True
        if copied:
            return True
    return False


def _copy_database(target: Path) -> None:
    shutil.rmtree(target, ignore_errors=True)
    source = _find_database_dir()
    if source is not None:
        shutil.copytree(source, target, ignore_dangling_symlinks=True)
    elif not _extract_spkg(target):
        searched = "\n  ".join(os.fspath(path) for path in _candidate_database_dirs())
        raise RuntimeError(
            "could not find the 2D/3D reflexive polytope database. "
            "Set SAGELITE_POLYTOPES_DATA_DIR or SAGELITE_POLYTOPES_SPKG.\n"
            f"Searched:\n  {searched}"
        )

    if not _has_polytopes_payload(target):
        raise RuntimeError("reflexive polytope database was not copied into the wheel")


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_polytopes"
            / "data"
            / "reflexive_polytopes"
        )
        _copy_database(target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_polytopes"
            / "data"
            / "reflexive_polytopes"
        )
        _copy_database(target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
