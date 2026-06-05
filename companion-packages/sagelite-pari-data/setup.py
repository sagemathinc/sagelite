from __future__ import annotations

import os
import shutil
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

        if not copied:
            raise RuntimeError(f"no PARI data directories copied from {pari_root}")


setup(cmdclass={"build_py": build_py})
