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
    for variable in ("SAGELITE_IMAGEMAGICK_BINDIR", "IMAGEMAGICK_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _program_path(bindir: Path, program: str) -> Path | None:
    candidate = bindir / program
    if candidate.is_file() and os.access(candidate, os.X_OK):
        return candidate.resolve()
    return None


def _find_executables() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for bindir in _candidate_bindirs():
        for program in ("magick", "convert"):
            if program in found:
                continue
            source = _program_path(bindir, program)
            if source is not None:
                found[program] = source
        if found:
            break
    if found:
        return found

    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a magick or convert executable. "
        "Set SAGELITE_IMAGEMAGICK_BINDIR to the Sage-built bin directory.\n"
        f"Searched:\n  {searched}"
    )


def _runtime_libraries(executables: dict[str, Path]) -> list[Path]:
    libraries: dict[str, Path] = {}
    skipped = (
        "ld-linux",
        "libanl.",
        "libc.",
        "libdl.",
        "libgcc_s.",
        "libm.",
        "libpthread.",
        "libresolv.",
        "librt.",
        "libstdc++.",
    )

    for executable in executables.values():
        output = subprocess.run(
            ["ldd", os.fspath(executable)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        for line in output.splitlines():
            if "=>" not in line:
                continue
            name, rest = line.split("=>", 1)
            name = name.strip()
            path = rest.strip().split(maxsplit=1)[0]
            if path == "not" or name.startswith(skipped):
                continue
            library = Path(path)
            if library.is_file():
                libraries.setdefault(library.name, library)
    return sorted(libraries.values())


def _write_wrapper(path: Path, real_name: str) -> None:
    path.write_text(
        "#!/bin/sh\n"
        'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
        'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
        "export LD_LIBRARY_PATH\n"
        f'exec "$HERE/{real_name}" "$@"\n'
    )
    path.chmod(0o755)


class build_py(_build_py):
    def run(self):
        sources = _find_executables()
        target = Path(self.build_lib) / "sagelite_imagemagick" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_imagemagick" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        real_names: dict[str, str] = {}
        for program, source in sources.items():
            real_name = f"{program}-real"
            real_names[program] = real_name
            shutil.copy2(source, target / real_name)
            _write_wrapper(target / program, real_name)

        if "magick" not in real_names and "convert" in real_names:
            _write_wrapper(target / "magick", real_names["convert"])
        if "convert" not in real_names and "magick" in real_names:
            _write_wrapper(target / "convert", real_names["magick"])

        for library in _runtime_libraries(sources):
            shutil.copy2(library, lib_target / library.name)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_IMAGEMAGICK_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
