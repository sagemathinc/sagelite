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
    prefixes = []
    for variable in ("SAGELITE_TIDES_PREFIX", "TIDES_PREFIX"):
        if os.environ.get(variable):
            prefixes.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        prefixes.append(Path(os.environ["SAGE_LOCAL"]))
    prefixes.extend([Path("/usr"), Path("/usr/local")])
    return prefixes


def _find_tides_prefix() -> Path:
    for prefix in _candidate_prefixes():
        if (prefix / "lib" / "libTIDES.a").is_file() and (
            prefix / "include" / "minc_tides.h"
        ).is_file():
            return prefix.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_prefixes())
    raise RuntimeError(
        "could not find TIDES headers and libTIDES.a. "
        "Set SAGELITE_TIDES_PREFIX to the Sage-built runtime prefix.\n"
        f"Searched:\n  {searched}"
    )


class build_py(_build_py):
    def run(self):
        prefix = _find_tides_prefix()
        data_root = Path(self.build_lib) / "sagelite_tides" / "data"
        include_target = data_root / "include"
        lib_target = data_root / "lib"
        shutil.rmtree(data_root, ignore_errors=True)
        include_target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        shutil.copy2(prefix / "lib" / "libTIDES.a", lib_target / "libTIDES.a")
        for header in ("minc_tides.h", "mp_tides.h"):
            source = prefix / "include" / header
            if source.is_file():
                shutil.copy2(source, include_target / header)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_TIDES_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
