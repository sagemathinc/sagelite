#!/usr/bin/env python3
"""
Probe Sage optional packages for binary-wheel availability.

The probe is intentionally conservative: it asks pip for a wheel or pure-Python
wheel for each not-yet-packaged optional package, without installing
dependencies. Follow-up install smoke tests decide whether a wheel-ready
package is actually a good Sagelite extra.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import sagelite_optional_package_inventory as inventory


ROOT = Path(__file__).resolve().parents[1]


REQUIREMENT_OVERRIDES = {
    "ecos_python": "ecos",
    "osqp_python": "osqp",
    "pyx": "PyX",
    "python_flint": "python-flint",
    "qdldl_python": "qdldl",
    "snappy": "snappy",
    "sqlalchemy": "SQLAlchemy",
}


def first_requirement_line(package: inventory.Package) -> str:
    if package.name in REQUIREMENT_OVERRIDES:
        return REQUIREMENT_OVERRIDES[package.name]
    package_dir = inventory.PKGS / package.name
    requirement_text = (
        inventory.read_text(package_dir / "version_requirements.txt")
        or inventory.read_text(package_dir / "requirements.txt")
        or package.pip_requirement
    )
    for line in requirement_text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return package.pip_requirement.strip()


def requirement_display(requirement: str) -> str:
    return requirement or "-"


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-") or "package"


def run_command(command: list[str], cwd: Path | None = None) -> dict[str, object]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def candidate_packages(tiers: set[str], statuses: set[str]) -> list[inventory.Package]:
    base_names, extras, sagelite_deps = inventory.load_pyproject()
    packages = [
        pkg
        for pkg_dir in sorted(inventory.PKGS.iterdir())
        if pkg_dir.is_dir()
        for pkg in [inventory.load_package(pkg_dir, base_names, extras, sagelite_deps)]
        if pkg is not None
    ]
    return [
        pkg
        for pkg in sorted(packages, key=lambda item: item.name)
        if pkg.tier in tiers and pkg.sagelite_status in statuses
    ]


def probe_package(
    python: str,
    package: inventory.Package,
    downloads_dir: Path,
    index_url: str | None,
    extra_index_url: str | None,
) -> dict[str, object]:
    requirement = first_requirement_line(package)
    package_dir = downloads_dir / package.name
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    if not requirement:
        return {
            "package": asdict(package),
            "requirement": requirement,
            "status": "no requirement",
            "artifacts": [],
            "download": None,
        }

    command = [
        python,
        "-m",
        "pip",
        "download",
        "--dest",
        str(package_dir),
        "--only-binary=:all:",
        "--no-deps",
    ]
    if index_url:
        command.extend(["--index-url", index_url])
    if extra_index_url:
        command.extend(["--extra-index-url", extra_index_url])
    command.append(requirement)

    result = run_command(command)
    artifacts = sorted(path.name for path in package_dir.iterdir() if path.is_file())
    wheels = [artifact for artifact in artifacts if artifact.endswith(".whl")]
    return {
        "package": asdict(package),
        "requirement": requirement,
        "status": "wheel" if result["returncode"] == 0 and wheels else "no wheel",
        "artifacts": artifacts,
        "wheels": wheels,
        "download": result,
    }


def render_markdown(results: list[dict[str, object]], work_dir: Path) -> str:
    wheel_ready = [result for result in results if result["status"] == "wheel"]
    missing = [result for result in results if result["status"] != "wheel"]
    lines: list[str] = []
    lines.append("# Sagelite Optional Binary-Wheel Probe")
    lines.append("")
    lines.append(
        "This generated report probes not-yet-packaged Sage optional packages "
        "for binary-wheel or pure-Python wheel availability."
    )
    lines.append("")
    lines.append("The probe command shape is:")
    lines.append("")
    lines.append("```bash")
    lines.append("python -m pip download --only-binary=:all: --no-deps <requirement>")
    lines.append("```")
    lines.append("")
    lines.append(f"Scratch output: `{work_dir}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Probed packages: {len(results)}")
    lines.append(f"- Wheel-ready packages: {len(wheel_ready)}")
    lines.append(f"- Missing/source-only packages: {len(missing)}")
    lines.append("")
    lines.append("## Wheel-Ready")
    lines.append("")
    lines.append("| Sage package | Requirement | Artifact | Notes |")
    lines.append("|---|---|---|---|")
    for result in wheel_ready:
        package = result["package"]
        assert isinstance(package, dict)
        wheels = result["wheels"]
        assert isinstance(wheels, list)
        lines.append(
            f"| `{package['name']}` | `{requirement_display(str(result['requirement']))}` | "
            f"`{', '.join(str(item) for item in wheels)}` | {package['notes']} |"
        )
    lines.append("")
    lines.append("## Missing Or Source-Only")
    lines.append("")
    lines.append("| Sage package | Requirement | Result | Likely next action |")
    lines.append("|---|---|---|---|")
    for result in missing:
        package = result["package"]
        assert isinstance(package, dict)
        download = result.get("download")
        stderr = ""
        if isinstance(download, dict):
            stderr = str(download.get("stderr", "")).splitlines()[-1:] or [""]
            stderr = stderr[0]
        lines.append(
            f"| `{package['name']}` | `{requirement_display(str(result['requirement']))}` | "
            f"{result['status']} | {stderr or package['notes']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=Path("/scratch/sagelite-optional-probes"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "agents" / "sagelite-optional-binary-wheel-probe-linux-x86_64-cp312.md",
    )
    parser.add_argument("--tier", action="append", default=["tier 1"])
    parser.add_argument("--status", action="append", default=["not packaged"])
    parser.add_argument("--index-url")
    parser.add_argument("--extra-index-url")
    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    work_dir = args.work_dir / f"binary-wheel-probe-{timestamp}"
    downloads_dir = work_dir / "downloads"
    downloads_dir.mkdir(parents=True)

    packages = candidate_packages(set(args.tier), set(args.status))
    results = [
        probe_package(
            args.python,
            package,
            downloads_dir,
            args.index_url,
            args.extra_index_url,
        )
        for package in packages
    ]

    (work_dir / "results.json").write_text(
        json.dumps(
            {
                "schema": "sagelite-optional-binary-wheel-probe-v1",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "python": args.python,
                "tiers": args.tier,
                "statuses": args.status,
                "results": results,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(results, work_dir), encoding="utf-8")
    print(args.output)
    print(work_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
