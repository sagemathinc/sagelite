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
    / "sagelite_database_odlyzko_zeta"
)
BUNDLED_SOURCE = PACKAGE_ROOT / "data" / "odlyzko"


def _candidate_database_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_ODLYZKO_ZETA_DATA_DIR", "DATABASE_ODLYZKO_ZETA_DIR"):
        value = os.environ.get(variable)
        if value:
            path = Path(value)
            dirs.append(path / "odlyzko" if (path / "odlyzko").is_dir() else path)
    if os.environ.get("SAGE_SHARE"):
        dirs.append(Path(os.environ["SAGE_SHARE"]) / "odlyzko")
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "odlyzko")
    dirs.extend(
        [
            BUNDLED_SOURCE,
            REPO_ROOT / "local" / "share" / "odlyzko",
            Path("/usr/share/odlyzko"),
            Path("/usr/local/share/odlyzko"),
        ]
    )
    return dirs


def _candidate_zeros6_files() -> list[Path]:
    files = []
    value = os.environ.get("SAGELITE_ODLYZKO_ZETA_ZEROS6")
    if value:
        files.append(Path(value))
    return files


def _candidate_spkg_tarballs() -> list[Path]:
    tarballs = []
    value = os.environ.get("SAGELITE_ODLYZKO_ZETA_SPKG")
    if value:
        tarballs.append(Path(value))
    upstream = REPO_ROOT / "upstream"
    tarballs.extend(sorted(upstream.glob("database_odlyzko_zeta-*.spkg")))
    tarballs.extend(sorted(upstream.glob("database_odlyzko_zeta-*.tar.*")))
    return tarballs


def _has_odlyzko_payload(path: Path) -> bool:
    return path.is_dir() and (path / "zeros.sobj").is_file()


def _find_database_dir() -> Path | None:
    for directory in _candidate_database_dirs():
        if _has_odlyzko_payload(directory):
            return directory.resolve()
    return None


def _write_zeros_sobj_from_text(source: Path, target: Path) -> None:
    try:
        from sage.all import save
    except Exception as error:
        raise RuntimeError(
            "building zeros.sobj from zeros6 requires importable Sage. "
            "Install sagelite first, or provide SAGELITE_ODLYZKO_ZETA_DATA_DIR "
            "containing zeros.sobj."
        ) from error

    zeros = [float(line) for line in source.read_text().splitlines() if line.strip()]
    target.parent.mkdir(parents=True, exist_ok=True)
    save(zeros, os.fspath(target))


def _extract_spkg(target: Path) -> bool:
    for tarball in _candidate_spkg_tarballs():
        if not tarball.is_file():
            continue
        with tarfile.open(tarball) as archive:
            sobj = next(
                (
                    item
                    for item in archive.getmembers()
                    if Path(item.name).name == "zeros.sobj" and item.isfile()
                ),
                None,
            )
            if sobj is not None:
                target.mkdir(parents=True, exist_ok=True)
                extracted = archive.extractfile(sobj)
                if extracted is None:
                    continue
                with (target / "zeros.sobj").open("wb") as output:
                    shutil.copyfileobj(extracted, output)
                return True

            zeros6 = next(
                (
                    item
                    for item in archive.getmembers()
                    if Path(item.name).name == "zeros6" and item.isfile()
                ),
                None,
            )
            if zeros6 is None:
                continue
            extracted = archive.extractfile(zeros6)
            if extracted is None:
                continue
            target.mkdir(parents=True, exist_ok=True)
            raw = target / "zeros6"
            with raw.open("wb") as output:
                shutil.copyfileobj(extracted, output)
            _write_zeros_sobj_from_text(raw, target / "zeros.sobj")
            raw.unlink()
            return True
    return False


def _copy_database(target: Path) -> None:
    shutil.rmtree(target, ignore_errors=True)
    source = _find_database_dir()
    if source is not None:
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / "zeros.sobj", target / "zeros.sobj")
    else:
        for zeros6 in _candidate_zeros6_files():
            if zeros6.is_file():
                _write_zeros_sobj_from_text(zeros6, target / "zeros.sobj")
                break
        else:
            if not _extract_spkg(target):
                searched = "\n  ".join(
                    os.fspath(path) for path in _candidate_database_dirs()
                )
                raise RuntimeError(
                    "could not find the Odlyzko zeta zero database. "
                    "Set SAGELITE_ODLYZKO_ZETA_DATA_DIR, "
                    "SAGELITE_ODLYZKO_ZETA_ZEROS6, or "
                    "SAGELITE_ODLYZKO_ZETA_SPKG.\n"
                    f"Searched:\n  {searched}"
                )

    if not _has_odlyzko_payload(target):
        raise RuntimeError("Odlyzko zeta zero database was not copied into the wheel")


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_odlyzko_zeta"
            / "data"
            / "odlyzko"
        )
        _copy_database(target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_database_odlyzko_zeta"
            / "data"
            / "odlyzko"
        )
        _copy_database(target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
