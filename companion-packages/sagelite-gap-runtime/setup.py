from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover - wheel is a build requirement
    _bdist_wheel = None


def _split_roots(value: str | None) -> list[Path]:
    if not value:
        return []
    roots = []
    for root in value.replace(os.pathsep, ";").split(";"):
        root = root.strip()
        if root:
            roots.append(Path(root))
    return roots


def _looks_like_gap_root(root: Path) -> bool:
    return (root / "lib" / "init.g").is_file()


def _candidate_gap_roots() -> list[Path]:
    roots = []
    roots.extend(_split_roots(os.environ.get("SAGELITE_GAP_ROOT")))
    roots.extend(_split_roots(os.environ.get("GAP_ROOT_PATHS")))
    roots.extend(
        [
            Path("/usr/share/gap"),
            Path("/usr/local/share/gap"),
            Path("/usr/lib/gap"),
            Path("/usr/local/lib/gap"),
        ]
    )
    return roots


def _find_gap_root() -> Path:
    for root in _candidate_gap_roots():
        if _looks_like_gap_root(root):
            return root

    searched = "\n  ".join(os.fspath(root) for root in _candidate_gap_roots())
    raise RuntimeError(
        "could not find a GAP root containing lib/init.g. "
        "Set SAGELITE_GAP_ROOT to the GAP root built with sagelite.\n"
        f"Searched:\n  {searched}"
    )


def _ignore_gap_files(directory: str, names: list[str]) -> set[str]:
    ignored = {
        "__pycache__",
        "doc",
        "docs",
        "example",
        "examples",
        "htm",
        "mathjax",
        "test",
        "tests",
        "tst",
    }
    ignored.update(
        name
        for name in names
        if name.endswith((".pyc", ".pyo", ".pdf", ".html", ".htm", ".css", ".js"))
    )
    return ignored


class build_py(_build_py):
    def run(self):
        super().run()

        gap_root = _find_gap_root()
        target = Path(self.build_lib) / "sagelite_gap_runtime" / "data" / "gap"
        shutil.rmtree(target, ignore_errors=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(gap_root, target, ignore=_ignore_gap_files, ignore_dangling_symlinks=True)


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_GAP_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
