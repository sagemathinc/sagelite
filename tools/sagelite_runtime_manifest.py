#!/usr/bin/env python3
"""
Collect and compare runtime manifests for self-contained Sage and sagelite.

The collector is intentionally defensive: it records import and probe failures
as JSON data instead of aborting, so partially repaired wheels still produce a
useful parity artifact.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import inspect
import json
import os
import platform
import re
import signal
import shutil
import site
import subprocess
import sys
import sysconfig
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_EXECUTABLES = [
    "gap",
    "gap3",
    "maxima",
    "giac",
    "fricas",
    "singular",
    "qepcad",
    "latte-count",
    "count",
    "integrate",
    "msolve",
    "dot",
    "neato",
    "fdp",
    "twopi",
    "pdf2svg",
    "dvipng",
    "gfan",
    "4ti2",
    "palp",
]

SAGE_ENV_KEYS = [
    "SAGE_ROOT",
    "SAGE_LOCAL",
    "SAGE_SHARE",
    "SAGE_EXTCODE",
    "SAGE_VENV",
    "SAGE_SRC",
    "SAGE_LIB",
    "SAGE_DOC",
    "SAGE_DATA_PATH",
    "SAGE_GAP_COMMAND",
    "SAGE_GAP3_COMMAND",
    "GAP_ROOT_PATHS",
    "GP_DATA_DIR",
    "MAXIMA",
    "MAXIMA_FAS",
    "MAXIMA_IMAGESDIR",
    "MAXIMA_LAYOUT_AUTOTOOLS",
    "MAXIMA_PREFIX",
    "MAXIMA_USERDIR",
    "ECLDIR",
    "FRICAS",
    "FRICAS_COMMAND",
    "FRICAS_INITFILE",
    "ALDORROOT",
    "SAGE_FPLLL_DEFAULT_STRATEGY",
    "FPLLL_DEFAULT_STRATEGY",
    "LD_LIBRARY_PATH",
    "PATH",
    "PYTHONPATH",
    "PYTHONNOUSERSITE",
]

SOURCE_INSPECTION_MODULES = [
    "sage.rings.integer",
    "sage.rings.rational",
    "sage.libs.braiding",
    "sage.libs.coxeter3.coxeter",
    "sage.libs.homfly",
    "sage.rings.polynomial.pbori.pbori",
]

GAP_PACKAGE_PROGRAMS = {
    "guava": ["wtdist"],
}

PLATFORM_LIBRARY_RE = re.compile(
    r"^/(?:lib|lib64|usr/lib|usr/lib64)(?:/|$)|^linux-vdso\\.so"
)


@dataclass(frozen=True)
class ProbeResult:
    command: list[str]
    returncode: int | None
    stdout: str
    stderr: str
    error: str | None = None


def _json_default(value: Any) -> str:
    return str(value)


def _safe_call(label: str, func, *args, **kwargs) -> Any:
    try:
        return func(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 - manifest must survive bad runtimes
        return {"error": label, "exception": f"{type(exc).__name__}: {exc}"}


def _run_probe(command: list[str], timeout: float = 5.0) -> ProbeResult:
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
    except Exception as exc:  # noqa: BLE001 - probes should be recorded
        return ProbeResult(command, None, "", "", f"{type(exc).__name__}: {exc}")
    return ProbeResult(
        command,
        completed.returncode,
        completed.stdout.strip(),
        completed.stderr.strip(),
    )


def _short_text(text: str, limit: int = 4000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n... truncated {len(text) - limit} bytes ..."


def _split_paths(value: str | None) -> list[str]:
    if not value:
        return []
    return [entry for entry in value.split(os.pathsep) if entry]


def _split_gap_roots(value: str | None) -> list[str]:
    if not value:
        return []
    roots = []
    for entry in value.replace(os.pathsep, ";").split(";"):
        entry = entry.strip()
        if entry:
            roots.append(entry)
    return roots


def _dedupe_strings(values: list[str]) -> list[str]:
    seen = set()
    deduped = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def collect_python_info() -> dict[str, Any]:
    return {
        "executable": sys.executable,
        "version": sys.version,
        "version_info": list(sys.version_info),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
        "exec_prefix": sys.exec_prefix,
        "path": sys.path,
        "site_packages": _safe_call("site.getsitepackages", site.getsitepackages),
        "user_site": _safe_call("site.getusersitepackages", site.getusersitepackages),
        "sysconfig": {
            "platform": sysconfig.get_platform(),
            "purelib": sysconfig.get_path("purelib"),
            "platlib": sysconfig.get_path("platlib"),
            "scripts": sysconfig.get_path("scripts"),
            "soabi": sysconfig.get_config_var("SOABI"),
            "ext_suffix": sysconfig.get_config_var("EXT_SUFFIX"),
            "multiarch": sysconfig.get_config_var("MULTIARCH"),
        },
    }


def collect_installed_packages() -> list[dict[str, str | None]]:
    packages = []
    for dist in importlib.metadata.distributions():
        metadata = dist.metadata
        packages.append(
            {
                "name": metadata.get("Name") or dist.name,
                "version": metadata.get("Version"),
                "location": str(dist.locate_file("")),
            }
        )
    return sorted(packages, key=lambda item: (item["name"] or "").lower())


def _interesting_environment() -> dict[str, str]:
    prefixes = ("SAGE_", "SAGELITE_", "MAXIMA_", "FRICAS", "ALDOR", "GAP", "FPLLL")
    keys = set(SAGE_ENV_KEYS)
    keys.update(key for key in os.environ if key.startswith(prefixes))
    return {key: os.environ[key] for key in sorted(keys) if key in os.environ}


def collect_sage_environment() -> dict[str, Any]:
    data: dict[str, Any] = {
        "process_environment": _interesting_environment(),
    }
    try:
        sage_env = importlib.import_module("sage.env")
    except Exception as exc:  # noqa: BLE001
        data["import_error"] = f"{type(exc).__name__}: {exc}"
        return data

    for key in SAGE_ENV_KEYS:
        if hasattr(sage_env, key):
            data[key] = getattr(sage_env, key)
    for key, value in getattr(sage_env, "SAGE_ENV", {}).items():
        if key.startswith(("SAGE_", "GAP", "MAXIMA", "GP_", "FRICAS", "ALDOR")):
            data.setdefault("sage_env_map", {})[key] = value

    version = _safe_call("sage.version", importlib.import_module, "sage.version")
    if not isinstance(version, dict):
        data["version"] = {
            "version": getattr(version, "version", None),
            "date": getattr(version, "date", None),
            "banner": getattr(version, "banner", None),
        }
    return data


class _FeatureTimeout(RuntimeError):
    pass


def _feature_timeout_handler(signum, frame):  # noqa: ARG001
    raise _FeatureTimeout("feature probe timed out")


def _feature_is_present(feature, timeout: float | None) -> Any:
    if not timeout:
        return feature.is_present()
    old_handler = signal.getsignal(signal.SIGALRM)
    try:
        signal.signal(signal.SIGALRM, _feature_timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout)
        return feature.is_present()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)


def collect_features(timeout: float | None = 10.0) -> dict[str, Any]:
    try:
        features_all = importlib.import_module("sage.features.all")
        features = list(features_all.all_features())
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}

    results = []
    seen: set[str] = set()
    for feature in sorted(features, key=lambda item: item.name):
        if feature.name in seen:
            continue
        seen.add(feature.name)
        entry = {
            "name": feature.name,
            "class": f"{type(feature).__module__}.{type(feature).__qualname__}",
            "spkg": getattr(feature, "spkg", None),
            "type": _safe_call("feature type", feature._spkg_type),
            "joined_features": [joined.name for joined in feature.joined_features()],
        }
        try:
            present = _feature_is_present(feature, timeout)
            entry.update(
                {
                    "present": bool(present),
                    "reason": getattr(present, "reason", None),
                    "resolution": getattr(present, "resolution", None),
                }
            )
        except Exception as exc:  # noqa: BLE001
            entry.update(
                {
                    "present": None,
                    "exception": f"{type(exc).__name__}: {exc}",
                }
            )
        results.append(entry)
    return {"features": results}


def _version_probe(path: str) -> dict[str, Any]:
    probes = [
        [path, "--version"],
        [path, "-version"],
        [path, "-v"],
        [path, "-h"],
    ]
    attempts = []
    for command in probes:
        result = _run_probe(command)
        attempts.append(
            {
                "command": result.command,
                "returncode": result.returncode,
                "stdout": _short_text(result.stdout),
                "stderr": _short_text(result.stderr),
                "error": result.error,
            }
        )
        if result.returncode == 0 and (result.stdout or result.stderr):
            break
    return {"attempts": attempts}


def collect_executables(names: list[str]) -> dict[str, Any]:
    data = {}
    for name in names:
        path = shutil.which(name)
        entry: dict[str, Any] = {"path": path}
        if path:
            entry.update(_version_probe(path))
        data[name] = entry
    return data


def _gap_package_dirs(roots: list[str], package: str) -> list[Path]:
    dirs = []
    for root in roots:
        pkg_root = Path(root) / "pkg"
        if not pkg_root.is_dir():
            continue
        dirs.extend(pkg_root.glob(f"{package}*"))
        dirs.extend(pkg_root.glob(f"{package.upper()}*"))
    return sorted({path.resolve() for path in dirs if path.is_dir()})


def _gap_package_program_dirs(package_dir: Path) -> list[Path]:
    bin_dir = package_dir / "bin"
    dirs = []
    if bin_dir.is_dir():
        dirs.append(bin_dir.resolve())
        dirs.extend(path.resolve() for path in bin_dir.iterdir() if path.is_dir())
    return sorted(set(dirs))


def _program_status(program_dir: Path, name: str) -> dict[str, Any]:
    path = program_dir / name
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_file": path.is_file(),
        "executable": path.is_file() and os.access(path, os.X_OK),
    }


def collect_gap_package_programs(roots: list[str]) -> dict[str, Any]:
    details = {}
    for package, program_names in GAP_PACKAGE_PROGRAMS.items():
        package_dirs = _gap_package_dirs(roots, package)
        program_dirs = []
        for package_dir in package_dirs:
            for program_dir in _gap_package_program_dirs(package_dir):
                programs = {
                    name: _program_status(program_dir, name)
                    for name in program_names
                }
                program_dirs.append(
                    {
                        "package_dir": str(package_dir),
                        "path": str(program_dir),
                        "programs": programs,
                    }
                )
        complete = any(
            all(
                program["executable"]
                for program in program_dir["programs"].values()
            )
            for program_dir in program_dirs
        )
        details[package] = {
            "required_programs": program_names,
            "package_dirs": [str(path) for path in package_dirs],
            "program_dirs": program_dirs,
            "complete": complete,
        }
    return details


def collect_gap_details() -> dict[str, Any]:
    details = {
        "GAP_ROOT_PATHS": os.environ.get("GAP_ROOT_PATHS"),
        "gap_roots": _split_gap_roots(os.environ.get("GAP_ROOT_PATHS")),
    }
    try:
        sage_env = importlib.import_module("sage.env")
    except Exception as exc:  # noqa: BLE001
        details["sage_env_error"] = f"{type(exc).__name__}: {exc}"
        details["gap_package_programs"] = collect_gap_package_programs(
            details["gap_roots"]
        )
        return details
    roots = getattr(sage_env, "GAP_ROOT_PATHS", None)
    details["sage_env_gap_root_paths"] = roots
    details["sage_env_gap_roots"] = _split_gap_roots(roots)
    details["SAGE_GAP_COMMAND"] = getattr(sage_env, "SAGE_GAP_COMMAND", None)
    roots_for_programs = _dedupe_strings(
        details["sage_env_gap_roots"] + details["gap_roots"]
    )
    details["gap_package_programs"] = collect_gap_package_programs(
        roots_for_programs
    )
    details["workspace"] = _safe_call(
        "sage.libs.gap.saved_workspace",
        lambda: getattr(
            importlib.import_module("sage.libs.gap.saved_workspace"),
            "WORKSPACE",
            None,
        ),
    )
    try:
        libgap = importlib.import_module("sage.libs.gap.libgap").libgap
        package_paths = libgap.eval("GAPInfo.RootPaths")
        details["libgap_root_paths"] = str(package_paths)
        details["guava_program_dirs"] = str(
            libgap.eval('DirectoriesPackagePrograms("guava")')
        )
    except Exception as exc:  # noqa: BLE001
        details["libgap_error"] = f"{type(exc).__name__}: {exc}"
    return details


def collect_maxima_details() -> dict[str, Any]:
    details = {
        key: os.environ.get(key)
        for key in [
            "MAXIMA",
            "MAXIMA_PREFIX",
            "MAXIMA_USERDIR",
            "MAXIMA_FAS",
            "MAXIMA_IMAGESDIR",
            "MAXIMA_LAYOUT_AUTOTOOLS",
            "ECLDIR",
        ]
        if os.environ.get(key) is not None
    }
    details["executable"] = shutil.which(os.environ.get("MAXIMA", "maxima"))
    try:
        sage_env = importlib.import_module("sage.env")
        for key in ["MAXIMA_FAS", "MAXIMA_PREFIX"]:
            details[f"sage_env_{key}"] = getattr(sage_env, key, None)
    except Exception as exc:  # noqa: BLE001
        details["sage_env_error"] = f"{type(exc).__name__}: {exc}"
    if details.get("executable"):
        details["version_probe"] = _version_probe(details["executable"])
    return details


def collect_fricas_details() -> dict[str, Any]:
    details = {
        key: os.environ.get(key)
        for key in ["FRICAS", "FRICAS_COMMAND", "FRICAS_INITFILE", "ALDORROOT", "ECLDIR"]
        if os.environ.get(key) is not None
    }
    details["executable"] = shutil.which(
        os.environ.get("FRICAS_COMMAND") or os.environ.get("FRICAS") or "fricas"
    )
    if details.get("executable"):
        details["version_probe"] = _version_probe(details["executable"])
    return details


def collect_fplll_details() -> dict[str, Any]:
    details = {
        key: os.environ.get(key)
        for key in ["SAGE_FPLLL_DEFAULT_STRATEGY", "FPLLL_DEFAULT_STRATEGY"]
        if os.environ.get(key) is not None
    }
    try:
        fpylll = importlib.import_module("fpylll")
        config = importlib.import_module("fpylll.config")
        details["fpylll_version"] = getattr(fpylll, "__version__", None)
        for key in ["default_strategy", "default_strategy_path"]:
            details[f"fpylll_config_{key}"] = getattr(config, key, None)
    except Exception as exc:  # noqa: BLE001
        details["fpylll_error"] = f"{type(exc).__name__}: {exc}"
    return details


def _ldd(path: Path) -> dict[str, Any]:
    result = _run_probe(["ldd", str(path)])
    dependencies = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if "=>" in line:
            name, remainder = line.split("=>", 1)
            resolved = remainder.strip().split(" ", 1)[0]
            dependencies.append({"name": name.strip(), "path": resolved})
        elif line:
            dependencies.append({"name": line.split(" ", 1)[0], "path": None})
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "error": result.error,
        "dependencies": dependencies,
    }


def _dynamic_tags(path: Path) -> dict[str, Any]:
    result = _run_probe(["readelf", "-d", str(path)])
    tags = []
    for line in result.stdout.splitlines():
        if "RPATH" in line or "RUNPATH" in line:
            tags.append(line.strip())
    return {
        "returncode": result.returncode,
        "tags": tags,
        "stderr": result.stderr,
        "error": result.error,
    }


def _is_allowed_dependency(path: str | None, allowed_roots: list[Path]) -> bool:
    if not path or path in {"not", "statically"}:
        return True
    if path == "not found":
        return False
    if PLATFORM_LIBRARY_RE.match(path):
        return True
    try:
        resolved = Path(path).resolve()
    except OSError:
        return False
    return any(
        resolved == root or root in resolved.parents
        for root in allowed_roots
        if root
    )


def _sage_search_roots() -> list[Path]:
    roots = []
    try:
        sage = importlib.import_module("sage")
    except Exception:
        return roots
    for root in getattr(sage, "__path__", []):
        roots.append(Path(root))
    return roots


def collect_compiled_modules(limit: int | None = None) -> list[dict[str, Any]]:
    suffixes = tuple(
        suffix
        for suffix in [
            sysconfig.get_config_var("EXT_SUFFIX"),
            ".so",
        ]
        if suffix
    )
    allowed_roots = [Path(sys.prefix).resolve(), Path(sys.exec_prefix).resolve()]
    modules = []
    for root in _sage_search_roots():
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.so")):
            if not path.name.endswith(suffixes):
                continue
            ldd = _ldd(path)
            readelf = _dynamic_tags(path)
            dependencies_outside_policy = [
                dep
                for dep in ldd["dependencies"]
                if not _is_allowed_dependency(dep.get("path"), allowed_roots)
            ]
            modules.append(
                {
                    "path": str(path),
                    "sage_relative_path": str(path.relative_to(root.parent)),
                    "ldd": ldd,
                    "dynamic_tags": readelf,
                    "dependencies_outside_policy": dependencies_outside_policy,
                }
            )
            if limit is not None and len(modules) >= limit:
                return modules
    return modules


def collect_source_inspection(modules: list[str]) -> dict[str, Any]:
    data = {}
    try:
        sageinspect = importlib.import_module("sage.misc.sageinspect")
    except Exception as exc:  # noqa: BLE001
        sageinspect = None
        sageinspect_error = f"{type(exc).__name__}: {exc}"
    else:
        sageinspect_error = None

    for module_name in modules:
        entry: dict[str, Any] = {}
        try:
            module = importlib.import_module(module_name)
            entry["file"] = getattr(module, "__file__", None)
            entry["inspect_getsourcefile"] = inspect.getsourcefile(module)
            if sageinspect is not None:
                entry["sage_getfile_relative"] = sageinspect.sage_getfile_relative(
                    module
                )
            else:
                entry["sage_getfile_relative_error"] = sageinspect_error
        except Exception as exc:  # noqa: BLE001
            entry["error"] = f"{type(exc).__name__}: {exc}"
        data[module_name] = entry
    return data


def collect_manifest(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "schema": "sagelite-runtime-manifest-v1",
        "label": args.label,
        "python": collect_python_info(),
        "sage": collect_sage_environment(),
        "packages": collect_installed_packages(),
        "features": collect_features(args.feature_timeout),
        "executables": collect_executables(args.executable),
        "gap": collect_gap_details(),
        "maxima": collect_maxima_details(),
        "fricas": collect_fricas_details(),
        "fplll": collect_fplll_details(),
        "compiled_modules": collect_compiled_modules(args.compiled_limit),
        "source_inspection": collect_source_inspection(args.inspect_module),
    }


def _package_map(manifest: dict[str, Any]) -> dict[str, str | None]:
    return {
        (package.get("name") or "").lower(): package.get("version")
        for package in manifest.get("packages", [])
    }


def _feature_map(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        feature["name"]: feature
        for feature in manifest.get("features", {}).get("features", [])
    }


def _dependency_leaks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    leaks = []
    for module in manifest.get("compiled_modules", []):
        if module.get("dependencies_outside_policy"):
            leaks.append(
                {
                    "module": module.get("sage_relative_path") or module.get("path"),
                    "dependencies": module["dependencies_outside_policy"],
                }
            )
    return leaks


def _gap_package_program_map(manifest: dict[str, Any]) -> dict[str, Any]:
    return manifest.get("gap", {}).get("gap_package_programs", {})


def _gap_package_program_differences(
    reference: dict[str, Any], candidate: dict[str, Any]
) -> dict[str, Any]:
    ref_programs = _gap_package_program_map(reference)
    cand_programs = _gap_package_program_map(candidate)
    differences = {}
    for package in sorted(set(ref_programs) | set(cand_programs)):
        ref = ref_programs.get(package, {})
        cand = cand_programs.get(package, {})
        if ref.get("complete") != cand.get("complete"):
            differences[package] = {
                "reference_complete": ref.get("complete"),
                "candidate_complete": cand.get("complete"),
                "candidate_package_dirs": cand.get("package_dirs", []),
                "candidate_program_dirs": cand.get("program_dirs", []),
            }
    return differences


def _is_gap_host_path(path: str | None) -> bool:
    if not path:
        return False
    return path.startswith(("/usr/share/gap", "/usr/lib/gap", "/usr/libexec/gap"))


def _candidate_gap_host_leaks(candidate: dict[str, Any]) -> list[str]:
    paths = []
    gap = candidate.get("gap", {})
    paths.extend(gap.get("sage_env_gap_roots") or [])
    paths.extend(gap.get("gap_roots") or [])
    for package in _gap_package_program_map(candidate).values():
        paths.extend(package.get("package_dirs", []))
        paths.extend(
            program_dir.get("path")
            for program_dir in package.get("program_dirs", [])
        )
    return sorted(path for path in _dedupe_strings(paths) if _is_gap_host_path(path))


def compare_manifests(reference: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    ref_packages = _package_map(reference)
    cand_packages = _package_map(candidate)
    ref_features = _feature_map(reference)
    cand_features = _feature_map(candidate)

    missing_packages = sorted(set(ref_packages) - set(cand_packages))
    version_differences = {
        name: {"reference": ref_packages[name], "candidate": cand_packages[name]}
        for name in sorted(set(ref_packages) & set(cand_packages))
        if ref_packages[name] != cand_packages[name]
    }
    feature_differences = {}
    for name in sorted(set(ref_features) | set(cand_features)):
        ref = ref_features.get(name, {})
        cand = cand_features.get(name, {})
        if ref.get("present") != cand.get("present"):
            feature_differences[name] = {
                "reference": ref.get("present"),
                "candidate": cand.get("present"),
                "candidate_reason": cand.get("reason") or cand.get("exception"),
            }

    executable_differences = {}
    for name in sorted(
        set(reference.get("executables", {})) | set(candidate.get("executables", {}))
    ):
        ref = reference.get("executables", {}).get(name, {})
        cand = candidate.get("executables", {}).get(name, {})
        if ref.get("path") != cand.get("path"):
            executable_differences[name] = {
                "reference": ref.get("path"),
                "candidate": cand.get("path"),
            }

    source_path_leaks = {
        name: entry
        for name, entry in candidate.get("source_inspection", {}).items()
        if any(
            marker in str(entry)
            for marker in ["/scratch/", "/project/", ".mesonpy-", "/tmp/"]
        )
    }

    return {
        "schema": "sagelite-runtime-manifest-diff-v1",
        "reference_label": reference.get("label"),
        "candidate_label": candidate.get("label"),
        "python": {
            "reference_executable": reference.get("python", {}).get("executable"),
            "candidate_executable": candidate.get("python", {}).get("executable"),
            "reference_prefix": reference.get("python", {}).get("prefix"),
            "candidate_prefix": candidate.get("python", {}).get("prefix"),
        },
        "missing_packages": missing_packages,
        "version_differences": version_differences,
        "feature_differences": feature_differences,
        "executable_differences": executable_differences,
        "candidate_dependency_leaks": _dependency_leaks(candidate),
        "candidate_source_path_leaks": source_path_leaks,
        "gap_package_program_differences": _gap_package_program_differences(
            reference, candidate
        ),
        "candidate_gap_host_leaks": _candidate_gap_host_leaks(candidate),
        "gap": {
            "reference_roots": reference.get("gap", {}).get("sage_env_gap_roots"),
            "candidate_roots": candidate.get("gap", {}).get("sage_env_gap_roots"),
        },
        "maxima": {
            "reference": reference.get("maxima", {}),
            "candidate": candidate.get("maxima", {}),
        },
        "fricas": {
            "reference": reference.get("fricas", {}),
            "candidate": candidate.get("fricas", {}),
        },
        "fplll": {
            "reference": reference.get("fplll", {}),
            "candidate": candidate.get("fplll", {}),
        },
    }


def render_diff_markdown(diff: dict[str, Any]) -> str:
    lines = [
        "# Sagelite runtime parity diff",
        "",
        f"- Reference: `{diff.get('reference_label')}`",
        f"- Candidate: `{diff.get('candidate_label')}`",
        f"- Reference Python: `{diff['python'].get('reference_executable')}`",
        f"- Candidate Python: `{diff['python'].get('candidate_executable')}`",
        "",
        "## Actionable buckets",
        "",
    ]
    buckets = [
        ("Missing packages", diff.get("missing_packages", [])),
        ("Package version differences", diff.get("version_differences", {})),
        ("Feature presence differences", diff.get("feature_differences", {})),
        ("Executable path differences", diff.get("executable_differences", {})),
        ("Candidate dependency leaks", diff.get("candidate_dependency_leaks", [])),
        ("Candidate source path leaks", diff.get("candidate_source_path_leaks", {})),
        (
            "GAP package program differences",
            diff.get("gap_package_program_differences", {}),
        ),
        ("Candidate GAP host path leaks", diff.get("candidate_gap_host_leaks", [])),
    ]
    for title, payload in buckets:
        count = len(payload)
        lines.extend([f"### {title}", "", f"Count: {count}", ""])
        if not payload:
            continue
        if isinstance(payload, dict):
            for key, value in list(payload.items())[:30]:
                lines.append(f"- `{key}`: `{json.dumps(value, default=_json_default)}`")
        else:
            for value in payload[:30]:
                lines.append(f"- `{json.dumps(value, default=_json_default)}`")
        if count > 30:
            lines.append(f"- ... {count - 30} more")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True, default=_json_default) + "\n",
        encoding="utf-8",
    )


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect = subparsers.add_parser("collect", help="collect a runtime manifest")
    collect.add_argument("--label", default="runtime")
    collect.add_argument("--output", type=Path, required=True)
    collect.add_argument(
        "--executable",
        action="append",
        default=list(DEFAULT_EXECUTABLES),
        help="external executable to probe; may be repeated",
    )
    collect.add_argument(
        "--inspect-module",
        action="append",
        default=list(SOURCE_INSPECTION_MODULES),
        help="module to inspect for source-path leakage; may be repeated",
    )
    collect.add_argument(
        "--compiled-limit",
        type=int,
        default=None,
        help="limit compiled module dependency probes for quick local tests",
    )
    collect.add_argument(
        "--feature-timeout",
        type=float,
        default=10.0,
        help="seconds allowed for each Sage feature probe; use 0 to disable",
    )

    compare = subparsers.add_parser("compare", help="compare two manifests")
    compare.add_argument("--reference", type=Path, required=True)
    compare.add_argument("--candidate", type=Path, required=True)
    compare.add_argument("--json-output", type=Path, required=True)
    compare.add_argument("--md-output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _make_parser().parse_args(argv)
    if args.command == "collect":
        manifest = collect_manifest(args)
        _write_json(args.output, manifest)
        print(args.output)
        return 0

    diff = compare_manifests(_load_json(args.reference), _load_json(args.candidate))
    _write_json(args.json_output, diff)
    args.md_output.parent.mkdir(parents=True, exist_ok=True)
    args.md_output.write_text(render_diff_markdown(diff), encoding="utf-8")
    print(args.json_output)
    print(args.md_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
