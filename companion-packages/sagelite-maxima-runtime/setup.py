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


REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_sage_locals() -> list[Path]:
    roots = []
    if os.environ.get("SAGE_LOCAL"):
        roots.append(Path(os.environ["SAGE_LOCAL"]))
    roots.append(REPO_ROOT / "local")
    return roots


def _install_roots_for_maxima_prefix(maxima_prefix: Path) -> list[Path]:
    """
    Return installation roots that plausibly own ``maxima_prefix``.

    A Maxima prefix is normally ``$prefix/share/maxima[-sage]/$version``.
    Looking up the matching ``lib`` tree from the chosen prefix avoids mixing a
    system Maxima share tree with stale ``local/lib/ecl`` data from the source
    checkout.
    """
    roots = []
    resolved = maxima_prefix.resolve()
    parent = resolved.parent
    if parent.name in {"maxima", "maxima-sage"} and parent.parent.name == "share":
        roots.append(parent.parent.parent)
    roots.extend(_candidate_sage_locals())
    by_path = {}
    for root in roots:
        by_path[root.resolve()] = root
    return list(by_path.values())


def _candidate_prefixes() -> list[Path]:
    roots = []
    if os.environ.get("SAGELITE_MAXIMA_PREFIX"):
        roots.append(Path(os.environ["SAGELITE_MAXIMA_PREFIX"]))
    if os.environ.get("MAXIMA_PREFIX"):
        roots.append(Path(os.environ["MAXIMA_PREFIX"]))
    for sage_local in _candidate_sage_locals():
        roots.extend((sage_local / "share").glob("maxima-sage/*"))
        roots.extend((sage_local / "share").glob("maxima/*"))
    roots.extend(Path("/usr/share").glob("maxima-sage/*"))
    roots.extend(Path("/usr/share").glob("maxima/*"))
    roots.extend(Path("/usr/local/share").glob("maxima/*"))
    return roots


def _candidate_fas_files(maxima_prefix: Path) -> list[Path]:
    files = []
    if os.environ.get("SAGELITE_MAXIMA_FAS"):
        files.append(Path(os.environ["SAGELITE_MAXIMA_FAS"]))
    if os.environ.get("MAXIMA_FAS"):
        files.append(Path(os.environ["MAXIMA_FAS"]))
    for root in _install_roots_for_maxima_prefix(maxima_prefix):
        files.append(root / "lib" / "ecl" / "maxima.fas")
    files.extend(
        [
            Path("/usr/lib/ecl/maxima.fas"),
            Path("/usr/local/lib/ecl/maxima.fas"),
        ]
    )
    return files


def _candidate_images_dirs(maxima_prefix: Path) -> list[Path]:
    dirs = []
    if os.environ.get("SAGELITE_MAXIMA_IMAGESDIR"):
        dirs.append(Path(os.environ["SAGELITE_MAXIMA_IMAGESDIR"]))
    version = maxima_prefix.name
    for root in _install_roots_for_maxima_prefix(maxima_prefix):
        dirs.extend((root / "lib").glob(f"maxima-sage/{version}"))
        dirs.extend((root / "lib").glob(f"maxima/{version}"))
    dirs.extend(Path("/usr/lib").glob(f"maxima-sage/{version}"))
    dirs.extend(Path("/usr/lib").glob(f"maxima/{version}"))
    dirs.extend(Path("/usr/local/lib").glob(f"maxima/{version}"))
    return dirs


def _candidate_ecl_dirs(maxima_prefix: Path) -> list[Path]:
    dirs = []
    if os.environ.get("SAGELITE_MAXIMA_ECLDIR"):
        dirs.append(Path(os.environ["SAGELITE_MAXIMA_ECLDIR"]))
    for root in _install_roots_for_maxima_prefix(maxima_prefix):
        dirs.extend((root / "lib").glob("ecl-*"))
        for directory in (root / "lib").glob("*-linux-gnu"):
            dirs.extend(directory.glob("ecl-*"))
    for directory in Path("/usr/lib").glob("*-linux-gnu"):
        dirs.extend(directory.glob("ecl-*"))
    dirs.extend(Path("/usr/lib").glob("ecl-*"))
    dirs.extend(Path("/usr/local/lib").glob("ecl-*"))
    return dirs


