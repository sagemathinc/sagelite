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


EXECUTABLES = ("gp", "gphelp", "tex2mail")
SCRIPT_EXECUTABLES = {"gphelp"}


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


def _candidate_share_roots(executables: dict[str, Path]) -> list[Path]:
    roots = []
    for variable in ("SAGELITE_PARI_SHAREDIR", "SAGELITE_PARI_DATADIR"):
        if os.environ.get(variable):
            roots.append(Path(os.environ[variable]))
    roots.extend(
        _prefix_for(executable) / "share" / "pari"
        for executable in executables.values()
    )
    roots.extend([Path("/usr/share/pari"), Path("/usr/local/share/pari")])
    return roots


def _find_pari_doc(executables: dict[str, Path]) -> Path:
    for root in _candidate_share_roots(executables):
        doc = root / "doc"
        if (doc / "translations").is_file():
            return doc.resolve()
    searched = "\n  ".join(
        os.fspath(path) for path in _candidate_share_roots(executables)
    )
    raise RuntimeError(
        "could not find PARI/GP help data. Set SAGELITE_PARI_SHAREDIR "
        "to a PARI share directory containing doc/translations.\n"
        f"Searched:\n  {searched}"
    )


def _ldd_environment(prefix: Path) -> dict[str, str]:
    env = os.environ.copy()
    libdir = os.fspath(prefix / "lib")
    current = env.get("LD_LIBRARY_PATH")
    env["LD_LIBRARY_PATH"] = libdir if not current else f"{libdir}:{current}"
    return env


def _is_elf(path: Path) -> bool:
    try:
        with path.open("rb") as executable:
            return executable.read(4) == b"\x7fELF"
    except OSError:
        return False


_RUNTIME_LIBRARY_PREFIXES = (
    "libpari",
    "libgmp",
    "libmpfr",
    "libmpfi",
    "libreadline",
    "libtinfo",
    "libtinfow",
    "libncurses",
    "libncursesw",
)


def _selected_runtime_library_name(name: str) -> bool:
    return name.startswith(_RUNTIME_LIBRARY_PREFIXES)


def _runtime_libraries(executables: dict[str, Path]) -> list[Path]:
    if sys.platform == "darwin":
        return _macho_runtime_libraries(executables)

    libraries: dict[str, Path] = {}
    for executable in executables.values():
        if not _is_elf(executable):
            continue
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
            if not _selected_runtime_library_name(name):
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


