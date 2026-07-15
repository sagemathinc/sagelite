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


def _darwin_runtime_libraries(bundle: Path) -> list[Path]:
    """Return the complete non-system dylib closure for *bundle*."""
    pending = _darwin_linked_libraries(bundle)
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


def _repair_macos_install_names(
    bundle: Path, libraries: dict[Path, Path]
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

    for binary in [bundle, *libraries.values()]:
        linked = set(_darwin_load_paths(binary))
        relative_libdir = "lib" if binary == bundle else "."
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
        for binary in [*libraries.values(), bundle]:
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(binary)],
                check=True,
            )


class build_py(_build_py):
    def run(self):
        source = _find_kenzo_fas()
        data_dir = Path(self.get_package_dir("sagelite_kenzo")) / "data"
        target = data_dir / "kenzo.fas"
        shutil.rmtree(data_dir, ignore_errors=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        target.chmod(target.stat().st_mode | 0o200)
        libraries: dict[Path, Path] = {}
        if sys.platform == "darwin":
            lib_target = data_dir / "lib"
            lib_target.mkdir(parents=True, exist_ok=True)
            for library in _darwin_runtime_libraries(source):
                destination = lib_target / library.name
                shutil.copy2(library, destination)
                destination.chmod(destination.stat().st_mode | 0o200)
                libraries[library] = destination
            _repair_macos_install_names(target, libraries)
        try:
            super().run()
        finally:
            shutil.rmtree(data_dir, ignore_errors=True)


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
