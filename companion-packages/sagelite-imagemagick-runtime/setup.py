from __future__ import annotations

from collections.abc import Iterable
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


def _candidate_bindirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_IMAGEMAGICK_BINDIR", "IMAGEMAGICK_BINDIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "bin")
    dirs.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return dirs


def _program_path(bindir: Path, program: str) -> Path | None:
    candidate = bindir / program
    if candidate.is_file() and os.access(candidate, os.X_OK):
        return candidate.resolve()
    return None


def _find_executables() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for bindir in _candidate_bindirs():
        for program in ("magick", "convert"):
            if program in found:
                continue
            source = _program_path(bindir, program)
            if source is not None:
                found[program] = source
        if found:
            break
    if found:
        return found

    searched = "\n  ".join(os.fspath(path) for path in _candidate_bindirs())
    raise RuntimeError(
        "could not find a magick or convert executable. "
        "Set SAGELITE_IMAGEMAGICK_BINDIR to the Sage-built bin directory.\n"
        f"Searched:\n  {searched}"
    )


def _runtime_libraries(binaries: Iterable[Path]) -> list[Path]:
    libraries: dict[str, Path] = {}
    skipped = (
        "ld-linux",
        "libanl.",
        "libc.",
        "libdl.",
        "libgcc_s.",
        "libm.",
        "libpthread.",
        "libresolv.",
        "librt.",
        "libstdc++.",
    )

    for binary in binaries:
        output = subprocess.run(
            ["ldd", os.fspath(binary)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        for line in output.splitlines():
            if "=>" not in line:
                continue
            name, rest = line.split("=>", 1)
            name = name.strip()
            path = rest.strip().split(maxsplit=1)[0]
            if path == "not" or name.startswith(skipped):
                continue
            library = Path(path)
            if library.is_file():
                libraries.setdefault(library.name, library)
    return sorted(libraries.values())


def _split_path_list(value: str | None) -> list[Path]:
    if not value:
        return []
    return [Path(path) for path in value.split(os.pathsep) if path]


def _candidate_prefixes(executables: dict[str, Path]) -> list[Path]:
    prefixes = []
    for executable in executables.values():
        try:
            prefixes.append(executable.parents[1])
        except IndexError:
            pass
    # Distribution packages keep global ImageMagick configuration below
    # /etc even though their executable prefix is /usr.
    prefixes.extend([Path("/"), Path("/usr"), Path("/usr/local")])
    deduped = {}
    for prefix in prefixes:
        if prefix.exists():
            deduped[prefix.resolve()] = prefix
    return list(deduped.values())


def _resource_directories(executables: dict[str, Path]) -> dict[str, list[Path]]:
    resources = {
        "configure": _split_path_list(os.environ.get("SAGELITE_IMAGEMAGICK_CONFIGURE_PATH"))
        + _split_path_list(os.environ.get("MAGICK_CONFIGURE_PATH")),
        "coders": _split_path_list(os.environ.get("SAGELITE_IMAGEMAGICK_CODER_MODULE_PATH"))
        + _split_path_list(os.environ.get("MAGICK_CODER_MODULE_PATH")),
        "filters": _split_path_list(os.environ.get("SAGELITE_IMAGEMAGICK_FILTER_MODULE_PATH"))
        + _split_path_list(os.environ.get("MAGICK_FILTER_MODULE_PATH")),
    }

    for prefix in _candidate_prefixes(executables):
        resources["configure"].extend(
            [
                prefix / "etc" / "ImageMagick-7",
                prefix / "etc" / "ImageMagick-6",
                prefix / "share" / "ImageMagick-7",
                prefix / "share" / "ImageMagick-6",
            ]
        )
        for libroot in (prefix / "lib64", prefix / "lib"):
            magick_roots = list(libroot.glob("ImageMagick-*"))
            # Debian multiarch installs use lib/<triplet>/ImageMagick-*.
            magick_roots.extend(libroot.glob("*/ImageMagick-*"))
            for magick_root in magick_roots:
                resources["configure"].extend(magick_root.glob("config-*"))
                resources["coders"].extend(magick_root.glob("modules-*/coders"))
                resources["filters"].extend(magick_root.glob("modules-*/filters"))

    deduped = {}
    for key, paths in resources.items():
        by_path = {}
        for path in paths:
            if path.is_dir():
                by_path[path.resolve()] = path
        deduped[key] = list(by_path.values())
    return deduped


def _copy_directory_contents(sources: list[Path], target: Path) -> None:
    if not sources:
        return
    target.mkdir(parents=True, exist_ok=True)
    for source in sources:
        for item in source.iterdir():
            destination = target / item.name
            if item.is_dir():
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.copytree(item, destination, ignore_dangling_symlinks=True)
            elif item.is_file() or item.is_symlink():
                shutil.copy2(item, destination)


def _write_wrapper(path: Path, real_name: str) -> None:
    path.write_text(
        "#!/bin/sh\n"
        'HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"\n'
        'if [ -d "$HERE/../etc" ]; then\n'
        '  MAGICK_CONFIGURE_PATH="$HERE/../etc${MAGICK_CONFIGURE_PATH:+:$MAGICK_CONFIGURE_PATH}"\n'
        "  export MAGICK_CONFIGURE_PATH\n"
        "fi\n"
        'if [ -d "$HERE/../lib/coders" ]; then\n'
        '  MAGICK_CODER_MODULE_PATH="$HERE/../lib/coders${MAGICK_CODER_MODULE_PATH:+:$MAGICK_CODER_MODULE_PATH}"\n'
        "  export MAGICK_CODER_MODULE_PATH\n"
        "fi\n"
        'if [ -d "$HERE/../lib/filters" ]; then\n'
        '  MAGICK_FILTER_MODULE_PATH="$HERE/../lib/filters${MAGICK_FILTER_MODULE_PATH:+:$MAGICK_FILTER_MODULE_PATH}"\n'
        "  export MAGICK_FILTER_MODULE_PATH\n"
        "fi\n"
        'LD_LIBRARY_PATH="$HERE/../lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\n'
        "export LD_LIBRARY_PATH\n"
        f'exec "$HERE/{real_name}" "$@"\n'
    )
    path.chmod(0o755)


class build_py(_build_py):
    def run(self):
        sources = _find_executables()
        target = Path(self.build_lib) / "sagelite_imagemagick" / "data" / "bin"
        config_target = Path(self.build_lib) / "sagelite_imagemagick" / "data" / "etc"
        lib_target = Path(self.build_lib) / "sagelite_imagemagick" / "data" / "lib"
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(config_target, ignore_errors=True)
        shutil.rmtree(lib_target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        lib_target.mkdir(parents=True, exist_ok=True)

        real_names: dict[str, str] = {}
        for program, source in sources.items():
            real_name = f"{program}-real"
            real_names[program] = real_name
            shutil.copy2(source, target / real_name)
            _write_wrapper(target / program, real_name)

        if "magick" not in real_names and "convert" in real_names:
            _write_wrapper(target / "magick", real_names["convert"])
        if "convert" not in real_names and "magick" in real_names:
            _write_wrapper(target / "convert", real_names["magick"])

        resources = _resource_directories(sources)
        runtime_binaries = list(sources.values())
        for resource_name in ("coders", "filters"):
            for directory in resources[resource_name]:
                runtime_binaries.extend(directory.glob("*.so"))
        for library in _runtime_libraries(runtime_binaries):
            shutil.copy2(library, lib_target / library.name)

        _copy_directory_contents(resources["configure"], config_target)
        _copy_directory_contents(resources["coders"], lib_target / "coders")
        _copy_directory_contents(resources["filters"], lib_target / "filters")

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_IMAGEMAGICK_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