def _candidate_library_dirs(maxima_prefix: Path) -> list[Path]:
    dirs = []
    if os.environ.get("SAGELITE_MAXIMA_LIBDIR"):
        dirs.append(Path(os.environ["SAGELITE_MAXIMA_LIBDIR"]))
    for root in _install_roots_for_maxima_prefix(maxima_prefix):
        dirs.append(root / "lib")
        dirs.extend((root / "lib").glob("*-linux-gnu"))
    dirs.extend(Path("/usr/lib").glob("*-linux-gnu"))
    dirs.extend([Path("/usr/lib"), Path("/usr/local/lib")])
    return dirs


def _looks_like_maxima_prefix(path: Path) -> bool:
    return (path / "share").is_dir()


def _maxima_version_tuple(path: Path) -> tuple[int, ...]:
    parts = []
    for part in path.name.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            break
    return tuple(parts)


def _validate_maxima_prefix(maxima_prefix: Path) -> None:
    """
    Validate that the selected Maxima payload is new enough for sagelite.

    Sage's library-mode initialization loads packages such as ``to_poly_solve``
    after applying Sage-specific Maxima setup.  Older distro ``maxima-sage``
    trees can have enough files to build a wheel, but still fail at import time.
    """
    required = (5, 47, 0)
    if _maxima_version_tuple(maxima_prefix) < required:
        raise RuntimeError(
            f"sagelite-maxima-runtime requires Maxima >= 5.47.0; "
            f"selected {maxima_prefix.name} at {maxima_prefix}. "
            "Set SAGELITE_MAXIMA_PREFIX to a Sage-built Maxima 5.47.0 share tree."
        )
    if not (maxima_prefix / "src" / "maxima-package.lisp").is_file():
        raise RuntimeError(
            f"{maxima_prefix} is missing src/maxima-package.lisp. "
            "Use the Sage-built Maxima share tree for this sagelite runtime."
        )


def _looks_like_images_dir(path: Path) -> bool:
    return (path / "binary-ecl" / "maxima").is_file()


def _find_maxima_prefix() -> Path:
    for prefix in _candidate_prefixes():
        if _looks_like_maxima_prefix(prefix):
            return prefix.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_prefixes())
    raise RuntimeError(
        "could not find a Maxima prefix containing share/. "
        "Set SAGELITE_MAXIMA_PREFIX to the Sage-built Maxima share directory.\n"
        f"Searched:\n  {searched}"
    )


def _find_maxima_images_dir(maxima_prefix: Path) -> Path | None:
    for images_dir in _candidate_images_dirs(maxima_prefix):
        if _looks_like_images_dir(images_dir):
            return images_dir.resolve()
    return None


def _find_maxima_fas(maxima_prefix: Path) -> Path:
    for fas in _candidate_fas_files(maxima_prefix):
        if fas.is_file():
            return fas.resolve()
    searched = "\n  ".join(
        os.fspath(path) for path in _candidate_fas_files(maxima_prefix)
    )
    raise RuntimeError(
        "could not find maxima.fas. Set SAGELITE_MAXIMA_FAS to the matching "
        f"Sage-built ECL Maxima image.\nSearched:\n  {searched}"
    )


def _find_ecl_dir(maxima_prefix: Path) -> Path:
    for ecl_dir in _candidate_ecl_dirs(maxima_prefix):
        if (ecl_dir / "sockets.fas").is_file():
            return ecl_dir.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_ecl_dirs(maxima_prefix))
    raise RuntimeError(
        "could not find the ECL runtime directory containing sockets.fas. "
        f"Set SAGELITE_MAXIMA_ECLDIR.\nSearched:\n  {searched}"
    )


def _find_library(soname: str, maxima_prefix: Path) -> Path:
    candidates = []
    for directory in _candidate_library_dirs(maxima_prefix):
        candidates.extend(directory.glob(f"{soname}*"))
        candidates.append(directory / soname)
    for candidate in candidates:
        if candidate.is_file() or candidate.is_symlink():
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in candidates)
    raise RuntimeError(
        f"could not find runtime library {soname}. Set SAGELITE_MAXIMA_LIBDIR.\n"
        f"Searched:\n  {searched}"
    )


def _find_library_with_prefix(prefix: str, maxima_prefix: Path) -> Path:
    candidates = []
    for directory in _candidate_library_dirs(maxima_prefix):
        candidates.extend(directory.glob(f"{prefix}*"))
    for candidate in candidates:
        if candidate.is_file() or candidate.is_symlink():
            return candidate.resolve()
    searched = "\n  ".join(os.fspath(path) for path in candidates)
    raise RuntimeError(
        f"could not find runtime library matching {prefix}*. "
        f"Set SAGELITE_MAXIMA_LIBDIR.\nSearched:\n  {searched}"
    )


