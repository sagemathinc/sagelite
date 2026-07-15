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
    for variable in ("SAGELITE_FRICAS_PREFIX", "FRICAS_PREFIX", "SAGE_LOCAL"):
        if os.environ.get(variable):
            prefixes.append(Path(os.environ[variable]))
    prefixes.extend([Path("/usr"), Path("/usr/local")])
    return prefixes


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_FRICAS_BINDIR", "FRICAS_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    dirs.extend(prefix / "bin" for prefix in _candidate_prefixes())
    return dirs


def _candidate_libdirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_FRICAS_LIBDIR", "FRICAS_LIBDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    dirs.extend(prefix / "lib" / "fricas" for prefix in _candidate_prefixes())
    return dirs


def _candidate_sharedirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_FRICAS_SHAREDIR", "FRICAS_SHAREDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    dirs.extend(prefix / "share" / "fricas" for prefix in _candidate_prefixes())
    return dirs


def _find_executable() -> Path:
    for bindir in _candidate_bindirs():
        candidate = bindir / "fricas"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a fricas executable. Set SAGELITE_FRICAS_BINDIR "
        f"to the Sage-built bin directory.\nSearched:\n  {searched}"
    )


def _find_libdir() -> Path:
    for libdir in _candidate_libdirs():
        if libdir.is_dir():
            return libdir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_libdirs())
    raise RuntimeError(
        "could not find a FriCAS lib directory. Set SAGELITE_FRICAS_LIBDIR.\n"
        f"Searched:\n  {searched}"
    )


def _find_sharedir() -> Path | None:
    for sharedir in _candidate_sharedirs():
        if sharedir.is_dir():
            return sharedir.resolve()
    return None


def _write_relocatable_command(source: Path, target: Path) -> None:
    try:
        script = source.read_text()
    except UnicodeDecodeError:
        shutil.copy2(source, target.with_name("fricas-real"))
        target.write_text(
            "#!/bin/sh\n"
            'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
            'FRICAS_PREFIX="$(CDPATH= cd -- "$HERE/.." && pwd)"\n'
            'export FRICAS_PREFIX\n'
            'exec "$HERE/fricas-real" "$@"\n'
        )
    else:
        lines = script.splitlines()
        injected = False
        patched = []
        for line in lines:
            if not injected and line.startswith("exec_prefix="):
                patched.extend(
                    [
                        'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"',
                        'FRICAS_PREFIX="$(CDPATH= cd -- "$HERE/.." && pwd)"',
                        "export FRICAS_PREFIX",
                    ]
                )
                injected = True
            patched.append(line)
        if not injected:
            shutil.copy2(source, target.with_name("fricas-real"))
            patched = [
                "#!/bin/sh",
                'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"',
                'FRICAS_PREFIX="$(CDPATH= cd -- "$HERE/.." && pwd)"',
                "export FRICAS_PREFIX",
                'exec "$HERE/fricas-real" "$@"',
            ]
        target.write_text("\n".join(patched) + "\n")

    target.chmod(0o755)


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


