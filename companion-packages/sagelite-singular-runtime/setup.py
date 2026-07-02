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


def _candidate_singular_roots() -> list[Path]:
    roots = []
    for key in (
        "SAGELITE_SINGULAR_ROOT",
        "SAGELITE_SINGULAR_DEFAULT_DIR",
        "SINGULAR_DEFAULT_DIR",
        "SINGULAR_ROOT_DIR",
    ):
        value = os.environ.get(key)
        if value:
            roots.append(Path(value))
    roots.extend(
        [
            Path("/usr"),
            Path("/usr/local"),
            Path("/host/sage-manylinux_2_28_x86_64"),
            Path("/host/sage-manylinux_2_28_aarch64"),
        ]
    )
    return roots


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for key in ("SAGELITE_SINGULAR_BINDIR", "SINGULAR_BINDIR"):
        value = os.environ.get(key)
        if value:
            dirs.append(Path(value))
    for root in _candidate_singular_roots():
        dirs.append(root / "bin")
    return dirs


def _looks_like_singular_root(root: Path) -> bool:
    return (root / "share" / "singular" / "LIB" / "standard.lib").is_file()


def _factory_data_dir(root: Path) -> Path | None:
    source = root / "share" / "factory"
    if (source / "gftables").is_dir():
        return source
    return None


def _singular_module_dirs(root: Path) -> list[Path]:
    module_dirs: list[Path] = []
    for base in (root / "lib", root / "libexec"):
        if not base.is_dir():
            continue
        for module in base.rglob("MOD/freealgebra.so"):
            singular_dir = module.parent.parent
            if singular_dir.is_dir() and singular_dir not in module_dirs:
                module_dirs.append(singular_dir)
    return module_dirs


def _find_singular_executable() -> Path:
    for bindir in _candidate_bindirs():
        candidate = bindir / "Singular"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a Singular executable. Set SAGELITE_SINGULAR_BINDIR "
        f"to the Sage-built bin directory.\nSearched:\n  {searched}"
    )


def _find_singular_root() -> Path:
    for root in _candidate_singular_roots():
        if _looks_like_singular_root(root):
            return root.resolve()
    searched = "\n  ".join(os.fspath(root) for root in _candidate_singular_roots())
    raise RuntimeError(
        "could not find a Singular root containing "
        "share/singular/LIB/standard.lib. Set SAGELITE_SINGULAR_ROOT.\n"
        f"Searched:\n  {searched}"
    )


_RUNTIME_LIBRARY_PREFIXES = (
    "libSingular",
    "libpolys",
    "libfactory",
    "libsingular_resources",
    "libomalloc",
    "libflint",
    "libntl",
    "libgmp",
    "libmpfr",
    "libgf2x",
    "libreadline",
    "libtinfo",
    "libtinfow",
    "libncurses",
    "libncursesw",
)


def _selected_runtime_library_name(name: str) -> bool:
    return name.startswith(_RUNTIME_LIBRARY_PREFIXES)


def _ldd_libraries(binary: Path) -> list[tuple[str, Path]]:
    output = subprocess.run(
        ["ldd", os.fspath(binary)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries = []
    for line in output.splitlines():
        if "=>" not in line:
            continue
        name, rest = line.split("=>", 1)
        name = name.strip()
        path = rest.strip().split(maxsplit=1)[0]
        if _selected_runtime_library_name(name) and path != "not":
            libraries.append((name, Path(path)))
    return libraries


def _runtime_libraries(executable: Path) -> list[tuple[str, Path]]:
    libraries: dict[str, Path] = {}
    pending = [executable]
    seen: set[Path] = set()

    while pending:
        current = pending.pop()
        resolved = current.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        for library_name, library in _ldd_libraries(resolved):
            if library.name not in libraries:
                libraries[library.name] = library
                pending.append(library)
            libraries.setdefault(library_name, library)

    return [(name, libraries[name]) for name in sorted(libraries)]


class build_py(_build_py):
    def run(self):
        singular_root = _find_singular_root()
        singular_executable = _find_singular_executable()
        target = Path(self.build_lib) / "sagelite_singular_runtime" / "data" / "singular"
        bin_target = Path(self.build_lib) / "sagelite_singular_runtime" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_singular_runtime" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(bin_target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        bin_target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        shutil.copy2(singular_executable, bin_target / "Singular-real")
        wrapper = bin_target / "Singular"
        wrapper.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
            'SINGULAR_ROOT_DIR="${SINGULAR_ROOT_DIR:-$HERE/../singular}"\n'
            'SINGULAR_DEFAULT_DIR="${SINGULAR_DEFAULT_DIR:-$HERE/../singular/share/singular}"\n'
            "export LD_LIBRARY_PATH\n"
            "export SINGULAR_ROOT_DIR SINGULAR_DEFAULT_DIR\n"
            'exec "$HERE/Singular-real" "$@"\n'
        )
        wrapper.chmod(0o755)

        libraries: dict[str, Path] = {}
        for library_name, library in _runtime_libraries(singular_executable):
            libraries.setdefault(library_name, library)
        for library_name, library in libraries.items():
            shutil.copy2(library, lib_target / library_name)

        source = singular_root / "share" / "singular"
        shutil.copytree(source, target / "share" / "singular", ignore_dangling_symlinks=True)

        factory_source = _factory_data_dir(singular_root)
        if factory_source is not None:
            shutil.copytree(
                factory_source,
                target / "share" / "factory",
                ignore_dangling_symlinks=True,
            )

        for module_dir in _singular_module_dirs(singular_root):
            relative = module_dir.relative_to(singular_root)
            shutil.copytree(module_dir, target / relative, ignore_dangling_symlinks=True)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_SINGULAR_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
