#!/usr/bin/env python3
"""
Create a fresh sagelite install from a wheelhouse and run installed validation.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent
RUNNER = TOOLS_DIR / "run-installed-wheel-doctests.py"
DEFAULT_WORK_DIR = Path("/scratch/sagelite-r2-work")
DEFAULT_PACKAGE = "sagelite[all-needed-extras]"

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
    status: str = "pending",
    exit_code: int | None = None,
    command_results: list[dict[str, object]] | None = None,
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
        "commands": commands,
        "status": status,
        "exit_code": exit_code,
        "command_results": command_results or [],
        "environment": environment,
        "removed_environment_prefixes": list(RUNTIME_ENV_PREFIXES_TO_REMOVE),
        "removed_environment_keys": sorted(RUNTIME_ENV_KEYS_TO_REMOVE),
    }
    path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
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
    venv_python = install_dir / "bin" / "python"
    env = _clean_environment()

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
        status="running",
    )
    command_results: list[dict[str, object]] = []
    for index, command in enumerate(commands, start=1):
        started = time.perf_counter()
        result = _run(command, env)
        command_results.append(
            {
                "index": index,
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
            status="running" if result.returncode == 0 else "failed",
            exit_code=None if result.returncode == 0 else result.returncode,
            command_results=command_results,
        )
        if result.returncode:
            print(f"metadata: {metadata_path}")
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
        status="passed",
        exit_code=0,
        command_results=command_results,
    )
    print(f"install: {install_dir}")
    print(f"validation: {output_dir}")
    print(f"metadata: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
