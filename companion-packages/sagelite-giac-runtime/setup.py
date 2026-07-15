from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover - wheel is a build requirement
    _bdist_wheel = None


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_GIAC_BINDIR", "GIAC_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        candidate = bindir / "giac"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a giac executable. "
        "Set SAGELITE_GIAC_BINDIR to the Sage-built bin directory.\n"
        f"Searched:\n  {searched}"
    )


def _find_help_file(executable: Path) -> Path:
    candidates = []
    for variable in ("SAGELITE_GIAC_HELPFILE", "XCAS_HELP"):
        if os.environ.get(variable):
            candidates.append(Path(os.environ[variable]))
    candidates.append(executable.parent.parent / "share" / "giac" / "aide_cas")
    if os.environ.get("SAGE_LOCAL"):
        candidates.append(
            Path(os.environ["SAGE_LOCAL"]) / "share" / "giac" / "aide_cas"
        )
    candidates.extend(
        [
            Path("/usr/share/giac/aide_cas"),
            Path("/usr/local/share/giac/aide_cas"),
        ]
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in candidates)
    raise RuntimeError(
        "could not find the Giac aide_cas completion database. "
        "Set SAGELITE_GIAC_HELPFILE to the Sage-built aide_cas file.\n"
        f"Searched:\n  {searched}"
    )


def _ldd_runtime_libraries(executable: Path) -> list[Path]:
    output = subprocess.run(
        ["ldd", os.fspath(executable)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries = []
    prefixes = (
        "libgiac",
        "libpari",
        "libgmp",
        "libmpfr",
        "libmpfi",
        "libntl",
        "libgsl",
        "libglpk",
        "libcliquer",
        "libecm",
        "libgf2x",
        "libgfortran",
        "libopenblas",
        "libquadmath",
        "libreadline",
        "libhistory",
        "libtinfo",
        "libcurl",
        "libssl",
        "libcrypto",
        "libpng",
    )
    for line in output.splitlines():
        if "=>" not in line:
            continue
        name, rest = line.split("=>", 1)
        name = name.strip()
        path = rest.strip().split(maxsplit=1)[0]
        if name.startswith(prefixes) and path != "not":
            libraries.append(Path(path))
    return libraries


def _darwin_load_paths(path: Path) -> list[str]:
    output = subprocess.run(
        ["otool", "-L", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [
        line.strip().split(" (", 1)[0]
        for line in output.splitlines()[1:]
    ]


def _darwin_linked_libraries(path: Path) -> list[Path]:
    libraries = []
    for dependency in _darwin_load_paths(path):
        if dependency.startswith(("@loader_path/", "@rpath/")):
            candidate = path.parent / dependency.split("/", 1)[1]
            if candidate.is_file():
                libraries.append(candidate)
            continue
        if not dependency.startswith("/"):
            continue
        if dependency.startswith(("/System/Library/", "/usr/lib/")):
            continue
        libraries.append(Path(dependency))
    return libraries


def _darwin_runtime_libraries(executable: Path) -> list[Path]:
    """Return the complete non-system dylib closure for *executable*."""
    pending = _darwin_linked_libraries(executable)
    libraries: dict[str, Path] = {}
    visited: set[Path] = set()
    while pending:
        library = pending.pop()
        resolved = library.resolve()
        if resolved in visited:
            continue
        if not library.is_file():
            raise RuntimeError(f"linked library does not exist: {library}")
        visited.add(resolved)
        previous = libraries.setdefault(library.name, library)
        if previous.resolve() != resolved:
            raise RuntimeError(
                "distinct linked libraries have the same basename: "
                f"{previous}, {library}"
            )
        pending.extend(_darwin_linked_libraries(library))
    return sorted(libraries.values())


def _runtime_libraries(executable: Path) -> list[Path]:
    if sys.platform == "darwin":
        return _darwin_runtime_libraries(executable)
    return _ldd_runtime_libraries(executable)


def _repair_macos_install_names(
    executable: Path, libraries: dict[Path, Path]
) -> None:
    if sys.platform != "darwin":
        return

    for bundled in libraries.values():
        subprocess.run(
            [
                "install_name_tool",
                "-id",
                f"@loader_path/{bundled.name}",
                os.fspath(bundled),
            ],
            check=True,
        )

    for binary in [executable, *libraries.values()]:
        linked = set(_darwin_load_paths(binary))
        relative_libdir = "../lib" if binary == executable else "."
        for source, bundled in libraries.items():
            original = os.fspath(source)
            if original in linked:
                load_path = original
            elif f"@rpath/{source.name}" in linked:
                load_path = f"@rpath/{source.name}"
            elif f"@loader_path/{source.name}" in linked:
                load_path = f"@loader_path/{source.name}"
            else:
                continue
            replacement = f"@loader_path/{relative_libdir}/{bundled.name}"
            subprocess.run(
                [
                    "install_name_tool",
                    "-change",
                    load_path,
                    replacement,
                    os.fspath(binary),
                ],
                check=True,
            )

    if shutil.which("codesign") is not None:
        for binary in [*libraries.values(), executable]:
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(binary)],
                check=True,
            )


class build_py(_build_py):
    def run(self):
        source = _find_executable()
        help_source = _find_help_file(source)
        target = Path(self.build_lib) / "sagelite_giac" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_giac" / "data" / "lib"
        help_target = (
            Path(self.build_lib) / "sagelite_giac" / "data" / "share" / "giac"
        )
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        shutil.rmtree(help_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)
        help_target.mkdir(parents=True, exist_ok=True)

        real = target / "giac-real"
        shutil.copy2(source, real)
        real.chmod(real.stat().st_mode | 0o200)
        shutil.copy2(help_source, help_target / "aide_cas")
        wrapper = target / "giac"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            'DYLD_LIBRARY_PATH="$HERE/../lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"\n'
            "export LD_LIBRARY_PATH DYLD_LIBRARY_PATH\n"
            'if [ -z "${XCAS_HELP:-}" ]; then\n'
            '  XCAS_HELP="$HERE/../share/giac/aide_cas"\n'
            "  export XCAS_HELP\n"
            "fi\n"
            'exec "$HERE/giac-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        libraries: dict[Path, Path] = {}
        for library in _runtime_libraries(source):
            destination = lib_target / library.name
            shutil.copy2(library, destination)
            destination.chmod(destination.stat().st_mode | 0o200)
            libraries[library] = destination

        _repair_macos_install_names(real, libraries)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_GIAC_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
