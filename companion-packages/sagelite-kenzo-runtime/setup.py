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


def _candidate_kenzo_fas() -> list[Path]:
    candidates = []
    for variable in ("SAGELITE_KENZO_FAS", "KENZO_FAS"):
        if os.environ.get(variable):
            candidates.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        candidates.append(Path(os.environ["SAGE_LOCAL"]) / "lib" / "ecl" / "kenzo.fas")
    candidates.extend(
        [
            Path("/usr/lib/ecl/kenzo.fas"),
            Path("/usr/local/lib/ecl/kenzo.fas"),
        ]
    )
    return candidates


def _find_kenzo_fas() -> Path:
    for candidate in _candidate_kenzo_fas():
        if candidate.is_file():
            return candidate.resolve()

    searched = "\n  ".join(os.fspath(path) for path in _candidate_kenzo_fas())
    raise RuntimeError(
        "could not find kenzo.fas. Set SAGELITE_KENZO_FAS to the Sage-built "
        f"Kenzo ECL image.\nSearched:\n  {searched}"
    )


class build_py(_build_py):
    def run(self):
        super().run()

        source = _find_kenzo_fas()
        target = Path(self.build_lib) / "sagelite_kenzo" / "data" / "kenzo.fas"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_KENZO_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
