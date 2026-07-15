from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


def _candidate_roots() -> list[Path]:
    roots = []
    for variable in ("SAGELITE_QEPCAD_ROOT", "QEPCAD_ROOT", "SAGE_LOCAL"):
        if os.environ.get(variable):
            roots.append(Path(os.environ[variable]))
    roots.extend([Path("/usr"), Path("/usr/local")])
    return roots


def _valid_root(root: Path) -> bool:
    return (
        (root / "bin" / "qepcad").is_file()
        and (root / "share" / "qepcad" / "qepcad.help").is_file()
        and (root / "etc" / "default.qepcadrc").is_file()
    )


def _find_root() -> Path:
    for root in _candidate_roots():
        if _valid_root(root):
            return root.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_roots())
    raise RuntimeError(
        "could not find a QEPCAD root containing bin/qepcad, "
        "share/qepcad/qepcad.help, and etc/default.qepcadrc. "
        "Set SAGELITE_QEPCAD_ROOT to the Sage-built local directory.\n"
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


def _darwin_runtime_libraries(executable: Path) -> list[Path]:
    pending = []
    for dependency in _darwin_load_paths(executable):
        if dependency.startswith(("/System/Library/", "/usr/lib/")):
            continue
        if dependency.startswith("/"):
            pending.append(Path(dependency))

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
        for dependency in _darwin_load_paths(library):
            if dependency.startswith(("/System/Library/", "/usr/lib/")):
                continue
            if dependency.startswith("/"):
                pending.append(Path(dependency))
            elif dependency.startswith(("@loader_path/", "@rpath/")):
                candidate = library.parent / dependency.split("/", 1)[1]
                if candidate.is_file():
                    pending.append(candidate)
    return sorted(libraries.values())


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
            candidates = (
                original,
                f"@rpath/{source.name}",
                f"@loader_path/{source.name}",
            )
            load_path = next((item for item in candidates if item in linked), None)
            if load_path is None:
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


def _copy_runtime(root: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)

    (target / "bin").mkdir(parents=True, exist_ok=True)
    (target / "etc").mkdir(parents=True, exist_ok=True)
    (target / "lib").mkdir(parents=True, exist_ok=True)
    (target / "share" / "qepcad").mkdir(parents=True, exist_ok=True)

    executable = target / "bin" / "qepcad"
    shutil.copy2(root / "bin" / "qepcad", executable)
    executable.chmod(executable.stat().st_mode | 0o200)
    shutil.copy2(
        root / "share" / "qepcad" / "qepcad.help",
        target / "share" / "qepcad" / "qepcad.help",
    )
    shutil.copy2(
        root / "etc" / "default.qepcadrc",
        target / "etc" / "default.qepcadrc",
    )

    libraries: dict[Path, Path] = {}
    if sys.platform == "darwin":
        for library in _darwin_runtime_libraries(root / "bin" / "qepcad"):
            destination = target / "lib" / library.name
            shutil.copy2(library, destination)
            destination.chmod(destination.stat().st_mode | 0o200)
            libraries[library] = destination
    _repair_macos_install_names(executable, libraries)


class build_py(_build_py):
    def run(self):
        super().run()
        root = _find_root()
        target = Path(self.build_lib) / "sagelite_qepcad" / "data" / "root"
        _copy_runtime(root, target)


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        target = (
            Path(base_dir)
            / "src"
            / "sagelite_qepcad"
            / "data"
            / "root"
        )
        _copy_runtime(_find_root(), target)


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:
    _bdist_wheel = None


cmdclass = {"build_py": build_py, "sdist": sdist}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_QEPCAD_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
