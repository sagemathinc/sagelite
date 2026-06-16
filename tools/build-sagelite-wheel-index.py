#!/usr/bin/env python3
"""Build a small PEP 503-style simple index for wheel artifacts."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import shutil
from pathlib import Path
from urllib.parse import quote


NORMALIZE_RE = re.compile(r"[-_.]+")


def normalized_project_name(name: str) -> str:
    return NORMALIZE_RE.sub("-", name).lower()


def project_name_from_wheel(path: Path) -> str:
    if path.suffix != ".whl":
        raise ValueError(f"not a wheel filename: {path.name}")
    parts = path.name.split("-")
    if len(parts) < 5:
        raise ValueError(f"invalid wheel filename: {path.name}")
    return normalized_project_name(parts[0])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_html(path: Path, title: str, links: list[tuple[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = "\n".join(
        f'    <a href="{html.escape(href, quote=True)}">{html.escape(label)}</a><br>'
        for label, href in links
    )
    path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<html>",
                "  <head>",
                '    <meta charset="utf-8">',
                f"    <title>{html.escape(title)}</title>",
                "  </head>",
                "  <body>",
                f"    <h1>{html.escape(title)}</h1>",
                rows,
                "  </body>",
                "</html>",
                "",
            ]
        ),
        encoding="utf-8",
    )


def wheel_href(wheel: Path, wheel_base_url: str | None) -> str:
    filename = quote(wheel.name)
    if wheel_base_url:
        return f"{wheel_base_url.rstrip('/')}/{filename}#sha256={sha256(wheel)}"
    return f"../../wheels/{filename}#sha256={sha256(wheel)}"


def build_index(
    wheels_dir: Path, output_dir: Path, wheel_base_url: str | None = None
) -> dict[str, list[Path]]:
    wheels = sorted(wheels_dir.glob("*.whl"))
    if not wheels:
        raise SystemExit(f"no wheels found in {wheels_dir}")

    projects: dict[str, list[Path]] = {}
    for wheel in wheels:
        projects.setdefault(project_name_from_wheel(wheel), []).append(wheel)

    shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_html(
        output_dir / "index.html",
        "Sagelite wheel index",
        [(name, f"{name}/") for name in sorted(projects)],
    )

    for name, project_wheels in sorted(projects.items()):
        links = []
        for wheel in sorted(project_wheels):
            links.append((wheel.name, wheel_href(wheel, wheel_base_url)))
        write_html(output_dir / name / "index.html", name, links)

    return projects


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheels_dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path("simple"))
    parser.add_argument(
        "--wheel-base-url",
        help="External URL prefix for wheel files; defaults to ../.. relative links.",
    )
    args = parser.parse_args()

    projects = build_index(args.wheels_dir, args.output, args.wheel_base_url)
    print(f"indexed {sum(len(wheels) for wheels in projects.values())} wheels")
    print(f"indexed {len(projects)} projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
