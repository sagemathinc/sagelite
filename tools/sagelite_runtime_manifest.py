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
import importlib.util
import inspect
import json
import os
import platform
import re
import shutil
import site
import subprocess
import sys
import sysconfig
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TOOLS_DIR = Path(__file__).resolve().parent

DEFAULT_EXECUTABLES = [
    "4ti2",
    "benzene",
    "buckygen",
    "cddexec",
    "cddexec_gmp",
    "class.x",
    "circuits",
    "convert",
    "csdp",
    "cu2",
    "cubex",
    "cws.x",
    "dikcube",
    "directg",
    "dot",
    "dvipng",
    "ecm",
    "fdp",
    "flatter",
    "fricas",
    "frobby",
    "gap",
    "gap3",
    "genbg",
    "geng",
    "genktreeg",
    "genposetg",
    "gentourng",
    "gentreeg",
    "gfan",
    "gfan_bases",
    "gfan_groebnercone",
    "gfan_render",
    "giac",
    "glucose",
    "glucose-syrup",
    "graver",
    "groebner",
    "hilbert",
    "info",
    "integrate",
    "kissat",
    "latte-count",
    "latte-integrate",
    "lcalc",
    "lie",
    "lrs",
    "lrsnash",
    "magick",
    "markov",
    "maxima",
    "mcube",
    "msolve",
    "mwrank",
    "neato",
    "nef.x",
    "optimal",
    "palp",
    "pdftocairo",
    "pdf2svg",
    "planarity",
    "plantri",
    "points2allfinetriang",
    "points2allfinetriangs",
    "points2alltriangs",
    "points2finetriang",
    "points2finetriangs",
    "points2placingtriang",
    "points2placingtriangs",
    "points2triang",
    "points2triangs",
    "poly.x",
    "ppi",
    "qepcad",
    "qsolve",
    "rays",
    "rubiks",
    "singular",
    "size222",
    "sympow",
    "tachyon",
    "theta",
    "count",
    "twopi",
    "zsolve",
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
    "FRICAS_PREFIX",
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

HOST_EXECUTABLE_PREFIXES = (
    "/bin/",
    "/sbin/",
    "/usr/bin/",
    "/usr/sbin/",
    "/usr/local/bin/",
    "/usr/local/sbin/",
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


def _run_python_probe(code: str, timeout: float | None) -> dict[str, Any]:
    result = _run_probe([sys.executable, "-c", code], timeout=timeout)
    return {
        "command": result.command,
        "returncode": result.returncode,
        "stdout": _short_text(result.stdout),
        "stderr": _short_text(result.stderr),
        "error": result.error,
    }


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
        "cwd": os.getcwd(),
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
        "platform_tags": collect_platform_tags(),
    }


def collect_platform_tags(limit: int = 50) -> dict[str, Any]:
    tags: dict[str, Any] = {
        "sysconfig_platform": sysconfig.get_platform(),
        "tags": [],
    }
    try:
        packaging_tags = importlib.import_module("packaging.tags")
        tags["tags"] = [
            str(tag)
            for index, tag in enumerate(packaging_tags.sys_tags())
            if index < limit
        ]
    except Exception as exc:  # noqa: BLE001 - packaging may be unavailable
        tags["error"] = f"{type(exc).__name__}: {exc}"
    return tags


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


def _normalize_distribution_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def collect_installed_sagelite_console_scripts() -> list[str]:
    """
    Return console scripts contributed by installed sagelite distributions.

    The static executable list covers the high-value parity probes from the
    plan. Installed companion wheels can expose many more script names, so
    discover them from package metadata when the manifest runs in a fresh venv.
    """
    scripts = set()
    for dist in importlib.metadata.distributions():
        raw_name = dist.metadata.get("Name") or dist.name
        normalized = _normalize_distribution_name(raw_name)
        if normalized != "sagelite" and not normalized.startswith("sagelite-"):
            continue
        for entry_point in dist.entry_points:
            if entry_point.group == "console_scripts":
                scripts.add(entry_point.name)
    return sorted(scripts)


def collect_default_executables() -> list[str]:
    return sorted(
        set(DEFAULT_EXECUTABLES) | set(collect_installed_sagelite_console_scripts())
    )


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


def _feature_presence_probe(name: str, timeout: float | None) -> dict[str, Any]:
    code = f"""
import json
from sage.features.all import all_features

for feature in sorted(all_features(), key=lambda item: item.name):
    if feature.name != {name!r}:
        continue
    present = feature.is_present()
    print(json.dumps({{
        "present": bool(present),
        "reason": getattr(present, "reason", None),
        "resolution": getattr(present, "resolution", None),
    }}))
    break
else:
    raise RuntimeError("feature not found: {name}")
"""
    probe = _run_python_probe(code, timeout)
    entry: dict[str, Any] = {
        "probe_returncode": probe["returncode"],
        "probe_stderr": probe["stderr"],
        "probe_error": probe["error"],
    }
    if probe["returncode"] != 0:
        entry.update(
            {
                "present": None,
                "exception": (
                    "FeatureProbeError: feature presence subprocess failed "
                    f"with return code {probe['returncode']}"
                ),
            }
        )
        if probe["stdout"]:
            entry["probe_stdout"] = probe["stdout"]
        return entry

    try:
        payload = json.loads(probe["stdout"].splitlines()[-1])
    except (IndexError, json.JSONDecodeError) as exc:
        entry.update(
            {
                "present": None,
                "exception": f"FeatureProbeError: invalid probe output: {exc}",
                "probe_stdout": probe["stdout"],
            }
        )
        return entry
    entry.update(payload)
    return entry


def collect_features(timeout: float | None = 10.0) -> dict[str, Any]:
    if not timeout:
        return {"skipped": "feature collection disabled"}

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
        entry.update(_feature_presence_probe(feature.name, timeout))
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
        entry: dict[str, Any] = {
            "path": path,
            "host_path": _is_host_executable_path(path),
        }
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
    roots_for_programs = details["sage_env_gap_roots"]
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
        for key in [
            "FRICAS",
            "FRICAS_COMMAND",
            "FRICAS_INITFILE",
            "FRICAS_PREFIX",
            "ALDORROOT",
            "ECLDIR",
        ]
        if os.environ.get(key) is not None
    }
    details["executable"] = shutil.which(
        os.environ.get("FRICAS_COMMAND") or os.environ.get("FRICAS") or "fricas"
    )
    try:
        runtime = importlib.import_module("sagelite_fricas.runtime")
        for attr in ["fricas_prefix", "library_dir", "share_dir", "initfile_path"]:
            details[f"companion_{attr}"] = _safe_call(
                f"sagelite_fricas.runtime.{attr}", getattr(runtime, attr)
            )
    except Exception as exc:  # noqa: BLE001
        details["companion_error"] = f"{type(exc).__name__}: {exc}"
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
        sage_env = importlib.import_module("sage.env")
        bootstrap = getattr(sage_env, "_bootstrap_sagelite_fplll_data_runtime", None)
        if callable(bootstrap):
            bootstrap()
    except Exception as exc:  # noqa: BLE001
        sage_env = None
        details["sage_env_error"] = f"{type(exc).__name__}: {exc}"
    try:
        runtime = importlib.import_module("sagelite_fplll_data.runtime")
        companion_strategy = _safe_call(
            "sagelite_fplll_data.runtime.default_strategy",
            runtime.default_strategy,
        )
        if isinstance(companion_strategy, (str, os.PathLike)):
            companion_strategy = os.fspath(companion_strategy)
        details["companion_default_strategy"] = companion_strategy
        details["companion_default_strategy_exists"] = (
            os.path.isfile(companion_strategy)
            if isinstance(companion_strategy, str)
            else False
        )
    except Exception as exc:  # noqa: BLE001
        details["companion_error"] = f"{type(exc).__name__}: {exc}"
    try:
        fpylll = importlib.import_module("fpylll")
        config = importlib.import_module("fpylll.config")
        details["fpylll_version"] = getattr(fpylll, "__version__", None)
        for key in ["default_strategy", "default_strategy_path"]:
            details[f"fpylll_config_{key}"] = getattr(config, key, None)
        try:
            if sage_env is None:
                sage_env = importlib.import_module("sage.env")
            resolved_strategy = sage_env._fplll_default_strategy_file(
                getattr(config, "default_strategy_path", ""),
                getattr(config, "default_strategy", "default.json"),
            )
            details["sage_resolved_default_strategy"] = resolved_strategy
            details["sage_resolved_default_strategy_exists"] = os.path.isfile(
                resolved_strategy
            )
        except Exception as exc:  # noqa: BLE001
            details["sage_resolved_default_strategy_error"] = (
                f"{type(exc).__name__}: {exc}"
            )
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
            remainder = remainder.strip()
            if remainder.startswith("not found"):
                resolved = "not found"
            else:
                resolved = remainder.split(" ", 1)[0]
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
    if not path or path == "statically":
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


