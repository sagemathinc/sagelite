from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_jmol_roots() -> list[Path]:
    roots = []
    for variable in ("SAGELITE_JMOL_DIR", "JMOL_DIR"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value))
    if os.environ.get("SAGE_SHARE"):
        roots.append(Path(os.environ["SAGE_SHARE"]) / "jmol")
    if os.environ.get("SAGE_LOCAL"):
        roots.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "jmol")
    roots.extend(
        [
            REPO_ROOT / "local" / "share" / "jmol",
            Path("/usr/share/jmol"),
            Path("/usr/local/share/jmol"),
        ]
    )
    return roots


def _jmol_data_root(root: Path) -> Path | None:
    if (root / "JmolData.jar").is_file():
        return root
    if (root / "src" / "JmolData.jar").is_file():
        return root / "src"
    return None


def _find_jmol_root() -> Path:
    for root in _candidate_jmol_roots():
        data_root = _jmol_data_root(root)
        if data_root is not None:
            return data_root.resolve()
    searched = "\n  ".join(os.fspath(root) for root in _candidate_jmol_roots())
    raise RuntimeError(
        "could not find a Jmol runtime root containing JmolData.jar. "
        "Set SAGELITE_JMOL_DIR.\n"
        f"Searched:\n  {searched}"
    )


class build_py(_build_py):
    def run(self):
        super().run()

        source = _find_jmol_root()
        target = Path(self.build_lib) / "sagelite_jmol_runtime" / "data" / "jmol"
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(source, target, ignore_dangling_symlinks=True)

        if _jmol_data_root(target) is None:
            raise RuntimeError(f"incomplete Jmol runtime copied from {source}")


setup(cmdclass={"build_py": build_py})
