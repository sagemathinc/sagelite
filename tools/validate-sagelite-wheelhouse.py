#!/usr/bin/env python3
"""
Create a fresh sagelite install from a wheelhouse and run installed validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import shlex
import subprocess
import sys
import sysconfig
import time
import tomllib
from datetime import datetime
from pathlib import Path

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import SpecifierSet
from packaging import tags as packaging_tags
from packaging.version import InvalidVersion, Version

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
if os.fspath(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, os.fspath(TOOLS_DIR))

import sagelite_native_wheel_catalog

RUNNER = TOOLS_DIR / "run-installed-wheel-doctests.py"
DEFAULT_WORK_DIR = Path("/scratch/sagelite-r2-work")
DEFAULT_PACKAGE = "sagelite[all-needed-extras]"
VALIDATION_PHASES = (
    "create virtual environment",
    "upgrade pip",
    "install wheelhouse package",
    "run pip check",
    "run installed doctest validation",
)

RUNTIME_ENV_PREFIXES_TO_REMOVE = (
    "SAGE_",
    "SAGELITE_",
    "MAXIMA_",
    "FRICAS",
    "ALDOR",
    "FPLLL",
)
RUNTIME_ENV_KEYS_TO_REMOVE = {
    "GAP_ROOT_PATHS",
    "LD_LIBRARY_PATH",
    "MAXIMA",
    "PYTHONPATH",
    }


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    print(f"+ {' '.join(shlex.quote(part) for part in command)}", flush=True)
    return subprocess.run(command, check=False, text=True, env=env)


def _clean_environment() -> dict[str, str]:
    env = os.environ.copy()
    for key in list(env):
        if key in RUNTIME_ENV_KEYS_TO_REMOVE or key.startswith(
            RUNTIME_ENV_PREFIXES_TO_REMOVE
        ):
            env.pop(key, None)
    env["PYTHONNOUSERSITE"] = "1"
    return env


def _ensure_wheelhouses(paths: list[Path]) -> list[Path]:
    wheelhouses = [path.resolve() for path in paths]
    missing = [path for path in wheelhouses if not path.is_dir()]
    if missing:
        raise FileNotFoundError(
            "wheelhouse directory does not exist: "
            + ", ".join(os.fspath(path) for path in missing)
        )
    return wheelhouses


def _wheel_tags(wheel: Path) -> dict[str, list[str]]:
    if wheel.suffix != ".whl":
        return {"python": [], "abi": [], "platform": []}
    parts = wheel.name[:-4].split("-")
    if len(parts) < 5:
        return {"python": [], "abi": [], "platform": []}
    return {
        "python": parts[-3].split("."),
        "abi": parts[-2].split("."),
        "platform": parts[-1].split("."),
    }


def _wheel_version(wheel: Path) -> str | None:
    if wheel.suffix != ".whl":
        return None
    parts = wheel.name[:-4].split("-")
    if len(parts) < 5:
        return None
    return parts[1]


def _wheel_file_identity(wheel: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with wheel.open("rb") as wheel_file:
        for chunk in iter(lambda: wheel_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "size_bytes": wheel.stat().st_size,
        "sha256": digest.hexdigest(),
    }


def _wheel_platform_tags(wheel: Path) -> list[str]:
    return _wheel_tags(wheel)["platform"]


def _is_sagelite_project_wheel(wheel: Path) -> bool:
    return re.match(r"^sagelite[-_]", wheel.name) is not None


def _is_primary_sagelite_wheel(wheel: Path) -> bool:
    return wheel.name.startswith("sagelite-")


def _wheel_project_name(wheel: Path) -> str | None:
    if wheel.suffix != ".whl":
        return None
    parts = wheel.name[:-4].split("-")
    if len(parts) < 5:
        return None
    return parts[0].replace("_", "-").lower()


def _sagelite_requirement_name(requirement: str) -> str | None:
    match = re.match(r"\s*([A-Za-z0-9_.-]+)", requirement)
    if not match:
        return None
    name = match.group(1).replace("_", "-").lower()
    if not name.startswith("sagelite-"):
        return None
    return name


def _sagelite_project_requirements() -> dict[str, list[str]]:
    requirements_by_name: dict[str, list[str]] = {}
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as pyproject:
        data = tomllib.load(pyproject)
    requirements = list(data["project"]["dependencies"])
    for extra_requirements in data["project"]["optional-dependencies"].values():
        requirements.extend(extra_requirements)

    for requirement_text in requirements:
        try:
            requirement = Requirement(requirement_text)
        except InvalidRequirement:
            continue
        name = requirement.name.replace("_", "-").lower()
        if not name.startswith("sagelite-"):
            continue
        requirements_by_name.setdefault(name, [])
        if str(requirement.specifier) not in requirements_by_name[name]:
            requirements_by_name[name].append(str(requirement.specifier))
    return requirements_by_name


def _all_needed_extra_sagelite_packages() -> list[str]:
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as pyproject:
        data = tomllib.load(pyproject)
    requirements = data["project"]["optional-dependencies"]["all-needed-extras"]
    package_names = {
        name
        for requirement in requirements
        if (name := _sagelite_requirement_name(requirement)) is not None
    }
    return sorted(package_names)


def _is_repaired_linux_wheel(wheel: Path) -> bool:
    return any(
        tag.startswith(("manylinux", "musllinux"))
        for tag in _wheel_platform_tags(wheel)
    )


def _is_raw_linux_wheel(wheel: Path) -> bool:
    return any(tag.startswith("linux_") for tag in _wheel_platform_tags(wheel))


def wheelhouse_inventory(wheelhouses: list[Path]) -> dict[str, object]:
    sagelite_requirements = _sagelite_project_requirements()
    files: list[dict[str, object]] = []
    for wheelhouse in wheelhouses:
        for wheel in sorted(wheelhouse.glob("*.whl")):
            wheel_tags = _wheel_tags(wheel)
            wheel_identity = _wheel_file_identity(wheel)
            is_primary_sagelite = _is_primary_sagelite_wheel(wheel)
            project_name = _wheel_project_name(wheel)
            version = _wheel_version(wheel)
            files.append(
                {
                    "name": wheel.name,
                    "path": os.fspath(wheel),
                    "wheelhouse": os.fspath(wheelhouse),
                    "project_name": project_name,
                    "version": version,
                    "size_bytes": wheel_identity["size_bytes"],
                    "sha256": wheel_identity["sha256"],
                    "python_tags": wheel_tags["python"],
                    "abi_tags": wheel_tags["abi"],
                    "platform_tags": wheel_tags["platform"],
                    "is_sagelite_project_wheel": _is_sagelite_project_wheel(wheel),
                    "is_primary_sagelite_wheel": is_primary_sagelite,
                    "is_repaired_linux_wheel": _is_repaired_linux_wheel(wheel),
                    "is_raw_linux_wheel": _is_raw_linux_wheel(wheel),
                }
            )
    primary_sagelite_wheels = [
        file for file in files if file["is_primary_sagelite_wheel"]
    ]
    duplicate_primary_sagelite_wheel_names = sorted(
        str(file["name"]) for file in primary_sagelite_wheels
    ) if len(primary_sagelite_wheels) > 1 else []
    sagelite_project_wheels = [
        file for file in files if file["is_sagelite_project_wheel"]
    ]
    companion_sagelite_wheels = [
        file
        for file in sagelite_project_wheels
        if not file["is_primary_sagelite_wheel"]
    ]
    companion_package_names = sorted(
        {
            str(file["project_name"])
            for file in companion_sagelite_wheels
            if file["project_name"]
        }
    )
    duplicate_companion_package_names = sorted(
        {
            str(file["project_name"])
            for file in companion_sagelite_wheels
            if file["project_name"]
            and sum(
                1
                for other in companion_sagelite_wheels
                if other["project_name"] == file["project_name"]
            )
            > 1
        }
    )
    all_needed_extra_packages = _all_needed_extra_sagelite_packages()
    missing_all_needed_extra_packages = sorted(
        set(all_needed_extra_packages) - set(companion_package_names)
    )
    unsatisfied_companion_requirements = []
    for file in companion_sagelite_wheels:
        project_name = file.get("project_name")
        version = file.get("version")
        if not project_name or not version:
            continue
        specifiers = sagelite_requirements.get(str(project_name), [])
        if not specifiers:
            continue
        try:
            parsed_version = Version(str(version))
        except InvalidVersion:
            unsatisfied_companion_requirements.append(
                {
                    "name": file["name"],
                    "project_name": project_name,
                    "version": version,
                    "required_specifiers": specifiers,
                    "reason": "invalid wheel version",
                }
            )
            continue
        failed_specifiers = [
            specifier
            for specifier in specifiers
            if specifier and parsed_version not in SpecifierSet(specifier)
        ]
        if failed_specifiers:
            unsatisfied_companion_requirements.append(
                {
                    "name": file["name"],
                    "project_name": project_name,
                    "version": version,
                    "required_specifiers": failed_specifiers,
                    "reason": "version does not satisfy sagelite requirements",
                }
            )
    return {
        "files": files,
        "sagelite_project_wheels": sagelite_project_wheels,
        "primary_sagelite_wheels": primary_sagelite_wheels,
        "duplicate_primary_sagelite_wheel_names": (
            duplicate_primary_sagelite_wheel_names
        ),
        "companion_sagelite_wheels": companion_sagelite_wheels,
        "companion_sagelite_package_names": companion_package_names,
        "duplicate_companion_sagelite_package_names": duplicate_companion_package_names,
        "unsatisfied_companion_sagelite_requirements": (
            unsatisfied_companion_requirements
        ),
        "all_needed_extra_sagelite_packages": all_needed_extra_packages,
        "missing_all_needed_extra_sagelite_packages": missing_all_needed_extra_packages,
        "contains_primary_sagelite_wheel": bool(primary_sagelite_wheels),
        "contains_companion_sagelite_wheels": bool(companion_sagelite_wheels),
        "contains_all_needed_extra_sagelite_wheels": not missing_all_needed_extra_packages,
        "contains_repaired_primary_sagelite_wheel": any(
            file["is_repaired_linux_wheel"] for file in primary_sagelite_wheels
        ),
        "contains_raw_linux_primary_sagelite_wheel": any(
            file["is_raw_linux_wheel"] for file in primary_sagelite_wheels
        ),
}


def _ensure_single_primary_sagelite_wheel(inventory: dict[str, object]) -> None:
    wheels = inventory["primary_sagelite_wheels"]  # type: ignore[index]
    if not isinstance(wheels, list):
        wheels = []
    if len(wheels) <= 1:
        return
    names = [
        str(wheel.get("name"))
        for wheel in wheels
        if isinstance(wheel, dict) and wheel.get("name")
    ]
    raise RuntimeError(
        "duplicate primary sagelite wheels are not allowed for validation: "
        + ", ".join(names)
    )


def _ensure_repaired_sagelite_wheel(inventory: dict[str, object]) -> None:
    wheels = [
        str(file["name"])
        for file in inventory["primary_sagelite_wheels"]  # type: ignore[index]
    ]
    detail = ", ".join(wheels) if wheels else "none"
    if len(wheels) != 1:
        raise RuntimeError(
            "exactly one primary sagelite wheel is required for repaired-wheel "
            f"validation; primary sagelite wheels: {detail}"
        )
    if inventory["contains_repaired_primary_sagelite_wheel"]:
        return
    raise RuntimeError(
        "repaired sagelite wheel is required but no primary sagelite wheel has a "
        f"manylinux or musllinux platform tag; primary sagelite wheels: {detail}"
    )


def _ensure_all_needed_extra_sagelite_wheels(inventory: dict[str, object]) -> None:
    missing = inventory["missing_all_needed_extra_sagelite_packages"]
    if not isinstance(missing, list):
        missing = []
    if not missing:
        return
    raise RuntimeError(
        "all-needed-extras companion sagelite wheels are required but missing: "
        + ", ".join(str(package) for package in missing)
    )


def _ensure_no_duplicate_companion_sagelite_wheels(
    inventory: dict[str, object],
) -> None:
    duplicates = inventory["duplicate_companion_sagelite_package_names"]
    if not isinstance(duplicates, list):
        duplicates = []
    if not duplicates:
        return
    raise RuntimeError(
        "duplicate sagelite companion wheels are not allowed for validation: "
        + ", ".join(str(package) for package in duplicates)
    )


def _ensure_companion_sagelite_wheel_requirements(
    inventory: dict[str, object],
) -> None:
    unsatisfied = inventory["unsatisfied_companion_sagelite_requirements"]
    if not isinstance(unsatisfied, list):
        unsatisfied = []
    if not unsatisfied:
        return
    details = []
    for item in unsatisfied:
        if not isinstance(item, dict):
            continue
        specifiers = item.get("required_specifiers", [])
        if not isinstance(specifiers, list):
            specifiers = []
        details.append(
            f"{item.get('name')} version {item.get('version')} requires "
            + ", ".join(str(specifier) for specifier in specifiers)
        )
    raise RuntimeError(
        "sagelite companion wheel versions do not satisfy sagelite package "
        "requirements: "
        + "; ".join(details)
    )


def _primary_sagelite_requirement(package: str) -> dict[str, object]:
    try:
        requirement = Requirement(package)
    except InvalidRequirement as exc:
        return {
            "package": package,
            "name": None,
            "extras": [],
            "specifier": None,
            "applies_to_sagelite": False,
            "requests_all_needed_extras": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    name = requirement.name.replace("_", "-").lower()
    extras = sorted(requirement.extras)
    return {
        "package": package,
        "name": name,
        "extras": extras,
        "specifier": str(requirement.specifier),
        "applies_to_sagelite": name == "sagelite",
        "requests_all_needed_extras": "all-needed-extras" in extras,
        "error": None,
    }


def _ensure_package_requests_all_needed_extras(package: str) -> None:
    requested = _primary_sagelite_requirement(package)
    if requested.get("error"):
        raise RuntimeError(
            "requested package requirement could not be parsed for "
            "all-needed-extras validation: "
            + str(requested.get("error"))
        )
    if requested.get("applies_to_sagelite") is not True:
        raise RuntimeError(
            "all-needed-extras validation requires a sagelite package "
            f"requirement, but requested package is {package!r}"
        )
    if requested.get("requests_all_needed_extras") is True:
        return
    extras = requested.get("extras", [])
    if not isinstance(extras, list):
        extras = []
    rendered_extras = ", ".join(str(extra) for extra in extras) or "none"
    raise RuntimeError(
        "strict repaired-wheelhouse validation must install "
        "sagelite[all-needed-extras]; requested package extras: "
        f"{rendered_extras}"
    )


def _primary_sagelite_wheel_requirement_satisfaction(
    inventory: dict[str, object],
    package: str,
) -> list[dict[str, object]]:
    requested = _primary_sagelite_requirement(package)
    specifier_text = requested.get("specifier")
    applies = requested.get("applies_to_sagelite") is True
    wheels = inventory["primary_sagelite_wheels"]  # type: ignore[index]
    if not isinstance(wheels, list):
        wheels = []
    report = []
    for wheel in wheels:
        if not isinstance(wheel, dict):
            continue
        version = wheel.get("version")
        satisfied = True
        reason = "no sagelite version specifier requested"
        if requested.get("error"):
            satisfied = False
            reason = "requested package requirement could not be parsed"
        elif not applies:
            satisfied = True
            reason = "requested package is not sagelite"
        elif not specifier_text:
            satisfied = True
            reason = "no sagelite version specifier requested"
        elif not version:
            satisfied = False
            reason = "wheel version could not be parsed from filename"
        else:
            try:
                parsed_version = Version(str(version))
            except InvalidVersion:
                satisfied = False
                reason = "invalid wheel version"
            else:
                specifier = SpecifierSet(str(specifier_text))
                satisfied = parsed_version in specifier
                reason = (
                    "version satisfies requested package requirement"
                    if satisfied
                    else "version does not satisfy requested package requirement"
                )
        report.append(
            {
                "name": wheel.get("name"),
                "project_name": wheel.get("project_name"),
                "version": version,
                "requested_package": package,
                "required_specifier": specifier_text,
                "satisfied": satisfied,
                "reason": reason,
            }
        )
    return report


def _ensure_primary_sagelite_wheel_requirement(
    inventory: dict[str, object],
    package: str,
) -> None:
    unsatisfied = [
        item
        for item in _primary_sagelite_wheel_requirement_satisfaction(
            inventory, package
        )
        if not item["satisfied"]
    ]
    if not unsatisfied:
        return
    details = []
    for item in unsatisfied:
        details.append(
            f"{item.get('name')} version {item.get('version')} does not satisfy "
            f"{item.get('requested_package')}"
        )
    raise RuntimeError(
        "primary sagelite wheel version does not satisfy requested package "
        "requirement: "
        + "; ".join(details)
    )


def _wheel_tags_rendered(wheel: dict[str, object]) -> str:
    python_tags = wheel.get("python_tags", [])
    if not isinstance(python_tags, list):
        python_tags = []
    abi_tags = wheel.get("abi_tags", [])
    if not isinstance(abi_tags, list):
        abi_tags = []
    platform_tags = wheel.get("platform_tags", [])
    if not isinstance(platform_tags, list):
        platform_tags = []
    return (
        f"python: {', '.join(str(tag) for tag in python_tags) or 'no python tags'}; "
        f"abi: {', '.join(str(tag) for tag in abi_tags) or 'no abi tags'}; "
        f"platform: {', '.join(str(tag) for tag in platform_tags) or 'no platform tags'}"
    )


def _wheel_identity_rendered(wheel: dict[str, object]) -> str:
    size = wheel.get("size_bytes")
    sha256 = wheel.get("sha256")
    return f"size: {size}; sha256: {sha256}"


def _companion_sagelite_wheel_compatibility(
    inventory: dict[str, object],
    expected_python_tag: str | None,
    expected_abi_tag: str | None,
    compatible_platform_tags: list[str],
) -> list[dict[str, object]]:
    wheels = inventory["companion_sagelite_wheels"]  # type: ignore[index]
    if not isinstance(wheels, list):
        wheels = []
    compatible_platforms = set(compatible_platform_tags)
    report = []
    for wheel in wheels:
        if not isinstance(wheel, dict):
            continue
        python_tags = wheel.get("python_tags", [])
        if not isinstance(python_tags, list):
            python_tags = []
        abi_tags = wheel.get("abi_tags", [])
        if not isinstance(abi_tags, list):
            abi_tags = []
        platform_tags = wheel.get("platform_tags", [])
        if not isinstance(platform_tags, list):
            platform_tags = []

        matched_platform_tags = [
            str(tag) for tag in platform_tags if str(tag) in compatible_platforms
        ]
        if "any" in platform_tags:
            matched_platform_tags.append("any")
        python_ok = "py3" in python_tags or (
            expected_python_tag is not None and expected_python_tag in python_tags
        )
        abi_ok = "none" in abi_tags or (
            expected_abi_tag is not None and expected_abi_tag in abi_tags
        )
        platform_ok = bool(matched_platform_tags)
        mismatches = []
        if not python_ok:
            mismatches.append("python")
        if not abi_ok:
            mismatches.append("abi")
        if not platform_ok:
            mismatches.append("platform")
        report.append(
            {
                "name": wheel.get("name"),
                "project_name": wheel.get("project_name"),
                "python_tags": python_tags,
                "abi_tags": abi_tags,
                "platform_tags": platform_tags,
                "python_compatible": python_ok,
                "abi_compatible": abi_ok,
                "platform_compatible": platform_ok,
                "matched_platform_tags": matched_platform_tags,
                "compatible": python_ok and abi_ok and platform_ok,
                "mismatches": mismatches,
            }
        )
    return report


def _primary_sagelite_wheel_compatibility(
    inventory: dict[str, object],
    expected_python_tag: str | None,
    expected_abi_tag: str | None,
    compatible_platform_tags: list[str],
) -> list[dict[str, object]]:
    wheels = inventory["primary_sagelite_wheels"]  # type: ignore[index]
    if not isinstance(wheels, list):
        wheels = []
    compatible_platforms = set(compatible_platform_tags)
    report = []
    for wheel in wheels:
        if not isinstance(wheel, dict):
            continue
        python_tags = wheel.get("python_tags", [])
        if not isinstance(python_tags, list):
            python_tags = []
        abi_tags = wheel.get("abi_tags", [])
        if not isinstance(abi_tags, list):
            abi_tags = []
        platform_tags = wheel.get("platform_tags", [])
        if not isinstance(platform_tags, list):
            platform_tags = []

        matched_platform_tags = [
            str(tag) for tag in platform_tags if str(tag) in compatible_platforms
        ]
        python_ok = (
            expected_python_tag is not None and expected_python_tag in python_tags
        )
        abi_ok = expected_abi_tag is not None and expected_abi_tag in abi_tags
        platform_ok = bool(matched_platform_tags)
        repaired_linux = bool(wheel.get("is_repaired_linux_wheel"))
        raw_linux = bool(wheel.get("is_raw_linux_wheel"))
        mismatches = []
        if not python_ok:
            mismatches.append("python")
        if not abi_ok:
            mismatches.append("abi")
        if not platform_ok:
            mismatches.append("platform")
        if not repaired_linux:
            mismatches.append("repaired")
        report.append(
            {
                "name": wheel.get("name"),
                "project_name": wheel.get("project_name"),
                "python_tags": python_tags,
                "abi_tags": abi_tags,
                "platform_tags": platform_tags,
                "python_compatible": python_ok,
                "abi_compatible": abi_ok,
                "platform_compatible": platform_ok,
                "matched_platform_tags": matched_platform_tags,
                "repaired_linux": repaired_linux,
                "raw_linux": raw_linux,
                "compatible": python_ok and abi_ok and platform_ok and repaired_linux,
                "mismatches": mismatches,
            }
        )
    return report


def _ensure_compatible_companion_sagelite_wheels(
    inventory: dict[str, object],
    expected_python_tag: str | None,
    expected_abi_tag: str | None,
    compatible_platform_tags: list[str],
) -> None:
    incompatible = []
    for item in _companion_sagelite_wheel_compatibility(
        inventory,
        expected_python_tag,
        expected_abi_tag,
        compatible_platform_tags,
    ):
        if item["compatible"]:
            continue
        mismatches = item.get("mismatches", [])
        if not isinstance(mismatches, list):
            mismatches = []
        incompatible.append(
            f"{item.get('name')} ({_wheel_tags_rendered(item)}; "
            "mismatches: "
            + ", ".join(str(mismatch) for mismatch in mismatches)
            + ")"
        )

    if not incompatible:
        return
    raise RuntimeError(
        "sagelite companion wheels are not compatible with the requested "
        "validation interpreter or host platform: "
        + "; ".join(incompatible)
    )


def _requested_python_wheel_tag(
    base_python: str, host_context: dict[str, object]
) -> str | None:
    match = re.search(r"cp(\d{2,3})", base_python)
    if match:
        return f"cp{match.group(1)}"
    match = re.search(r"python3[._-]?(\d{1,2})", base_python)
    if match:
        return f"cp3{match.group(1)}"
    base_context = host_context.get("base_python", {})
    if isinstance(base_context, dict):
        tag_probe = base_context.get("tag_probe", {})
        if isinstance(tag_probe, dict):
            cache_tag = tag_probe.get("cache_tag")
            if isinstance(cache_tag, str) and re.fullmatch(
                r"cpython-\d{2,3}", cache_tag
            ):
                return "cp" + cache_tag.rsplit("-", 1)[1]
    if isinstance(base_context, dict) and base_context.get("matches_controller"):
        cache_tag = sys.implementation.cache_tag
        if cache_tag and re.fullmatch(r"cpython-\d{2,3}", cache_tag):
            return "cp" + cache_tag.rsplit("-", 1)[1]
    return None


def _ensure_primary_sagelite_wheel_python_tag(
    inventory: dict[str, object],
    expected_python_tag: str | None,
) -> None:
    if expected_python_tag is None:
        raise RuntimeError(
            "primary sagelite wheel Python tag validation was requested, but "
            "the requested base Python tag could not be inferred"
        )
    wheels = inventory["primary_sagelite_wheels"]  # type: ignore[index]
    if not isinstance(wheels, list):
        wheels = []
    details = []
    for wheel in wheels:
        if not isinstance(wheel, dict):
            continue
        python_tags = wheel.get("python_tags", [])
        if not isinstance(python_tags, list):
            python_tags = []
        name = wheel.get("name")
        rendered_tags = ", ".join(str(tag) for tag in python_tags) or "none"
        details.append(f"{name} ({rendered_tags})")
        if expected_python_tag in python_tags:
            return
    detail = ", ".join(details) if details else "none"
    raise RuntimeError(
        "primary sagelite wheel Python tag does not match requested base "
        f"Python tag {expected_python_tag}; primary sagelite wheels: {detail}"
    )


def _ensure_primary_sagelite_wheel_abi_tag(
    inventory: dict[str, object],
    expected_abi_tag: str | None,
) -> None:
    if expected_abi_tag is None:
        raise RuntimeError(
            "primary sagelite wheel ABI tag validation was requested, but "
            "the requested base Python ABI tag could not be inferred"
        )
    wheels = inventory["primary_sagelite_wheels"]  # type: ignore[index]
    if not isinstance(wheels, list):
        wheels = []
    details = []
    for wheel in wheels:
        if not isinstance(wheel, dict):
            continue
        abi_tags = wheel.get("abi_tags", [])
        if not isinstance(abi_tags, list):
            abi_tags = []
        name = wheel.get("name")
        rendered_tags = ", ".join(str(tag) for tag in abi_tags) or "none"
        details.append(f"{name} ({rendered_tags})")
        if expected_abi_tag in abi_tags:
            return
    detail = ", ".join(details) if details else "none"
    raise RuntimeError(
        "primary sagelite wheel ABI tag does not match requested base "
        f"Python ABI tag {expected_abi_tag}; primary sagelite wheels: {detail}"
    )


def _normalized_platform_machine(machine: str | None) -> str | None:
    if not machine:
        return None
    normalized = machine.lower().replace("-", "_")
    aliases = {
        "amd64": "x86_64",
        "arm64": "aarch64",
    }
    return aliases.get(normalized, normalized)


def _compatible_platform_tags() -> list[str]:
    seen = set()
    platforms = []
    for tag in packaging_tags.sys_tags():
        platform_tag = tag.platform
        if platform_tag in seen:
            continue
        seen.add(platform_tag)
        platforms.append(platform_tag)
    return platforms


def _ensure_primary_sagelite_wheel_platform_tag_compatible(
    inventory: dict[str, object],
    compatible_platform_tags: list[str],
) -> None:
    if not compatible_platform_tags:
        raise RuntimeError(
            "primary sagelite wheel platform tag compatibility validation was "
            "requested, but compatible platform tags could not be inferred"
        )
    compatible = set(compatible_platform_tags)
    wheels = inventory["primary_sagelite_wheels"]  # type: ignore[index]
    if not isinstance(wheels, list):
        wheels = []
    details = []
    for wheel in wheels:
        if not isinstance(wheel, dict):
            continue
        platform_tags = wheel.get("platform_tags", [])
        if not isinstance(platform_tags, list):
            platform_tags = []
        name = wheel.get("name")
        rendered_tags = ", ".join(str(tag) for tag in platform_tags) or "none"
        details.append(f"{name} ({rendered_tags})")
        if any(str(tag) in compatible for tag in platform_tags):
            return
    detail = ", ".join(details) if details else "none"
    sample = ", ".join(compatible_platform_tags[:8])
    raise RuntimeError(
        "primary sagelite wheel platform tag is not compatible with the "
        f"validation host; compatible platform tags include: {sample}; "
        f"primary sagelite wheels: {detail}"
    )


def _ensure_primary_sagelite_wheel_platform_machine(
    inventory: dict[str, object],
    expected_machine: str | None,
) -> None:
    expected_machine = _normalized_platform_machine(expected_machine)
    if expected_machine is None:
        raise RuntimeError(
            "primary sagelite wheel platform validation was requested, but "
            "the validation host machine could not be inferred"
        )
    wheels = inventory["primary_sagelite_wheels"]  # type: ignore[index]
    if not isinstance(wheels, list):
        wheels = []
    details = []
    for wheel in wheels:
        if not isinstance(wheel, dict):
            continue
        platform_tags = wheel.get("platform_tags", [])
        if not isinstance(platform_tags, list):
            platform_tags = []
        name = wheel.get("name")
        rendered_tags = ", ".join(str(tag) for tag in platform_tags) or "none"
        details.append(f"{name} ({rendered_tags})")
        for tag in platform_tags:
            if _normalized_platform_machine(str(tag)).endswith(
                f"_{expected_machine}"
            ):
                return
            if _normalized_platform_machine(str(tag)) == expected_machine:
                return
    detail = ", ".join(details) if details else "none"
    raise RuntimeError(
        "primary sagelite wheel platform tag does not match validation host "
        f"machine {expected_machine}; primary sagelite wheels: {detail}"
    )


def _resolve_executable(executable: str) -> str | None:
    path = Path(executable)
    if path.is_absolute() or os.sep in executable:
        return os.fspath(path.resolve()) if path.exists() else None
    resolved = shutil.which(executable)
    return os.fspath(Path(resolved).resolve()) if resolved else None


def _base_python_tag_probe(resolved_base_python: str | None) -> dict[str, object]:
    if resolved_base_python is None:
        return {
            "attempted": False,
            "error": "base Python executable could not be resolved",
        }
    probe = r"""
