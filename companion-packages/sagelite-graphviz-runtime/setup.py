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
        for program in PROGRAMS:
            source = (bindir / program).resolve()
            shutil.copy2(source, bin_target / f"{program}-real")
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

        plugin_libraries = _copy_plugin_dir(plugin_source, plugin_target)
        for library in _ldd_libraries(executables + plugin_libraries).values():
            if library.exists():
                shutil.copy2(library, lib_target / library.name)

        super().run()


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
