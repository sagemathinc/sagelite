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


def find_cypari_package_root(prefix: Path) -> Path:
    matches = sorted(path.parent.parent for path in prefix.rglob("cypari2/__init__.py"))
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


def copytree_if_present(src: Path, dest: Path) -> None:
    if not src.exists():
        return
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        src,
        dest,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )


def reject_private_pari_runtime(src_root: Path) -> None:
    libraries = sorted((src_root / "cypari2.libs").glob("libpari*"))
    if libraries:
        joined = "\n".join(str(path) for path in libraries)
        raise SystemExit(
            "refusing to vendor cypari2 with a private PARI runtime. "
            "Build cypari2 from source against Sage's PARI before merging it "
            f"into sagelite:\n{joined}"
        )


def reject_private_pari_extension_dependencies(src_root: Path) -> None:
    """
    Reject cypari2 extension modules that still name an auditwheel-private PARI.

    Source-built cypari2 should link to the ordinary ``libpari.so`` from the
    Sage prefix.  Prebuilt wheels often depend on a hashed ``libpari-*.so``;
    copying such an extension into sagelite can later load a second PARI
    runtime even if the companion ``cypari2.libs`` directory was pruned.
    """
    offenders = []
    for extension in sorted((src_root / "cypari2").glob("*.so")):
        try:
            payload = extension.read_bytes()
        except OSError:
            continue
        if b"libpari-" in payload:
            offenders.append(extension)

    if offenders:
        joined = "\n".join(str(path) for path in offenders)
        raise SystemExit(
            "refusing to vendor cypari2 extension modules that still depend "
            "on an auditwheel-private PARI runtime. Build cypari2 from source "
            f"against Sage's PARI before merging it into sagelite:\n{joined}"
        )


def copy_cypari_runtime(src_root: Path, dest_root: Path) -> None:
    reject_private_pari_runtime(src_root)
    reject_private_pari_extension_dependencies(src_root)
    copytree_if_present(src_root / "cypari2", dest_root / "cypari2")
    copytree_if_present(src_root / "cypari2.libs", dest_root / "cypari2.libs")


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

    cypari_root = find_cypari_package_root(args.prefix)

    with tempfile.TemporaryDirectory() as tempdir:
        root = Path(tempdir) / "wheel"
        unpack_wheel(args.wheel, root)
        copy_cypari_runtime(cypari_root, root)
        metadata_path = next(root.glob("*.dist-info/METADATA"))
        remove_external_cypari_requirement(metadata_path)
        pack_wheel(root, args.out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
