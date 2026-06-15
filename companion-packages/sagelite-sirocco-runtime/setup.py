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
    for variable in ("SAGELITE_SIROCCO_PREFIX", "SIROCCO_PREFIX"):
        if os.environ.get(variable):
            prefixes.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        prefixes.append(Path(os.environ["SAGE_LOCAL"]))
    prefixes.extend([Path("/usr"), Path("/usr/local")])
    return prefixes


def _library_dirs(prefix: Path) -> tuple[Path, ...]:
    return (prefix / "lib", prefix / "lib64")


def _libsirocco_files(prefix: Path) -> list[Path]:
    libraries: list[Path] = []
    for libdir in _library_dirs(prefix):
        libraries.extend(
            path
            for path in libdir.glob("libsirocco*")
            if path.is_file() and path.suffix != ".la"
        )
    return sorted(libraries)


def _find_sirocco_prefix() -> Path:
    for prefix in _candidate_prefixes():
        if (prefix / "include" / "sirocco.h").is_file() and _libsirocco_files(prefix):
            return prefix.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_prefixes())
    raise RuntimeError(
        "could not find SIROCCO headers and libsirocco. "
        "Set SAGELITE_SIROCCO_PREFIX to the Sage-built runtime prefix.\n"
        f"Searched:\n  {searched}"
    )


class build_py(_build_py):
    def run(self):
        prefix = _find_sirocco_prefix()
        data_root = Path(self.build_lib) / "sagelite_sirocco" / "data"
        include_target = data_root / "include"
        lib_target = data_root / "lib"
        shutil.rmtree(data_root, ignore_errors=True)
        include_target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        shutil.copy2(prefix / "include" / "sirocco.h", include_target / "sirocco.h")
        for library in _libsirocco_files(prefix):
            shutil.copy2(library, lib_target / library.name)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_SIROCCO_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