import json
import platform
import sys
import sysconfig

payload = {
    "python_version": platform.python_version(),
    "implementation": platform.python_implementation(),
    "cache_tag": sys.implementation.cache_tag,
    "sysconfig_platform": sysconfig.get_platform(),
    "machine": platform.machine(),
}
try:
    from packaging import tags
except Exception as exc:
    payload["packaging_tags_available"] = False
    payload["error"] = f"{type(exc).__name__}: {exc}"
else:
    seen_platforms = []
    seen_platforms_set = set()
    tag_strings = []
    for tag in tags.sys_tags():
        if len(tag_strings) < 20:
            tag_strings.append(str(tag))
        if tag.platform not in seen_platforms_set:
            seen_platforms_set.add(tag.platform)
            seen_platforms.append(tag.platform)
    payload["packaging_tags_available"] = True
    payload["compatible_tags_sample"] = tag_strings
    payload["compatible_platform_tags"] = seen_platforms
    payload["compatible_platform_tags_sample"] = seen_platforms[:20]
    payload["compatible_platform_tag_count"] = len(seen_platforms_set)
print(json.dumps(payload, sort_keys=True))
"""
    try:
        completed = subprocess.run(
            [resolved_base_python, "-c", probe],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "attempted": True,
            "executable": resolved_base_python,
            "returncode": None,
            "error": f"{type(exc).__name__}: {exc}",
        }
    result: dict[str, object] = {
        "attempted": True,
        "executable": resolved_base_python,
        "returncode": completed.returncode,
    }
    stdout = completed.stdout.strip()
    if completed.stderr.strip():
        result["stderr"] = completed.stderr.strip()
    if completed.returncode != 0:
        result["error"] = stdout or completed.stderr.strip()
        return result
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        result["error"] = "base Python tag probe did not return JSON"
        result["stdout"] = stdout
        return result
    if isinstance(payload, dict):
        result.update(payload)
    return result


def validation_host_context(base_python: str) -> dict[str, object]:
    resolved_base_python = _resolve_executable(base_python)
    resolved_controller_python = _resolve_executable(sys.executable)
    compatible_platform_tags = _compatible_platform_tags()
    return {
        "controller_python": {
            "executable": sys.executable,
            "resolved_executable": resolved_controller_python,
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "cache_tag": sys.implementation.cache_tag,
            "sysconfig_platform": sysconfig.get_platform(),
            "machine": platform.machine(),
            "compatible_platform_tag_count": len(compatible_platform_tags),
            "compatible_platform_tags_sample": compatible_platform_tags[:20],
        },
        "base_python": {
            "requested": base_python,
            "resolved_executable": resolved_base_python,
            "exists": resolved_base_python is not None,
            "matches_controller": (
                resolved_base_python is not None
                and resolved_controller_python is not None
                and Path(resolved_base_python) == Path(resolved_controller_python)
            ),
            "tag_probe": _base_python_tag_probe(resolved_base_python),
        },
    }


def _host_context_machine(host_context: dict[str, object]) -> str | None:
    controller = host_context.get("controller_python", {})
    if not isinstance(controller, dict):
        return None
    machine = controller.get("machine")
    return str(machine) if machine else None


def _validation_platform_tags(
    host_context: dict[str, object],
    controller_platform_tags: list[str],
) -> tuple[list[str], str]:
    base_context = host_context.get("base_python", {})
    if isinstance(base_context, dict):
        tag_probe = base_context.get("tag_probe", {})
        if isinstance(tag_probe, dict):
            base_platform_tags = tag_probe.get("compatible_platform_tags", [])
            if isinstance(base_platform_tags, list) and base_platform_tags:
                return [str(tag) for tag in base_platform_tags], "base-python-probe"
            base_platform_tags_sample = tag_probe.get(
                "compatible_platform_tags_sample", []
            )
            if isinstance(base_platform_tags_sample, list) and base_platform_tags_sample:
                return (
                    [str(tag) for tag in base_platform_tags_sample],
                    "base-python-probe-sample",
                )
    return controller_platform_tags, "controller-python"


def _validation_contract(
    *,
    inventory: dict[str, object],
    package: str,
    expected_python_tag: str | None,
    expected_abi_tag: str | None,
    host_context: dict[str, object],
    compatible_platform_tags: list[str],
    compatible_platform_tag_source: str,
    enabled_preflights: list[str],
) -> dict[str, object]:
    controller = host_context.get("controller_python", {})
    if not isinstance(controller, dict):
        controller = {}
    compatible_platform_tags_sample = controller.get(
        "compatible_platform_tags_sample", []
    )
    if not isinstance(compatible_platform_tags_sample, list):
        compatible_platform_tags_sample = []
    companion_compatibility = _companion_sagelite_wheel_compatibility(
        inventory,
        expected_python_tag,
        expected_abi_tag,
        compatible_platform_tags,
    )
    primary_compatibility = _primary_sagelite_wheel_compatibility(
        inventory,
        expected_python_tag,
        expected_abi_tag,
        compatible_platform_tags,
    )
    primary_requirement_satisfaction = (
        _primary_sagelite_wheel_requirement_satisfaction(inventory, package)
    )
    return {
        "primary_sagelite_requirement": _primary_sagelite_requirement(package),
        "primary_sagelite_wheel_requirement_satisfaction": (
            primary_requirement_satisfaction
        ),
        "unsatisfied_primary_sagelite_wheel_requirements": [
            item
            for item in primary_requirement_satisfaction
            if not item["satisfied"]
        ],
        "expected_python_tag": expected_python_tag,
        "expected_abi_tag": expected_abi_tag,
        "expected_platform_machine": _normalized_platform_machine(
            _host_context_machine(host_context)
        ),
        "compatible_platform_tag_source": compatible_platform_tag_source,
        "compatible_platform_tag_count": len(compatible_platform_tags),
        "compatible_platform_tags_sample": compatible_platform_tags[:20]
        or compatible_platform_tags_sample,
        "base_python_tag_probe": (
            host_context.get("base_python", {}).get("tag_probe", {})
            if isinstance(host_context.get("base_python", {}), dict)
            else {}
        ),
        "primary_sagelite_wheel_compatibility": primary_compatibility,
        "incompatible_primary_sagelite_wheels": [
            item for item in primary_compatibility if not item["compatible"]
        ],
        "companion_sagelite_wheel_compatibility": companion_compatibility,
        "incompatible_companion_sagelite_wheels": [
            item for item in companion_compatibility if not item["compatible"]
        ],
        "enabled_preflights": enabled_preflights,
    }


def build_venv_command(base_python: str, install_dir: Path) -> list[str]:
    return [base_python, "-m", "venv", os.fspath(install_dir)]


def build_upgrade_pip_command(venv_python: Path) -> list[str]:
    return [os.fspath(venv_python), "-m", "pip", "install", "-U", "pip"]


def build_install_command(
    venv_python: Path,
    wheelhouses: list[Path],
    package: str,
) -> list[str]:
    command = [
        os.fspath(venv_python),
        "-m",
        "pip",
        "install",
        "--no-index",
    ]
    for wheelhouse in wheelhouses:
        command.extend(["--find-links", os.fspath(wheelhouse)])
    command.append(package)
    return command


def build_pip_check_command(venv_python: Path) -> list[str]:
    return [os.fspath(venv_python), "-m", "pip", "check"]


def write_install_metadata(
    output_dir: Path,
    *,
    label: str,
    package: str,
    base_python: str,
    install_dir: Path,
    venv_python: Path,
    wheelhouses: list[Path],
    commands: list[list[str]],
    env: dict[str, str],
    inventory: dict[str, object],
    host_context: dict[str, object],
    validation_contract: dict[str, object] | None = None,
    status: str = "pending",
    exit_code: int | None = None,
    command_results: list[dict[str, object]] | None = None,
    preflight_error: str | None = None,
) -> Path:
    path = output_dir / "install-metadata.json"
    environment = {
        "PATH": env.get("PATH", ""),
        "PYTHONNOUSERSITE": env.get("PYTHONNOUSERSITE"),
    }
    for key in sorted(RUNTIME_ENV_KEYS_TO_REMOVE):
        environment[key] = env.get(key)
    metadata = {
        "schema": "sagelite-wheelhouse-validation-install-v1",
        "label": label,
        "package": package,
        "base_python": base_python,
        "install_dir": os.fspath(install_dir),
        "venv_python": os.fspath(venv_python),
        "wheelhouses": [os.fspath(path) for path in wheelhouses],
        "wheelhouse_inventory": inventory,
        "native_wheel_catalog": sagelite_native_wheel_catalog.catalog(),
        "validation_host": host_context,
        "validation_contract": validation_contract or {},
        "commands": commands,
        "status": status,
        "exit_code": exit_code,
        "preflight_error": preflight_error,
        "command_results": command_results or [],
        "environment": environment,
        "removed_environment_prefixes": list(RUNTIME_ENV_PREFIXES_TO_REMOVE),
        "removed_environment_keys": sorted(RUNTIME_ENV_KEYS_TO_REMOVE),
    }
    path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    return path


def _format_command(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def write_validation_summary(
    output_dir: Path,
    *,
    label: str,
    package: str,
    install_dir: Path,
    wheelhouses: list[Path],
    status: str,
    exit_code: int | None,
    command_results: list[dict[str, object]] | None = None,
    preflight_error: str | None = None,
    host_context: dict[str, object] | None = None,
    validation_contract: dict[str, object] | None = None,
) -> Path:
    path = output_dir / "validation-summary.md"
    inventory = wheelhouse_inventory(wheelhouses)
    lines = [
        f"# Sagelite wheelhouse validation: {label}",
        "",
        f"- Status: `{status}`",
        f"- Exit code: `{exit_code}`",
        f"- Package: `{package}`",
        f"- Install dir: `{install_dir}`",
    ]
    if host_context:
        controller = host_context.get("controller_python", {})
        base_python = host_context.get("base_python", {})
        if not isinstance(controller, dict):
            controller = {}
        if not isinstance(base_python, dict):
            base_python = {}
        lines.extend(
            [
                f"- Base Python: `{base_python.get('requested')}`",
                f"- Resolved base Python: `{base_python.get('resolved_executable')}`",
                (
                    "- Controller Python: "
                    f"`{controller.get('executable')}` "
                    f"({controller.get('version')}, "
                    f"{controller.get('sysconfig_platform')})"
                ),
                (
                    "- Controller compatible platform tag count: "
                    f"`{controller.get('compatible_platform_tag_count')}`"
                ),
            ]
        )
        tag_probe = base_python.get("tag_probe", {})
        if isinstance(tag_probe, dict):
            lines.extend(
                [
                    (
                        "- Base Python tag probe attempted: "
                        f"`{tag_probe.get('attempted')}`"
                    ),
                    (
                        "- Base Python probe version: "
                        f"`{tag_probe.get('python_version')}`"
                    ),
                    (
                        "- Base Python probe cache tag: "
                        f"`{tag_probe.get('cache_tag')}`"
                    ),
                    (
                        "- Base Python probe platform: "
                        f"`{tag_probe.get('sysconfig_platform')}`"
                    ),
                    (
                        "- Base Python packaging tags available: "
                        f"`{tag_probe.get('packaging_tags_available')}`"
                    ),
                    (
                        "- Base Python compatible platform tag count: "
                        f"`{tag_probe.get('compatible_platform_tag_count')}`"
                    ),
                ]
            )
            compatible_tags_sample = tag_probe.get("compatible_tags_sample", [])
            if not isinstance(compatible_tags_sample, list):
                compatible_tags_sample = []
            if compatible_tags_sample:
                lines.append(
                    "- Base Python compatible tag sample: "
                    + ", ".join(
                        f"`{tag}`" for tag in compatible_tags_sample[:5]
                    )
                )
    if validation_contract:
        primary_requirement = validation_contract.get(
            "primary_sagelite_requirement", {}
        )
        if not isinstance(primary_requirement, dict):
            primary_requirement = {}
        lines.extend(
            [
                "- Primary sagelite requirement: "
                f"`{primary_requirement.get('package')}`",
                "- Primary sagelite requirement extras: "
                + (
                    ", ".join(
                        f"`{extra}`"
                        for extra in primary_requirement.get("extras", [])
                        if isinstance(extra, str)
                    )
                    if isinstance(primary_requirement.get("extras"), list)
                    and primary_requirement.get("extras")
                    else "`none`"
                ),
                "- Primary sagelite requirement specifier: "
                f"`{primary_requirement.get('specifier')}`",
                "- Primary sagelite requests all-needed-extras: "
                f"`{primary_requirement.get('requests_all_needed_extras')}`",
                "- Expected wheel Python tag: "
                f"`{validation_contract.get('expected_python_tag')}`",
                "- Expected wheel ABI tag: "
                f"`{validation_contract.get('expected_abi_tag')}`",
                "- Expected platform machine: "
                f"`{validation_contract.get('expected_platform_machine')}`",
                "- Compatible platform tag source: "
                f"`{validation_contract.get('compatible_platform_tag_source')}`",
            ]
        )
        enabled_preflights = validation_contract.get("enabled_preflights", [])
        if not isinstance(enabled_preflights, list):
            enabled_preflights = []
        lines.append(
            "- Enabled preflights: "
            + (
                ", ".join(f"`{preflight}`" for preflight in enabled_preflights)
                if enabled_preflights
                else "`none`"
            )
        )
    lines.append("- Wheelhouses:")
    lines.extend(f"  - `{wheelhouse}`" for wheelhouse in wheelhouses)
    primary_sagelite_wheels = inventory.get("primary_sagelite_wheels", [])
    if not isinstance(primary_sagelite_wheels, list):
        primary_sagelite_wheels = []
    lines.append("- Primary sagelite wheels:")
    for wheel in primary_sagelite_wheels:
        if not isinstance(wheel, dict):
            continue
        lines.append(f"  - `{wheel.get('name')}` ({_wheel_tags_rendered(wheel)})")
        lines.append(f"    - {_wheel_identity_rendered(wheel)}")
    if not primary_sagelite_wheels:
        lines.append("  - none")
    companion_sagelite_wheels = inventory.get("companion_sagelite_wheels", [])
    if not isinstance(companion_sagelite_wheels, list):
        companion_sagelite_wheels = []
    lines.append("- Companion sagelite wheels:")
    for wheel in companion_sagelite_wheels:
        if not isinstance(wheel, dict):
            continue
        lines.append(f"  - `{wheel.get('name')}` ({_wheel_tags_rendered(wheel)})")
        lines.append(f"    - {_wheel_identity_rendered(wheel)}")
    if not companion_sagelite_wheels:
        lines.append("  - none")
    contains_repaired = inventory["contains_repaired_primary_sagelite_wheel"]
    contains_raw_linux = inventory["contains_raw_linux_primary_sagelite_wheel"]
    lines.extend(
        [
            (
                "- Contains companion sagelite wheels: "
                f"`{inventory['contains_companion_sagelite_wheels']}`"
            ),
            (
                "- Contains all-needed-extra sagelite wheels: "
                f"`{inventory['contains_all_needed_extra_sagelite_wheels']}`"
            ),
            f"- Contains repaired primary sagelite wheel: `{contains_repaired}`",
            f"- Contains raw Linux primary sagelite wheel: `{contains_raw_linux}`",
        ]
    )
    companion_package_names = inventory.get("companion_sagelite_package_names", [])
    if not isinstance(companion_package_names, list):
        companion_package_names = []
    missing_all_needed_extra_packages = inventory.get(
        "missing_all_needed_extra_sagelite_packages", []
    )
    if not isinstance(missing_all_needed_extra_packages, list):
        missing_all_needed_extra_packages = []
    duplicate_companion_package_names = inventory.get(
        "duplicate_companion_sagelite_package_names", []
    )
    if not isinstance(duplicate_companion_package_names, list):
        duplicate_companion_package_names = []
    duplicate_primary_wheel_names = inventory.get(
        "duplicate_primary_sagelite_wheel_names", []
    )
    if not isinstance(duplicate_primary_wheel_names, list):
        duplicate_primary_wheel_names = []
    lines.extend(
        [
            f"- Companion sagelite package count: `{len(companion_package_names)}`",
            (
                "- Missing all-needed-extra sagelite package count: "
                f"`{len(missing_all_needed_extra_packages)}`"
            ),
        ]
    )
    if missing_all_needed_extra_packages:
        lines.append(
            "- Missing all-needed-extra sagelite packages: "
            + ", ".join(f"`{name}`" for name in missing_all_needed_extra_packages)
        )
    lines.append(
        "- Duplicate primary sagelite wheels: "
        + (
            ", ".join(f"`{name}`" for name in duplicate_primary_wheel_names)
            if duplicate_primary_wheel_names
            else "`none`"
        )
    )
    if duplicate_companion_package_names:
        lines.append(
            "- Duplicate companion sagelite packages: "
            + ", ".join(f"`{name}`" for name in duplicate_companion_package_names)
        )
    unsatisfied_companion_requirements = inventory.get(
        "unsatisfied_companion_sagelite_requirements", []
    )
    if not isinstance(unsatisfied_companion_requirements, list):
        unsatisfied_companion_requirements = []
    lines.append(
        "- Unsatisfied companion sagelite requirements: "
        + (
            ", ".join(
                f"`{item.get('name')}`"
                for item in unsatisfied_companion_requirements
                if isinstance(item, dict)
            )
            if unsatisfied_companion_requirements
            else "`none`"
        )
    )
    incompatible_primary_wheels = []
    primary_wheel_compatibility = []
    if validation_contract:
        primary_wheel_compatibility = validation_contract.get(
            "primary_sagelite_wheel_compatibility", []
        )
        incompatible_primary_wheels = validation_contract.get(
            "incompatible_primary_sagelite_wheels", []
        )
    if not isinstance(primary_wheel_compatibility, list):
        primary_wheel_compatibility = []
    if not isinstance(incompatible_primary_wheels, list):
        incompatible_primary_wheels = []
    compatible_primary_wheels = [
        item
        for item in primary_wheel_compatibility
        if isinstance(item, dict) and item.get("compatible")
    ]
    lines.extend(
        [
            (
                "- Primary compatibility checked wheels: "
                f"`{len(primary_wheel_compatibility)}`"
            ),
            (
                "- Primary compatibility passed wheels: "
                f"`{len(compatible_primary_wheels)}`"
            ),
        ]
    )
    lines.append(
        "- Incompatible primary sagelite wheels: "
        + (
            ", ".join(
                f"`{item.get('name')}`"
                for item in incompatible_primary_wheels
                if isinstance(item, dict)
            )
            if incompatible_primary_wheels
            else "`none`"
        )
    )
    if primary_wheel_compatibility:
        lines.append("- Primary compatibility details:")
    for item in primary_wheel_compatibility:
        if not isinstance(item, dict):
            continue
        mismatches = item.get("mismatches", [])
        if not isinstance(mismatches, list):
            mismatches = []
        matched_platform_tags = item.get("matched_platform_tags", [])
        if not isinstance(matched_platform_tags, list):
            matched_platform_tags = []
        lines.append(
            "  - "
            f"`{item.get('name')}`: "
            f"compatible `{item.get('compatible')}` "
            f"(python: `{item.get('python_compatible')}`; "
            f"abi: `{item.get('abi_compatible')}`; "
            f"platform: `{item.get('platform_compatible')}`; "
            f"repaired: `{item.get('repaired_linux')}`; "
            f"raw-linux: `{item.get('raw_linux')}`; "
            "mismatches: "
            + (
                ", ".join(f"`{mismatch}`" for mismatch in mismatches)
                if mismatches
                else "`none`"
            )
            + ") matched platform tags: "
            + (
                ", ".join(f"`{tag}`" for tag in matched_platform_tags)
                if matched_platform_tags
                else "`none`"
            )
        )
    primary_requirement_satisfaction = []
    unsatisfied_primary_requirements = []
    if validation_contract:
        primary_requirement_satisfaction = validation_contract.get(
            "primary_sagelite_wheel_requirement_satisfaction", []
        )
        unsatisfied_primary_requirements = validation_contract.get(
            "unsatisfied_primary_sagelite_wheel_requirements", []
        )
    if not isinstance(primary_requirement_satisfaction, list):
        primary_requirement_satisfaction = []
    if not isinstance(unsatisfied_primary_requirements, list):
        unsatisfied_primary_requirements = []
    lines.append(
        "- Unsatisfied primary sagelite wheel requirements: "
        + (
            ", ".join(
                f"`{item.get('name')}`"
                for item in unsatisfied_primary_requirements
                if isinstance(item, dict)
            )
            if unsatisfied_primary_requirements
            else "`none`"
        )
    )
    if primary_requirement_satisfaction:
        lines.append("- Primary requirement details:")
    for item in primary_requirement_satisfaction:
        if not isinstance(item, dict):
            continue
        lines.append(
            "  - "
            f"`{item.get('name')}`: "
            f"version `{item.get('version')}`; "
            f"specifier `{item.get('required_specifier')}`; "
            f"satisfied `{item.get('satisfied')}`; "
            f"reason `{item.get('reason')}`"
        )
    incompatible_companion_wheels = []
    companion_wheel_compatibility = []
    if validation_contract:
        companion_wheel_compatibility = validation_contract.get(
            "companion_sagelite_wheel_compatibility", []
        )
        incompatible_companion_wheels = validation_contract.get(
            "incompatible_companion_sagelite_wheels", []
        )
    if not isinstance(companion_wheel_compatibility, list):
        companion_wheel_compatibility = []
    if not isinstance(incompatible_companion_wheels, list):
        incompatible_companion_wheels = []
    compatible_companion_wheels = [
        item
        for item in companion_wheel_compatibility
        if isinstance(item, dict) and item.get("compatible")
    ]
    lines.extend(
        [
            (
                "- Companion compatibility checked wheels: "
                f"`{len(companion_wheel_compatibility)}`"
            ),
            (
                "- Companion compatibility passed wheels: "
                f"`{len(compatible_companion_wheels)}`"
            ),
        ]
    )
    lines.append(
        "- Incompatible companion sagelite wheels: "
        + (
            ", ".join(
                f"`{item.get('name')}`"
                for item in incompatible_companion_wheels
                if isinstance(item, dict)
            )
            if incompatible_companion_wheels
            else "`none`"
        )
    )
    if companion_wheel_compatibility:
        lines.append("- Companion compatibility details:")
    for item in companion_wheel_compatibility:
        if not isinstance(item, dict):
            continue
        mismatches = item.get("mismatches", [])
        if not isinstance(mismatches, list):
            mismatches = []
        matched_platform_tags = item.get("matched_platform_tags", [])
        if not isinstance(matched_platform_tags, list):
            matched_platform_tags = []
        lines.append(
            "  - "
            f"`{item.get('name')}`: "
            f"compatible `{item.get('compatible')}` "
            f"(python: `{item.get('python_compatible')}`; "
            f"abi: `{item.get('abi_compatible')}`; "
            f"platform: `{item.get('platform_compatible')}`; "
            "mismatches: "
            + (
                ", ".join(f"`{mismatch}`" for mismatch in mismatches)
                if mismatches
                else "`none`"
            )
            + ") matched platform tags: "
            + (
                ", ".join(f"`{tag}`" for tag in matched_platform_tags)
                if matched_platform_tags
                else "`none`"
            )
        )
    native_catalog = sagelite_native_wheel_catalog.catalog()
    required_meson_options = native_catalog["required_meson_options"]
    required_import_modules = native_catalog["required_native_import_modules"]
    required_library_prefixes = native_catalog["required_native_library_prefixes"]
    lines.extend(
        [
            "",
            "## Native Wheel Catalog",
            "",
            (
                "- Required Meson options: "
                + ", ".join(f"`{option}`" for option in required_meson_options)
            ),
            (
                "- Required native import modules: "
                f"`{len(required_import_modules)}`"
            ),
            (
                "- Required native library prefixes: "
                + ", ".join(f"`{prefix}`" for prefix in required_library_prefixes)
            ),
        ]
    )
    if preflight_error:
        lines.extend(["", "## Preflight Error", "", preflight_error])

    if command_results:
        lines.extend(["", "## Steps", ""])
        for result in command_results:
            command = result.get("command")
            rendered_command = (
                _format_command(command)
                if isinstance(command, list) and all(
                    isinstance(part, str) for part in command
                )
                else str(command)
            )
            lines.extend(
                [
                    (
                        f"### {result.get('index')}. {result.get('phase')}: "
                        f"{result.get('status')}"
                    ),
                    "",
                    f"- Return code: `{result.get('returncode')}`",
                    f"- Elapsed seconds: `{result.get('elapsed_seconds')}`",
                    "",
                    "```bash",
                    rendered_command,
                    "```",
                    "",
                ]
            )

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def build_validation_command(
    venv_python: Path,
    output_dir: Path,
    label: str,
    wheelhouses: list[Path],
    *,
    full: bool,
    short: int | None,
    nthreads: int,
    manifest_compiled_limit: int | None,
    extra_doctest_args: list[str],
) -> list[str]:
    command = [
        os.fspath(venv_python),
        os.fspath(RUNNER),
        "--python",
        os.fspath(venv_python),
        "--output-dir",
        os.fspath(output_dir),
        "--label",
        label,
        "--runtime-summary",
        "--selftest",
        "--nthreads",
        str(nthreads),
    ]
    if full:
        command.append("--full")
    elif short is not None:
        command.extend(["--short", str(short)])
    if manifest_compiled_limit is not None:
        command.extend(["--manifest-compiled-limit", str(manifest_compiled_limit)])
    for wheelhouse in wheelhouses:
        command.extend(["--wheelhouse", os.fspath(wheelhouse)])
    if extra_doctest_args:
        command.append("--")
        command.extend(extra_doctest_args)
    return command


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wheelhouse",
        action="append",
        required=True,
        type=Path,
        help="wheelhouse used for --no-index installation; may be repeated",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=DEFAULT_WORK_DIR,
        help="scratch work directory for fresh installs and validation artifacts",
    )
    parser.add_argument(
        "--install-dir",
        type=Path,
        default=None,
        help="fresh virtualenv path; defaults under --work-dir",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="validation artifact directory; defaults under --work-dir",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="artifact label; defaults to repaired-wheel-<timestamp>",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="base Python used to create the fresh virtualenv",
    )
    parser.add_argument(
        "--package",
        default=DEFAULT_PACKAGE,
        help="package requirement installed from the wheelhouse",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--full",
        action="store_true",
        help="run the full installed doctest sweep",
    )
    mode.add_argument(
        "--short",
        type=int,
        default=300,
        metavar="SECONDS",
        help="target walltime for a short installed doctest sweep",
    )
    parser.add_argument(
        "--nthreads",
        type=int,
        default=1,
        help="value passed to the installed doctest runner -p/--nthreads option",
    )
    parser.add_argument(
        "--manifest-compiled-limit",
        type=int,
        default=200,
        help="compiled-module probe limit for runtime manifest collection",
    )
    parser.add_argument(
        "--require-repaired-sagelite-wheel",
        action="store_true",
        help=(
            "fail before installation unless a primary sagelite wheel has a "
            "manylinux or musllinux platform tag"
        ),
    )
    parser.add_argument(
        "--strict-repaired-wheelhouse-preflight",
        action="store_true",
        help=(
            "enable every repaired-wheelhouse proof preflight before creating "
            "the fresh install"
        ),
    )
    parser.add_argument(
        "--require-all-needed-extra-sagelite-wheels",
        action="store_true",
        help=(
            "fail before installation unless every sagelite companion package "
            "declared by the all-needed-extras extra is present in the wheelhouse"
        ),
    )
    parser.add_argument(
        "--reject-duplicate-companion-sagelite-wheels",
        action="store_true",
        help=(
            "fail before installation when more than one sagelite companion "
            "wheel provides the same normalized package name"
        ),
    )
    parser.add_argument(
        "--reject-duplicate-primary-sagelite-wheels",
        action="store_true",
        help=(
            "fail before installation when more than one primary sagelite "
            "wheel is staged"
        ),
    )
    parser.add_argument(
        "--require-sagelite-companion-wheel-requirements",
        action="store_true",
        help=(
            "fail before installation when staged sagelite companion wheels do "
            "not satisfy sagelite's declared dependency specifiers"
        ),
    )
    parser.add_argument(
        "--require-primary-sagelite-wheel-requirement",
        action="store_true",
        help=(
            "fail before installation when the primary sagelite wheel version "
            "does not satisfy the requested --package requirement"
        ),
    )
    parser.add_argument(
        "--require-package-all-needed-extras",
        action="store_true",
        help=(
            "fail before installation unless --package requests "
            "sagelite[all-needed-extras]"
        ),
    )
    parser.add_argument(
        "--require-compatible-companion-sagelite-wheels",
        action="store_true",
        help=(
            "fail before installation unless every sagelite companion wheel has "
            "Python, ABI, and platform tags compatible with the requested "
            "validation interpreter and host"
        ),
    )
    parser.add_argument(
        "--require-primary-sagelite-wheel-python-tag",
        action="store_true",
        help=(
            "fail before installation unless the primary sagelite wheel Python "
            "tag matches the requested base Python"
        ),
    )
    parser.add_argument(
        "--require-primary-sagelite-wheel-abi-tag",
        action="store_true",
        help=(
            "fail before installation unless the primary sagelite wheel ABI "
            "tag matches the requested base Python ABI"
        ),
    )
    parser.add_argument(
        "--require-primary-sagelite-wheel-platform-machine",
        action="store_true",
        help=(
            "fail before installation unless the primary sagelite wheel "
            "platform tag matches the validation host machine architecture"
        ),
    )
    parser.add_argument(
        "--require-primary-sagelite-wheel-compatible-platform-tag",
        action="store_true",
        help=(
            "fail before installation unless the primary sagelite wheel has a "
            "platform tag compatible with the validation host"
        ),
    )
    parser.add_argument(
        "doctest_args",
        nargs=argparse.REMAINDER,
        help="extra arguments passed through to the installed doctest runner",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _make_parser().parse_args(argv)
    stamp = _timestamp()
    label = args.label or f"repaired-wheel-{stamp}"
    install_dir = args.install_dir or args.work_dir / f"install-{stamp}"
    output_dir = args.output_dir or args.work_dir / f"validation-{stamp}"
    wheelhouses = _ensure_wheelhouses(args.wheelhouse)
    inventory = wheelhouse_inventory(wheelhouses)
    venv_python = install_dir / "bin" / "python"
    env = _clean_environment()
    host_context = validation_host_context(args.python)
    expected_python_tag = _requested_python_wheel_tag(args.python, host_context)
    expected_abi_tag = expected_python_tag
    compatible_platform_tags, compatible_platform_tag_source = _validation_platform_tags(
        host_context, _compatible_platform_tags()
    )

    install_dir.parent.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    commands = [
        build_venv_command(args.python, install_dir),
        build_upgrade_pip_command(venv_python),
        build_install_command(venv_python, wheelhouses, args.package),
        build_pip_check_command(venv_python),
        build_validation_command(
            venv_python,
            output_dir,
            label,
            wheelhouses,
            full=args.full,
            short=None if args.full else args.short,
            nthreads=args.nthreads,
            manifest_compiled_limit=args.manifest_compiled_limit,
            extra_doctest_args=args.doctest_args[1:]
            if args.doctest_args[:1] == ["--"]
            else args.doctest_args,
        ),
    ]
    command_phases = list(VALIDATION_PHASES)
    preflight_checks = []
    enabled_preflights = []
    strict_preflight = args.strict_repaired_wheelhouse_preflight
    if strict_preflight:
        enabled_preflights.append("strict-repaired-wheelhouse-preflight")
    if args.reject_duplicate_primary_sagelite_wheels or strict_preflight:
        preflight_checks.append(_ensure_single_primary_sagelite_wheel)
        enabled_preflights.append("reject-duplicate-primary-sagelite-wheels")
    if args.require_repaired_sagelite_wheel or strict_preflight:
        preflight_checks.append(_ensure_repaired_sagelite_wheel)
        enabled_preflights.append("require-repaired-sagelite-wheel")
    if args.require_package_all_needed_extras or strict_preflight:
        preflight_checks.append(
            lambda inventory: _ensure_package_requests_all_needed_extras(args.package)
        )
        enabled_preflights.append("require-package-all-needed-extras")
    if args.require_all_needed_extra_sagelite_wheels or strict_preflight:
        preflight_checks.append(_ensure_all_needed_extra_sagelite_wheels)
        enabled_preflights.append("require-all-needed-extra-sagelite-wheels")
    if args.reject_duplicate_companion_sagelite_wheels or strict_preflight:
        preflight_checks.append(_ensure_no_duplicate_companion_sagelite_wheels)
        enabled_preflights.append("reject-duplicate-companion-sagelite-wheels")
    if args.require_sagelite_companion_wheel_requirements or strict_preflight:
        preflight_checks.append(_ensure_companion_sagelite_wheel_requirements)
        enabled_preflights.append("require-sagelite-companion-wheel-requirements")
    if args.require_primary_sagelite_wheel_requirement or strict_preflight:
        preflight_checks.append(
            lambda inventory: _ensure_primary_sagelite_wheel_requirement(
                inventory,
                args.package,
            )
        )
        enabled_preflights.append("require-primary-sagelite-wheel-requirement")
    if args.require_compatible_companion_sagelite_wheels or strict_preflight:
        preflight_checks.append(
            lambda inventory: _ensure_compatible_companion_sagelite_wheels(
                inventory,
                expected_python_tag,
                expected_abi_tag,
                compatible_platform_tags,
            )
        )
        enabled_preflights.append("require-compatible-companion-sagelite-wheels")
    if args.require_primary_sagelite_wheel_python_tag or strict_preflight:
        preflight_checks.append(
            lambda inventory: _ensure_primary_sagelite_wheel_python_tag(
                inventory, expected_python_tag
            )
        )
        enabled_preflights.append("require-primary-sagelite-wheel-python-tag")
    if args.require_primary_sagelite_wheel_abi_tag or strict_preflight:
        preflight_checks.append(
            lambda inventory: _ensure_primary_sagelite_wheel_abi_tag(
                inventory, expected_abi_tag
            )
        )
        enabled_preflights.append("require-primary-sagelite-wheel-abi-tag")
    if args.require_primary_sagelite_wheel_platform_machine or strict_preflight:
        preflight_checks.append(
            lambda inventory: _ensure_primary_sagelite_wheel_platform_machine(
                inventory,
                _host_context_machine(host_context),
            )
        )
        enabled_preflights.append("require-primary-sagelite-wheel-platform-machine")
    if (
        args.require_primary_sagelite_wheel_compatible_platform_tag
        or strict_preflight
    ):
        preflight_checks.append(
            lambda inventory: _ensure_primary_sagelite_wheel_platform_tag_compatible(
                inventory,
                compatible_platform_tags,
            )
        )
        enabled_preflights.append(
            "require-primary-sagelite-wheel-compatible-platform-tag"
        )
    validation_contract = _validation_contract(
        inventory=inventory,
        package=args.package,
        expected_python_tag=expected_python_tag,
        expected_abi_tag=expected_abi_tag,
        host_context=host_context,
        compatible_platform_tags=compatible_platform_tags,
        compatible_platform_tag_source=compatible_platform_tag_source,
        enabled_preflights=enabled_preflights,
    )
    for check in preflight_checks:
        try:
            check(inventory)
        except RuntimeError as exc:
            metadata_path = write_install_metadata(
                output_dir,
                label=label,
                package=args.package,
                base_python=args.python,
                install_dir=install_dir,
                venv_python=venv_python,
                wheelhouses=wheelhouses,
                commands=commands,
                env=env,
                inventory=inventory,
                host_context=host_context,
                validation_contract=validation_contract,
                status="failed",
                exit_code=2,
                preflight_error=str(exc),
            )
            summary_path = write_validation_summary(
                output_dir,
                label=label,
                package=args.package,
                install_dir=install_dir,
                wheelhouses=wheelhouses,
                status="failed",
                exit_code=2,
                preflight_error=str(exc),
                host_context=host_context,
                validation_contract=validation_contract,
            )
            print(str(exc), file=sys.stderr)
            print(f"metadata: {metadata_path}")
            print(f"summary: {summary_path}")
            return 2
    metadata_path = write_install_metadata(
        output_dir,
        label=label,
        package=args.package,
        base_python=args.python,
        install_dir=install_dir,
        venv_python=venv_python,
        wheelhouses=wheelhouses,
        commands=commands,
        env=env,
        inventory=inventory,
        host_context=host_context,
        validation_contract=validation_contract,
        status="running",
    )
    summary_path = write_validation_summary(
        output_dir,
        label=label,
        package=args.package,
        install_dir=install_dir,
        wheelhouses=wheelhouses,
        status="running",
        exit_code=None,
        host_context=host_context,
        validation_contract=validation_contract,
    )
    command_results: list[dict[str, object]] = []
    for index, command in enumerate(commands, start=1):
        started = time.perf_counter()
        result = _run(command, env)
        command_results.append(
            {
                "index": index,
                "phase": command_phases[index - 1],
                "command": command,
                "returncode": result.returncode,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
                "status": "passed" if result.returncode == 0 else "failed",
            }
        )
        write_install_metadata(
            output_dir,
            label=label,
            package=args.package,
            base_python=args.python,
            install_dir=install_dir,
            venv_python=venv_python,
            wheelhouses=wheelhouses,
            commands=commands,
            env=env,
            inventory=inventory,
            host_context=host_context,
            validation_contract=validation_contract,
            status="running" if result.returncode == 0 else "failed",
            exit_code=None if result.returncode == 0 else result.returncode,
            command_results=command_results,
        )
        summary_path = write_validation_summary(
            output_dir,
            label=label,
            package=args.package,
            install_dir=install_dir,
            wheelhouses=wheelhouses,
            status="running" if result.returncode == 0 else "failed",
            exit_code=None if result.returncode == 0 else result.returncode,
            command_results=command_results,
            host_context=host_context,
            validation_contract=validation_contract,
        )
        if result.returncode:
            print(f"metadata: {metadata_path}")
            print(f"summary: {summary_path}")
            return result.returncode

    metadata_path = write_install_metadata(
        output_dir,
        label=label,
        package=args.package,
        base_python=args.python,
        install_dir=install_dir,
        venv_python=venv_python,
        wheelhouses=wheelhouses,
        commands=commands,
        env=env,
        inventory=inventory,
        host_context=host_context,
        validation_contract=validation_contract,
        status="passed",
        exit_code=0,
        command_results=command_results,
    )
    summary_path = write_validation_summary(
        output_dir,
        label=label,
        package=args.package,
        install_dir=install_dir,
        wheelhouses=wheelhouses,
        status="passed",
        exit_code=0,
        command_results=command_results,
        host_context=host_context,
        validation_contract=validation_contract,
    )
    print(f"install: {install_dir}")
    print(f"validation: {output_dir}")
    print(f"metadata: {metadata_path}")
    print(f"summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
