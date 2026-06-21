#!/usr/bin/env python3
"""
Create a fresh sagelite install from a wheelhouse and run installed validation.
"""

from __future__ import annotations

import argparse
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
    files: list[dict[str, object]] = []
    for wheelhouse in wheelhouses:
        for wheel in sorted(wheelhouse.glob("*.whl")):
            wheel_tags = _wheel_tags(wheel)
            is_primary_sagelite = _is_primary_sagelite_wheel(wheel)
            project_name = _wheel_project_name(wheel)
            files.append(
                {
                    "name": wheel.name,
                    "path": os.fspath(wheel),
                    "wheelhouse": os.fspath(wheelhouse),
                    "project_name": project_name,
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
    return {
        "files": files,
        "sagelite_project_wheels": sagelite_project_wheels,
        "primary_sagelite_wheels": primary_sagelite_wheels,
        "companion_sagelite_wheels": companion_sagelite_wheels,
        "companion_sagelite_package_names": companion_package_names,
        "duplicate_companion_sagelite_package_names": duplicate_companion_package_names,
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


def _resolve_executable(executable: str) -> str | None:
    path = Path(executable)
    if path.is_absolute() or os.sep in executable:
        return os.fspath(path.resolve()) if path.exists() else None
    resolved = shutil.which(executable)
    return os.fspath(Path(resolved).resolve()) if resolved else None


def validation_host_context(base_python: str) -> dict[str, object]:
    resolved_base_python = _resolve_executable(base_python)
    resolved_controller_python = _resolve_executable(sys.executable)
    return {
        "controller_python": {
            "executable": sys.executable,
            "resolved_executable": resolved_controller_python,
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "cache_tag": sys.implementation.cache_tag,
            "sysconfig_platform": sysconfig.get_platform(),
            "machine": platform.machine(),
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
        },
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
            ]
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
        python_tags = wheel.get("python_tags", [])
        if not isinstance(python_tags, list):
            python_tags = []
        abi_tags = wheel.get("abi_tags", [])
        if not isinstance(abi_tags, list):
            abi_tags = []
        platform_tags = wheel.get("platform_tags", [])
        if not isinstance(platform_tags, list):
            platform_tags = []
        rendered_python_tags = ", ".join(str(tag) for tag in python_tags)
        rendered_abi_tags = ", ".join(str(tag) for tag in abi_tags)
        rendered_tags = ", ".join(str(tag) for tag in platform_tags)
        lines.append(
            (
                f"  - `{wheel.get('name')}` "
                f"(python: {rendered_python_tags or 'no python tags'}; "
                f"abi: {rendered_abi_tags or 'no abi tags'}; "
                f"platform: {rendered_tags or 'no platform tags'})"
            )
        )
    if not primary_sagelite_wheels:
        lines.append("  - none")
    companion_sagelite_wheels = inventory.get("companion_sagelite_wheels", [])
    if not isinstance(companion_sagelite_wheels, list):
        companion_sagelite_wheels = []
    lines.append("- Companion sagelite wheels:")
    for wheel in companion_sagelite_wheels:
        if not isinstance(wheel, dict):
            continue
        lines.append(f"  - `{wheel.get('name')}`")
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
    if duplicate_companion_package_names:
        lines.append(
            "- Duplicate companion sagelite packages: "
            + ", ".join(f"`{name}`" for name in duplicate_companion_package_names)
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
        "--require-primary-sagelite-wheel-python-tag",
        action="store_true",
        help=(
            "fail before installation unless the primary sagelite wheel Python "
            "tag matches the requested base Python"
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
    if args.require_repaired_sagelite_wheel:
        preflight_checks.append(_ensure_repaired_sagelite_wheel)
    if args.require_all_needed_extra_sagelite_wheels:
        preflight_checks.append(_ensure_all_needed_extra_sagelite_wheels)
    if args.reject_duplicate_companion_sagelite_wheels:
        preflight_checks.append(_ensure_no_duplicate_companion_sagelite_wheels)
    if args.require_primary_sagelite_wheel_python_tag:
        preflight_checks.append(
            lambda inventory: _ensure_primary_sagelite_wheel_python_tag(
                inventory, expected_python_tag
            )
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
    )
    print(f"install: {install_dir}")
    print(f"validation: {output_dir}")
    print(f"metadata: {metadata_path}")
    print(f"summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
