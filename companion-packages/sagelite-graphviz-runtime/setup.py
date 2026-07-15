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


PROGRAMS = ["dot", "neato", "twopi", "fdp", "circo"]
EXCLUDED_LIBRARY_NAMES = {
    "ld-linux-x86-64.so.2",
    "libBrokenLocale.so.1",
    "libanl.so.1",
    "libc.so.6",
    "libdl.so.2",
    "libm.so.6",
    "libmvec.so.1",
    "libpthread.so.0",
    "libresolv.so.2",
    "librt.so.1",
    "libthread_db.so.1",
    "libutil.so.1",
}


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_GRAPHVIZ_BINDIR", "GRAPHVIZ_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _find_bindir() -> Path:
    for bindir in _candidate_bindirs():
        if all((bindir / program).is_file() and os.access(bindir / program, os.X_OK) for program in PROGRAMS):
            return bindir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a Graphviz executable directory containing "
        f"{', '.join(PROGRAMS)}. Set SAGELITE_GRAPHVIZ_BINDIR to the "
        f"Graphviz bin directory.\nSearched:\n  {searched}"
    )


def _ldd_libraries(paths: list[Path]) -> dict[str, Path]:
    if sys.platform == "darwin":
        return _darwin_libraries(paths)

    libraries: dict[str, Path] = {}
    for path in paths:
        output = subprocess.run(
            ["ldd", os.fspath(path)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        for line in output.splitlines():
            if "=>" not in line:
                continue
            name, rest = line.split("=>", 1)
            name = name.strip()
            lib_path = rest.strip().split(maxsplit=1)[0]
            if (
                not name
                or name in EXCLUDED_LIBRARY_NAMES
                or lib_path == "not"
                or not lib_path.startswith("/")
            ):
                continue
            libraries[name] = Path(lib_path)
    return libraries


def _darwin_linked_libraries(path: Path) -> list[Path]:
    output = subprocess.run(
        ["otool", "-L", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries = []
    for line in output.splitlines()[1:]:
        dependency = line.strip().split(" (", 1)[0]
        if not dependency.startswith("/"):
            continue
        if dependency.startswith(("/System/Library/", "/usr/lib/")):
            continue
        libraries.append(Path(dependency))
    return libraries


def _darwin_libraries(paths: list[Path]) -> dict[str, Path]:
    """Return the complete non-system dylib closure for *paths*."""
    pending = [dependency for path in paths for dependency in _darwin_linked_libraries(path)]
    libraries: dict[str, Path] = {}
    visited: set[Path] = set()
    while pending:
        library = pending.pop()
        libraries[os.fspath(library)] = library
        resolved = library.resolve()
        if resolved in visited:
            continue
        if not library.is_file():
            raise RuntimeError(f"linked library does not exist: {library}")
        visited.add(resolved)
        pending.extend(_darwin_linked_libraries(library))
    return libraries


def _install_name_tool(*args: str) -> None:
    subprocess.run(["install_name_tool", *args], check=True)


def _add_rpath(binary: Path, rpath: str) -> None:
    result = subprocess.run(
        ["install_name_tool", "-add_rpath", rpath, os.fspath(binary)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 and "would duplicate path" not in result.stderr:
        result.check_returncode()


def _codesign_darwin(path: Path) -> None:
    if sys.platform != "darwin" or shutil.which("codesign") is None:
        return
    subprocess.run(["codesign", "--force", "--sign", "-", os.fspath(path)], check=True)


def _fix_macos_install_names(
    executables: list[Path], libraries: dict[Path, Path], plugins: list[Path]
) -> None:
    if sys.platform != "darwin":
        return

    for library in libraries.values():
        _install_name_tool("-id", f"@rpath/{library.name}", os.fspath(library))
        _add_rpath(library, "@loader_path")
    for executable in executables:
        _add_rpath(executable, "@loader_path/../lib")
    for plugin in plugins:
        _add_rpath(plugin, "@loader_path/..")

    machos = [*executables, *libraries.values(), *plugins]
    for mach_o in machos:
        linked = {os.fspath(path) for path in _darwin_linked_libraries(mach_o)}
        for original, bundled in libraries.items():
            if os.fspath(original) in linked:
                _install_name_tool(
                    "-change",
                    os.fspath(original),
                    f"@rpath/{bundled.name}",
                    os.fspath(mach_o),
                )
        _codesign_darwin(mach_o)


def _graphviz_plugin_dir(bindir: Path) -> Path:
    env = os.environ.copy()
    env["LC_ALL"] = "C"
    probe = subprocess.run(
        [os.fspath(bindir / "dot"), "-v", "-Tdot", "/dev/null"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    for line in (probe.stderr + "\n" + probe.stdout).splitlines():
        line = line.strip()
        if line.startswith("libdir = "):
            _, value = line.split("=", 1)
            return Path(value.strip().strip('"')).resolve()

    for parent in (bindir.parent / "lib", Path("/usr/lib"), Path("/usr/local/lib")):
        matches = sorted(parent.glob("**/graphviz/config*"))
        if matches:
            return matches[0].parent.resolve()

    raise RuntimeError("could not locate Graphviz plugin directory")


def _copy_plugin_dir(source: Path, target: Path) -> list[Path]:
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)
    copied = []
    for item in source.iterdir():
        if not item.is_file():
            continue
        destination = target / item.name
        if item.is_symlink():
            shutil.copy2(item.resolve(), destination)
        else:
            shutil.copy2(item, destination)
        if destination.name.startswith("libgvplugin_"):
            copied.append(destination)
    return copied


class build_py(_build_py):
    def run(self):
        bindir = _find_bindir()
        plugin_source = _graphviz_plugin_dir(bindir)
        package_root = Path(self.build_lib) / "sagelite_graphviz" / "data"
        bin_target = package_root / "bin"
        lib_target = package_root / "lib"
        plugin_target = lib_target / "graphviz"
        shutil.rmtree(bin_target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        bin_target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        executables = []
        copied_executables = []
        for program in PROGRAMS:
            source = (bindir / program).resolve()
            copied_executable = bin_target / f"{program}-real"
            shutil.copy2(source, copied_executable)
            copied_executable.chmod(copied_executable.stat().st_mode | 0o200)
            wrapper = bin_target / program
            wrapper.write_text(
                "#!/usr/bin/env python3\n"
                "import os\n"
                "import sys\n"
                "from pathlib import Path\n"
                "here = Path(__file__).resolve().parent\n"
                "libdir = here.parent / 'lib'\n"
                "old_library_path = os.environ.get('LD_LIBRARY_PATH')\n"
                "os.environ['LD_LIBRARY_PATH'] = str(libdir) if not old_library_path else f'{libdir}{os.pathsep}{old_library_path}'\n"
                "os.environ['GV_PLUGIN_PATH'] = str(libdir / 'graphviz')\n"
                f"os.execve(here / '{program}-real', ['{program}', *sys.argv[1:]], os.environ)\n"
            )
            wrapper.chmod(0o755)
            executables.append(source)
            copied_executables.append(copied_executable)

        plugin_libraries = _copy_plugin_dir(plugin_source, plugin_target)
        copied_libraries = {}
        copied_sources = {}
        for library in _ldd_libraries(executables + plugin_libraries).values():
            if library.exists():
                destination = lib_target / library.name
                existing_source = copied_sources.get(destination)
                if existing_source is None:
                    shutil.copy2(library, destination)
                    destination.chmod(destination.stat().st_mode | 0o200)
                    copied_sources[destination] = library
                elif existing_source.resolve() != library.resolve():
                    raise RuntimeError(
                        "distinct linked libraries have the same basename: "
                        f"{existing_source}, {library}"
                    )
                copied_libraries[library] = destination

        _fix_macos_install_names(
            copied_executables, copied_libraries, plugin_libraries
        )

        super().run()
        pth = Path(self.build_lib) / "sagelite_graphviz_runtime_autoload.pth"
        pth.write_text("import sagelite_graphviz._autoload\n")


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_GRAPHVIZ_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