def _runtime_libraries(executable: Path, maxima_prefix: Path) -> list[Path]:
    output = subprocess.run(
        ["ldd", os.fspath(executable)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    libraries = []
    prefixes = ("libecl.so", "libgmp.so")
    for line in output.splitlines():
        if "=>" not in line:
            continue
        name, rest = line.split("=>", 1)
        name = name.strip()
        path = rest.strip().split(maxsplit=1)[0]
        if name.startswith(prefixes) and path != "not":
            libraries.append(Path(path))

    if not any(path.name.startswith("libecl.so") for path in libraries):
        libraries.append(_find_library_with_prefix("libecl.so", maxima_prefix))
    if not any(path.name.startswith("libgmp.so") for path in libraries):
        libraries.append(_find_library_with_prefix("libgmp.so", maxima_prefix))

    by_name = {path.name: path for path in libraries}
    return sorted(by_name.values())


def _fallback_runtime_libraries(maxima_prefix: Path) -> list[Path]:
    libraries = [
        _find_library_with_prefix("libecl.so", maxima_prefix),
        _find_library_with_prefix("libgmp.so", maxima_prefix),
    ]
    by_name = {path.name: path for path in libraries}
    return sorted(by_name.values())


def _dynamic_symbols(path: Path, *args: str) -> set[str]:
    try:
        output = subprocess.run(
            ["nm", "-D", *args, os.fspath(path)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except FileNotFoundError as err:
        raise RuntimeError("nm is required to validate copied ECL images") from err

    symbols = set()
    for line in output.splitlines():
        parts = line.split()
        if not parts:
            continue
        symbols.add(parts[-1])
    return symbols


def _is_ecl_runtime_symbol(symbol: str) -> bool:
    """
    Return whether ``symbol`` should be provided by the loaded ECL runtime.

    Compiled ECL images reference more than the public ``ecl_*`` namespace.
    In particular, Maxima and ECL support images can require ``FE*`` entry
    points such as ``FEstack_advance``; missing those passes a narrow
    ``ecl_*`` check but fails when Sage evaluates ``(require 'maxima)``.
    """
    return symbol.startswith(("ecl_", "_ecl_", "cl_", "si_", "ext_", "FE"))


def _system_ecl_libraries() -> list[Path]:
    """
    Return system ECL shared libraries that an unrepaired sagelite wheel may load.

    ``SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL=1`` is only for local or distribution
    test builds where Sage's ``sage.libs.ecl`` extension is expected to bind to
    the system ECL library.  Validate copied Maxima images against that runtime
    too, otherwise a Sage-built Maxima/ECL image can be accidentally packaged
    with symbols that the installed extension will not provide.
    """
    candidates = []
    for directory in (
        Path("/usr/lib"),
        Path("/usr/local/lib"),
        *Path("/usr/lib").glob("*-linux-gnu"),
        *Path("/usr/local/lib").glob("*-linux-gnu"),
    ):
        candidates.extend(directory.glob("libecl.so*"))

    libraries = [
        path.resolve()
        for path in candidates
        if path.is_file() or path.is_symlink()
    ]
    return sorted({path.name: path for path in libraries}.values())


def _environment_path(name: str) -> Path | None:
    value = os.environ.get(name)
    if not value:
        return None

    path = Path(value)
    if path.is_absolute():
        return path

    repo_path = REPO_ROOT / path
    if repo_path.exists():
        return repo_path

    return path


def _validation_targets(runtime_library_dir: Path) -> dict[str, list[Path]]:
    """
    Return ECL libraries that copied images must be loadable against.

    The copied runtime library is used by the standalone Maxima launcher.  In
    Sage library mode, however, ``sage.libs.ecl`` has already loaded the ECL
    library bundled in the repaired ``sagelite`` wheel.  Release builds pass
    that library explicitly so this package rejects ABI-mismatched images
    before publishing a wheel.
    """
    ecl_libraries = sorted(runtime_library_dir.glob("libecl.so*"))
    if not ecl_libraries:
        raise RuntimeError(
            f"could not validate copied ECL images: no libecl.so* in {runtime_library_dir}"
        )

    targets = {"copied ECL runtime": ecl_libraries}

    path = _environment_path("SAGELITE_MAXIMA_ECL_LIBRARY")
    if path is not None:
        if not path.is_file():
            raise RuntimeError(
                f"SAGELITE_MAXIMA_ECL_LIBRARY does not name a file: {path}"
            )
        targets["sagelite ECL runtime"] = [path]
    elif os.environ.get("SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL") == "1":
        system_libraries = _system_ecl_libraries()
        if not system_libraries:
            raise RuntimeError(
                "SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL=1 was set, but no system "
                "libecl.so* could be found for validation"
            )
        targets["system ECL runtime"] = system_libraries

    return targets


def _validate_copied_ecl_images(ecl_dir: Path, runtime_library_dir: Path) -> None:
    """
    Check copied ECL images against the copied ECL shared library.

    This catches mixed build inputs such as a Maxima/ECL support tree from one
    distribution release and ``libecl`` from another, which otherwise build a
    wheel that installs but fails when Sage evaluates ``(require 'maxima)``.
    """
    missing_by_target = {}
    for target, libraries in _validation_targets(runtime_library_dir).items():
        exported = set()
        for library in libraries:
            exported.update(_dynamic_symbols(library, "--defined-only"))

        missing_by_image = {}
        for image in sorted(ecl_dir.glob("*.fas")):
            undefined = {
                symbol
                for symbol in _dynamic_symbols(image, "--undefined-only")
                if _is_ecl_runtime_symbol(symbol) and symbol not in exported
            }
            if undefined:
                missing_by_image[image.name] = sorted(undefined)

        if missing_by_image:
            missing_by_target[target] = missing_by_image

    if missing_by_target:
        details = "\n".join(
            f"  {target}:\n"
            + "\n".join(
                f"    {image}: {', '.join(symbols)}"
                for image, symbols in missing_by_image.items()
            )
            for target, missing_by_image in missing_by_target.items()
        )
        raise RuntimeError(
            "copied ECL images require symbols that are not exported by the "
            f"target ECL runtime:\n{details}\n"
            "Use matching Maxima, ECL support, and libecl inputs; set "
            "SAGELITE_MAXIMA_ECLDIR, SAGELITE_MAXIMA_LIBDIR, and "
            "SAGELITE_MAXIMA_ECL_LIBRARY explicitly if auto-detection selected "
            "mixed installation trees."
        )



def _ignore_maxima_files(directory: str, names: list[str]) -> set[str]:
    ignored = {
        "__pycache__",
        "doc",
        "html",
        "locale",
        "tests",
        "xmaxima",
    }
    ignored.update(
        name
        for name in names
        if name.endswith((".pyc", ".pyo", ".pdf", ".html", ".htm", ".css", ".js"))
    )
    return ignored


def _write_maxima_command(path: Path, version: str, ecl_dir_name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""#!/bin/sh
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PREFIX=$(dirname "$HERE")
export MAXIMA_PREFIX="${{MAXIMA_PREFIX:-$PREFIX}}"
export MAXIMA_LAYOUT_AUTOTOOLS=true
export MAXIMA_IMAGESDIR="$PREFIX/lib/maxima/{version}"
export ECLDIR="$PREFIX/lib/{ecl_dir_name}/"
export LD_LIBRARY_PATH="$PREFIX/lib/runtime${{LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}}"
exec "$PREFIX/lib/maxima/{version}/binary-ecl/maxima" \\
  --frame-stack 4096 --lisp-stack 65536 -- "$@"
""",
    )
    path.chmod(0o755)


def _patch_ecl_fas(path: Path) -> None:
    """
    Make an ECL-loaded image compatible with the sagelite wheel.

    In library mode, Sage has already loaded the auditwheel-renamed ECL shared
    library bundled in ``sagelite.libs``.  If copied ECL images still depend on
    the original ``libecl.so`` SONAME, dlopen can load a second ECL runtime and
    crash the process.  Release builds pass the repaired sagelite ECL SONAME so
    these images bind to the already-loaded library.  All builds remove RPATHs
    from copied images so they cannot keep searching the original Sage build
    prefix after installation.
    """
    ecl_soname = os.environ.get("SAGELITE_MAXIMA_ECL_SONAME")
    allow_system_ecl = os.environ.get("SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL") == "1"

    try:
        needed = subprocess.run(
            ["patchelf", "--print-needed", os.fspath(path)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        ecl_needed = [name for name in needed if name.startswith("libecl")]
        if ecl_needed and not ecl_soname:
            if allow_system_ecl:
                subprocess.run(
                    ["patchelf", "--remove-rpath", os.fspath(path)], check=True
                )
                return
            raise RuntimeError(
                f"{path} depends on {', '.join(ecl_needed)} but "
                "SAGELITE_MAXIMA_ECL_SONAME is not set. Build production "
                "Maxima runtime wheels from the repaired sagelite wheel and "
                "set SAGELITE_MAXIMA_ECL_SONAME to its bundled ECL SONAME, "
                "or set SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL=1 for an explicit "
                "system-ECL test build."
            )
        for original in needed:
            if not original.startswith("libecl") or original == ecl_soname:
                continue
            subprocess.run(
                [
                    "patchelf",
                    "--replace-needed",
                    original,
                    ecl_soname,
                    os.fspath(path),
                ],
                check=True,
            )
        subprocess.run(["patchelf", "--remove-rpath", os.fspath(path)], check=True)
    except FileNotFoundError as err:
        raise RuntimeError(
            "patchelf is required to validate or patch Maxima ECL images"
        ) from err


def _copy_maxima_info_indexes(maxima_prefix: Path, target: Path) -> None:
    """
    Copy the small CL-INFO indexes used during Maxima startup if available.
    """
    source = maxima_prefix.parents[1] / "info"
    if not source.is_dir():
        return

    files = sorted(source.glob("maxima-index*.lisp"))
    if not files:
        return

    info_target = target / "share" / "info"
    info_target.mkdir(parents=True, exist_ok=True)
    for path in files:
        shutil.copy2(path, info_target / path.name)


def _write_maxima_asd(path: Path) -> None:
    """
    Register the bundled Maxima image with ECL's ``require`` mechanism.
    """
    path.write_text(
        """(defsystem "maxima" :class asdf::prebuilt-system
        :lib #P"SYS:MAXIMA.FAS"
        :depends-on NIL
        :components ((:compiled-file "maxima" :pathname #P"SYS:MAXIMA.FAS")))
""",
    )


class build_py(_build_py):
    def run(self):
        maxima_prefix = _find_maxima_prefix()
        _validate_maxima_prefix(maxima_prefix)
        maxima_images_dir = _find_maxima_images_dir(maxima_prefix)
        maxima_fas = _find_maxima_fas(maxima_prefix)
        ecl_dir = _find_ecl_dir(maxima_prefix)
        target = Path(self.build_lib) / "sagelite_maxima" / "data"
        shutil.rmtree(target, ignore_errors=True)

        share_target = target / "share" / "maxima" / maxima_prefix.name
        share_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            maxima_prefix,
            share_target,
            ignore=_ignore_maxima_files,
            ignore_dangling_symlinks=True,
        )
        _copy_maxima_info_indexes(maxima_prefix, target)

        images_target = target / "lib" / "maxima" / maxima_prefix.name
        if maxima_images_dir is not None:
            shutil.copytree(
                maxima_images_dir, images_target, ignore_dangling_symlinks=True
            )

        ecl_target = target / "lib" / ecl_dir.name
        shutil.copytree(ecl_dir, ecl_target, ignore_dangling_symlinks=True)
        fas_target = ecl_target / "maxima.fas"
        shutil.copy2(maxima_fas, fas_target)
        _patch_ecl_fas(fas_target)
        _write_maxima_asd(ecl_target / "maxima.asd")
        for ecl_fas in ecl_target.glob("*.fas"):
            if ecl_fas == fas_target:
                continue
            _patch_ecl_fas(ecl_fas)

        runtime_target = target / "lib" / "runtime"
        runtime_target.mkdir(parents=True, exist_ok=True)
        if maxima_images_dir is None:
            libraries = _fallback_runtime_libraries(maxima_prefix)
        else:
            libraries = _runtime_libraries(
                maxima_images_dir / "binary-ecl" / "maxima", maxima_prefix
            )
        for library in libraries:
            shutil.copy2(library, runtime_target / library.name)
        _validate_copied_ecl_images(ecl_target, runtime_target)

        if maxima_images_dir is not None:
            _write_maxima_command(
                target / "bin" / "maxima", maxima_prefix.name, ecl_dir.name
            )

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_MAXIMA_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
