#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def find_cypari_package(prefix: Path) -> Path:
    matches = sorted(path.parent for path in prefix.rglob("cypari2/__init__.py"))
    if not matches:
        raise SystemExit(f"cypari2 package not found under {prefix}")
    if len(matches) > 1:
        joined = "\n".join(str(path) for path in matches)
        raise SystemExit(f"multiple cypari2 package directories found under {prefix}:\n{joined}")
    return matches[0]


def unpack_wheel(wheel_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(wheel_path) as wheel:
        wheel.extractall(dest)


def remove_external_cypari_requirement(metadata_path: Path) -> None:
    lines = metadata_path.read_text(encoding="utf-8").splitlines()
    filtered = [line for line in lines if not line.startswith("Requires-Dist: cypari2")]
    metadata_path.write_text("\n".join(filtered) + "\n", encoding="utf-8")


def copy_cypari_package(src: Path, dest_root: Path) -> None:
    dest = dest_root / "cypari2"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        src,
        dest,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )


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
        if not path.is_file():
            continue
        if path == record_path:
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
    parser = argparse.ArgumentParser(
        description="Merge the source-built cypari2 package into a raw project wheel before auditwheel repair.",
    )
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--prefix", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    if not args.wheel.is_file():
        raise SystemExit(f"raw wheel not found: {args.wheel}")

    cypari_package = find_cypari_package(args.prefix)

    with tempfile.TemporaryDirectory() as tempdir:
        root = Path(tempdir) / "wheel"
        unpack_wheel(args.wheel, root)
        copy_cypari_package(cypari_package, root)
        metadata_path = next(root.glob("*.dist-info/METADATA"))
        remove_external_cypari_requirement(metadata_path)
        pack_wheel(root, args.out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