SOURCE_INSPECTION_LEAK_FIELDS = (
    "inspect_getsourcefile",
    "sage_getfile_relative",
    "sage_getfile_relative_error",
)
ABSOLUTE_PATH_RE = re.compile(r"/[^\s:'\"`]+")


def _absolute_paths_in_text(value: str) -> list[Path]:
    paths = []
    for match in ABSOLUTE_PATH_RE.finditer(value):
        raw_path = match.group(0).rstrip(".,;)]}")
        try:
            paths.append(Path(raw_path).resolve())
        except OSError:
            paths.append(Path(raw_path).absolute())
    return paths


def _source_inspection_path_leak(entry: Any, allowed_roots: list[Path]) -> bool:
    if not isinstance(entry, dict):
        return False
    values = [entry.get(field) for field in SOURCE_INSPECTION_LEAK_FIELDS]
    if "error" in entry:
        values.append(entry.get("error"))
    for value in values:
        if not isinstance(value, str):
            continue
        if not any(
            marker in value
            for marker in ["/scratch/", "/project/", ".mesonpy-", "/tmp/"]
        ):
            continue
        paths = _absolute_paths_in_text(value)
        if paths and all(
            any(_path_is_under(path, root) for root in allowed_roots)
            for path in paths
        ):
            continue
        return True
    return False


