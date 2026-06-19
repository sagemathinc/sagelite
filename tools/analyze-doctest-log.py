#!/usr/bin/env python3
"""
Summarize Sage doctest logs into a smaller set of actionable buckets.

This is intended for wheel/distribution triage, where the raw doctest output
is too large to reason about directly. The script combines the plain-text log
with the per-module stats JSON and produces:

- per-module summaries with status, category, and a root-cause fingerprint;
- aggregate counts by category and fingerprint;
- a compact Markdown report suitable for humans.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


RUN_RE = re.compile(
    r"^(?:python3 -m sage\.doctest|(?:\S+/)?sage -t) .* (?P<path>\S+?)(?:\s+#\s+(?P<summary>.+))?$"
)

FILE_RE = re.compile(
    r'^File "(?P<path>[^"]+)", line \d+, in (?P<context>\S+)$'
)

FAIL_LINE_RE = re.compile(r"^\s*(?P<count>\d+)\s+doctests failed$")
ITEM_FAILURES_RE = re.compile(r"^\d+\s+items?\s+had failures:$")


def normalize_module_name(path: str) -> str:
    parts = Path(path).parts
    if "site-packages" in parts:
        idx = parts.index("site-packages") + 1
        rel = Path(*parts[idx:])
    else:
        rel = Path(path)
        if "sage" in parts:
            idx = parts.index("sage")
            rel = Path(*parts[idx:])
    suffixes = "".join(rel.suffixes)
    stem = str(rel)
    for suffix in (".py", ".pyx", ".pxd", ".rst", ".sage"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    return stem.replace("/", ".")


@dataclass
class ModuleResult:
    module: str
    path: str
    summary: str | None = None
    status: str = "passed"
    failed_examples: int = 0
    traceback_lines: list[str] = field(default_factory=list)
    ntests: int | None = None
    walltime: float | None = None
    failed_flag: bool | None = None
    category: str = "unknown"
    fingerprint: str = "unknown"
    evidence: str = ""
    suggested_package: str = ""


def classify(result: ModuleResult) -> tuple[str, str, str]:
    text = "\n".join(
        [result.summary or "", *result.traceback_lines[:80]]
    ).lower()

    if (
        "timed out" in text
        or result.status == "timed_out"
        or (result.failed_flag and result.ntests == 0 and result.walltime == 1_000_000.0)
    ):
        return "performance-only", "timeout", "module exceeded doctest time limit"

    if result.failed_examples == 0 and "warning: slow doctest:" in text:
        return "performance-only", "slow-doctest", "example exceeded the long-doctest warning threshold"

    if (
        result.failed_examples == 0
        and "referenced here was set only in doctest marked" in text
    ):
        return (
            "core-supported",
            "doctest-dependency-warning",
            "doctest depends on a variable set only by a skipped feature-tagged example",
        )

    if "runtimeerror in doctesting framework" in text or result.status == "framework_error":
        return "framework", "doctest-framework", "doctest harness failed before normal example evaluation"

    data_patterns = [
        ("cremona", "optional-data", "missing-cremona-db", "Cremona database not installed"),
        ("database_", "optional-data", "missing-database", "optional data package not installed"),
        ("knotinfo", "optional-data", "missing-knotinfo-db", "optional data package not installed"),
    ]
    for needle, category, fingerprint, evidence in data_patterns:
        if needle in text:
            return category, fingerprint, evidence

    if (
        "cypari2" in text
        and "sage.libs.pari" in text
        and ("segmentation fault" in text or "signalerror" in text)
    ):
        return (
            "optional-external",
            "mixed-pari-runtime",
            "cypari2 and Sage PARI conversion crashed in native code",
        )

    external_patterns = [
        (
            "undefined symbol: festack_advance",
            "optional-external",
            "maxima-runtime-abi-mismatch",
            "Maxima runtime wheel is ABI-incompatible with the loaded ECL library",
        ),
        ("executable '", "optional-external", "missing-executable", "standalone executable not found"),
        ("not found on path", "optional-external", "missing-executable", "standalone executable not found"),
        ("featurenotpresenterror", "optional-external", "optional-feature-missing", "optional feature is unavailable"),
        ("module error: don't know how to require maxima", "optional-external", "maxima-library-mode-missing", "Maxima library mode is unavailable"),
        (".mesonpy-", "optional-external", "stale-build-path", "installed code still refers to a build-tree path"),
        ("/src/sage/", "optional-external", "stale-build-path", "installed code still refers to a build-tree path"),
        ("/project/local/", "optional-external", "stale-build-path", "installed code still refers to a build-tree path"),
        ("attributeerror: module 'sage.interfaces' has no attribute 'maxima_lib'", "optional-external", "maxima-library-mode-missing", "Maxima library mode is unavailable"),
        ("sage.libs.", "optional-external", "optional-native-lib-missing", "optional native feature is not bundled"),
        ("libbraiding", "optional-external", "optional-native-lib-missing", "optional native feature is not bundled"),
        ("libhomfly", "optional-external", "optional-native-lib-missing", "optional native feature is not bundled"),
        ("leftnormalform failed", "optional-external", "optional-native-lib-missing", "optional native feature is not bundled"),
    ]
    for needle, category, fingerprint, evidence in external_patterns:
        if needle in text:
            return category, fingerprint, evidence

    crash_patterns = [
        ("segmentation fault", "core-supported", "crash", "process crashed"),
        ("signalerror", "core-supported", "crash", "signal-level crash or abort"),
        ("abort", "core-supported", "crash", "process aborted"),
        ("sigdie", "core-supported", "crash", "process crashed in native code"),
        ("cysigs_signal_handler", "core-supported", "crash", "process crashed in native code"),
        ("no symbol table info available.", "core-supported", "crash", "native backtrace captured after crash"),
    ]
    for needle, category, fingerprint, evidence in crash_patterns:
        if needle in text:
            return category, fingerprint, evidence

    if _is_output_mismatch(text):
        if _looks_like_numeric_tolerance_mismatch(text):
            return (
                "core-supported",
                "numeric-tolerance",
                "numeric output differs only in displayed floating-point precision",
            )
        if _looks_like_symbolic_variant(text):
            return (
                "core-supported",
                "symbolic-output-variant",
                "symbolic output has an algebraically plausible representation difference",
            )
        if _looks_like_external_output_variant(text):
            return (
                "optional-external",
                "external-output-variant",
                "external runtime emitted verbose or formatting output that differs",
            )
        if _looks_like_representative_choice(text):
            return (
                "core-supported",
                "representative-choice",
                "algorithm selected a different valid representative or ordering",
            )
        return (
            "core-supported",
            "output-mismatch",
            "example output differs from expected output",
        )

    semantic_patterns = [
        ("failed example:", "core-supported", "doctest-failure", "example output or behavior mismatch"),
        ("traceback (most recent call last)", "core-supported", "runtime-exception", "example raised an exception"),
    ]
    for needle, category, fingerprint, evidence in semantic_patterns:
        if needle in text:
            return category, fingerprint, evidence

    if result.failed_flag is False:
        return "core-supported", "passed", "module passed"

    return "unknown", "unknown", "no rule matched"


FLOAT_RE = re.compile(r"(?<![\w.])[-+]?(?:\d+\.\d*|\.\d+)(?:e[-+]?\d+)?(?![\w.])")

SYMBOLIC_VARIANT_MARKERS = (
    "integrate(",
    "laplace(",
    "arctan",
    "dilog",
    "erf(",
    "exp_polar",
    "fresnel",
    "gamma(",
    "log(",
    "piecewise(",
    "real_nth_root",
    "sgn(",
    "sqrt(",
)

EXTERNAL_OUTPUT_MARKERS = (
    "computing hermitean normal form",
    "computing vertices",
    "executing",
    "reading .ext file",
    "time for reading",
    "latte",
    "normaliz",
    "qepcad",
)

REPRESENTATIVE_CHOICE_MARKERS = (
    "character_table",
    "graph on",
    "subgraph of",
    "uniformizer",
)


def _is_output_mismatch(text: str) -> bool:
    return "expected:" in text and "got:" in text


def _looks_like_numeric_tolerance_mismatch(text: str) -> bool:
    return len(FLOAT_RE.findall(text)) >= 2


def _looks_like_symbolic_variant(text: str) -> bool:
    return any(marker in text for marker in SYMBOLIC_VARIANT_MARKERS)


def _looks_like_external_output_variant(text: str) -> bool:
    return any(marker in text for marker in EXTERNAL_OUTPUT_MARKERS)


def _looks_like_representative_choice(text: str) -> bool:
    return any(marker in text for marker in REPRESENTATIVE_CHOICE_MARKERS)


MISSING_EXECUTABLE_PACKAGES = {
    "4ti2": "sagelite-4ti2-runtime",
    "benzene": "sagelite-benzene-runtime",
    "buckygen": "sagelite-buckygen-runtime",
    "cddexec": "sagelite-cddlib-runtime",
    "cddexec_gmp": "sagelite-cddlib-runtime",
    "class.x": "sagelite-palp-runtime",
    "csdp": "sagelite-csdp-runtime",
    "circuits": "sagelite-4ti2-runtime",
    "convert": "sagelite-imagemagick-runtime",
    "cu2": "sagelite-rubiks-runtime",
    "cubex": "sagelite-rubiks-runtime",
    "cws.x": "sagelite-palp-runtime",
    "dikcube": "sagelite-rubiks-runtime",
    "directg": "sagelite-nauty-runtime",
    "dot": "sagelite-graphviz-runtime",
    "dvipng": "sagelite-dvipng-runtime",
    "ecm": "sagelite-ecm-runtime",
    "flatter": "sagelite-flatter-runtime",
    "fricas": "sagelite-fricas-runtime",
    "frobby": "sagelite-frobby-runtime",
    "gap": "sagelite-gap-runtime",
    "gap3": "sagelite-gap3-runtime",
    "genbg": "sagelite-nauty-runtime",
    "geng": "sagelite-nauty-runtime",
    "genktreeg": "sagelite-nauty-runtime",
    "genposetg": "sagelite-nauty-runtime",
    "gentourng": "sagelite-nauty-runtime",
    "gentreeg": "sagelite-nauty-runtime",
    "gfan": "sagelite-gfan-runtime",
    "gfan_bases": "sagelite-gfan-runtime",
    "gfan_groebnercone": "sagelite-gfan-runtime",
    "gfan_render": "sagelite-gfan-runtime",
    "graver": "sagelite-4ti2-runtime",
    "giac": "sagelite-giac-runtime",
    "glucose": "sagelite-glucose-runtime",
    "glucose-syrup": "sagelite-glucose-runtime",
    "groebner": "sagelite-4ti2-runtime",
    "hilbert": "sagelite-4ti2-runtime",
    "info": "sagelite-info-runtime",
    "kissat": "sagelite-kissat-runtime",
    "latte-count": "sagelite-latte-runtime",
    "latte-integrate": "sagelite-latte-runtime",
    "lcalc": "sagelite-lcalc-runtime",
    "lie": "sagelite-lie-runtime",
    "lrs": "sagelite-lrslib-runtime",
    "lrsnash": "sagelite-lrslib-runtime",
    "magick": "sagelite-imagemagick-runtime",
    "markov": "sagelite-4ti2-runtime",
    "mcube": "sagelite-rubiks-runtime",
    "mwrank": "sagelite-mwrank-runtime",
    "msolve": "sagelite-msolve-runtime",
    "neato": "sagelite-graphviz-runtime",
    "nef.x": "sagelite-palp-runtime",
    "optimal": "sagelite-rubiks-runtime",
    "pdftocairo": "sagelite-poppler-runtime",
    "pdf2svg": "sagelite-pdf2svg-runtime",
    "points2allfinetriang": "sagelite-topcom-runtime",
    "planarity": "sagelite-planarity-runtime",
    "plantri": "sagelite-plantri-runtime",
    "poly.x": "sagelite-palp-runtime",
    "points2allfinetriangs": "sagelite-topcom-runtime",
    "points2alltriangs": "sagelite-topcom-runtime",
    "points2finetriang": "sagelite-topcom-runtime",
    "points2finetriangs": "sagelite-topcom-runtime",
    "points2placingtriang": "sagelite-topcom-runtime",
    "points2placingtriangs": "sagelite-topcom-runtime",
    "points2triang": "sagelite-topcom-runtime",
    "points2triangs": "sagelite-topcom-runtime",
    "ppi": "sagelite-4ti2-runtime",
    "qepcad": "sagelite-qepcad-runtime",
    "qsolve": "sagelite-4ti2-runtime",
    "rays": "sagelite-4ti2-runtime",
    "rubiks": "sagelite-rubiks-runtime",
    "singular": "sagelite-singular-runtime",
    "size222": "sagelite-rubiks-runtime",
    "sympow": "sagelite-sympow-runtime",
    "tachyon": "sagelite-tachyon-runtime",
    "theta": "sagelite-csdp-runtime",
    "twopi": "sagelite-graphviz-runtime",
    "zsolve": "sagelite-4ti2-runtime",
}

MISSING_DATABASE_PACKAGES = {
    "conway_polynomials": "conway-polynomials",
    "cubic_hecke": "database-cubic-hecke",
    "cunningham": "sagelite-cunningham-tables",
    "database_cremona_ellcurve": "sagelite-database-cremona-ellcurve",
    "database_cremona_mini_ellcurve": "sagelite-database-cremona-mini",
    "database_cubic_hecke": "database-cubic-hecke",
    "database_ellcurves": "sagelite-database-ellcurves",
    "database_graphs": "sagelite-database-graphs",
    "database_jones_numfield": "sagelite-database-jones-numfield",
    "database_knotinfo": "database-knotinfo",
    "database_kohel": "sagelite-database-kohel",
    "database_matroids": "matroid-database",
    "database_mutation_class": "sagelite-database-mutation-class",
    "database_odlyzko_zeta": "sagelite-database-odlyzko-zeta",
    "database_polytopes": "sagelite-database-polytopes",
    "database_polytopes_4d": "sagelite-database-polytopes-4d",
    "database_sloane": "sagelite-database-sloane",
    "database_stein_watkins": "sagelite-database-stein-watkins",
    "database_stein_watkins_mini": "sagelite-database-stein-watkins-mini",
    "database_symbolic_data": "sagelite-database-symbolic-data",
    "knotinfo": "database-knotinfo",
    "matroid": "matroid-database",
    "matroid_database": "matroid-database",
}


def _matched_package(text: str, packages: dict[str, str]) -> str:
    for needle, package in sorted(packages.items(), key=lambda item: -len(item[0])):
        if re.search(
            rf"(?<![a-z0-9_-]){re.escape(needle)}(?![a-z0-9_-])",
            text,
        ):
            return package
    return ""


def suggested_package(result: ModuleResult) -> str:
    """
    Return the companion package most likely to address a failed doctest.

    The analyzer is used during sagelite wheel triage, where the next useful
    action is often "build or install this companion wheel" rather than just
    reading the exception text.
    """
    text = "\n".join([result.summary or "", *result.traceback_lines[:80]]).lower()
    if result.fingerprint == "missing-executable":
        package = _matched_package(text, MISSING_EXECUTABLE_PACKAGES)
        if package:
            return package
    if result.fingerprint in {"missing-database", "optional-feature-missing"}:
        package = _matched_package(text, MISSING_DATABASE_PACKAGES)
        if package:
            return package

    return {
        "maxima-runtime-abi-mismatch": "sagelite-maxima-runtime >=10.9.post13",
        "maxima-library-mode-missing": "sagelite-maxima-runtime >=10.9.post13",
        "missing-cremona-db": "sagelite-database-cremona-mini",
        "missing-knotinfo-db": "database-knotinfo",
        "missing-database": "matching sagelite-database-* companion package",
        "missing-executable": "matching sagelite-*-runtime companion package",
        "mixed-pari-runtime": "rebuild sagelite with source-built cypari2 and one repaired libpari",
        "optional-feature-missing": "matching sagelite companion package or PyPI dependency",
        "optional-native-lib-missing": "matching sagelite runtime or sagelite core extension",
    }.get(result.fingerprint, "")


def parse_log(log_path: Path) -> dict[str, ModuleResult]:
    results: dict[str, ModuleResult] = {}
    current: ModuleResult | None = None
    capture_traceback = False

    with log_path.open(encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            match = RUN_RE.match(line)
            if match:
                module = normalize_module_name(match.group("path"))
                current = results.setdefault(
                    module,
                    ModuleResult(module=module, path=match.group("path")),
                )
                if match.group("summary"):
                    current.summary = match.group("summary")
                    lowered = current.summary.lower()
                    if "timed out" in lowered:
                        current.status = "timed_out"
                    elif "runtimeerror in doctesting framework" in lowered:
                        current.status = "framework_error"
                    elif "failed" in lowered:
                        current.status = "failed"
                capture_traceback = False
                continue

            match = FILE_RE.match(line)
            if match:
                module = normalize_module_name(match.group("path"))
                current = results.setdefault(
                    module,
                    ModuleResult(module=module, path=match.group("path")),
                )
                if current.status == "passed":
                    current.status = "failed"
                capture_traceback = False
                continue

            if current is None:
                continue

            stripped = line.strip()
            if stripped == "**********************************************************************":
                capture_traceback = True
                continue

            if stripped == "Failed example:":
                current.failed_examples += 1
                current.status = "failed"
                capture_traceback = True
                continue

            if stripped.startswith("Warning:"):
                current.status = "failed"
                current.traceback_lines.append(stripped)
                capture_traceback = True
                continue

            if ITEM_FAILURES_RE.match(stripped):
                capture_traceback = False
                continue

            fail_match = FAIL_LINE_RE.match(stripped)
            if fail_match:
                current.summary = f"{fail_match.group('count')} doctests failed"
                current.status = "failed"
                continue

            if capture_traceback and stripped:
                current.traceback_lines.append(stripped)
                if len(current.traceback_lines) > 120:
                    current.traceback_lines.pop(0)

    return results


def merge_stats(results: dict[str, ModuleResult], stats_path: Path | None) -> None:
    if stats_path is None:
        return
    with stats_path.open(encoding="utf-8") as handle:
        stats = json.load(handle)
    if not isinstance(stats, dict):
        return
    for module, payload in stats.items():
        result = results.setdefault(module, ModuleResult(module=module, path=module))
        if isinstance(payload, dict):
            result.ntests = payload.get("ntests")
            result.walltime = payload.get("walltime")
            result.failed_flag = payload.get("failed")
            if payload.get("failed") and result.status == "passed":
                result.status = "failed"


def build_report(results: dict[str, ModuleResult]) -> dict[str, Any]:
    for result in results.values():
        result.category, result.fingerprint, result.evidence = classify(result)
        result.suggested_package = suggested_package(result)

    failed = [r for r in results.values() if r.status != "passed" or r.failed_flag]
    category_counts = Counter(r.category for r in failed)
    fingerprint_counts = Counter(r.fingerprint for r in failed)
    subsystem_counts = Counter(r.module.split(".")[1] if "." in r.module else r.module for r in failed)

    top_examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in sorted(
        failed,
        key=lambda r: (
            r.category,
            -(r.failed_examples or 0),
            -(r.ntests or 0),
            r.module,
        ),
    ):
        bucket = top_examples[result.category]
        if len(bucket) >= 12:
            continue
        bucket.append(
            {
                "module": result.module,
                "summary": result.summary,
                "fingerprint": result.fingerprint,
                "failed_examples": result.failed_examples,
                "ntests": result.ntests,
                "walltime": result.walltime,
                "evidence": result.evidence,
                "suggested_package": result.suggested_package,
                "traceback_excerpt": result.traceback_lines[:12],
            }
        )

    return {
        "totals": {
            "modules_seen": len(results),
            "modules_failed": len(failed),
        },
        "category_counts": dict(category_counts.most_common()),
        "fingerprint_counts": dict(fingerprint_counts.most_common()),
        "subsystem_counts": dict(subsystem_counts.most_common(25)),
        "modules": [asdict(r) for r in sorted(failed, key=lambda r: r.module)],
        "top_examples": dict(top_examples),
    }


def render_markdown(report: dict[str, Any], log_path: Path, stats_path: Path | None) -> str:
    lines: list[str] = []
    lines.append("# Doctest Analysis")
    lines.append("")
    lines.append(f"- Log: `{log_path}`")
    if stats_path is not None:
        lines.append(f"- Stats: `{stats_path}`")
    lines.append(f"- Failed modules: `{report['totals']['modules_failed']}` / `{report['totals']['modules_seen']}`")
    lines.append("")

    lines.append("## Category Counts")
    lines.append("")
    for category, count in report["category_counts"].items():
        lines.append(f"- `{category}`: {count}")
    lines.append("")

    lines.append("## Top Fingerprints")
    lines.append("")
    for fingerprint, count in list(report["fingerprint_counts"].items())[:12]:
        lines.append(f"- `{fingerprint}`: {count}")
    lines.append("")

    lines.append("## Top Subsystems")
    lines.append("")
    for subsystem, count in list(report["subsystem_counts"].items())[:15]:
        lines.append(f"- `{subsystem}`: {count}")
    lines.append("")

    lines.append("## Representative Failures")
    lines.append("")
    for category, examples in report["top_examples"].items():
        lines.append(f"### `{category}`")
        lines.append("")
        for example in examples[:6]:
            summary = example["summary"] or "failed"
            lines.append(f"- `{example['module']}`: {summary}")
            lines.append(f"  fingerprint: `{example['fingerprint']}`")
            lines.append(f"  evidence: {example['evidence']}")
            if example["suggested_package"]:
                lines.append(f"  suggested package: `{example['suggested_package']}`")
            if example["traceback_excerpt"]:
                excerpt = " | ".join(example["traceback_excerpt"][:3])
                lines.append(f"  excerpt: `{excerpt}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", required=True, type=Path, help="path to sage.doctest log")
    parser.add_argument("--stats", type=Path, help="path to doctest stats JSON")
    parser.add_argument("--json-out", type=Path, help="write structured summary JSON")
    parser.add_argument("--md-out", type=Path, help="write Markdown summary")
    args = parser.parse_args()

    results = parse_log(args.log)
    merge_stats(results, args.stats)
    report = build_report(results)

    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.md_out:
        args.md_out.write_text(render_markdown(report, args.log, args.stats), encoding="utf-8")

    print(json.dumps(report["totals"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
