#!/usr/bin/env python3
"""
Run an installed-wheel Sage doctest sweep and reduce it into triage artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from packaging.utils import InvalidWheelFilename, parse_wheel_filename
from packaging.version import InvalidVersion, Version


TOOLS_DIR = Path(__file__).resolve().parent
ANALYZER = TOOLS_DIR / "analyze-doctest-log.py"
MANIFEST = TOOLS_DIR / "sagelite_runtime_manifest.py"


@dataclass(frozen=True)
class ArtifactPaths:
    base: str
    log: Path
    stats: Path
    analysis_json: Path
    analysis_md: Path
    runtime_manifest: Path
    runtime_summary: Path


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _slugify(label: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    return slug or "run"


def make_artifact_paths(output_dir: Path, label: str) -> ArtifactPaths:
    base = f"doctest-installed-{_slugify(label)}-{_timestamp()}"
    return ArtifactPaths(
        base=base,
        log=output_dir / f"{base}.log",
        stats=output_dir / f"{base}.json",
        analysis_json=output_dir / f"{base}.analysis.json",
        analysis_md=output_dir / f"{base}.analysis.md",
        runtime_manifest=output_dir / f"{base}.runtime-manifest.json",
        runtime_summary=output_dir / f"{base}.runtime-summary.json",
    )


def _extra_doctest_args(extra_args: list[str]) -> list[str]:
    if extra_args[:1] == ["--"]:
        return extra_args[1:]
    return extra_args


def build_doctest_command(args: argparse.Namespace, paths: ArtifactPaths) -> list[str]:
    command = [
        args.python,
        "-m",
        "sage.doctest",
        "--installed",
        "--logfile",
        str(paths.log),
        "--stats-path",
        str(paths.stats),
        "--optional",
        args.optional,
        "-p",
        str(args.nthreads),
    ]
    if args.short is not None:
        command.extend(["--short", str(args.short)])
    if not args.show_passes:
        command.append("--only-errors")
    command.extend(_extra_doctest_args(args.doctest_args))
    return command


def build_analyzer_command(
    python: str,
    paths: ArtifactPaths,
    *,
    include_stats: bool,
) -> list[str]:
    command = [
        python,
        str(ANALYZER),
        "--log",
        str(paths.log),
        "--json-out",
        str(paths.analysis_json),
        "--md-out",
        str(paths.analysis_md),
    ]
    if include_stats:
        command.extend(["--stats", str(paths.stats)])
    return command


def build_manifest_command(
    python: str,
    paths: ArtifactPaths,
    *,
    label: str,
    compiled_limit: int | None,
) -> list[str]:
    command = [
        python,
        str(MANIFEST),
        "collect",
        "--label",
        label,
        "--output",
        str(paths.runtime_manifest),
    ]
    if compiled_limit is not None:
        command.extend(["--compiled-limit", str(compiled_limit)])
    return command


def build_clean_environment(python: str) -> dict[str, str]:
    env = os.environ.copy()
    python_bin = os.fspath(Path(python).resolve().parent)
    path = env.get("PATH", "")
    env["PATH"] = python_bin if not path else f"{python_bin}{os.pathsep}{path}"
    env["PYTHONNOUSERSITE"] = "1"
    env.pop("PYTHONPATH", None)
    env.pop("LD_LIBRARY_PATH", None)
    return env


def _path_head(env: dict[str, str], limit: int = 8) -> list[str]:
    return [entry for entry in env.get("PATH", "").split(os.pathsep) if entry][:limit]


def _manifest_feature_summary(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"available": False, "reason": "manifest not created"}
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - summary should survive bad manifests
        return {
            "available": False,
            "reason": f"{type(exc).__name__}: {exc}",
        }

    features = manifest.get("features", {}).get("features", [])
    if not isinstance(features, list):
        return {
            "available": False,
            "reason": "manifest features section has unexpected shape",
        }

    groups = {
        "present": [],
        "absent": [],
        "unknown": [],
        "errored": [],
    }
    for feature in features:
        if not isinstance(feature, dict):
            continue
        name = feature.get("name")
        if not name:
            continue
        if feature.get("exception"):
            groups["errored"].append(name)
        elif feature.get("present") is True:
            groups["present"].append(name)
        elif feature.get("present") is False:
            groups["absent"].append(name)
        else:
            groups["unknown"].append(name)

    for names in groups.values():
        names.sort()

    return {
        "available": True,
        "counts": {name: len(values) for name, values in groups.items()},
        **groups,
    }


def _manifest_smoke_summary(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"available": False, "reason": "manifest not created"}
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - summary should survive bad manifests
        return {
            "available": False,
            "reason": f"{type(exc).__name__}: {exc}",
        }

    smoke_tests = manifest.get("smoke_tests", {})
    if not isinstance(smoke_tests, dict):
        return {
            "available": False,
            "reason": "manifest smoke_tests section has unexpected shape",
        }
    if "skipped" in smoke_tests:
        return {
            "available": True,
            "skipped": smoke_tests["skipped"],
            "counts": {"passed": 0, "failed": 0, "unknown": 0},
            "failures": {},
        }

    counts = {"passed": 0, "failed": 0, "unknown": 0}
    failures = {}

    native = smoke_tests.get("required_native_imports", {})
    if isinstance(native, dict):
        for module_name, result in native.get("modules", {}).items():
            if not isinstance(result, dict):
                counts["unknown"] += 1
                continue
            if result.get("present") is True:
                counts["passed"] += 1
            elif result.get("present") is False:
                counts["failed"] += 1
                failures[f"required_native_imports.{module_name}"] = result
            else:
                counts["unknown"] += 1

    for name, result in smoke_tests.items():
        if name == "required_native_imports":
            continue
        if not isinstance(result, dict):
            counts["unknown"] += 1
            continue
        returncode = result.get("returncode")
        if returncode == 0:
            counts["passed"] += 1
        elif returncode is None:
            counts["unknown"] += 1
        else:
            counts["failed"] += 1
            failures[name] = result

    return {
        "available": True,
        "counts": counts,
        "failures": failures,
    }


def _normalize_distribution_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _wheel_distribution_name(path: Path) -> str | None:
    if path.suffix != ".whl":
        return None
    try:
        name, _version, _build, _tags = parse_wheel_filename(path.name)
    except InvalidWheelFilename:
        stem = path.name[:-4]
        parts = stem.split("-")
        if len(parts) < 5:
            return None
        name_and_version = parts[:-3]
        for version_index in range(len(name_and_version) - 1, 0, -1):
            try:
                Version(name_and_version[version_index])
            except InvalidVersion:
                continue
            return _normalize_distribution_name(
                "-".join(name_and_version[:version_index])
            )
        return None
    return _normalize_distribution_name(name)


def _manual_companion_packages(args: argparse.Namespace) -> list[str]:
    return _companion_packages_from_wheels(args.installed_wheel)


def _companion_packages_from_wheels(wheels: list[Path]) -> list[str]:
    return sorted(
        {
            name
            for path in wheels
            for name in [_wheel_distribution_name(Path(path))]
            if name is not None
        }
        - {"sagelite"}
    )


def _wheelhouse_sagelite_wheels(paths: list[Path]) -> list[Path]:
    wheels = []
    seen = set()
    for wheelhouse in paths:
        if not wheelhouse.is_dir():
            continue
        for wheel in sorted(wheelhouse.glob("*.whl")):
            distribution = _wheel_distribution_name(wheel)
            if distribution is None:
                continue
            if distribution != "sagelite" and not distribution.startswith("sagelite-"):
                continue
            resolved = wheel.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            wheels.append(wheel)
    return wheels


def _recorded_installed_wheels(args: argparse.Namespace) -> tuple[list[str], bool]:
    if args.installed_wheel:
        return [Path(path).name for path in args.installed_wheel], False
    return [path.name for path in _wheelhouse_sagelite_wheels(args.wheelhouse)], True


def _manifest_sagelite_packages(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {
            "available": False,
            "reason": "manifest not created",
            "packages": [],
            "companion_packages": [],
        }
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - summary should survive bad manifests
        return {
            "available": False,
            "reason": f"{type(exc).__name__}: {exc}",
            "packages": [],
            "companion_packages": [],
        }

    packages = []
    companion_names = set()
    for package in manifest.get("packages", []):
        if not isinstance(package, dict):
            continue
        raw_name = package.get("name")
        if not raw_name:
            continue
        normalized = _normalize_distribution_name(str(raw_name))
        if normalized != "sagelite" and not normalized.startswith("sagelite-"):
            continue
        entry = {
            "name": normalized,
            "version": package.get("version"),
            "location": package.get("location"),
        }
        packages.append(entry)
        if normalized != "sagelite":
            companion_names.add(normalized)

    packages.sort(key=lambda package: str(package["name"]))
    return {
        "available": True,
        "packages": packages,
        "companion_packages": sorted(companion_names),
    }


def _analysis_summary(
    path: Path,
    *,
    analyzer_returncode: int | None,
    limit: int = 12,
) -> dict[str, object]:
    summary: dict[str, object] = {
        "returncode": analyzer_returncode,
        "path": str(path),
        "created": path.is_file(),
    }
    if not path.is_file():
        summary["available"] = False
        summary["reason"] = "analysis not created"
        return summary
    try:
        analysis = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - summary should survive bad analysis
        summary["available"] = False
        summary["reason"] = f"{type(exc).__name__}: {exc}"
        return summary

    summary.update(
        {
            "available": True,
            "totals": analysis.get("totals", {}),
            "category_counts": analysis.get("category_counts", {}),
            "fingerprint_counts": analysis.get("fingerprint_counts", {}),
            "top_actionable_buckets": analysis.get("actionable_buckets", [])[:limit],
        }
    )
    return summary


def _runtime_summary(
    args: argparse.Namespace,
    paths: ArtifactPaths,
    env: dict[str, str],
    doctest_command: list[str],
    manifest_command: list[str],
    manifest_returncode: int,
    analyzer_command: list[str] | None = None,
    analyzer_returncode: int | None = None,
) -> dict[str, object]:
    wheelhouse_paths = [str(path) for path in args.wheelhouse]
    wheelhouse_files = {}
    for path in args.wheelhouse:
        if path.is_dir():
            wheelhouse_files[str(path)] = sorted(
                child.name for child in path.glob("*.whl")
            )
        else:
            wheelhouse_files[str(path)] = None

    installed_wheels, installed_wheels_inferred = _recorded_installed_wheels(args)
    manifest_packages = _manifest_sagelite_packages(paths.runtime_manifest)
    inferred_companion_packages = (
        _companion_packages_from_wheels(_wheelhouse_sagelite_wheels(args.wheelhouse))
        if installed_wheels_inferred
        else []
    )
    companion_packages = sorted(
        set(_manual_companion_packages(args))
        | set(inferred_companion_packages)
        | set(manifest_packages.get("companion_packages", []))
    )

    return {
        "schema": "sagelite-installed-doctest-runtime-summary-v1",
        "python": str(Path(args.python).resolve()),
        "cwd": os.getcwd(),
        "environment": {
            "PATH_head": _path_head(env),
            "PYTHONNOUSERSITE": env.get("PYTHONNOUSERSITE"),
            "PYTHONPATH_present": "PYTHONPATH" in env,
            "LD_LIBRARY_PATH_present": "LD_LIBRARY_PATH" in env,
        },
        "artifacts": {
            "log": str(paths.log),
            "stats": str(paths.stats),
            "analysis_json": str(paths.analysis_json),
            "analysis_md": str(paths.analysis_md),
            "runtime_manifest": str(paths.runtime_manifest),
        },
        "runtime_manifest": {
            "command": manifest_command,
            "returncode": manifest_returncode,
            "path": str(paths.runtime_manifest),
            "created": paths.runtime_manifest.is_file(),
        },
        "features": _manifest_feature_summary(paths.runtime_manifest),
        "smoke_tests": _manifest_smoke_summary(paths.runtime_manifest),
        "analysis": {
            "command": analyzer_command or [],
            **_analysis_summary(
                paths.analysis_json,
                analyzer_returncode=analyzer_returncode,
            ),
        },
        "wheels": {
            "wheelhouse_paths": wheelhouse_paths,
            "wheelhouse_files": wheelhouse_files,
            "installed_wheels": installed_wheels,
            "installed_wheels_inferred_from_wheelhouse": installed_wheels_inferred,
            "installed_sagelite_packages": manifest_packages,
            "companion_packages": companion_packages,
        },
        "doctest_command": doctest_command,
    }


def write_runtime_summary(
    args: argparse.Namespace,
    paths: ArtifactPaths,
    env: dict[str, str],
    doctest_command: list[str],
    manifest_command: list[str],
    manifest_returncode: int,
    analyzer_command: list[str] | None = None,
    analyzer_returncode: int | None = None,
) -> None:
    summary = _runtime_summary(
        args,
        paths,
        env,
        doctest_command,
        manifest_command,
        manifest_returncode,
        analyzer_command,
        analyzer_returncode,
    )
    paths.runtime_summary.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    print(f"+ {' '.join(shlex.quote(part) for part in command)}", flush=True)
    return subprocess.run(command, check=False, text=True, env=env)


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python interpreter from the installed-wheel environment",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(".local-build-logs"),
        help="directory for doctest and analysis artifacts",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="label used in artifact filenames (defaults to short or full)",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--short",
        type=int,
        default=300,
        metavar="SECONDS",
        help="target walltime for a short installed-wheel doctest sweep",
    )
    mode.add_argument(
        "--full",
        action="store_true",
        help="omit --short and let the installed-wheel doctest run proceed normally",
    )
    parser.add_argument(
        "--optional",
        default="sage,optional",
        help="value passed to sage.doctest --optional",
    )
    parser.add_argument(
        "--nthreads",
        type=int,
        default=1,
        help="value passed to sage.doctest -p/--nthreads",
    )
    parser.add_argument(
        "--show-passes",
        action="store_true",
        help="omit --only-errors so successful modules are also printed",
    )
    parser.add_argument(
        "--runtime-summary",
        action="store_true",
        help="write a sanitized environment summary and runtime manifest before doctesting",
    )
    parser.add_argument(
        "--manifest-compiled-limit",
        type=int,
        default=None,
        help="limit compiled-module probes when --runtime-summary collects a manifest",
    )
    parser.add_argument(
        "--wheelhouse",
        action="append",
        type=Path,
        default=[],
        help="wheelhouse directory to record in --runtime-summary; may be repeated",
    )
    parser.add_argument(
        "--installed-wheel",
        action="append",
        type=Path,
        default=[],
        help="wheel filename installed for this run to record in --runtime-summary; may be repeated",
    )
    parser.add_argument(
        "doctest_args",
        nargs=argparse.REMAINDER,
        help="extra arguments passed through to python -m sage.doctest; prefix with --",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _make_parser().parse_args(argv)
    if args.full:
        args.short = None
    label = args.label or ("full" if args.short is None else "short")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    paths = make_artifact_paths(args.output_dir, label)
    env = build_clean_environment(args.python)
    doctest_command = build_doctest_command(args, paths)

    if args.runtime_summary:
        manifest_command = build_manifest_command(
            args.python,
            paths,
            label=label,
            compiled_limit=args.manifest_compiled_limit,
        )
        manifest = _run(manifest_command, env)
        write_runtime_summary(
            args,
            paths,
            env,
            doctest_command,
            manifest_command,
            manifest.returncode,
        )
        print(f"runtime manifest: {paths.runtime_manifest}")
        print(f"runtime summary: {paths.runtime_summary}")

    doctest = _run(doctest_command, env)

    if not paths.log.is_file():
        raise RuntimeError(
            f"installed-wheel doctest run did not create the expected log file: {paths.log}"
        )

    analyzer_command = build_analyzer_command(
        args.python,
        paths,
        include_stats=paths.stats.is_file(),
    )
    analyzer = _run(analyzer_command, env)

    if args.runtime_summary:
        write_runtime_summary(
            args,
            paths,
            env,
            doctest_command,
            manifest_command,
            manifest.returncode,
            analyzer_command,
            analyzer.returncode,
        )

    print(f"log: {paths.log}")
    if paths.stats.is_file():
        print(f"stats: {paths.stats}")
    else:
        print(f"stats: missing ({paths.stats})")
    print(f"analysis json: {paths.analysis_json}")
    print(f"analysis md: {paths.analysis_md}")
    if args.runtime_summary:
        print(f"runtime manifest: {paths.runtime_manifest}")
        print(f"runtime summary: {paths.runtime_summary}")

    if analyzer.returncode:
        return analyzer.returncode
    return doctest.returncode


if __name__ == "__main__":
    raise SystemExit(main())
