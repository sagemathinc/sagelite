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


def _candidate_gap3_roots() -> list[Path]:
    roots = []
    for variable in ("SAGELITE_GAP3_ROOT", "GAP3_ROOT"):
        if os.environ.get(variable):
            roots.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        roots.append(Path(os.environ["SAGE_LOCAL"]) / "gap3" / "latest" / "gap3")
    return roots


def _looks_like_gap3_root(root: Path) -> bool:
    return (root / "bin" / "gap.sh").is_file() and (root / "lib" / "init.g").is_file()


def _find_gap3_root() -> Path:
    for root in _candidate_gap3_roots():
        if _looks_like_gap3_root(root):
            return root.resolve()

    searched = "\n  ".join(os.fspath(root) for root in _candidate_gap3_roots())
    raise RuntimeError(
        "could not find a GAP3 root containing bin/gap.sh and lib/init.g. "
        "Set SAGELITE_GAP3_ROOT to the GAP3 root built with sagelite.\n"
        f"Searched:\n  {searched}"
    )


def _ignore_gap3_files(directory: str, names: list[str]) -> set[str]:
    ignored = {
        "__pycache__",
        "htm",
        "manual.pdf",
    }
    ignored.update(
        name
        for name in names
        if name.endswith((".pyc", ".pyo", ".html", ".htm", ".pdf"))
    )
    return ignored


class build_py(_build_py):
    def run(self):
        super().run()

        gap3_root = _find_gap3_root()
        target = Path(self.build_lib) / "sagelite_gap3" / "data" / "gap3"
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(
            gap3_root,
            target,
            ignore=_ignore_gap3_files,
            ignore_dangling_symlinks=True,
        )


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_GAP3_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
