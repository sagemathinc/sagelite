from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover - wheel is a build requirement
    _bdist_wheel = None


def _candidate_prefixes() -> list[Path]:
    prefixes = []
    for variable in ("SAGELITE_INFO_PREFIX", "SAGE_LOCAL"):
        if os.environ.get(variable):
            prefixes.append(Path(os.environ[variable]))
    prefixes.extend([Path("/usr"), Path("/usr/local")])
    return prefixes


def _find_prefix() -> Path:
    for prefix in _candidate_prefixes():
        if (prefix / "bin" / "info").is_file() and (
            prefix / "share" / "info" / "singular.info"
        ).is_file():
            return prefix.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_prefixes())
    raise RuntimeError(
        "could not find a GNU Info prefix containing bin/info and "
        "share/info/singular.info. Set SAGELITE_INFO_PREFIX.\n"
        f"Searched:\n  {searched}"
    )


def _runtime_libraries(executable: Path) -> list[Path]:
    output = subprocess.run(
        ["ldd", os.fspath(executable)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries = []
    prefixes = ("libreadline", "libtinfo", "libncurses", "libz")
    for line in output.splitlines():
        if "=>" not in line:
            continue
        name, rest = line.split("=>", 1)
        name = name.strip()
        path = rest.strip().split(maxsplit=1)[0]
        if name.startswith(prefixes) and path != "not":
            libraries.append(Path(path))
    return libraries


class build_py(_build_py):
    def run(self):
        prefix = _find_prefix()
        target = Path(self.build_lib) / "sagelite_info" / "data"
        bin_target = target / "bin"
        lib_target = target / "lib"
        share_target = target / "share" / "info"
        shutil.rmtree(target, ignore_errors=True)
        bin_target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        source = prefix / "bin" / "info"
        shutil.copy2(source, bin_target / "info-real")
        wrapper = bin_target / "info"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            'INFOPATH="$HERE/../share/info${INFOPATH:+:$INFOPATH}"\n'
            "export LD_LIBRARY_PATH INFOPATH\n"
            'exec "$HERE/info-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        libraries: dict[str, Path] = {}
        for library in _runtime_libraries(source):
            libraries.setdefault(library.name, library)
        for library in libraries.values():
            shutil.copy2(library, lib_target / library.name)

        shutil.copytree(
            prefix / "share" / "info",
            share_target,
            ignore_dangling_symlinks=True,
        )

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_INFO_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