def _manifest_python_roots(manifest: dict[str, Any]) -> list[Path]:
    python = manifest.get("python", {})
    if not isinstance(python, dict):
        return []
    return [
        Path(value).resolve()
        for value in [python.get("prefix"), python.get("exec_prefix")]
        if isinstance(value, str) and value
    ]


def _load_native_catalog() -> dict[str, list[str]]:
    catalog_path = TOOLS_DIR / "sagelite_native_wheel_catalog.py"
    try:
        spec = importlib.util.spec_from_file_location(
            "sagelite_native_wheel_catalog", catalog_path
        )
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load spec for {catalog_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.catalog()
    except Exception as exc:  # noqa: BLE001 - manifest should report the issue
        return {"error": [f"{type(exc).__name__}: {exc}"]}


def collect_required_native_import_smokes(timeout: float) -> dict[str, Any]:
    catalog = _load_native_catalog()
    if "error" in catalog:
        return {"catalog_error": catalog["error"][0], "modules": {}}

    results = {}
    module_names = catalog.get(
        "required_native_smoke_import_modules",
        catalog["required_native_import_modules"],
    )
    for module_name in module_names:
        code = f"""
import importlib
import json
module = importlib.import_module({module_name!r})
print(json.dumps({{
    "module": {module_name!r},
    "file": getattr(module, "__file__", None),
    "package": getattr(module, "__package__", None),
}}))
"""
        probe = _run_python_probe(code, timeout)
        entry: dict[str, Any] = {
            "present": probe["returncode"] == 0,
            "returncode": probe["returncode"],
            "stderr": probe["stderr"],
            "error": probe["error"],
        }
        if probe["stdout"]:
            try:
                entry.update(json.loads(probe["stdout"].splitlines()[-1]))
            except json.JSONDecodeError:
                entry["stdout"] = probe["stdout"]
        results[module_name] = entry
    return {"modules": results}


def collect_runtime_smoke_tests(timeout: float | None = 10.0) -> dict[str, Any]:
    if not timeout:
        return {"skipped": "smoke timeout disabled"}

    smoke_tests = {
        "required_native_imports": collect_required_native_import_smokes(timeout),
        "gap_guava": _run_python_probe(
            """
import os
from pathlib import Path
from sage.libs.gap.libgap import libgap
from sage.coding.linear_code import LinearCode
from sage.matrix.constructor import matrix
from sage.rings.finite_rings.finite_field_constructor import GF
loaded = libgap.LoadPackage("guava")
program_dirs = libgap.eval('DirectoriesPackagePrograms("guava")')
program_dir_paths = [Path(str(path).strip('"')) for path in program_dirs]
wtdist_paths = [path / "wtdist" for path in program_dir_paths]
wtdist_executable = any(path.is_file() and os.access(path, os.X_OK) for path in wtdist_paths)
code = LinearCode(matrix(GF(2), [[1, 0, 1], [0, 1, 1]]))
weight_distribution = code.weight_distribution(algorithm="leon")
result = {
    "loaded": bool(loaded),
    "program_dirs": str(program_dirs),
    "wtdist_paths": [str(path) for path in wtdist_paths],
    "wtdist_executable": wtdist_executable,
    "weight_distribution": weight_distribution,
}
print(result)
if not loaded or not wtdist_executable or weight_distribution != [1, 0, 3, 0]:
    raise SystemExit(1)
""",
            timeout,
        ),
        "cypari2_private_pari": _run_python_probe(
            """
import importlib.util
import json
from pathlib import Path

spec = importlib.util.find_spec("cypari2")
if spec is None or spec.origin is None:
    print(json.dumps({"cypari2": "not importable", "private_pari": []}))
    raise SystemExit(1)

package_dir = Path(spec.origin).parent
private_lib_dir = package_dir.parent / "cypari2.libs"
private_pari = sorted(path.name for path in private_lib_dir.glob("libpari*"))
print(json.dumps({
    "cypari2_origin": spec.origin,
    "private_lib_dir": str(private_lib_dir),
    "private_pari": private_pari,
}))
if private_pari:
    raise SystemExit(1)
""",
            timeout,
        ),
        "fplll_strategy_data": _run_python_probe(
            """
import json
from pathlib import Path

from fpylll import config
from sage import env as sage_env

bootstrap = getattr(sage_env, "_bootstrap_sagelite_fplll_data_runtime", None)
if callable(bootstrap):
    bootstrap()

default_strategy_path = getattr(config, "default_strategy_path", "")
default_strategy = getattr(config, "default_strategy", "default.json")
resolver = getattr(sage_env, "_fplll_default_strategy_file", None)
if callable(resolver):
    resolved_strategy = resolver(default_strategy_path, default_strategy)
else:
    candidate = Path(default_strategy)
    resolved_strategy = (
        candidate
        if candidate.is_absolute()
        else Path(default_strategy_path) / candidate
    )

resolved_path = Path(resolved_strategy)
result = {
    "default_strategy_path": str(default_strategy_path),
    "default_strategy": str(default_strategy),
    "resolved_strategy": str(resolved_path),
    "resolved_strategy_exists": resolved_path.is_file(),
}
print(json.dumps(result))
if not resolved_path.is_file() or str(resolved_path).startswith("/project/local/"):
    raise SystemExit(1)
""",
            timeout,
        ),
        "maxima_help": _run_python_probe(
            """
from sage.interfaces.maxima import maxima
text = maxima.help("gcd")
print(str(text)[:200])
""",
            timeout,
        ),
        "maxima_example_arrays": _run_python_probe(
            """
from sage.interfaces.maxima_lib import maxima
text = str(maxima.example("arrays"))
print(text[:200])
if "a[n]:=n*a[n-1]" not in text:
    raise SystemExit(1)
""",
            timeout,
        ),
        "maxima_lib_sr_integral": _run_python_probe(
            """
from sage.all import RR, cos, sin, var
from sage.interfaces.maxima_lib import maxima_lib
x = var("x", domain=RR)
value = maxima_lib.sr_integral(sin(x), x)._sage_()
print(value)
if value != -cos(x):
    raise SystemExit(1)
""",
            timeout,
        ),
        "msolve_variety": _run_python_probe(
            """
from sage.rings.rational_field import QQ
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing

R = PolynomialRing(QQ, ("x", "y"))
x, y = R.gens()
values = R.ideal([x**2 - 1, y**2 - 1]).variety(
    QQ, algorithm="msolve", proof=False
)
normalized = sorted(
    tuple(sorted((str(variable), value) for variable, value in point.items()))
    for point in values
)
print(normalized)
expected = [
    (("x", -1), ("y", -1)),
    (("x", -1), ("y", 1)),
    (("x", 1), ("y", -1)),
    (("x", 1), ("y", 1)),
]
if normalized != expected:
    raise SystemExit(1)
""",
            timeout,
        ),
        "gap3_interface": _run_python_probe(
            """
from sage.interfaces.gap3 import Gap3
gap3 = Gap3()
try:
    output, error = gap3._execute_line("1+1;")
    values = gap3([1, 2, 3])
    indexed = values[2]
    latex = values._latex_()
    print({"output": output, "error": error, "indexed": str(indexed), "latex": latex})
    if error or str(indexed) != "2" or "1" not in latex:
        raise SystemExit(1)
finally:
    gap3.quit()
""",
            timeout,
        ),
        "fricas_factor_sage": _run_python_probe(
            """
from sage.interfaces.fricas import fricas
value = fricas("factor(x^2-1)").sage()
print(value)
""",
            timeout,
        ),
        "fricas_solve_sage": _run_python_probe(
            """
from sage.interfaces.fricas import fricas
value = str(fricas("solve(x^2 - 1=0,x)"))
print(value)
if "x = 1" not in value or "x = - 1" not in value:
    raise SystemExit(1)
""",
            timeout,
        ),
        "fricas_record_sage": _run_python_probe(
            """
from sage.calculus.var import function, var
from sage.interfaces.fricas import fricas
x = var("x")
y = function("y")(x)
value = fricas(y.diff(x) + y - 1).solve(y.operator(), x).sage()
print(value)
if value["particular"] != 1 or len(value["basis"]) != 1:
    raise SystemExit(1)
""",
            timeout,
        ),
    }
    return smoke_tests


def collect_manifest(args: argparse.Namespace) -> dict[str, Any]:
    executables = args.executable or collect_default_executables()
    return {
        "schema": "sagelite-runtime-manifest-v1",
        "label": args.label,
        "python": collect_python_info(),
        "sage": collect_sage_environment(),
        "packages": collect_installed_packages(),
        "features": collect_features(args.feature_timeout),
        "executables": collect_executables(executables),
        "gap": collect_gap_details(),
        "maxima": collect_maxima_details(),
        "fricas": collect_fricas_details(),
        "fplll": collect_fplll_details(),
        "compiled_modules": collect_compiled_modules(args.compiled_limit),
        "source_inspection": collect_source_inspection(args.inspect_module),
        "smoke_tests": collect_runtime_smoke_tests(args.smoke_timeout),
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


def _feature_collection_error(manifest: dict[str, Any]) -> str | None:
    features = manifest.get("features", {})
    if isinstance(features, dict) and not isinstance(features.get("features"), list):
        error = features.get("error")
        if error:
            return str(error)
    return None


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


def _is_host_executable_path(path: str | None) -> bool:
    if not path:
        return False
    return path.startswith(HOST_EXECUTABLE_PREFIXES)


def _candidate_executable_host_leaks(candidate: dict[str, Any]) -> list[dict[str, str]]:
    leaks = []
    for name, details in sorted(candidate.get("executables", {}).items()):
        path = details.get("path") if isinstance(details, dict) else None
        if _is_host_executable_path(path):
            leaks.append({"name": name, "path": path})
    return leaks


def _path_is_under(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _candidate_python_path_leaks(candidate: dict[str, Any]) -> list[dict[str, str]]:
    python = candidate.get("python", {})
    prefixes = [
        Path(value).resolve()
        for value in [
            python.get("prefix"),
            python.get("exec_prefix"),
        ]
        if value
    ]
    entries = []
    for raw_path in python.get("path", []):
        if not raw_path:
            continue
        path = Path(raw_path)
        try:
            resolved = path.resolve()
        except OSError:
            resolved = path.absolute()
        if any(_path_is_under(resolved, prefix) for prefix in prefixes):
            continue

        text = str(resolved)
        reasons = []
        if ".mesonpy-" in text:
            reasons.append("meson build tree")
        if text.startswith(("/project/", "/tmp/")):
            reasons.append("temporary or project build tree")
        if "/src" in text and (resolved / "sage").exists():
            reasons.append("source-tree sage package")

        if reasons:
            entries.append({"path": raw_path, "reason": ", ".join(reasons)})
    return entries


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


RUNTIME_SECTION_COMPARE_KEYS = {
    "maxima": [
        "executable",
        "MAXIMA",
        "MAXIMA_PREFIX",
        "MAXIMA_USERDIR",
        "MAXIMA_FAS",
        "MAXIMA_IMAGESDIR",
        "MAXIMA_LAYOUT_AUTOTOOLS",
        "ECLDIR",
        "sage_env_MAXIMA_FAS",
        "sage_env_MAXIMA_PREFIX",
    ],
    "fricas": [
        "executable",
        "FRICAS",
        "FRICAS_COMMAND",
        "FRICAS_INITFILE",
        "FRICAS_PREFIX",
        "companion_fricas_prefix",
        "companion_library_dir",
        "companion_share_dir",
        "companion_initfile_path",
        "ALDORROOT",
        "ECLDIR",
    ],
    "fplll": [
        "SAGE_FPLLL_DEFAULT_STRATEGY",
        "FPLLL_DEFAULT_STRATEGY",
        "companion_default_strategy",
        "companion_default_strategy_exists",
        "fpylll_version",
        "fpylll_config_default_strategy",
        "fpylll_config_default_strategy_path",
        "sage_resolved_default_strategy",
        "sage_resolved_default_strategy_exists",
    ],
}


def _runtime_section_differences(
    reference: dict[str, Any], candidate: dict[str, Any], section: str
) -> dict[str, Any]:
    ref_section = reference.get(section, {})
    cand_section = candidate.get(section, {})
    differences = {}
    for key in RUNTIME_SECTION_COMPARE_KEYS[section]:
        ref_value = ref_section.get(key)
        cand_value = cand_section.get(key)
        if ref_value != cand_value:
            differences[key] = {
                "reference": ref_value,
                "candidate": cand_value,
            }
    return differences


def _smoke_failures(manifest: dict[str, Any]) -> dict[str, Any]:
    smoke_tests = manifest.get("smoke_tests", {})
    failures = {}
    native = smoke_tests.get("required_native_imports", {})
    for module_name, result in native.get("modules", {}).items():
        if not result.get("present"):
            failures[f"required_native_imports.{module_name}"] = result
    for name, result in smoke_tests.items():
        if name == "required_native_imports":
            continue
        if isinstance(result, dict) and result.get("returncode") not in (None, 0):
            failures[name] = result
    return failures


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
    feature_collection_errors = {
        label: error
        for label, error in {
            "reference": _feature_collection_error(reference),
            "candidate": _feature_collection_error(candidate),
        }.items()
        if error
    }
    if feature_collection_errors:
        ref_features = {}
        cand_features = {}
    else:
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

    allowed_source_roots = _manifest_python_roots(candidate)
    source_path_leaks = {
        name: entry
        for name, entry in candidate.get("source_inspection", {}).items()
        if _source_inspection_path_leak(entry, allowed_source_roots)
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
        "feature_collection_errors": feature_collection_errors,
        "feature_differences": feature_differences,
        "executable_differences": executable_differences,
        "candidate_executable_host_leaks": _candidate_executable_host_leaks(
            candidate
        ),
        "candidate_python_path_leaks": _candidate_python_path_leaks(candidate),
        "candidate_dependency_leaks": _dependency_leaks(candidate),
        "candidate_source_path_leaks": source_path_leaks,
        "gap_package_program_differences": _gap_package_program_differences(
            reference, candidate
        ),
        "candidate_gap_host_leaks": _candidate_gap_host_leaks(candidate),
        "maxima_differences": _runtime_section_differences(
            reference, candidate, "maxima"
        ),
        "fricas_differences": _runtime_section_differences(
            reference, candidate, "fricas"
        ),
        "fplll_differences": _runtime_section_differences(
            reference, candidate, "fplll"
        ),
        "candidate_smoke_failures": _smoke_failures(candidate),
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
        ("Feature collection issues", diff.get("feature_collection_errors", {})),
        ("Feature presence differences", diff.get("feature_differences", {})),
        ("Executable path differences", diff.get("executable_differences", {})),
        (
            "Candidate executable host path leaks",
            diff.get("candidate_executable_host_leaks", []),
        ),
        ("Candidate Python path leaks", diff.get("candidate_python_path_leaks", [])),
        ("Candidate dependency leaks", diff.get("candidate_dependency_leaks", [])),
        ("Candidate source path leaks", diff.get("candidate_source_path_leaks", {})),
        (
            "GAP package program differences",
            diff.get("gap_package_program_differences", {}),
        ),
        ("Candidate GAP host path leaks", diff.get("candidate_gap_host_leaks", [])),
        ("Maxima runtime differences", diff.get("maxima_differences", {})),
        ("FriCAS runtime differences", diff.get("fricas_differences", {})),
        ("FPLLL runtime differences", diff.get("fplll_differences", {})),
        ("Candidate smoke test failures", diff.get("candidate_smoke_failures", {})),
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
        default=None,
        help=(
            "external executable to probe; may be repeated. By default, probes "
            "the built-in parity list plus installed sagelite companion scripts."
        ),
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
    collect.add_argument(
        "--smoke-timeout",
        type=float,
        default=10.0,
        help="seconds allowed for each runtime smoke probe; use 0 to skip",
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
