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


EXECUTABLES = ("gp", "gphelp", "tex2mail")


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_PARI_BINDIR", "PARI_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_executables() -> dict[str, Path]:
    found = {}
    for bindir in _candidate_bindirs():
        for name in EXECUTABLES:
            if name in found:
                continue
            candidate = bindir / name
            if candidate.is_file() and os.access(candidate, os.X_OK):
                found[name] = candidate.resolve()
        if all(name in found for name in EXECUTABLES):
            return found
    missing = sorted(set(EXECUTABLES) - set(found))
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find PARI/GP executable(s): "
        f"{', '.join(missing)}. Set SAGELITE_PARI_BINDIR to the Sage-built "
        f"bin directory.\nSearched:\n  {searched}"
    )


def _prefix_for(executable: Path) -> Path:
    return executable.parent.parent


def _ldd_environment(prefix: Path) -> dict[str, str]:
    env = os.environ.copy()
    libdir = os.fspath(prefix / "lib")
    current = env.get("LD_LIBRARY_PATH")
    env["LD_LIBRARY_PATH"] = libdir if not current else f"{libdir}:{current}"
    return env


def _runtime_libraries(executables: dict[str, Path]) -> list[Path]:
    prefixes = (
        "libpari",
        "libgmp",
        "libreadline",
        "libtinfo",
        "libncurses",
    )
    libraries: dict[str, Path] = {}
    for executable in executables.values():
        prefix = _prefix_for(executable)
        output = subprocess.run(
            ["ldd", os.fspath(executable)],
            check=True,
            capture_output=True,
            text=True,
            env=_ldd_environment(prefix),
        ).stdout
        for line in output.splitlines():
            if "=>" not in line:
                continue
            name, rest = line.split("=>", 1)
            name = name.strip()
            if not name.startswith(prefixes):
                continue
            path = rest.strip().split(maxsplit=1)[0]
            if path == "not":
                candidate = prefix / "lib" / name
                if not candidate.exists():
                    raise RuntimeError(
                        f"could not resolve required PARI/GP library {name}"
                    )
                library = candidate
            else:
                library = Path(path)
            libraries.setdefault(name, library)
    return list(libraries.values())


def _write_wrapper(path: Path, real_name: str) -> None:
    path.write_text(
        "#!/bin/sh\n"
        'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
        'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
        'PATH="$HERE${PATH:+:$PATH}"\n'
        "export LD_LIBRARY_PATH PATH\n"
        f'exec "$HERE/{real_name}" "$@"\n'
    )
    path.chmod(0o755)


class build_py(_build_py):
    def run(self):
        executables = _find_executables()
        target = Path(self.build_lib) / "sagelite_pari" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_pari" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        for name, source in executables.items():
            real_name = f"{name}-real"
            shutil.copy2(source, target / real_name)
            _write_wrapper(target / name, real_name)

        for library in _runtime_libraries(executables):
            shutil.copy2(library, lib_target / library.name)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_PARI_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
