#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import re
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


WHEEL_FILENAME_RE = re.compile(
    r"^(?P<namever>sagelite-(?P<version>[^-]+))-(?P<tags>.+)\.whl$"
)


def unpack_wheel(wheel_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(wheel_path) as wheel:
        wheel.extractall(dest)


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


def load_optional_dependencies(pyproject: Path) -> dict[str, list[str]]:
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    return data["project"]["optional-dependencies"]


def format_extra_requirement(requirement: str, extra: str) -> str:
    if ";" not in requirement:
        return f'Requires-Dist: {requirement}; extra == "{extra}"'
    dependency, marker = requirement.split(";", 1)
    return (
        f'Requires-Dist: {dependency.strip()}; '
        f'({marker.strip()}) and extra == "{extra}"'
    )


def add_optional_metadata(
    metadata_path: Path,
    extras: dict[str, list[str]],
    extra_names: list[str],
    version: str,
) -> None:
    lines = metadata_path.read_text(encoding="utf-8").splitlines()
    updated: list[str] = []
    skip_extra: str | None = None

    for line in lines:
        if line.startswith("Version: "):
            updated.append(f"Version: {version}")
            continue
        if line.startswith("Provides-Extra: "):
            extra = line.split(":", 1)[1].strip()
            skip_extra = extra if extra in extra_names else None
            if skip_extra is not None:
                continue
        elif line.startswith("Requires-Dist: ") and skip_extra is not None:
            if f'extra == "{skip_extra}"' in line or f"extra == '{skip_extra}'" in line:
                continue
            skip_extra = None
        else:
            skip_extra = None
        updated.append(line)

    insert_at = next(
        (
            index
            for index, line in enumerate(updated)
            if line.startswith("Provides-Extra: ")
        ),
        len(updated),
    )
    extra_lines: list[str] = []
    for extra in extra_names:
        if extra not in extras:
            raise SystemExit(f"extra {extra!r} is not present in pyproject metadata")
        extra_lines.append(f"Provides-Extra: {extra}")
        extra_lines.extend(format_extra_requirement(req, extra) for req in extras[extra])

    updated[insert_at:insert_at] = extra_lines
    metadata_path.write_text("\n".join(updated) + "\n", encoding="utf-8")


def update_sage_version(root: Path, version: str) -> None:
    version_path = root / "sage" / "version.py"
    text = version_path.read_text(encoding="utf-8")
    text = re.sub(r"^version = '.*'$", f"version = '{version}'", text, flags=re.M)
    text = re.sub(
        r"^banner = 'SageMath version .*?, Release Date: (.*?)'$",
        f"banner = 'SageMath version {version}, Release Date: \\1'",
        text,
        flags=re.M,
    )
    version_path.write_text(text, encoding="utf-8")


def retag_wheel(
    wheel_path: Path,
    out_dir: Path,
    version: str,
    pyproject: Path,
    extra_names: list[str],
) -> Path:
    match = WHEEL_FILENAME_RE.match(wheel_path.name)
    if match is None:
        raise SystemExit(f"unsupported wheel filename: {wheel_path.name}")

    out_name = f"sagelite-{version}-{match.group('tags')}.whl"
    out_path = out_dir / out_name
    optional_dependencies = load_optional_dependencies(pyproject)

    with tempfile.TemporaryDirectory() as tempdir:
        root = Path(tempdir) / "wheel"
        unpack_wheel(wheel_path, root)

        old_dist_info = root / f"sagelite-{match.group('version')}.dist-info"
        new_dist_info = root / f"sagelite-{version}.dist-info"
        if not old_dist_info.is_dir():
            raise SystemExit(f"dist-info directory not found: {old_dist_info.name}")
        old_dist_info.rename(new_dist_info)

        add_optional_metadata(
            new_dist_info / "METADATA",
            optional_dependencies,
            extra_names,
            version,
        )
        update_sage_version(root, version)
        pack_wheel(root, out_path)

    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Retag repaired sagelite wheels for metadata-only preview releases."
        )
    )
    parser.add_argument("wheels", nargs="+", type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--pyproject", default=Path("pyproject.toml"), type=Path)
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        help="optional dependency group to refresh in the wheel metadata",
    )
    args = parser.parse_args()

    if not args.extra:
        raise SystemExit("at least one --extra is required")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for wheel in args.wheels:
        if not wheel.is_file():
            raise SystemExit(f"wheel not found: {wheel}")
        out_path = retag_wheel(
            wheel,
            args.out_dir,
            args.version,
            args.pyproject,
            args.extra,
        )
        print(out_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
