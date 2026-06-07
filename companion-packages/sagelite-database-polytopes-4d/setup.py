from __future__ import annotations

import os
import shutil
import tarfile
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_hodge4d_roots() -> list[Path]:
    roots = []
    for variable in ("SAGELITE_POLYTOPES_4D_DIR", "POLYTOPES_4D_DIR"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value))
    if os.environ.get("SAGE_SHARE"):
        roots.append(Path(os.environ["SAGE_SHARE"]) / "reflexive_polytopes" / "Hodge4d")
    if os.environ.get("SAGE_LOCAL"):
        roots.append(
            Path(os.environ["SAGE_LOCAL"]) / "share" / "reflexive_polytopes" / "Hodge4d"
        )
    roots.extend(
        [
            REPO_ROOT / "local" / "share" / "reflexive_polytopes" / "Hodge4d",
            Path("/usr/share/reflexive_polytopes/Hodge4d"),
            Path("/usr/local/share/reflexive_polytopes/Hodge4d"),
        ]
    )
    return roots


def _candidate_spkg_tarballs() -> list[Path]:
    tarballs = []
    value = os.environ.get("SAGELITE_POLYTOPES_4D_SPKG")
    if value:
        tarballs.append(Path(value))
    upstream = REPO_ROOT / "upstream"
    tarballs.extend(sorted(upstream.glob("polytopes_db_4d-*.spkg")))
    tarballs.extend(sorted(upstream.glob("polytopes_db_4d-*.tar.*")))
    return tarballs


def _looks_like_hodge4d_root(root: Path) -> bool:
    return root.is_dir() and any(root.iterdir())


def _find_hodge4d_root() -> Path:
    for root in _candidate_hodge4d_roots():
        candidate = root / "Hodge4d" if root.name != "Hodge4d" else root
        if _looks_like_hodge4d_root(candidate):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(root) for root in _candidate_hodge4d_roots())
    raise RuntimeError(
        "could not find the 4-dimensional reflexive polytope database Hodge4d "
        "directory. Set SAGELITE_POLYTOPES_4D_DIR.\n"
        f"Searched:\n  {searched}"
    )


def _extract_hodge4d_spkg(target: Path) -> bool:
    for tarball in _candidate_spkg_tarballs():
        if not tarball.is_file():
            continue
        with tarfile.open(tarball) as archive:
            members = [
                member
                for member in archive.getmembers()
                if "/Hodge4d/" in f"/{member.name}/" and member.isfile()
            ]
            if not members:
                continue
            for member in members:
                parts = Path(member.name).parts
                hodge_index = parts.index("Hodge4d")
                relative = Path(*parts[hodge_index + 1 :])
                if not relative.parts:
                    continue
                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                extracted = archive.extractfile(member)
                if extracted is None:
                    continue
                with destination.open("wb") as output:
                    shutil.copyfileobj(extracted, output)
            return True
    return False


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_database_polytopes_4d"
            / "data"
            / "reflexive_polytopes"
            / "Hodge4d"
        )
        shutil.rmtree(target, ignore_errors=True)

        if not _extract_hodge4d_spkg(target):
            source = _find_hodge4d_root()
            shutil.copytree(source, target, ignore_dangling_symlinks=True)

        if not _looks_like_hodge4d_root(target):
            raise RuntimeError("incomplete Hodge4d database copied into the wheel")


setup(cmdclass={"build_py": build_py})
