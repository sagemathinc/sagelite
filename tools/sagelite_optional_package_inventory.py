#!/usr/bin/env python3
"""
Generate a first-pass inventory of Sage optional packages for Sagelite.

This is intentionally a metadata triage tool, not a build oracle. It reads the
Sage package metadata under build/pkgs and the Sagelite extras in
pyproject.toml, then emits a Markdown report that separates already packaged
extras from plausible next candidates and known hard cases.
"""

from __future__ import annotations

import argparse
import configparser
import re
import tomllib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
PKGS = ROOT / "build" / "pkgs"
PYPROJECT = ROOT / "pyproject.toml"


def normalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def first_metadata_line(path: Path) -> str:
    text = read_text(path)
    return text.splitlines()[0].strip() if text.splitlines() else ""


def extract_rst_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower() != heading.lower():
            continue
        if i + 1 >= len(lines) or not set(lines[i + 1].strip()) <= {"-"}:
            continue
        body: list[str] = []
        for j in range(i + 2, len(lines)):
            candidate = lines[j]
            if body and candidate and not candidate.startswith((" ", "\t")):
                if j + 1 < len(lines) and set(lines[j + 1].strip()) <= {"-"}:
                    break
            body.append(candidate)
        return " ".join(part.strip() for part in body if part.strip())
    return ""


