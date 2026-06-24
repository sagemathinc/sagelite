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
    return (
        (root / "lib" / "init.g").is_file()
        and (root / "lib" / "system.g").is_file()
        and (root / "lib" / "package.gi").is_file()
    )


def _candidate_gap_roots() -> list[Path]:
    roots = []
    roots.extend(_split_roots(os.environ.get("SAGELITE_GAP_ROOTS")))
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


def _candidate_gap_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_GAP_BINDIR", "GAP_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_gap_executable() -> Path | None:
    for bindir in _candidate_gap_bindirs():
        command = bindir / "gap"
        if command.is_file():
            return command.resolve()
    return None


def _deduplicate_existing_roots(roots: list[Path]) -> list[Path]:
    seen = set()
    deduped = []
    for root in roots:
        root = root.resolve()
        if root in seen or not root.exists():
            continue
        seen.add(root)
        deduped.append(root)
    return deduped


def _looks_like_gap_package_root(root: Path) -> bool:
    pkg = root / "pkg"
    if not pkg.is_dir():
        return False
    return any(pkg.glob("*/PackageInfo.g"))


def _find_gap_roots() -> list[Path]:
    valid = []
    for root in _candidate_gap_roots():
        if _looks_like_gap_root(root) or _looks_like_gap_package_root(root):
            valid.append(root)

    roots = _deduplicate_existing_roots(valid)
    init_roots = [root for root in roots if _looks_like_gap_root(root)]
    package_only_roots = [root for root in roots if root not in init_roots]
    if init_roots:
        return init_roots + package_only_roots

    searched = "\n  ".join(os.fspath(root) for root in _candidate_gap_roots())
    raise RuntimeError(
        "could not find GAP 4 roots containing lib/init.g and package data. "
        "Set SAGELITE_GAP_ROOTS to the GAP roots built with sagelite.\n"
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
        gap_roots = _find_gap_roots()
        target = Path(self.build_lib) / "sagelite_gap_runtime" / "data"
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        for idx, gap_root in enumerate(gap_roots):
            shutil.copytree(
                gap_root,
                target / f"gap{idx}",
                ignore=_ignore_gap_files,
                ignore_dangling_symlinks=True,
            )

        gap_executable = _find_gap_executable()
        if gap_executable is not None:
            bin_target = target / "bin"
            bin_target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(gap_executable, bin_target / "gap")

        super().run()


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
