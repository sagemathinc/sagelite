from __future__ import annotations

import os
import shutil
import tarfile
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_mathjax_roots() -> list[Path]:
    roots = []
    for variable in ("SAGELITE_MATHJAX_DIR", "MATHJAX_DIR"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value))
    if os.environ.get("SAGE_SHARE"):
        roots.extend(
            [
                Path(os.environ["SAGE_SHARE"]) / "mathjax" / "mathjax",
                Path(os.environ["SAGE_SHARE"]) / "mathjax",
            ]
        )
    if os.environ.get("SAGE_LOCAL"):
        roots.extend(
            [
                Path(os.environ["SAGE_LOCAL"]) / "share" / "mathjax" / "mathjax",
                Path(os.environ["SAGE_LOCAL"]) / "share" / "mathjax",
            ]
        )
    roots.extend(
        [
            REPO_ROOT / "local" / "share" / "mathjax" / "mathjax",
            REPO_ROOT / "local" / "share" / "mathjax",
            Path("/usr/share/mathjax"),
            Path("/usr/local/share/mathjax"),
        ]
    )
    return roots


def _candidate_mathjax_tarballs() -> list[Path]:
    tarballs = []
    value = os.environ.get("SAGELITE_MATHJAX_TARBALL")
    if value:
        tarballs.append(Path(value))
    upstream = REPO_ROOT / "upstream"
    tarballs.extend(sorted(upstream.glob("mathjax-*.tar.*")))
    tarballs.extend(sorted(upstream.glob("mathjax-*.tgz")))
    return tarballs


def _looks_like_mathjax_root(root: Path) -> bool:
    return (root / "tex-chtml.js").is_file() and (root / "loader.js").is_file()


def _find_mathjax_root() -> Path | None:
    for root in _candidate_mathjax_roots():
        if _looks_like_mathjax_root(root):
            return root.resolve()
    return None


def _extract_mathjax_tarball(target: Path) -> bool:
    for tarball in _candidate_mathjax_tarballs():
        if not tarball.is_file():
            continue
        with tarfile.open(tarball) as archive:
            members = archive.getmembers()
            root = None
            for member in members:
                path = Path(member.name)
                if path.name == "tex-chtml.js":
                    root = path.parent
                    break
            if root is None:
                continue
            for member in members:
                path = Path(member.name)
                if root not in path.parents and path != root:
                    continue
                relative = path.relative_to(root)
                if not relative.parts:
                    continue
                member.name = os.fspath(relative)
                archive.extract(member, target)
        if _looks_like_mathjax_root(target):
            return True
        shutil.rmtree(target, ignore_errors=True)
    return False


def _searched_message() -> str:
    roots = "\n  ".join(os.fspath(root) for root in _candidate_mathjax_roots())
    tarballs = "\n  ".join(os.fspath(path) for path in _candidate_mathjax_tarballs())
    return (
        "could not find a MathJax runtime root containing tex-chtml.js and "
        "loader.js. Set SAGELITE_MATHJAX_DIR or SAGELITE_MATHJAX_TARBALL.\n"
        f"Searched roots:\n  {roots}\n"
        f"Searched tarballs:\n  {tarballs}"
    )


class build_py(_build_py):
    def run(self):
        target = (
            Path(self.build_lib)
            / "sagelite_mathjax_runtime"
            / "data"
            / "mathjax"
        )
        shutil.rmtree(target, ignore_errors=True)

        source = _find_mathjax_root()
        if source is not None:
            shutil.copytree(source, target, ignore_dangling_symlinks=True)
        elif not _extract_mathjax_tarball(target):
            raise RuntimeError(_searched_message())

        if not _looks_like_mathjax_root(target):
            raise RuntimeError("incomplete MathJax runtime copied")

        super().run()


setup(cmdclass={"build_py": build_py})