def parse_checksums(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        checksums[key.strip()] = value.strip()
    return checksums


def parse_requirement_name(requirement: str) -> str:
    requirement = requirement.strip().strip("'\"")
    requirement = requirement.split(";", 1)[0].strip()
    match = re.match(r"([A-Za-z0-9_.-]+)", requirement)
    return normalize_name(match.group(1)) if match else ""


@dataclass(frozen=True)
class Package:
    name: str
    normalized: str
    type: str
    version: str
    license: str
    upstream_url: str
    dependencies: str
    pip_requirement: str
    has_pip_metadata: bool
    has_native_install: bool
    has_patches: bool
    is_huge: bool
    has_nonfree_dependencies: bool
    has_distros: bool
    sagelite_status: str
    tier: str
    notes: str


def load_pyproject() -> tuple[set[str], dict[str, list[str]], set[str]]:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    project = data["project"]
    dependencies = project.get("dependencies", [])
    optional_dependencies = project.get("optional-dependencies", {})
    base_names = {parse_requirement_name(dep) for dep in dependencies}
    extras = {
        normalize_name(extra): list(deps)
        for extra, deps in optional_dependencies.items()
    }
    sagelite_deps = {
        parse_requirement_name(dep)
        for dep in dependencies
        if parse_requirement_name(dep).startswith("sagelite-")
    }
    for deps in optional_dependencies.values():
        for dep in deps:
            name = parse_requirement_name(dep)
            if name.startswith("sagelite-"):
                sagelite_deps.add(name)
    return base_names, extras, sagelite_deps


def matching_sagelite_deps(package: str, sagelite_deps: Iterable[str]) -> list[str]:
    package = normalize_name(package)
    candidates = {
        f"sagelite-{package}",
        f"sagelite-{package}-runtime",
        f"sagelite-{package}-data",
    }
    return sorted(
        dep
        for dep in sagelite_deps
        if dep in candidates
        or dep.startswith(f"sagelite-{package}-")
        or dep.endswith(f"-{package}")
        or dep.endswith(f"-{package}-runtime")
    )


def package_status(
    normalized: str,
    base_names: set[str],
    extras: dict[str, list[str]],
    sagelite_deps: set[str],
) -> str:
    if normalized in base_names:
        return "base dependency"
    if normalized in extras:
        deps = [parse_requirement_name(dep) for dep in extras[normalized]]
        if any(dep.startswith("sagelite-") for dep in deps):
            return "extra -> companion"
        return "extra -> PyPI/system"
    matches = matching_sagelite_deps(normalized, sagelite_deps)
    if matches:
        return "companion dependency"
    return "not packaged"


def classify_tier(
    name: str,
    type_: str,
    status: str,
    has_nonfree_dependencies: bool,
    is_huge: bool,
    has_pip_metadata: bool,
    has_native_install: bool,
    has_patches: bool,
    has_distros: bool,
    license_hint: str,
) -> tuple[str, str]:
    license_lower = license_hint.lower()
    if name.startswith("_"):
        return "tier 3", "internal Sage aggregate/tooling package"
    if name.startswith("sagemath_"):
        return "tier 3", "modular Sage split package, not a Sagelite optional target"
    if name in {"auditwheel_or_delocate", "ccache", "gdb", "git", "github_cli", "llvm"}:
        return "tier 3", "developer/build tooling, not user-facing Sage functionality"
    if has_nonfree_dependencies or "proprietary" in license_lower or "non-free" in license_lower:
        return "excluded", "nonfree dependency or license signal"
    if status != "not packaged":
        return "tier 0", "already represented in Sagelite metadata"
    if is_huge:
        return "tier 3", "large data/runtime payload"
    if type_ == "experimental":
        return "tier 3", "Sage marks this package experimental"
    if has_pip_metadata and not has_native_install:
        return "tier 1", "pip-style package metadata"
    if has_pip_metadata and has_native_install and not has_patches:
        return "tier 1", "pip package with Sage install wrapper"
    if has_native_install and has_distros and not has_patches:
        return "tier 2", "native source package with distro package names"
    if has_native_install:
        return "tier 3", "native source package needing build work"
    return "tier 2", "metadata needs manual review"


def load_package(pkg_dir: Path, base_names: set[str], extras: dict[str, list[str]], sagelite_deps: set[str]) -> Package | None:
    type_ = first_metadata_line(pkg_dir / "type")
    if type_ not in {"optional", "experimental"}:
        return None
    name = pkg_dir.name
    normalized = normalize_name(name)
    rst = read_text(pkg_dir / "SPKG.rst")
    checksums = parse_checksums(pkg_dir / "checksums.ini")
    pip_requirement = (
        first_metadata_line(pkg_dir / "version_requirements.txt")
        or first_metadata_line(pkg_dir / "requirements.txt")
    )
    has_pip_metadata = bool(pip_requirement)
    has_native_install = (pkg_dir / "spkg-install.in").exists() or (pkg_dir / "spkg-install").exists()
    has_patches = (pkg_dir / "patches").exists()
    is_huge = (pkg_dir / "huge").exists()
    has_nonfree_dependencies = (pkg_dir / "has_nonfree_dependencies").exists()
    has_distros = (pkg_dir / "distros").exists()
    license_hint = extract_rst_section(rst, "License") or "unknown"
    status = package_status(normalized, base_names, extras, sagelite_deps)
    tier, notes = classify_tier(
        name,
        type_,
        status,
        has_nonfree_dependencies,
        is_huge,
        has_pip_metadata,
        has_native_install,
        has_patches,
        has_distros,
        license_hint,
    )
    return Package(
        name=name,
        normalized=normalized,
        type=type_,
        version=first_metadata_line(pkg_dir / "package-version.txt"),
        license=license_hint,
        upstream_url=checksums.get("upstream_url", ""),
        dependencies=first_metadata_line(pkg_dir / "dependencies"),
        pip_requirement=pip_requirement,
        has_pip_metadata=has_pip_metadata,
        has_native_install=has_native_install,
        has_patches=has_patches,
        is_huge=is_huge,
        has_nonfree_dependencies=has_nonfree_dependencies,
        has_distros=has_distros,
        sagelite_status=status,
        tier=tier,
        notes=notes,
    )


def md_escape(value: str) -> str:
    value = value.replace("\n", " ").strip()
    value = value.replace("|", "\\|")
    return value or "-"


def package_row(pkg: Package) -> str:
    flags = []
    if pkg.has_pip_metadata:
        flags.append("pip")
    if pkg.has_native_install:
        flags.append("native")
    if pkg.has_patches:
        flags.append("patches")
    if pkg.is_huge:
        flags.append("huge")
    if pkg.has_nonfree_dependencies:
        flags.append("nonfree-deps")
    if pkg.has_distros:
        flags.append("distros")
    return (
        f"| `{pkg.name}` | {md_escape(pkg.version)} | {md_escape(pkg.license)} | "
        f"{md_escape(pkg.sagelite_status)} | {md_escape(', '.join(flags))} | "
        f"{md_escape(pkg.dependencies)} | {md_escape(pkg.notes)} |"
    )


def write_table(lines: list[str], packages: list[Package], limit: int | None = None) -> None:
    lines.append("| Package | Version | License hint | Sagelite status | Signals | Sage dependencies | Notes |")
    lines.append("|---|---:|---|---|---|---|---|")
    for pkg in packages[:limit]:
        lines.append(package_row(pkg))
    if limit is not None and len(packages) > limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | {len(packages) - limit} more omitted |")


def render(packages: list[Package]) -> str:
    packages = sorted(packages, key=lambda pkg: (pkg.tier, pkg.type, pkg.name))
    by_type = Counter(pkg.type for pkg in packages)
    by_tier = Counter(pkg.tier for pkg in packages)
    by_status = Counter(pkg.sagelite_status for pkg in packages)

    lines: list[str] = []
    lines.append("# Sagelite Optional Package Inventory")
    lines.append("")
    lines.append("This generated report is a first-pass triage of Sage packages whose")
    lines.append("`build/pkgs/*/type` is `optional` or `experimental`. It is not a legal")
    lines.append("review and it is not proof that a package builds as a wheel.")
    lines.append("")
    lines.append("Regenerate with:")
    lines.append("")
    lines.append("```bash")
    lines.append("python tools/sagelite_optional_package_inventory.py > agents/sagelite-optional-package-inventory.md")
    lines.append("```")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Optional/experimental package directories: {len(packages)}")
    lines.append(f"- By Sage type: {', '.join(f'{key}={value}' for key, value in sorted(by_type.items()))}")
    lines.append(f"- By triage tier: {', '.join(f'{key}={value}' for key, value in sorted(by_tier.items()))}")
    lines.append(f"- By Sagelite status: {', '.join(f'{key}={value}' for key, value in sorted(by_status.items()))}")
    lines.append("")
    lines.append("Tier meanings:")
    lines.append("")
    lines.append("- `tier 0`: already represented in Sagelite base dependencies, extras, or companion-wheel metadata.")
    lines.append("- `tier 1`: likely first-batch candidate: pip-style metadata, no huge/nonfree signal, and limited native packaging risk.")
    lines.append("- `tier 2`: plausible but needs native packaging or manual metadata review.")
    lines.append("- `tier 3`: high-risk, huge, experimental, patched native source, or otherwise likely to need focused work.")
    lines.append("- `excluded`: nonfree dependency or license signal in Sage metadata.")
    lines.append("")

    for tier in ["tier 1", "tier 2", "tier 3", "excluded", "tier 0"]:
        tier_packages = [pkg for pkg in packages if pkg.tier == tier]
        if not tier_packages:
            continue
        title = {
            "tier 1": "First-Batch Candidates",
            "tier 2": "Second-Batch Candidates",
            "tier 3": "Hard Cases",
            "excluded": "Excluded By Metadata Signal",
            "tier 0": "Already Represented",
        }[tier]
        lines.append(f"## {title}")
        lines.append("")
        write_table(lines, sorted(tier_packages, key=lambda pkg: pkg.name), None)
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    base_names, extras, sagelite_deps = load_pyproject()
    packages = [
        pkg
        for pkg_dir in sorted(PKGS.iterdir())
        if pkg_dir.is_dir()
        for pkg in [load_package(pkg_dir, base_names, extras, sagelite_deps)]
        if pkg is not None
    ]
    print(render(packages), end="")


if __name__ == "__main__":
    main()
