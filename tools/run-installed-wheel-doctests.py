#!/usr/bin/env python3
"""
Run an installed-wheel Sage doctest sweep and reduce it into triage artifacts.
"""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent
ANALYZER = TOOLS_DIR / "analyze-doctest-log.py"


@dataclass(frozen=True)
class ArtifactPaths:
    base: str
    log: Path
    stats: Path
    analysis_json: Path
    analysis_md: Path


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


def build_clean_environment(python: str) -> dict[str, str]:
    env = os.environ.copy()
    python_bin = os.fspath(Path(python).resolve().parent)
    path = env.get("PATH", "")
    env["PATH"] = python_bin if not path else f"{python_bin}{os.pathsep}{path}"
    env["PYTHONNOUSERSITE"] = "1"
    env.pop("PYTHONPATH", None)
    return env


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

    doctest = _run(build_doctest_command(args, paths), env)

    if not paths.log.is_file():
        raise RuntimeError(
            f"installed-wheel doctest run did not create the expected log file: {paths.log}"
        )

    analyzer = _run(
        build_analyzer_command(
            args.python,
            paths,
            include_stats=paths.stats.is_file(),
        ),
        env,
    )

    print(f"log: {paths.log}")
    if paths.stats.is_file():
        print(f"stats: {paths.stats}")
    else:
        print(f"stats: missing ({paths.stats})")
    print(f"analysis json: {paths.analysis_json}")
    print(f"analysis md: {paths.analysis_md}")

    if analyzer.returncode:
        return analyzer.returncode
    return doctest.returncode


if __name__ == "__main__":
    raise SystemExit(main())
