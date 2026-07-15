#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


MACHO_MAGICS = {
    b"\xcf\xfa\xed\xfe",
    b"\xfe\xed\xfa\xcf",
    b"\xca\xfe\xba\xbe",
    b"\xca\xfe\xba\xbf",
}
SYSTEM_PREFIXES = ("/System/Library/", "/usr/lib/")
PARI_RUNTIME_PREFIXES = ("libpari", "libgmp", "libmpfr", "libmpfi")
SINGULAR_RUNTIME_PREFIXES = (
    "libSingular",
    "libpolys",
    "libfactory",
    "libsingular_resources",
    "libomalloc",
)
COMPANION_RUNTIME_DIRS = {
    "pari": Path("sagelite_pari/data/lib"),
    "singular": Path("sagelite_singular_runtime/data/lib"),
}


def unpack_wheel(wheel_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(wheel_path) as wheel:
        wheel.extractall(dest)


def is_macho(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        with path.open("rb") as binary:
            return binary.read(4) in MACHO_MAGICS
    except OSError:
        return False


def macho_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if is_macho(path))


def otool_libraries(path: Path) -> list[str]:
    output = subprocess.run(
        ["otool", "-L", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [line.strip().split(maxsplit=1)[0] for line in output.splitlines()[1:]]


def otool_install_ids(path: Path) -> set[str]:
    output = subprocess.run(
        ["otool", "-D", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return {line.strip() for line in output.splitlines()[1:] if line.strip()}


def companion_owner(dependency: str) -> str | None:
    name = Path(dependency).name
    if name.startswith(PARI_RUNTIME_PREFIXES):
        return "pari"
    if name.startswith(SINGULAR_RUNTIME_PREFIXES):
        return "singular"
    return None


def companion_dependency(binary: Path, root: Path, dependency: str) -> str | None:
    owner = companion_owner(dependency)
    if owner is None:
        return None
    runtime_dir = root / COMPANION_RUNTIME_DIRS[owner]
    relative_dir = os.path.relpath(runtime_dir, binary.parent)
    return f"@loader_path/{relative_dir}/{Path(dependency).name}"


def sign_macho(path: Path) -> None:
    if shutil.which("codesign") is None:
        return
    subprocess.run(
        ["codesign", "--force", "--sign", "-", os.fspath(path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def rewrite_companion_dependencies(root: Path) -> tuple[int, int]:
    changed_files = 0
    changed_dependencies = 0
    for binary in macho_files(root):
        args: list[str] = []
        for dependency in otool_libraries(binary):
            replacement = companion_dependency(binary, root, dependency)
            if replacement is None or replacement == dependency:
                continue
            args.extend(["-change", dependency, replacement])
            changed_dependencies += 1
        if not args:
            continue
        subprocess.run(
            ["install_name_tool", *args, os.fspath(binary)],
            check=True,
        )
        sign_macho(binary)
        changed_files += 1
    return changed_files, changed_dependencies


def is_system_dependency(dependency: str) -> bool:
    return dependency.startswith(SYSTEM_PREFIXES)


def resolved_loader_path(binary: Path, dependency: str) -> Path:
    suffix = dependency.removeprefix("@loader_path/")
    return Path(os.path.normpath(binary.parent / suffix))


def expected_companion_path(binary: Path, root: Path, dependency: str) -> Path | None:
    owner = companion_owner(dependency)
    if owner is None:
        return None
    return root / COMPANION_RUNTIME_DIRS[owner] / Path(dependency).name


def audit_portable_dependencies(root: Path) -> tuple[int, int]:
    binaries = macho_files(root)
    dependency_count = 0
    failures: list[str] = []
    for binary in binaries:
        install_ids = otool_install_ids(binary)
        for dependency in otool_libraries(binary):
            # A dylib's LC_ID_DYLIB is printed by ``otool -L`` but is not a
            # library load command. Delocate's unique /DLC identity is valid
            # here and must not be mistaken for an absolute dependency.
            if dependency in install_ids:
                continue
            dependency_count += 1
            if is_system_dependency(dependency):
                continue
            if dependency.startswith("@loader_path/"):
                resolved = resolved_loader_path(binary, dependency)
                expected = expected_companion_path(binary, root, dependency)
                bundled = resolved.is_relative_to(root) and resolved.is_file()
                if bundled or (expected is not None and resolved == expected):
                    continue
                failures.append(
                    f"{binary.relative_to(root)}: unresolved {dependency} -> {resolved}"
                )
                continue
            failures.append(f"{binary.relative_to(root)}: non-portable {dependency}")
    if failures:
        detail = "\n".join(failures)
        raise RuntimeError(f"macOS wheel portability audit failed:\n{detail}")
    return len(binaries), dependency_count


def delocate_command(wheel: Path, wheel_dir: Path, delocate_wheel: str) -> list[str]:
    # The companion libraries are intentionally absent from the primary wheel,
    # so delocate cannot resolve their already-relative paths. Its permissive
    # scan is followed by audit_portable_dependencies, which is deliberately
    # stricter and rejects every unresolved dependency outside those companions.
    command = [
        delocate_wheel,
        "--ignore-missing-dependencies",
        "--sanitize-rpaths",
        "--require-archs",
        "arm64",
        "--wheel-dir",
        os.fspath(wheel_dir),
        "--lib-sdir",
        "sagelite.libs",
    ]
    for prefix in (*PARI_RUNTIME_PREFIXES, *SINGULAR_RUNTIME_PREFIXES):
        command.extend(["--exclude", prefix])
    command.append(os.fspath(wheel))
    return command


def record_row(path: Path, root: Path) -> tuple[str, str, str]:
    data = path.read_bytes()
    digest = hashlib.sha256(data).digest()
    encoded = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    relpath = path.relative_to(root).as_posix()
    return relpath, f"sha256={encoded}", str(len(data))


def pack_wheel(root: Path, wheel_path: Path) -> None:
    dist_infos = list(root.glob("*.dist-info"))
    if len(dist_infos) != 1:
        raise RuntimeError(f"expected one dist-info directory, found {len(dist_infos)}")
    record_path = dist_infos[0] / "RECORD"

    rows: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == record_path:
            continue
        rows.append(record_row(path, root))

    with record_path.open("w", encoding="utf-8", newline="") as record_file:
        writer = csv.writer(record_file)
        writer.writerows(rows)
        writer.writerow((record_path.relative_to(root).as_posix(), "", ""))

    wheel_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as wheel:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            arcname = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo.from_file(path, arcname)
            info.compress_type = zipfile.ZIP_DEFLATED
            with path.open("rb") as source:
                wheel.writestr(info, source.read())


def repair_wheel(
    wheel: Path,
    out: Path,
    *,
    delocate_wheel: str = "delocate-wheel",
    search_paths: tuple[Path, ...] = (),
) -> tuple[int, int, int, int]:
    with tempfile.TemporaryDirectory() as tempdir:
        temp = Path(tempdir)
        delocated_dir = temp / "delocated"
        delocated_dir.mkdir()
        environment = os.environ.copy()
        if search_paths:
            configured = os.pathsep.join(os.fspath(path) for path in search_paths)
            inherited = environment.get("DYLD_LIBRARY_PATH")
            environment["DYLD_LIBRARY_PATH"] = (
                f"{configured}{os.pathsep}{inherited}" if inherited else configured
            )
        subprocess.run(
            delocate_command(wheel, delocated_dir, delocate_wheel),
            check=True,
            env=environment,
        )
        delocated_wheel = delocated_dir / wheel.name
        if not delocated_wheel.is_file():
            raise RuntimeError(f"delocate did not create {delocated_wheel}")

        root = temp / "wheel"
        unpack_wheel(delocated_wheel, root)
        changed_files, changed_dependencies = rewrite_companion_dependencies(root)
        binary_count, dependency_count = audit_portable_dependencies(root)
        if changed_dependencies == 0:
            raise RuntimeError("no companion runtime dependencies were found")
        pack_wheel(root, out)
        return changed_files, changed_dependencies, binary_count, dependency_count


def main() -> int:
    if sys.platform != "darwin":
        raise SystemExit("this repair helper is only for macOS wheels")

    parser = argparse.ArgumentParser(
        description=(
            "Bundle the general macOS Sagelite dylib closure while preserving "
            "PARI and Singular libraries as companion-wheel-owned runtimes."
        )
    )
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--delocate-wheel", default="delocate-wheel")
    parser.add_argument(
        "--search-path",
        action="append",
        default=[],
        type=Path,
        help="additional build library directory used only while resolving dylibs",
    )
    args = parser.parse_args()

    if not args.wheel.is_file():
        raise SystemExit(f"input wheel not found: {args.wheel}")
    if args.out.resolve() == args.wheel.resolve():
        raise SystemExit("--out must differ from --wheel")
    missing_search_paths = [path for path in args.search_path if not path.is_dir()]
    if missing_search_paths:
        raise SystemExit(f"search path is not a directory: {missing_search_paths[0]}")

    result = repair_wheel(
        args.wheel,
        args.out,
        delocate_wheel=args.delocate_wheel,
        search_paths=tuple(args.search_path),
    )
    changed_files, changed_dependencies, binary_count, dependency_count = result
    print(
        f"repaired {changed_dependencies} companion dependencies in "
        f"{changed_files} Mach-O files"
    )
    print(
        f"audited {dependency_count} dependencies across {binary_count} Mach-O files"
    )
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
