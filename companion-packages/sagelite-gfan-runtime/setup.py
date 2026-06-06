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


PROGRAMS = [
    "gfan",
    "gfan_bases",
    "gfan_buchberger",
    "gfan_combinerays",
    "gfan_doesidealcontain",
    "gfan_fancommonrefinement",
    "gfan_fanhomology",
    "gfan_fanisbalanced",
    "gfan_fanlink",
    "gfan_fanproduct",
    "gfan_fansubfan",
    "gfan_genericlinearchange",
    "gfan_groebnercone",
    "gfan_groebnerfan",
    "gfan_homogeneityspace",
    "gfan_homogenize",
    "gfan_initialforms",
    "gfan_interactive",
    "gfan_ismarkedgroebnerbasis",
    "gfan_krulldimension",
    "gfan_latticeideal",
    "gfan_leadingterms",
    "gfan_list",
    "gfan_markpolynomialset",
    "gfan_minkowskisum",
    "gfan_minors",
    "gfan_mixedvolume",
    "gfan_overintegers",
    "gfan_padic",
    "gfan_polynomialsetunion",
    "gfan_render",
    "gfan_renderstaircase",
    "gfan_resultantfan",
    "gfan_saturation",
    "gfan_secondaryfan",
    "gfan_stats",
    "gfan_substitute",
    "gfan_symmetries",
    "gfan_tolatex",
    "gfan_topolyhedralfan",
    "gfan_tropicalbasis",
    "gfan_tropicalbruteforce",
    "gfan_tropicalcurve",
    "gfan_tropicalevaluation",
    "gfan_tropicalfunction",
    "gfan_tropicalhypersurface",
    "gfan_tropicalintersection",
    "gfan_tropicallifting",
    "gfan_tropicallinearspace",
    "gfan_tropicalmultiplicity",
    "gfan_tropicalprevariety",
    "gfan_tropicalrank",
    "gfan_tropicalstartingcone",
    "gfan_tropicaltraverse",
    "gfan_tropicalweildivisor",
    "gfan_version",
]


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_GFAN_BINDIR", "GFAN_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _program_path(bindir: Path, program: str) -> Path | None:
    candidate = bindir / program
    if candidate.is_file() and os.access(candidate, os.X_OK):
        return candidate
    return None


def _find_bindir() -> Path:
    for bindir in _candidate_bindirs():
        if _program_path(bindir, "gfan") and _program_path(bindir, "gfan_bases"):
            return bindir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a gfan executable directory containing gfan and "
        "gfan_bases. Set SAGELITE_GFAN_BINDIR to the Sage-built bin "
        f"directory.\nSearched:\n  {searched}"
    )


def _runtime_libraries(executable: Path) -> list[Path]:
    output = subprocess.run(
        ["ldd", os.fspath(executable)],
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
        if name.startswith(("libcddgmp.so", "libgmp.so")) and path != "not":
            libraries.append(Path(path))
    return libraries


class build_py(_build_py):
    def run(self):
        super().run()

        bindir = _find_bindir()
        source = _program_path(bindir, "gfan")
        if source is None:
            raise RuntimeError(f"gfan executable disappeared from {bindir}")

        target = Path(self.build_lib) / "sagelite_gfan" / "data" / "bin"
        lib_target = Path(self.build_lib) / "sagelite_gfan" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source.resolve(), target / "gfan-real")
        for program in PROGRAMS:
            if _program_path(bindir, program) is None:
                continue
            wrapper = target / program
            wrapper.write_text(
                "#!/usr/bin/env bash\n"
                'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
                'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
                "export LD_LIBRARY_PATH\n"
                f'exec -a "{program}" "$HERE/gfan-real" "$@"\n'
            )
            wrapper.chmod(0o755)

        for library in _runtime_libraries(source.resolve()):
            shutil.copy2(library, lib_target / library.name)


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_GFAN_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
