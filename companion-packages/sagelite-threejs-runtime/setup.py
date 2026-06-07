from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_threejs_roots() -> list[Path]:
    roots = []
    for variable in ("SAGELITE_THREEJS_DIR", "THREEJS_DIR"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value))
    if os.environ.get("SAGE_SHARE"):
        roots.append(Path(os.environ["SAGE_SHARE"]) / "threejs-sage")
    if os.environ.get("SAGE_LOCAL"):
        roots.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "threejs-sage")
    roots.extend(
        [
            REPO_ROOT / "local" / "share" / "threejs-sage",
            Path("/usr/share/threejs-sage"),
            Path("/usr/local/share/threejs-sage"),
        ]
    )
    return roots


def _looks_like_threejs_root(root: Path) -> bool:
    version_file = root / "version"
    if not version_file.is_file():
        return False
    version = version_file.read_text(encoding="utf-8").strip()
    return bool(version) and (root / version / "three.min.js").is_file()


def _find_threejs_root() -> Path:
    for root in _candidate_threejs_roots():
        if _looks_like_threejs_root(root):
            return root.resolve()
    searched = "\n  ".join(os.fspath(root) for root in _candidate_threejs_roots())
    raise RuntimeError(
        "could not find a threejs-sage runtime root containing a version file "
        "and <version>/three.min.js. Set SAGELITE_THREEJS_DIR.\n"
        f"Searched:\n  {searched}"
    )


class build_py(_build_py):
    def run(self):
        source = _find_threejs_root()
        target = (
            Path(self.build_lib)
            / "sagelite_threejs_runtime"
            / "data"
            / "threejs-sage"
        )
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(source, target, ignore_dangling_symlinks=True)

        if not _looks_like_threejs_root(target):
            raise RuntimeError(f"incomplete threejs-sage runtime copied from {source}")

        super().run()


setup(cmdclass={"build_py": build_py})
