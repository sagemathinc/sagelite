from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAXIMA_LIB = ROOT / "src" / "sage" / "interfaces" / "maxima_lib.py"


def _maxima_path_helpers(optional_runtime_value):
    source = MAXIMA_LIB.read_text()
    start = source.index("def _maxima_library_prefix_is_usable")
    end = source.index("MAXIMA_FAS, MAXIMA_PREFIX = _configured_maxima_paths")
    namespace = {"os": os, "_optional_runtime_value": optional_runtime_value}
    exec(source[start:end], namespace)
    return namespace


def _maxima_require_helpers(optional_runtime_value, ecl_eval):
    source = MAXIMA_LIB.read_text()
    start = source.index("def _maxima_library_prefix_is_usable")
    end = source.index("# We begin here by initializing Maxima in library mode")
    namespace = {
        "os": os,
        "_optional_runtime_value": optional_runtime_value,
        "ecl_eval": ecl_eval,
        "MAXIMA_FAS": "",
        "MAXIMA_PREFIX": "",
    }
    exec(source[start:end], namespace)
    return namespace


def test_maxima_lib_uses_companion_library_path_for_stale_build_paths(tmp_path):
    fas = tmp_path / "runtime" / "lib" / "ecl-24.5.10" / "maxima.fas"
    library = tmp_path / "runtime" / "share" / "maxima" / "5.47.0"
    fas.parent.mkdir(parents=True)
    library.mkdir(parents=True)
    fas.write_text("maxima fas\n")
    (library / "src").mkdir()
    (library / "src" / "maxima-package.lisp").write_text("maxima package\n")

    def optional_runtime_value(module_name, attr_name):
        return {
            ("sagelite_maxima.runtime", "maxima_fas"): str(fas),
            ("sagelite_maxima.runtime", "maxima_library_path"): str(library),
        }.get((module_name, attr_name))

    helpers = _maxima_path_helpers(optional_runtime_value)

    assert helpers["_configured_maxima_paths"](
        str(tmp_path / "stale.fas"), str(tmp_path / "stale-prefix")
    ) == (str(fas), str(library))


def test_maxima_require_retries_companion_fas_after_plain_lookup_failure(tmp_path):
    fas = tmp_path / "runtime" / "lib" / "ecl-24.5.10" / "maxima.fas"
    fas.parent.mkdir(parents=True)
    fas.write_text("maxima fas\n")
    calls = []
    fallback_enabled = False

    def optional_runtime_value(module_name, attr_name):
        if (
            fallback_enabled
            and (module_name, attr_name) == ("sagelite_maxima.runtime", "maxima_fas")
        ):
            return str(fas)
        return None

    def ecl_eval(command):
        calls.append(command)
        if command == "(require 'maxima)":
            raise RuntimeError(
                "ECL says: Module error: Don't know how to REQUIRE MAXIMA."
            )

    helpers = _maxima_require_helpers(optional_runtime_value, ecl_eval)
    fallback_enabled = True

    helpers["_require_maxima"]()

    assert calls == [
        "(require 'maxima)",
        f"(require 'maxima \"{fas}\")",
    ]


def test_maxima_lib_resolves_companion_install_root_without_library_helper(tmp_path):
    fas = tmp_path / "runtime" / "lib" / "ecl-24.5.10" / "maxima.fas"
    install_root = tmp_path / "runtime"
    library = install_root / "share" / "maxima" / "5.47.0"
    fas.parent.mkdir(parents=True)
    library.mkdir(parents=True)
    fas.write_text("maxima fas\n")
    (library / "share").mkdir()
    (library / "share" / "builtins-list.txt").write_text("builtins\n")

    def optional_runtime_value(module_name, attr_name):
        return {
            ("sagelite_maxima.runtime", "maxima_fas"): str(fas),
            ("sagelite_maxima.runtime", "maxima_prefix"): str(install_root),
        }.get((module_name, attr_name))

    helpers = _maxima_path_helpers(optional_runtime_value)

    assert helpers["_configured_maxima_paths"](
        str(tmp_path / "stale.fas"), str(tmp_path / "stale-prefix")
    ) == (str(fas), str(library))
