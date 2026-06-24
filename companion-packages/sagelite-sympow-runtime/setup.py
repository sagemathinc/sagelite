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


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_SYMPOW_BINDIR", "SYMPOW_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        candidate = bindir / "sympow"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a sympow executable. Set SAGELITE_SYMPOW_BINDIR "
        f"to the Sage-built bin directory.\nSearched:\n  {searched}"
    )


def _candidate_datafiles(executable: Path) -> list[Path]:
    files = []
    if os.environ.get("SAGELITE_SYMPOW_DATAFILES"):
        files.append(Path(os.environ["SAGELITE_SYMPOW_DATAFILES"]))
    if os.environ.get("SAGE_LOCAL"):
        sage_local = Path(os.environ["SAGE_LOCAL"])
        files.extend(
            [
                sage_local / "share" / "sympow" / "datafiles",
                sage_local / "var" / "lib" / "sympow" / "datafiles",
                sage_local / "var" / "cache" / "sympow" / "datafiles",
            ]
        )
    files.extend(
        [
            executable.parent / "datafiles",
            executable.parent.parent / "share" / "sympow" / "datafiles",
            Path("/usr/share/sympow/datafiles"),
            Path("/usr/local/share/sympow/datafiles"),
        ]
    )
    return files


def _candidate_libdirs(executable: Path) -> list[Path]:
    dirs = []
    if os.environ.get("SAGELITE_SYMPOW_LIBDIR"):
        dirs.append(Path(os.environ["SAGELITE_SYMPOW_LIBDIR"]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "lib" / "sympow")
    dirs.extend(
        [
            executable.parent / "sympow",
            executable.parent.parent / "lib" / "sympow",
            Path("/usr/lib/sympow"),
            Path("/usr/local/lib/sympow"),
        ]
    )
    return dirs


def _find_datafiles(executable: Path) -> Path | None:
    for path in _candidate_datafiles(executable):
        if path.is_dir():
            return path.resolve()
    return None


def _find_libdir(executable: Path) -> Path | None:
    for path in _candidate_libdirs(executable):
        if (path / "new_data").is_file():
            return path.resolve()
    return None


def _patch_new_data_script(script: Path) -> None:
    text = script.read_text()
    text = text.replace("GP=$2\n", "GP=${SYMPOW_GP:-$2}\n")
    script.write_text(text)
    script.chmod(0o755)


def _runtime_libraries(executable: Path) -> list[Path]:
    output = subprocess.run(
        ["ldd", os.fspath(executable)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries = []
    prefixes = ("libpari", "libgmp.so", "libmpfr.so", "libm.so")
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
        source = _find_executable()
        target = Path(self.build_lib) / "sagelite_sympow" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_sympow" / "data" / "lib"
        data_target = Path(self.build_lib) / "sagelite_sympow" / "data" / "datafiles"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        shutil.rmtree(data_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target / "sympow-real")
        wrapper = target / "sympow"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            'SYMPOW_PKGDATADIR="${SYMPOW_PKGDATADIR:-$HERE/../datafiles}"\n'
            'SYMPOW_PKGLIBDIR="${SYMPOW_PKGLIBDIR:-$HERE/../lib/sympow}"\n'
            'SYMPOW_CACHEDIR="${SYMPOW_CACHEDIR:-${XDG_CACHE_HOME:-${HOME:-/tmp}}/sagelite-sympow}"\n'
            'SYMPOW_PKGCACHEDIR="${SYMPOW_PKGCACHEDIR:-$SYMPOW_CACHEDIR}"\n'
            'if [ -z "${SYMPOW_GP:-}" ]; then\n'
            '  if [ -n "${SAGE_GP_COMMAND:-}" ]; then\n'
            '    SYMPOW_GP="$SAGE_GP_COMMAND"\n'
            '  elif [ -x "$HERE/../../../sagelite_pari/data/bin/gp" ]; then\n'
            '    SYMPOW_GP="$HERE/../../../sagelite_pari/data/bin/gp"\n'
            '  elif command -v gp >/dev/null 2>&1; then\n'
            '    SYMPOW_GP="$(command -v gp)"\n'
            "  fi\n"
            "fi\n"
            'mkdir -p "$SYMPOW_CACHEDIR"\n'
            "export LD_LIBRARY_PATH SYMPOW_PKGDATADIR SYMPOW_PKGLIBDIR SYMPOW_CACHEDIR SYMPOW_PKGCACHEDIR SYMPOW_GP\n"
            'cd "$HERE/.." || exit 127\n'
            'exec "$HERE/sympow-real" "$@"\n'
        )
        wrapper.chmod(0o755)
        for library in _runtime_libraries(source):
            shutil.copy2(library, lib_target / library.name)

        datafiles = _find_datafiles(source)
        if datafiles is not None:
            shutil.copytree(datafiles, data_target, ignore_dangling_symlinks=True)

        libdir = _find_libdir(source)
        if libdir is not None:
            helper_target = lib_target / "sympow"
            shutil.copytree(libdir, helper_target, ignore_dangling_symlinks=True)
            new_data = helper_target / "new_data"
            if new_data.is_file():
                _patch_new_data_script(new_data)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_SYMPOW_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
