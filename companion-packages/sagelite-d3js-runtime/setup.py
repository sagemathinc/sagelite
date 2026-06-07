from __future__ import annotations

import os
import shutil
import tarfile
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_d3js_roots() -> list[Path]:
    roots = []
    for variable in ("SAGELITE_D3JS_DIR", "D3JS_DIR"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value))
    if os.environ.get("SAGE_SHARE"):
        roots.append(Path(os.environ["SAGE_SHARE"]) / "d3js")
    if os.environ.get("SAGE_LOCAL"):
        roots.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "d3js")
    roots.extend(
        [
            REPO_ROOT / "local" / "share" / "d3js",
            Path("/usr/share/d3js"),
            Path("/usr/local/share/d3js"),
        ]
    )
    return roots


def _candidate_d3js_tarballs() -> list[Path]:
    tarballs = []
    value = os.environ.get("SAGELITE_D3JS_TARBALL")
    if value:
        tarballs.append(Path(value))
    upstream = REPO_ROOT / "upstream"
    tarballs.extend(sorted(upstream.glob("d3js-*.tar.*")))
    tarballs.extend(sorted(upstream.glob("d3js-*.tgz")))
    return tarballs


def _looks_like_d3js_root(root: Path) -> bool:
    return (root / "d3.min.js").is_file()


def _find_d3js_root() -> Path:
    for root in _candidate_d3js_roots():
        if _looks_like_d3js_root(root):
            return root.resolve()
    searched = "\n  ".join(os.fspath(root) for root in _candidate_d3js_roots())
    raise RuntimeError(
        "could not find a D3.js runtime root containing d3.min.js. "
        "Set SAGELITE_D3JS_DIR.\n"
        f"Searched:\n  {searched}"
    )


def _extract_d3js_tarball(target: Path) -> bool:
    for tarball in _candidate_d3js_tarballs():
        if not tarball.is_file():
            continue
        with tarfile.open(tarball) as archive:
            member = next(
                (
                    member
                    for member in archive.getmembers()
                    if Path(member.name).name == "d3.min.js"
                ),
                None,
            )
            if member is None:
                continue
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            target.mkdir(parents=True, exist_ok=True)
            with (target / "d3.min.js").open("wb") as output:
                shutil.copyfileobj(extracted, output)
            return True
    return False


class build_py(_build_py):
    def run(self):
        super().run()

        target = Path(self.build_lib) / "sagelite_d3js_runtime" / "data" / "d3js"
        shutil.rmtree(target, ignore_errors=True)

        if not _extract_d3js_tarball(target):
            source = _find_d3js_root()
            shutil.copytree(source, target, ignore_dangling_symlinks=True)

        if not _looks_like_d3js_root(target):
            raise RuntimeError("incomplete D3.js runtime copied into the wheel")


setup(cmdclass={"build_py": build_py})
