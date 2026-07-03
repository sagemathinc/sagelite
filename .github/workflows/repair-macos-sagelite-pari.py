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


PARI_RUNTIME_PREFIXES = (
    "libpari",
    "libgmp",
    "libmpfr",
    "libmpfi",
)


def unpack_wheel(wheel_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(wheel_path) as wheel:
        wheel.extractall(dest)


def is_macho(path: Path) -> bool:
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


def otool_libraries(path: Path) -> list[str]:
    output = subprocess.run(
        ["otool", "-L", os.fspath(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [line.strip().split(maxsplit=1)[0] for line in output.splitlines()[1:]]


def is_pari_runtime_dependency(path: str) -> bool:
    return Path(path).name.startswith(PARI_RUNTIME_PREFIXES)


def repair_extensions(root: Path) -> int:
    runtime_lib_dir = root / "sagelite_pari" / "data" / "lib"
    changed = 0
    for extension in sorted(root.rglob("*.so")):
        if not is_macho(extension):
            continue
        args: list[str] = []
        rel_runtime_lib_dir = os.path.relpath(runtime_lib_dir, extension.parent)
        for dependency in otool_libraries(extension):
            if is_pari_runtime_dependency(dependency):
                args.extend(
                    [
                        "-change",
                        dependency,
                        f"@loader_path/{rel_runtime_lib_dir}/{Path(dependency).name}",
                    ]
                )
        if args:
            subprocess.run(["install_name_tool", *args, os.fspath(extension)], check=True)
            changed += 1
            if shutil.which("codesign") is not None:
                subprocess.run(
                    ["codesign", "--force", "--sign", "-", os.fspath(extension)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
    return changed


def record_row(path: Path, root: Path) -> tuple[str, str, str]:
    data = path.read_bytes()
    digest = hashlib.sha256(data).digest()
    encoded = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    relpath = path.relative_to(root).as_posix()
    return relpath, f"sha256={encoded}", str(len(data))


def pack_wheel(root: Path, wheel_path: Path) -> None:
    dist_info = next(root.glob("*.dist-info"))
    record_path = dist_info / "RECORD"

    rows: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == record_path:
            continue
        rows.append(record_row(path, root))

    with record_path.open("w", encoding="utf-8", newline="") as record_file:
        writer = csv.writer(record_file)
        writer.writerows(rows)
        writer.writerow((record_path.relative_to(root).as_posix(), "", ""))

    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as wheel:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            arcname = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo.from_file(path, arcname)
            info.compress_type = zipfile.ZIP_DEFLATED
            with path.open("rb") as source:
                wheel.writestr(info, source.read())


def main() -> int:
    if sys.platform != "darwin":
        raise SystemExit("this repair helper is only for macOS wheels")

    parser = argparse.ArgumentParser(
        description=(
            "Rewrite macOS sagelite extension modules to load PARI, GMP, "
            "and MPFR from the sagelite-pari-runtime companion package."
        )
    )
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    if not args.wheel.is_file():
        raise SystemExit(f"raw wheel not found: {args.wheel}")

    with tempfile.TemporaryDirectory() as tempdir:
        root = Path(tempdir) / "wheel"
        unpack_wheel(args.wheel, root)
        changed = repair_extensions(root)
        if changed == 0:
            raise SystemExit("no extension modules referenced PARI runtime libraries")
        pack_wheel(root, args.out)
        print(f"repaired {changed} extension modules")

    return 0


if __name__ == "__main__":
    sys.exit(main())