def _darwin_install_id(path: Path) -> str | None:
    output = subprocess.run(
        ["otool", "-D", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if len(output) > 1:
        return output[1].strip()
    return None


def _darwin_macho_files(root: Path) -> list[Path]:
    macho_magics = {
        b"\xfe\xed\xfa\xce",
        b"\xce\xfa\xed\xfe",
        b"\xfe\xed\xfa\xcf",
        b"\xcf\xfa\xed\xfe",
        b"\xca\xfe\xba\xbe",
        b"\xbe\xba\xfe\xca",
        b"\xca\xfe\xba\xbf",
        b"\xbf\xba\xfe\xca",
    }
    files = []
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        with path.open("rb") as handle:
            magic = handle.read(4)
        if magic in macho_magics:
            files.append(path)
    return files


def _darwin_linked_libraries(path: Path) -> list[Path]:
    install_id = _darwin_install_id(path)
    libraries = []
    for dependency in _darwin_load_paths(path):
        if dependency == install_id:
            continue
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


def _darwin_runtime_libraries(binaries: list[Path]) -> list[Path]:
    """Return the complete external non-system dylib closure."""
    pending = []
    for binary in binaries:
        pending.extend(_darwin_linked_libraries(binary))
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


def _loader_relative_path(binary: Path, target: Path) -> str:
    relative = os.path.relpath(target, binary.parent)
    return "@loader_path/" + relative.replace(os.sep, "/")


def _darwin_linkedit_end(path: Path) -> int:
    output = subprocess.run(
        ["otool", "-l", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    for index, line in enumerate(output):
        if line.strip() != "segname __LINKEDIT":
            continue
        fields = {}
        for detail in output[index + 1 : index + 12]:
            parts = detail.strip().split()
            if len(parts) == 2 and parts[0] in {"fileoff", "filesize"}:
                fields[parts[0]] = int(parts[1], 0)
        if fields.keys() >= {"fileoff", "filesize"}:
            return fields["fileoff"] + fields["filesize"]
    raise RuntimeError(f"could not locate __LINKEDIT in Mach-O file: {path}")


def _change_macos_load_paths(path: Path, changes: list[tuple[str, str]]) -> bool:
    """Apply load-path changes, preserving an appended SBCL core if present.

    FriCAS' ``FRICASsys`` is an executable Mach-O followed by a saved SBCL
    core.  Apple tooling only accepts the Mach-O portion, so detach the core,
    repair and sign the executable, then restore the unchanged core bytes.
    Return whether signing was completed inside this function.
    """
    linkedit_end = _darwin_linkedit_end(path)
    original = path.read_bytes()
    appended = original[linkedit_end:]
    if appended:
        path.write_bytes(original[:linkedit_end])
    try:
        for old, new in changes:
            subprocess.run(
                [
                    "install_name_tool",
                    "-change",
                    old,
                    new,
                    os.fspath(path),
                ],
                check=True,
            )
        signed = bool(appended and shutil.which("codesign") is not None)
        if signed:
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(path)],
                check=True,
            )
        repaired = path.read_bytes()
    except BaseException:
        path.write_bytes(original)
        raise
    if appended:
        path.write_bytes(repaired + appended)
    return signed


def _repair_macos_install_names(
    binaries: list[Path], libraries: dict[Path, Path]
) -> None:
    if sys.platform != "darwin":
        return

    for binary in [*binaries, *libraries.values()]:
        if _darwin_install_id(binary) is not None:
            subprocess.run(
                [
                    "install_name_tool",
                    "-id",
                    f"@loader_path/{binary.name}",
                    os.fspath(binary),
                ],
                check=True,
            )

    signed_with_appended_payload: set[Path] = set()
    for binary in [*binaries, *libraries.values()]:
        install_id = _darwin_install_id(binary)
        linked = set(_darwin_load_paths(binary))
        changes = []
        for source, bundled in libraries.items():
            candidates = {
                os.fspath(source),
                f"@rpath/{source.name}",
                f"@loader_path/{source.name}",
            }
            for load_path in linked & candidates:
                if load_path == install_id:
                    continue
                changes.append(
                    (load_path, _loader_relative_path(binary, bundled))
                )
        if changes and _change_macos_load_paths(binary, changes):
            signed_with_appended_payload.add(binary)

    if shutil.which("codesign") is not None:
        for binary in [*libraries.values(), *binaries]:
            if binary in signed_with_appended_payload:
                continue
            subprocess.run(
                ["codesign", "--force", "--sign", "-", os.fspath(binary)],
                check=True,
            )


class build_py(_build_py):
    def run(self):
        source = _find_executable()
        libdir = _find_libdir()
        sharedir = _find_sharedir()
        target = Path(self.build_lib) / "sagelite_fricas" / "data"
        bin_target = target / "bin"
        lib_target = target / "lib" / "fricas"
        share_target = target / "share" / "fricas"
        shutil.rmtree(target, ignore_errors=True)
        bin_target.mkdir(parents=True, exist_ok=True)

        _write_relocatable_command(source, bin_target / "fricas")
        shutil.copytree(libdir, lib_target, ignore_dangling_symlinks=True)
        if sharedir is not None:
            shutil.copytree(sharedir, share_target, ignore_dangling_symlinks=True)

        if sys.platform == "darwin":
            binaries = _darwin_macho_files(lib_target)
            library_target = lib_target / "_sagelite_lib"
            library_target.mkdir(parents=True, exist_ok=True)
            libraries: dict[Path, Path] = {}
            for library in _darwin_runtime_libraries(binaries):
                destination = library_target / library.name
                shutil.copy2(library, destination)
                destination.chmod(destination.stat().st_mode | 0o200)
                libraries[library] = destination
            _repair_macos_install_names(binaries, libraries)

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_FRICAS_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
