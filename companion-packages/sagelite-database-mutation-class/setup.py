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
    / "sagelite_database_mutation_class"
)
BUNDLED_SOURCE = PACKAGE_ROOT / "data" / "cluster_algebra_quiver"


def _candidate_database_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_MUTATION_CLASS_DATA_DIR", "DATABASE_MUTATION_CLASS_DIR"):
        value = os.environ.get(variable)
        if value:
            path = Path(value)
            dirs.append(
                path / "cluster_algebra_quiver"
                if (path / "cluster_algebra_quiver").is_dir()
                else path
            )
    if os.environ.get("SAGE_SHARE"):
        dirs.append(Path(os.environ["SAGE_SHARE"]) / "cluster_algebra_quiver")
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "cluster_algebra_quiver")
    dirs.extend(
        [
            BUNDLED_SOURCE,
            REPO_ROOT / "local" / "share" / "cluster_algebra_quiver",
            Path("/usr/share/cluster_algebra_quiver"),
            Path("/usr/local/share/cluster_algebra_quiver"),
        ]
    )
    return dirs


def _candidate_spkg_tarballs() -> list[Path]:
    tarballs = []
    value = os.environ.get("SAGELITE_MUTATION_CLASS_SPKG")
    if value:
        tarballs.append(Path(value))
    upstream = REPO_ROOT / "upstream"
    tarballs.extend(sorted(upstream.glob("database_mutation_class-*.spkg")))
    tarballs.extend(sorted(upstream.glob("database_mutation_class-*.tar.*")))
    return tarballs


def _database_files(path: Path) -> list[Path]:
    return sorted(path.glob("mutation_classes_*.dig6")) if path.is_dir() else []


def _has_mutation_class_payload(path: Path) -> bool:
    return (path / "mutation_classes_2.dig6").is_file() and bool(_database_files(path))


def _find_database_dir() -> Path | None:
    for directory in _candidate_database_dirs():
        if _has_mutation_class_payload(directory):
            return directory.resolve()
    return None


def _copy_database_files(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for path in _database_files(source):
        shutil.copy2(path, target / path.name)


def _extract_spkg(target: Path) -> bool:
    for tarball in _candidate_spkg_tarballs():
        if not tarball.is_file():
            continue
        copied = False
        with tarfile.open(tarball) as archive:
            for member in archive.getmembers():
                name = Path(member.name).name
                if not name.startswith("mutation_classes_") or not name.endswith(
                    ".dig6"
                ):
                    continue
                if not member.isfile():
                    continue
                target.mkdir(parents=True, exist_ok=True)
                extracted = archive.extractfile(member)
                if extracted is None:
                    continue
                with (target / name).open("wb") as output:
                    shutil.copyfileobj(extracted, output)
                copied = True
        if copied:
            return True
    return False


def _copy_database(target: Path) -> None:
    shutil.rmtree(target, ignore_errors=True)
    source = _find_database_dir()
    if source is not None:
        _copy_database_files(source, target)
    elif not _extract_spkg(target):
        searched = "\n  ".join(os.fspath(path) for path in _candidate_database_dirs())
        raise RuntimeError(
            "could not find the mutation class database files. "
            "Set SAGELITE_MUTATION_CLASS_DATA_DIR or SAGELITE_MUTATION_CLASS_SPKG.\n"
            f"Searched:\n  {searched}"
        )

    if not _has_mutation_class_payload(target):
        raise RuntimeError("mutation class database was not copied into the wheel")


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_mutation_class"
            / "data"
            / "cluster_algebra_quiver"
        )
        _copy_database(target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_mutation_class"
            / "data"
            / "cluster_algebra_quiver"
        )
        _copy_database(target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
