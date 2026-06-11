from __future__ import annotations

import os
import shutil
import tarfile
from pathlib import PurePosixPath
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

PARI_DATA_DIRS = ("galdata", "elldata", "seadata", "galpol", "nftables")


def _candidate_pari_roots() -> list[Path]:
    roots = []
    for key in ("SAGELITE_PARI_DATA_DIR", "SAGELITE_PARI_DATADIR", "GP_DATA_DIR"):
        value = os.environ.get(key)
        if value:
            roots.append(Path(value))
    roots.extend(
        [
            Path("/usr/share/pari"),
            Path("/usr/local/share/pari"),
            Path("/host/sage-manylinux_2_28_x86_64/share/pari"),
            Path("/host/sage-manylinux_2_28_aarch64/share/pari"),
        ]
    )
    return roots


def _looks_like_pari_data_root(root: Path) -> bool:
    return any((root / name).is_dir() for name in PARI_DATA_DIRS)


def _find_pari_data_root() -> Path:
    for root in _candidate_pari_roots():
        if _looks_like_pari_data_root(root):
            return root.resolve()
    searched = "\n  ".join(os.fspath(root) for root in _candidate_pari_roots())
    raise RuntimeError(
        "could not find a PARI data root containing one of "
        f"{', '.join(PARI_DATA_DIRS)}. Set SAGELITE_PARI_DATA_DIR.\n"
        f"Searched:\n  {searched}"
    )


def _candidate_nftables_tarballs() -> list[Path]:
    tarballs = []
    for key in ("SAGELITE_PARI_NFTABLES_TARBALL", "SAGELITE_PARI_NFTABLES_SPKG"):
        value = os.environ.get(key)
        if value:
            tarballs.append(Path(value))
    return tarballs


def _safe_tar_relative_path(name: str) -> Path | None:
    parts = PurePosixPath(name).parts
    if not parts or parts[0] == "/" or ".." in parts:
        return None

    if "src" in parts:
        parts = parts[parts.index("src") + 1 :]
    elif len(parts) > 1:
        parts = parts[1:]

    if not parts:
        return None
    return Path(*parts)


def _extract_nftables_tarball(target: Path) -> bool:
    for tarball in _candidate_nftables_tarballs():
        if not tarball.is_file():
            continue

        copied = 0
        with tarfile.open(tarball) as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                relative = _safe_tar_relative_path(member.name)
                if relative is None:
                    continue

                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    continue
                with destination.open("wb") as output:
                    shutil.copyfileobj(source, output)
                copied += 1

        if copied:
            return True
    return False


class build_py(_build_py):
    def run(self):
        super().run()

        pari_root = _find_pari_data_root()
        target = Path(self.build_lib) / "sagelite_pari_data" / "data" / "pari"
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)

        copied = []
        for name in PARI_DATA_DIRS:
            source = pari_root / name
            if source.is_dir():
                shutil.copytree(source, target / name, ignore_dangling_symlinks=True)
                copied.append(name)

        if "nftables" not in copied and _extract_nftables_tarball(target / "nftables"):
            copied.append("nftables")

        missing = sorted(set(PARI_DATA_DIRS) - set(copied))
        if missing:
            raise RuntimeError(
                "incomplete PARI data payload copied into the wheel; missing "
                f"{', '.join(missing)} from {pari_root}. Set SAGELITE_PARI_DATA_DIR "
                "and SAGELITE_PARI_NFTABLES_TARBALL to complete the payload."
            )


setup(cmdclass={"build_py": build_py})