def _is_macho(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        return path.read_bytes()[:4] in {
            b"\xcf\xfa\xed\xfe",
            b"\xfe\xed\xfa\xcf",
            b"\xca\xfe\xba\xbe",
            b"\xca\xfe\xba\xbf",
        }
    except OSError:
        return False


def _macho_dependencies(path: Path) -> list[str]:
    output = subprocess.run(
        ["otool", "-L", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [line.strip().split(maxsplit=1)[0] for line in output.splitlines()[1:]]


def _otool_libraries(binary: Path) -> list[Path]:
    libraries = []
    for dependency in _macho_dependencies(binary):
        if not dependency.startswith("/"):
            continue
        library = Path(dependency)
        if library.parts[:2] in {("/", "usr"), ("/", "System")}:
            continue
        if library.is_file() and _selected_runtime_library_name(library.name):
            libraries.append(library)
    return libraries


def _macho_runtime_libraries(executables: dict[str, Path]) -> list[Path]:
    libraries: dict[str, Path] = {}
    pending = list(executables.values())
    seen: set[Path] = set()

    while pending:
        current = pending.pop()
        resolved = current.resolve()
        if resolved in seen or not _is_macho(resolved):
            continue
        seen.add(resolved)
        for library in _otool_libraries(resolved):
            if library.name not in libraries:
                libraries[library.name] = library
                pending.append(library)

    candidate_libdirs = {
        _prefix_for(executable) / "lib" for executable in executables.values()
    }
    candidate_libdirs.update(
        {
            Path("/opt/homebrew/lib"),
            Path("/opt/homebrew/opt/gmp/lib"),
            Path("/opt/homebrew/opt/mpfr/lib"),
            Path("/opt/homebrew/opt/mpfi/lib"),
            Path("/opt/homebrew/opt/readline/lib"),
        }
    )
    for libdir in sorted(candidate_libdirs):
        if not libdir.is_dir():
            continue
        for library in sorted(libdir.glob("*.dylib")):
            if _selected_runtime_library_name(library.name):
                libraries.setdefault(library.name, library)

    return [libraries[name] for name in sorted(libraries)]


def _rewrite_macos_runtime_paths(root: Path, lib_target: Path) -> None:
    runtime_libraries = {path.name for path in lib_target.iterdir() if path.is_file()}
    if not runtime_libraries:
        return

    modified: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not _is_macho(path):
            continue

        args: list[str] = []
        if path.parent == lib_target and path.suffix == ".dylib":
            args.extend(["-id", f"@rpath/{path.name}"])

        rel_lib_dir = os.path.relpath(lib_target, path.parent)
        for dependency in _macho_dependencies(path):
            dependency_name = Path(dependency).name
            if dependency_name in runtime_libraries and dependency != path.name:
                args.extend(
                    [
                        "-change",
                        dependency,
                        f"@loader_path/{rel_lib_dir}/{dependency_name}",
                    ]
                )

        if args:
            subprocess.run(["install_name_tool", *args, os.fspath(path)], check=True)
            modified.append(path)

    if shutil.which("codesign") is not None:
        for path in modified:
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(path)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )


def _write_wrapper(path: Path, real_name: str) -> None:
    path.write_text(
        "#!/bin/sh\n"
        'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
        'DATADIR="$HERE/../share/pari"\n'
        'if [ -d "$DATADIR" ]; then\n'
        '    SAGELITE_PARI_DATADIR="$DATADIR"\n'
        "    export SAGELITE_PARI_DATADIR\n"
        "fi\n"
        'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
        'DYLD_LIBRARY_PATH="$HERE/../lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"\n'
        'PATH="$HERE${PATH:+:$PATH}"\n'
        "export LD_LIBRARY_PATH DYLD_LIBRARY_PATH PATH\n"
        f'exec "$HERE/{real_name}" "$@"\n'
    )
    path.chmod(0o755)


def _patch_gphelp_datadir(path: Path) -> None:
    lines = path.read_text().splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.lstrip().startswith("$datadir="):
            newline = "\n" if line.endswith("\n") else ""
            lines[index] = (
                '$datadir = $ENV{"SAGELITE_PARI_DATADIR"} || ".";'
                f"{newline}"
            )
            path.write_text("".join(lines))
            return
    raise RuntimeError(f"could not patch PARI/GP help data directory in {path}")


class build_py(_build_py):
    def run(self):
        executables = _find_executables()
        target = Path(self.build_lib) / "sagelite_pari" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_pari" / "data" / "lib"
        doc_target = (
            Path(self.build_lib)
            / "sagelite_pari"
            / "data"
            / "share"
            / "pari"
            / "doc"
        )
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        shutil.rmtree(doc_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        for name, source in executables.items():
            real_name = f"{name}-real"
            real_path = target / real_name
            shutil.copy2(source, real_path)
            if name in SCRIPT_EXECUTABLES:
                _patch_gphelp_datadir(real_path)
            _write_wrapper(target / name, real_name)

        for library in _runtime_libraries(executables):
            shutil.copy2(library, lib_target / library.name)

        if sys.platform == "darwin":
            runtime_root = Path(self.build_lib) / "sagelite_pari" / "data"
            _rewrite_macos_runtime_paths(runtime_root, lib_target)

        shutil.copytree(
            _find_pari_doc(executables),
            doc_target,
            ignore_dangling_symlinks=True,
        )

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
