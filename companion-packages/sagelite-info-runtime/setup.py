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
            subprocess.run(
                [
                    "install_name_tool",
                    "-change",
                    load_path,
                    f"@loader_path/{relative_libdir}/{bundled.name}",
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
        prefix = _find_prefix()
        target = Path(self.build_lib) / "sagelite_info" / "data"
        bin_target = target / "bin"
        lib_target = target / "lib"
        share_target = target / "share" / "info"
        shutil.rmtree(target, ignore_errors=True)
        bin_target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        source = prefix / "bin" / "info"
        real = bin_target / "info-real"
        shutil.copy2(source, real)
        real.chmod(real.stat().st_mode | 0o200)
        wrapper = bin_target / "info"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            'DYLD_LIBRARY_PATH="$HERE/../lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"\n'
            'INFOPATH="$HERE/../share/info${INFOPATH:+:$INFOPATH}"\n'
            "export LD_LIBRARY_PATH DYLD_LIBRARY_PATH INFOPATH\n"
            'exec "$HERE/info-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        libraries: dict[Path, Path] = {}
        for library in _runtime_libraries(source):
            destination = lib_target / library.name
            previous = next(
                (item for item in libraries.values() if item.name == library.name),
                None,
            )
            if previous is not None:
                raise RuntimeError(
                    f"distinct runtime libraries share basename {library.name}"
                )
            shutil.copy2(library, destination)
            destination.chmod(destination.stat().st_mode | 0o200)
            libraries[library] = destination

        _repair_macos_install_names(real, libraries)

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
