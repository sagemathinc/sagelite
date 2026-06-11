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
    for variable in ("SAGELITE_ECL_PREFIX", "SAGE_LOCAL"):
        if os.environ.get(variable):
            prefixes.append(Path(os.environ[variable]))
    prefixes.extend([Path("/usr"), Path("/usr/local")])
    return prefixes


def _looks_like_ecl_prefix(prefix: Path) -> bool:
    return (
        (prefix / "bin" / "ecl").is_file()
        and (prefix / "bin" / "ecl-config").is_file()
        and (prefix / "include" / "ecl" / "ecl.h").is_file()
        and any(path.is_dir() for path in (prefix / "lib").glob("ecl-*"))
    )


def _find_prefix() -> Path:
    for prefix in _candidate_prefixes():
        if _looks_like_ecl_prefix(prefix):
            return prefix.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_prefixes())
    raise RuntimeError(
        "could not find an ECL prefix containing bin/ecl, bin/ecl-config, "
        "include/ecl/ecl.h, and lib/ecl-*. Set SAGELITE_ECL_PREFIX.\n"
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
    prefixes = ("libecl", "libgmp", "libgc", "libffi")
    for line in output.splitlines():
        if "=>" not in line:
            continue
        name, rest = line.split("=>", 1)
        name = name.strip()
        path = rest.strip().split(maxsplit=1)[0]
        if name.startswith(prefixes) and path != "not":
            libraries.append(Path(path))
    return libraries


def _copy_runtime_libraries(prefix: Path, executable: Path, target: Path) -> None:
    libraries: dict[str, Path] = {}
    for library in _runtime_libraries(executable):
        libraries.setdefault(library.name, library)

    for library in (prefix / "lib").glob("libecl.so*"):
        libraries.setdefault(library.name, library)

    for library in libraries.values():
        if library.is_file() or library.is_symlink():
            shutil.copy2(library.resolve(), target / library.name)

    for archive in (prefix / "lib").glob("ecl-*/lib*.a"):
        shutil.copy2(archive, target / archive.name)

    sonames = {path.name for path in target.iterdir()}
    if "libecl.so" not in sonames:
        libecl = sorted(
            path for path in target.glob("libecl.so*") if path.name != "libecl.so"
        )
        if libecl:
            shutil.copy2(libecl[-1], target / "libecl.so")


def _write_ecl_wrapper(path: Path, ecl_dir_name: str) -> None:
    path.write_text(
        "#!/bin/sh\n"
        'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
        'PREFIX="$(dirname "$HERE")"\n'
        f'export ECLDIR="${{ECLDIR:-$PREFIX/lib/{ecl_dir_name}/}}"\n'
        'LD_LIBRARY_PATH="$PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
        "export LD_LIBRARY_PATH\n"
        'exec "$HERE/ecl-real" "$@"\n'
    )
    path.chmod(0o755)


def _write_ecl_config(path: Path) -> None:
    path.write_text(
        """#!/bin/sh
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PREFIX="$(dirname "$HERE")"
LDFLAGS="-lecl"
for arg in "$@"; do
  case "$arg" in
    --cflags|-c)
      echo_cflags=yes
      ;;
    --libs|--ldflags|-l)
      echo_ldflags=yes
      ;;
    cmp)
      LDFLAGS="$LDFLAGS -lcmp"
      ;;
    *)
      echo "Usage: $0 [--cflags] [--libs|--ldflags] [cmp]" >&2
      exit 1
      ;;
  esac
done

if [ "$echo_cflags" = yes ]; then
  echo "-Dlinux -I$PREFIX/include"
fi

if [ "$echo_ldflags" = yes ]; then
  echo "-Wl,--rpath,$PREFIX/lib -L$PREFIX/lib $LDFLAGS -Wl,-rpath-link,$PREFIX/lib -lpthread -ldl -lm"
fi
"""
    )
    path.chmod(0o755)


class build_py(_build_py):
    def run(self):
        prefix = _find_prefix()
        ecl_dir = sorted(
            path for path in (prefix / "lib").glob("ecl-*") if path.is_dir()
        )[-1]
        target = Path(self.build_lib) / "sagelite_ecl" / "data"
        bin_target = target / "bin"
        include_target = target / "include" / "ecl"
        lib_target = target / "lib"
        shutil.rmtree(target, ignore_errors=True)
        bin_target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        shutil.copy2(prefix / "bin" / "ecl", bin_target / "ecl-real")
        _write_ecl_wrapper(bin_target / "ecl", ecl_dir.name)
        _write_ecl_config(bin_target / "ecl-config")

        shutil.copytree(
            prefix / "include" / "ecl",
            include_target,
            ignore_dangling_symlinks=True,
        )
        shutil.copytree(
            ecl_dir, lib_target / ecl_dir.name, ignore_dangling_symlinks=True
        )
        _copy_runtime_libraries(prefix, prefix / "bin" / "ecl", lib_target)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_ECL_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
