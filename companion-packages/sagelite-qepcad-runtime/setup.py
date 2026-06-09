from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


def _candidate_roots() -> list[Path]:
    roots = []
    for variable in ("SAGELITE_QEPCAD_ROOT", "QEPCAD_ROOT", "SAGE_LOCAL"):
        if os.environ.get(variable):
            roots.append(Path(os.environ[variable]))
    roots.extend([Path("/usr"), Path("/usr/local")])
    return roots


def _valid_root(root: Path) -> bool:
    return (
        (root / "bin" / "qepcad").is_file()
        and (root / "share" / "qepcad" / "qepcad.help").is_file()
        and (root / "etc" / "default.qepcadrc").is_file()
    )


def _find_root() -> Path:
    for root in _candidate_roots():
        if _valid_root(root):
            return root.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_roots())
    raise RuntimeError(
        "could not find a QEPCAD root containing bin/qepcad, "
        "share/qepcad/qepcad.help, and etc/default.qepcadrc. "
        "Set SAGELITE_QEPCAD_ROOT to the Sage-built local directory.\n"
        f"Searched:\n  {searched}"
    )


def _copy_runtime(root: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)

    (target / "bin").mkdir(parents=True, exist_ok=True)
    (target / "etc").mkdir(parents=True, exist_ok=True)
    (target / "share" / "qepcad").mkdir(parents=True, exist_ok=True)

    shutil.copy2(root / "bin" / "qepcad", target / "bin" / "qepcad")
    shutil.copy2(
        root / "share" / "qepcad" / "qepcad.help",
        target / "share" / "qepcad" / "qepcad.help",
    )
    shutil.copy2(
        root / "etc" / "default.qepcadrc",
        target / "etc" / "default.qepcadrc",
    )


class build_py(_build_py):
    def run(self):
        super().run()
        root = _find_root()
        target = Path(self.build_lib) / "sagelite_qepcad" / "data" / "root"
        _copy_runtime(root, target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_qepcad"
            / "data"
            / "root"
        )
        _copy_runtime(_find_root(), target)


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:
    _bdist_wheel = None


cmdclass = {"build_py": build_py, "sdist": sdist}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_QEPCAD_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
