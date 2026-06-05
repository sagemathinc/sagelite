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


def _candidate_prefixes() -> list[Path]:
    roots = []
    if os.environ.get("SAGELITE_MAXIMA_PREFIX"):
        roots.append(Path(os.environ["SAGELITE_MAXIMA_PREFIX"]))
    if os.environ.get("MAXIMA_PREFIX"):
        roots.append(Path(os.environ["MAXIMA_PREFIX"]))
    roots.extend(Path("/usr/share").glob("maxima-sage/*"))
    roots.extend(Path("/usr/share").glob("maxima/*"))
    roots.extend(Path("/usr/local/share").glob("maxima/*"))
    return roots


def _candidate_fas_files() -> list[Path]:
    files = []
    if os.environ.get("SAGELITE_MAXIMA_FAS"):
        files.append(Path(os.environ["SAGELITE_MAXIMA_FAS"]))
    if os.environ.get("MAXIMA_FAS"):
        files.append(Path(os.environ["MAXIMA_FAS"]))
    files.extend(
        [
            Path("/usr/lib/ecl/maxima.fas"),
            Path("/usr/local/lib/ecl/maxima.fas"),
        ]
    )
    return files


def _looks_like_maxima_prefix(path: Path) -> bool:
    return (path / "src").is_dir() and (path / "share").is_dir()


def _find_maxima_prefix() -> Path:
    for prefix in _candidate_prefixes():
        if _looks_like_maxima_prefix(prefix):
            return prefix.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_prefixes())
    raise RuntimeError(
        "could not find a Maxima prefix containing src/ and share/. "
        "Set SAGELITE_MAXIMA_PREFIX to the Sage-built Maxima share directory.\n"
        f"Searched:\n  {searched}"
    )


def _find_maxima_fas() -> Path:
    for fas in _candidate_fas_files():
        if fas.is_file():
            return fas.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_fas_files())
    raise RuntimeError(
        "could not find maxima.fas. Set SAGELITE_MAXIMA_FAS to the matching "
        f"Sage-built ECL Maxima image.\nSearched:\n  {searched}"
    )


def _ignore_maxima_files(directory: str, names: list[str]) -> set[str]:
    ignored = {
        "__pycache__",
        "doc",
        "html",
        "locale",
        "tests",
        "xmaxima",
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

        maxima_prefix = _find_maxima_prefix()
        maxima_fas = _find_maxima_fas()
        target = Path(self.build_lib) / "sagelite_maxima" / "data"
        shutil.rmtree(target, ignore_errors=True)

        share_target = target / "share" / "maxima" / maxima_prefix.name
        share_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            maxima_prefix,
            share_target,
            ignore=_ignore_maxima_files,
            ignore_dangling_symlinks=True,
        )

        fas_target = target / "lib" / "ecl" / "maxima.fas"
        fas_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(maxima_fas, fas_target)


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_MAXIMA_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
