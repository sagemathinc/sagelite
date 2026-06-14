r"""
Sage Runtime Environment

AUTHORS:

- \R. Andrew Ohana (2012): initial version
"""

# ****************************************************************************
#       Copyright (C) 2013 R. Andrew Ohana <andrew.ohana@gmail.com>
#       Copyright (C) 2019 Jeroen Demeyer <J.Demeyer@UGent.be>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

import importlib.metadata as importlib_metadata
import os
import shutil
import socket
import subprocess
import sys
import sysconfig
from importlib import import_module
from os import PathLike
from typing import Optional

from platformdirs import site_data_dir, user_data_dir

import sage.config
from sage import version
from sage.config import get_include_dirs

# All variables set by var() appear in this SAGE_ENV dict
SAGE_ENV = dict()


def join(*args) -> str | None:
    """
    Join paths like ``os.path.join`` except that the result is ``None``
    if any of the components is ``None``.

    EXAMPLES::

        sage: from sage.env import join
        sage: print(join("hello", "world"))
        hello/world
        sage: print(join("hello", None))
        None
    """
    if any(a is None for a in args):
        return None
    return os.path.join(*args)


def _optional_runtime_value(module_name: str, attr_name: str) -> Optional[str]:
    """
    Return an optional runtime path from a companion package.

    Any import or runtime failure is treated as "runtime unavailable" so that
    optional companion packages do not become hard dependencies of ``sagelib``.
    """
    try:
        module = import_module(module_name)
    except ImportError:
        return None

    getter = getattr(module, attr_name, None)
    if getter is None:
        return None

    try:
        value = getter() if callable(getter) else getter
    except Exception:
        return None

    if not value:
        return None
    return os.fspath(value)


def _prepend_env_path(name: str, path: Optional[str]) -> None:
    """
    Prepend ``path`` to an environment variable containing search paths.
    """
    if not path:
        return
    path = os.fspath(path)
    current = os.environ.get(name)
    paths = current.split(os.pathsep) if current else []
    if path in paths:
        return
    os.environ[name] = path if not current else os.pathsep.join([path, current])


def _bootstrap_sagelite_maxima_runtime() -> None:
    """
    Seed Maxima runtime variables from an optional ``sagelite_maxima`` package.

    This is only used when the user or the build configuration has not already
    provided usable Maxima paths.  Binary wheels can contain build-time Maxima
    paths that no longer exist after installation; those stale paths should not
    prevent a companion runtime from being used.
    """
    configured_prefix = getattr(sage.config, "MAXIMA_PREFIX", None)
    configured_fas = getattr(sage.config, "MAXIMA_FAS", None)
    configured_command = getattr(sage.config, "MAXIMA", None)

    needs_prefix = (
        not os.environ.get("MAXIMA_PREFIX")
        and not (configured_prefix and os.path.isdir(os.fspath(configured_prefix)))
    )
    needs_fas = (
        not os.environ.get("MAXIMA_FAS")
        and not (configured_fas and os.path.isfile(os.fspath(configured_fas)))
    )
    needs_command = (
        not os.environ.get("MAXIMA")
        and not (
            configured_command
            and os.path.isfile(os.fspath(configured_command))
            and os.access(os.fspath(configured_command), os.X_OK)
        )
    )
    needs_ecldir = not _ecldir_contains_maxima(os.environ.get("ECLDIR"))
    needs_layout = not os.environ.get("MAXIMA_LAYOUT_AUTOTOOLS")
    needs_imagesdir = not os.environ.get("MAXIMA_IMAGESDIR")
    runtime_library_dir = _optional_runtime_value(
        "sagelite_maxima.runtime", "runtime_library_dir"
    )
    _prepend_env_path("LD_LIBRARY_PATH", runtime_library_dir)

    if not (
        needs_prefix
        or needs_fas
        or needs_command
        or needs_ecldir
        or needs_layout
        or needs_imagesdir
    ):
        return

    prefix = fas = command = ecldir = layout = imagesdir = None
    if needs_prefix:
        prefix = _optional_runtime_value("sagelite_maxima.runtime", "maxima_prefix")
    if needs_fas:
        fas = _optional_runtime_value("sagelite_maxima.runtime", "maxima_fas")
    if needs_command:
        command = _optional_runtime_value("sagelite_maxima.runtime", "maxima_command")
    if needs_ecldir:
        ecldir = _optional_runtime_value("sagelite_maxima.runtime", "ecl_dir")
    if needs_layout:
        layout = _optional_runtime_value(
            "sagelite_maxima.runtime", "maxima_layout_autotools"
        )
    if needs_imagesdir:
        imagesdir = _optional_runtime_value(
            "sagelite_maxima.runtime", "maxima_imagesdir"
        )

    if needs_prefix and prefix and os.path.isdir(prefix):
        os.environ.setdefault("MAXIMA_PREFIX", os.fspath(prefix))
    if needs_fas and fas and os.path.isfile(fas):
        os.environ.setdefault("MAXIMA_FAS", os.fspath(fas))
    if (
        needs_command
        and command
        and os.path.isfile(command)
        and os.access(command, os.X_OK)
    ):
        os.environ.setdefault("MAXIMA", os.fspath(command))
    if needs_ecldir and ecldir and os.path.isdir(ecldir):
        os.environ["ECLDIR"] = os.fspath(ecldir)
    if needs_layout and layout:
        os.environ.setdefault("MAXIMA_LAYOUT_AUTOTOOLS", os.fspath(layout))
    if needs_imagesdir and imagesdir and os.path.isdir(imagesdir):
        os.environ.setdefault("MAXIMA_IMAGESDIR", os.fspath(imagesdir))


def _bootstrap_sagelite_kenzo_runtime() -> None:
    """
    Seed Kenzo runtime variables from an optional ``sagelite_kenzo`` package.

    Binary ``sagelite`` wheels can contain a build-prefix ``KENZO_FAS`` path
    that does not exist after installation.  A companion package can provide a
    relocatable ECL image without making Kenzo a hard dependency.
    """
    configured_fas = getattr(sage.config, "KENZO_FAS", None)
    needs_fas = (
        not os.environ.get("KENZO_FAS")
        and not (configured_fas and os.path.isfile(os.fspath(configured_fas)))
    )
    if not needs_fas:
        return

    fas = _optional_runtime_value("sagelite_kenzo.runtime", "kenzo_fas")
    if fas and os.path.isfile(fas):
        os.environ.setdefault("KENZO_FAS", os.fspath(fas))


def _ecldir_contains_maxima(ecldir: str | os.PathLike | None) -> bool:
    """
    Return whether ``ecldir`` can satisfy ECL's plain ``(require 'maxima)``.
    """
    return bool(ecldir) and os.path.isfile(os.path.join(ecldir, "maxima.asd"))


def _bootstrap_sagelite_ecl_runtime() -> None:
    """
    Seed ECL runtime variables from an optional ``sagelite_ecl`` package.

    Installed ``sagelite`` wheels can contain build-prefix ``ECL_CONFIG``
    values.  A companion package can provide relocatable ECL headers,
    libraries, support files, and ``ecl-config`` without making ECL a hard
    dependency of sagelib.
    """
    configured_command = getattr(sage.config, "ECL_CONFIG", None)
    needs_command = (
        not os.environ.get("ECL_CONFIG")
        and not (
            configured_command
            and os.path.isfile(os.fspath(configured_command))
            and os.access(os.fspath(configured_command), os.X_OK)
        )
    )
    needs_ecldir = not os.environ.get("ECLDIR")
    if not (needs_command or needs_ecldir):
        return

    command = ecldir = None
    if needs_command:
        command = _optional_runtime_value("sagelite_ecl.runtime", "ecl_config_command")
    if needs_ecldir:
        ecldir = _optional_runtime_value("sagelite_ecl.runtime", "ecl_dir")

    if (
        needs_command
        and command
        and os.path.isfile(command)
        and os.access(command, os.X_OK)
    ):
        os.environ.setdefault("ECL_CONFIG", os.fspath(command))
    if needs_ecldir and ecldir and os.path.isdir(ecldir):
        os.environ.setdefault("ECLDIR", os.fspath(ecldir))


def _pari_data_dir_is_usable(path: str | os.PathLike | None) -> bool:
    """
    Return whether ``path`` looks like a usable PARI optional-data directory.
    """
    if not path:
        return False

    root = os.fspath(path)
    return os.path.isdir(root) and any(
        os.path.isdir(os.path.join(root, name))
        for name in ("galdata", "elldata", "seadata", "galpol", "nftables")
    )


def _bootstrap_sagelite_pari_data_runtime() -> None:
    """
    Seed ``GP_DATA_DIR`` from an optional ``sagelite_pari_data`` package.

    PARI reads optional data such as Galois group tables through its data
    directory.  Installed ``sagelite`` wheels can supply those files through a
    companion wheel without making the data a hard dependency of sagelib.
    """
    if os.environ.get("GP_DATA_DIR"):
        return

    data_dir = _optional_runtime_value("sagelite_pari_data.runtime", "pari_data_dir")
    if _pari_data_dir_is_usable(data_dir):
        os.environ.setdefault("GP_DATA_DIR", os.fspath(data_dir))


def _optional_runtime_data_dir(
    module_name: str,
    attr_name: str,
    marker: str,
    *,
    path_is_file: bool = False,
) -> Optional[str]:
    """
    Return a usable data directory from a companion package.

    ``attr_name`` may point either at the directory itself or, with
    ``path_is_file=True``, at a marker file inside the desired directory.
    """
    path = _optional_runtime_value(module_name, attr_name)
    if not path:
        return None

    directory = os.path.dirname(path) if path_is_file else path
    if os.path.exists(os.path.join(directory, marker)):
        return os.fspath(directory)
    return None


def _fplll_default_strategy_file(default_strategy_path, default_strategy) -> str:
    """
    Return a usable FPLLL default BKZ strategy file.

    Some binary ``fpylll`` wheels expose an absolute build-prefix
    ``BKZ.DEFAULT_STRATEGY``.  When that file is stale, prefer the optional
    ``sagelite-fplll-data`` companion package.
    """
    strategy = os.path.normpath(
        os.path.join(
            os.fsdecode(default_strategy_path),
            os.path.basename(os.fsdecode(default_strategy)),
        )
    )
    if os.path.isfile(strategy):
        return strategy

    bundled_strategy = _optional_runtime_value(
        "sagelite_fplll_data.runtime", "default_strategy"
    )
    if bundled_strategy and os.path.isfile(bundled_strategy):
        return bundled_strategy

    return strategy


def _gap_root_path_contains_gap(root: str | None) -> bool:
    """
    Return whether ``root`` looks like a usable GAP root directory.
    """
    return bool(root) and os.path.exists(os.path.join(root, "lib", "init.g"))


def _gap_root_path_contains_gap_packages(root: str | None) -> bool:
    """
    Return whether ``root`` looks like a usable GAP package root directory.
    """
    if not root:
        return False

    pkg = os.path.join(root, "pkg")
    if not os.path.isdir(pkg):
        return False

    try:
        package_names = os.listdir(pkg)
    except OSError:
        return False

    return any(
        os.path.exists(os.path.join(pkg, package_name, "PackageInfo.g"))
        for package_name in package_names
    )


def _entry_points(group: str):
    """
    Return package entry points in ``group`` across importlib.metadata APIs.
    """
    try:
        return importlib_metadata.entry_points(group=group)
    except TypeError:
        all_entry_points = importlib_metadata.entry_points()
        if hasattr(all_entry_points, "select"):
            return all_entry_points.select(group=group)
        return all_entry_points.get(group, ())


def _registered_gap_root_paths() -> list[str]:
    """
    Return GAP roots contributed by companion-package entry points.

    Optional GAP package wheels can register an entry point in the
    ``sagemath.gap_root_paths`` group.  Each entry point may return a single
    root, a semicolon-separated root string, or an iterable of roots.
    """
    roots = []
    for entry_point in _entry_points(group="sagemath.gap_root_paths"):
        try:
            value = entry_point.load()
            value = value() if callable(value) else value
        except Exception:
            continue

        if isinstance(value, (str, bytes, PathLike)):
            values = str(value).split(";")
        else:
            try:
                values = list(value)
            except TypeError:
                continue

        for root in values:
            root = os.fspath(root).strip()
            if root:
                roots.append(root)

    return roots


def _append_gap_root(core_roots: list[str], package_roots: list[str], root: str) -> None:
    """
    Add ``root`` to the right GAP root bucket if it looks usable.
    """
    root = root.strip()
    if not root:
        return

    if _gap_root_path_contains_gap(root):
        if root not in core_roots:
            core_roots.append(root)
    elif _gap_root_path_contains_gap_packages(root) and root not in package_roots:
        package_roots.append(root)


def _gap_root_paths() -> str:
    """
    Return GAP root paths, preferring an explicitly configured or companion
    package GAP runtime.

    Binary ``sagelite`` wheels bundle ``libgap`` but not the optional GAP
    runtime tree.  The tree can be supplied by setting ``GAP_ROOT_PATHS`` or
    by installing the ``sagelite-gap-runtime`` companion package.  Optional
    GAP package companion wheels can append package-only roots through the
    ``sagemath.gap_root_paths`` entry point group.
    """
    core_roots = []
    package_roots = []

    configured = os.environ.get("GAP_ROOT_PATHS") or ""
    for root in configured.split(";"):
        _append_gap_root(core_roots, package_roots, root)

    companion = _optional_runtime_value("sagelite_gap_runtime.runtime", "gap_root_paths")
    if companion:
        for root in companion.split(";"):
            _append_gap_root(core_roots, package_roots, root)

    for root in _registered_gap_root_paths():
        _append_gap_root(core_roots, package_roots, root)

    bundled = join(SAGE_EXTCODE, "gap_root")
    if bundled:
        _append_gap_root(core_roots, package_roots, bundled)

    configured = getattr(sage.config, "GAP_ROOT_PATHS", "")
    for root in configured.split(";"):
        _append_gap_root(core_roots, package_roots, root)

    if core_roots:
        return ";".join(core_roots + package_roots)

    return ""


def _installed_command_or_fallback(command: str | None, fallback: str) -> str:
    """
    Return ``command`` unless it is a stale absolute path.
    """
    if command and os.path.isabs(command) and not os.path.exists(command):
        return fallback
    return command or fallback


def _bootstrap_sagelite_gap_runtime() -> None:
    """
    Seed ``SAGE_GAP_COMMAND`` from an optional GAP runtime companion package.

    ``GAP_ROOT_PATHS`` is handled separately because it is needed by libgap at
    import time.  The command is for Sage's pexpect GAP interface, whose
    doctests still invoke a standalone ``gap`` executable.
    """
    if os.environ.get("SAGE_GAP_COMMAND"):
        return

    command = _optional_runtime_value("sagelite_gap_runtime.runtime", "gap_command")
    if command and os.path.isfile(command) and os.access(command, os.X_OK):
        os.environ.setdefault("SAGE_GAP_COMMAND", os.fspath(command))


def _bootstrap_sagelite_gap3_runtime() -> None:
    """
    Seed ``SAGE_GAP3_COMMAND`` from an optional GAP3 runtime companion package.

    Sage's GAP3 interface is pexpect-based and normally looks for ``gap3`` on
    ``PATH``.  The companion package supplies a relocatable startup script for
    installed wheels.
    """
    if os.environ.get("SAGE_GAP3_COMMAND"):
        return

    command = _optional_runtime_value("sagelite_gap3.runtime", "gap3_command")
    if command and os.path.isfile(command) and os.access(command, os.X_OK):
        os.environ.setdefault("SAGE_GAP3_COMMAND", os.fspath(command))


def _bootstrap_sagelite_ecm_runtime() -> None:
    """
    Seed ``SAGE_ECMBIN`` from an optional ``sagelite_ecm`` package.

    Binary wheels can contain a build-time ``ecm`` path that no longer exists
    after installation.  The companion package supplies a relocatable
    executable and should be used when no environment override is already set.
    """
    configured = getattr(sage.config, "SAGE_ECMBIN", None)
    needs_command = (
        not os.environ.get("SAGE_ECMBIN")
        and not (
            configured
            and os.path.isfile(os.fspath(configured))
            and os.access(os.fspath(configured), os.X_OK)
        )
    )
    if not needs_command:
        return

    command = _optional_runtime_value("sagelite_ecm.runtime", "ecm_command")
    if command and os.path.isfile(command) and os.access(command, os.X_OK):
        os.environ.setdefault("SAGE_ECMBIN", os.fspath(command))


def _bootstrap_sagelite_mwrank_runtime() -> None:
    """
    Seed ``MWRANK`` from an optional ``sagelite_mwrank`` package.

    Sage mostly uses eclib's in-process mwrank library, but some doctests and
    interfaces still invoke Cremona's standalone ``mwrank`` executable.  The
    companion package supplies that executable for installed ``sagelite``
    wheels without requiring it as a core dependency.
    """
    configured = getattr(sage.config, "MWRANK", None)
    needs_command = (
        not os.environ.get("MWRANK")
        and not (
            configured
            and os.path.isfile(os.fspath(configured))
            and os.access(os.fspath(configured), os.X_OK)
        )
    )
    if not needs_command:
        return

    command = _optional_runtime_value("sagelite_mwrank.runtime", "mwrank_command")
    if command and os.path.isfile(command) and os.access(command, os.X_OK):
        os.environ.setdefault("MWRANK", os.fspath(command))


def _bootstrap_sagelite_sympow_runtime() -> None:
    """
    Seed ``SYMPOW`` from an optional ``sagelite_sympow`` package.

    Sage's symmetric-power L-function interface shells out to Watkins's
    standalone ``sympow`` executable.  The companion package supplies a
    relocatable command for installed ``sagelite`` wheels.
    """
    if os.environ.get("SYMPOW") or shutil.which("sympow"):
        return

    command = _optional_runtime_value("sagelite_sympow.runtime", "sympow_command")
    if command and os.path.isfile(command) and os.access(command, os.X_OK):
        os.environ.setdefault("SYMPOW", os.fspath(command))


def _bootstrap_sagelite_tachyon_runtime() -> None:
    """
    Seed ``TACHYON`` from an optional ``sagelite_tachyon`` package.

    Sage's Tachyon interface shells out to the standalone ray tracer.  The
    companion package supplies a relocatable executable copy for installed
    wheels.
    """
    if os.environ.get("TACHYON") or shutil.which("tachyon"):
        return

    command = _optional_runtime_value("sagelite_tachyon.runtime", "executable_path")
    if command and os.path.isfile(command) and os.access(command, os.X_OK):
        os.environ.setdefault("TACHYON", os.fspath(command))


def _bootstrap_sagelite_gfan_runtime() -> None:
    """
    Seed ``GFAN_BINS_PREFIX`` from an optional ``sagelite_gfan`` package.

    Sage's Groebner fan interface calls gfan command-line executables.  The
    companion package supplies relocatable executable wrappers for installed
    wheels.
    """
    configured = getattr(sage.config, "GFAN_BINS_PREFIX", None)
    needs_prefix = (
        not os.environ.get("GFAN_BINS_PREFIX")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "gfan"))
        )
    )
    if not needs_prefix:
        return

    prefix = _optional_runtime_value("sagelite_gfan.runtime", "bin_prefix")
    if prefix and os.path.isfile(os.path.join(prefix, "gfan")):
        os.environ.setdefault("GFAN_BINS_PREFIX", os.fspath(prefix))


def _bootstrap_sagelite_latte_runtime() -> None:
    """
    Seed ``LATTE_BINS_PREFIX`` from an optional ``sagelite_latte`` package.

    Sage's LattE interface calls the standalone ``count`` and ``integrate``
    executables.  The companion package supplies relocatable executable copies
    for installed wheels.
    """
    configured = getattr(sage.config, "LATTE_BINS_PREFIX", None)
    needs_prefix = (
        not os.environ.get("LATTE_BINS_PREFIX")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "count"))
            and os.path.isfile(os.path.join(os.fspath(configured), "integrate"))
        )
    )
    if not needs_prefix:
        return

    prefix = _optional_runtime_value("sagelite_latte.runtime", "bin_prefix")
    if (
        prefix
        and os.path.isfile(os.path.join(prefix, "count"))
        and os.path.isfile(os.path.join(prefix, "integrate"))
    ):
        os.environ.setdefault("LATTE_BINS_PREFIX", os.fspath(prefix))


def _bootstrap_sagelite_singular_runtime() -> None:
    """
    Seed Singular data-root variables from an optional companion package.

    Binary ``sagelite`` wheels link against libSingular, but Singular's
    library files can live outside the wheel.  The companion package supplies
    that tree without making it a hard dependency.
    """
    root = _optional_runtime_value(
        "sagelite_singular_runtime.runtime", "singular_root_dir"
    )
    default_dir = _optional_runtime_value(
        "sagelite_singular_runtime.runtime", "singular_default_dir"
    )

    if root and os.path.isdir(os.path.join(root, "share", "singular", "LIB")):
        os.environ.setdefault("SINGULAR_ROOT_DIR", os.fspath(root))
    if default_dir and os.path.isdir(os.path.join(default_dir, "LIB")):
        os.environ.setdefault("SINGULAR_DEFAULT_DIR", os.fspath(default_dir))


def _bootstrap_sagelite_info_runtime() -> None:
    """
    Seed GNU Info paths from an optional companion package.

    Sage's Singular interface shells out to ``info`` to build generated
    docstrings.  The companion package supplies both the executable and the
    installed Info manuals for binary wheels.
    """
    info_dir = _optional_runtime_value("sagelite_info.runtime", "info_dir")
    command = _optional_runtime_value("sagelite_info.runtime", "executable_path")

    if info_dir and os.path.isfile(os.path.join(info_dir, "singular.info")):
        current = os.environ.get("INFOPATH")
        paths = current.split(os.pathsep) if current else []
        if os.fspath(info_dir) not in paths:
            os.environ["INFOPATH"] = (
                os.fspath(info_dir)
                if not current
                else os.fspath(info_dir) + os.pathsep + current
            )

    if command and os.path.isfile(command) and os.access(command, os.X_OK):
        bindir = os.path.dirname(os.fspath(command))
        current = os.environ.get("PATH", "")
        paths = current.split(os.pathsep) if current else []
        if bindir not in paths:
            os.environ["PATH"] = (
                bindir if not current else bindir + os.pathsep + current
            )


def _bootstrap_sagelite_meataxe_runtime() -> None:
    """
    Seed ``MTXLIB`` from an optional ``sagelite_meataxe`` package.

    Binary wheels can bundle the MeatAxe extension and shared library without
    Sage's generated finite-field multiplication tables.  The companion package
    supplies a relocatable table directory.
    """
    configured = getattr(sage.config, "MTXLIB", None) or join(SAGE_SHARE, "meataxe")
    needs_tables = (
        not os.environ.get("MTXLIB")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "p009.zzz"))
        )
    )
    if not needs_tables:
        return

    table_dir = _optional_runtime_value("sagelite_meataxe.runtime", "meataxe_dir")
    if table_dir and os.path.isfile(os.path.join(table_dir, "p009.zzz")):
        os.environ.setdefault("MTXLIB", os.fspath(table_dir))


def _bootstrap_sagelite_mathjax_runtime() -> None:
    """
    Seed ``MATHJAX_DIR`` from an optional ``sagelite_mathjax_runtime`` package.

    Sage's configured MathJax directory can point at a build prefix that does
    not exist in an installed wheel.  The companion package supplies the
    redistributable JavaScript runtime in a relocatable package-data tree.
    """
    configured = getattr(sage.config, "MATHJAX_DIR", None) or join(SAGE_SHARE, "mathjax")
    needs_runtime = (
        not os.environ.get("MATHJAX_DIR")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "tex-chtml.js"))
        )
    )
    if not needs_runtime:
        return

    mathjax_dir = _optional_runtime_value("sagelite_mathjax_runtime", "mathjax_dir")
    if mathjax_dir and os.path.isfile(os.path.join(mathjax_dir, "tex-chtml.js")):
        os.environ.setdefault("MATHJAX_DIR", os.fspath(mathjax_dir))


def _bootstrap_sagelite_nauty_runtime() -> None:
    """
    Seed ``SAGE_NAUTY_BINS_PREFIX`` from an optional ``sagelite_nauty`` package.

    Sage's nauty interfaces call several standalone graph-generation
    executables.  The companion package supplies relocatable copies for
    installed wheels.
    """
    configured = getattr(sage.config, "SAGE_NAUTY_BINS_PREFIX", None)
    needs_prefix = (
        not os.environ.get("SAGE_NAUTY_BINS_PREFIX")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "geng"))
        )
    )
    if not needs_prefix:
        return

    prefix = _optional_runtime_value("sagelite_nauty.runtime", "bin_prefix")
    if prefix and os.path.isfile(os.path.join(prefix, "geng")):
        os.environ.setdefault("SAGE_NAUTY_BINS_PREFIX", os.fspath(prefix))


def _bootstrap_sagelite_rubiks_runtime() -> None:
    """
    Seed ``RUBIKS_BINS_PREFIX`` from an optional ``sagelite_rubiks`` package.
    """
    configured = getattr(sage.config, "RUBIKS_BINS_PREFIX", None)
    needs_prefix = (
        not os.environ.get("RUBIKS_BINS_PREFIX")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "cubex"))
        )
    )
    if not needs_prefix:
        return

    prefix = _optional_runtime_value("sagelite_rubiks.runtime", "bin_prefix")
    if prefix and os.path.isfile(os.path.join(prefix, "cubex")):
        os.environ.setdefault("RUBIKS_BINS_PREFIX", os.fspath(prefix))


def _bootstrap_sagelite_palp_runtime() -> None:
    """
    Seed ``PALP_BINS_PREFIX`` from an optional ``sagelite_palp`` package.

    Sage calls PALP's standalone executables for lattice-polytope features.
    The companion package supplies relocatable executable copies for installed
    wheels.
    """
    configured = getattr(sage.config, "PALP_BINS_PREFIX", None)
    needs_prefix = (
        not os.environ.get("PALP_BINS_PREFIX")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "poly.x"))
        )
    )
    if not needs_prefix:
        return

    prefix = _optional_runtime_value("sagelite_palp.runtime", "bin_prefix")
    if prefix and os.path.isfile(os.path.join(prefix, "poly.x")):
        os.environ.setdefault("PALP_BINS_PREFIX", os.fspath(prefix))


def _bootstrap_sagelite_four_ti_2_runtime() -> None:
    """
    Seed 4ti2 executable variables from an optional companion package.

    Sage's 4ti2 interface looks up individual ``FOURTITWO_*`` variables before
    falling back to commands on ``PATH``.  The companion package supplies
    relocatable executable copies for installed wheels.
    """
    for program in (
        "hilbert",
        "markov",
        "graver",
        "zsolve",
        "qsolve",
        "rays",
        "ppi",
        "circuits",
        "groebner",
    ):
        variable = f"FOURTITWO_{program.upper()}"
        configured = getattr(sage.config, variable, None)
        needs_command = (
            not os.environ.get(variable)
            and not (
                configured
                and os.path.isfile(os.fspath(configured))
                and os.access(os.fspath(configured), os.X_OK)
            )
        )
        if not needs_command:
            continue

        command = _optional_runtime_value(
            "sagelite_four_ti_2.runtime", f"{program}_command"
        )
        if command and os.path.isfile(command) and os.access(command, os.X_OK):
            os.environ.setdefault(variable, os.fspath(command))


def _bootstrap_sagelite_lie_runtime() -> None:
    """
    Seed LiE runtime variables from an optional ``sagelite_lie`` package.

    Sage's LiE interface reads the upstream ``INFO.*`` help files directly.
    The companion package supplies those files for installed wheels while the
    ``lie`` command itself is exposed as relocatable package data.
    """
    configured = getattr(sage.config, "LIE_INFO_DIR", None) or join(SAGE_LOCAL, "lib", "LiE")
    needs_info = (
        not os.environ.get("LIE_INFO_DIR")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "INFO.0"))
            and os.path.isfile(os.path.join(os.fspath(configured), "INFO.3"))
        )
    )
    needs_command = not os.environ.get("SAGE_LIE_COMMAND") and not shutil.which("lie")

    if needs_info:
        info_dir = _optional_runtime_value("sagelite_lie.runtime", "info_dir")
        if (
            info_dir
            and os.path.isfile(os.path.join(info_dir, "INFO.0"))
            and os.path.isfile(os.path.join(info_dir, "INFO.3"))
        ):
            os.environ.setdefault("LIE_INFO_DIR", os.fspath(info_dir))

    if needs_command:
        command = _optional_runtime_value("sagelite_lie.runtime", "lie_command")
        if command and os.path.isfile(command) and os.access(command, os.X_OK):
            os.environ.setdefault("SAGE_LIE_COMMAND", os.fspath(command))


def _bootstrap_sagelite_jmol_runtime() -> None:
    """
    Seed ``JMOL_DIR`` from an optional ``sagelite_jmol_runtime`` package.

    Installed wheels can carry a build-time ``JMOL_DIR`` that does not exist
    after installation.  The companion package supplies ``JmolData.jar`` as
    relocatable package data.
    """
    configured = getattr(sage.config, "JMOL_DIR", None)
    needs_jmol = (
        not os.environ.get("JMOL_DIR")
        and not (
            configured
            and os.path.isfile(os.path.join(os.fspath(configured), "JmolData.jar"))
        )
    )
    if not needs_jmol:
        return

    jmol_dir = _optional_runtime_value("sagelite_jmol_runtime", "jmol_path")
    if jmol_dir and os.path.isfile(os.path.join(jmol_dir, "JmolData.jar")):
        os.environ.setdefault("JMOL_DIR", os.fspath(jmol_dir))


def _bootstrap_sagelite_threejs_runtime() -> None:
    """
    Seed ``THREEJS_DIR`` from an optional ``sagelite_threejs_runtime`` package.

    Installed wheels can carry a build-time ``THREEJS_DIR`` that does not
    exist after installation.  The companion package supplies ``threejs-sage``
    as relocatable package data.
    """
    configured = getattr(sage.config, "THREEJS_DIR", None)
    needs_threejs = (
        not os.environ.get("THREEJS_DIR")
        and not _threejs_dir_is_usable(configured)
    )
    if not needs_threejs:
        return

    threejs_dir = _optional_runtime_value(
        "sagelite_threejs_runtime", "threejs_sage_path"
    )
    if _threejs_dir_is_usable(threejs_dir):
        os.environ.setdefault("THREEJS_DIR", os.fspath(threejs_dir))


def _threejs_dir_is_usable(path: str | os.PathLike | None) -> bool:
    """
    Return whether ``path`` looks like a usable ``threejs-sage`` runtime.
    """
    if not path:
        return False

    root = os.fspath(path)
    version_file = os.path.join(root, "version")
    if not os.path.isfile(version_file):
        return False

    try:
        with open(version_file, encoding="utf-8") as handle:
            version = handle.read().strip()
    except OSError:
        return False

    return bool(version) and os.path.isfile(os.path.join(root, version, "three.min.js"))


def var(key: str, *fallbacks: Optional[str], force: bool = False) -> Optional[str]:
    """
    Set ``SAGE_ENV[key]`` and return the value.

    If ``key`` is an environment variable, this is the value.
    Otherwise, the ``fallbacks`` are tried until one is found which
    is not ``None``. If the environment variable is not set and all
    fallbacks are ``None``, then the final value is ``None``.

    INPUT:

    - ``key`` -- string

    - ``fallbacks`` -- tuple containing ``str`` or ``None`` values

    - ``force`` -- boolean (default: ``False``); if
      ``True``, skip the environment variable and only use the
      fallbacks

    OUTPUT: the value of the environment variable or its fallbacks

    EXAMPLES::

        sage: import os, sage.env
        sage: sage.env.SAGE_ENV = dict()
        sage: os.environ['SAGE_FOO'] = 'foo'
        sage: sage.env.var('SAGE_FOO', 'unused')
        'foo'
        sage: sage.env.SAGE_FOO
        'foo'
        sage: sage.env.SAGE_ENV['SAGE_FOO']
        'foo'

    If the environment variable does not exist, the fallbacks (if any)
    are used. In most typical uses, there is exactly one fallback::

        sage: _ = os.environ.pop('SAGE_BAR', None)  # ensure that SAGE_BAR does not exist
        sage: sage.env.var('SAGE_BAR', 'bar')
        'bar'
        sage: sage.env.SAGE_BAR
        'bar'
        sage: sage.env.SAGE_ENV['SAGE_BAR']
        'bar'

    Test multiple fallbacks::

        sage: sage.env.var('SAGE_BAR', None, 'yes', 'no')
        'yes'
        sage: sage.env.SAGE_BAR
        'yes'

    If all fallbacks are ``None``, the result is ``None``::

        sage: sage.env.var('SAGE_BAR')
        sage: print(sage.env.SAGE_BAR)
        None
        sage: sage.env.var('SAGE_BAR', None)
        sage: print(sage.env.SAGE_BAR)
        None

    Test the ``force`` keyword::

        sage: os.environ['SAGE_FOO'] = 'foo'
        sage: sage.env.var('SAGE_FOO', 'forced', force=True)
        'forced'
        sage: sage.env.SAGE_FOO
        'forced'
        sage: sage.env.var('SAGE_FOO', 'forced', force=False)
        'foo'
        sage: sage.env.SAGE_FOO
        'foo'
    """
    if force:
        value = None
    else:
        value = os.environ.get(key)
    if value is None:
        value = getattr(sage.config, key, None)

    # Try all fallbacks in order as long as we don't have a non-empty value
    for f in fallbacks:
        if value not in (None, ""):
            break
        value = f
    SAGE_ENV[key] = value
    globals()[key] = value
    return value


# system info
HOSTNAME = var("HOSTNAME", socket.gethostname())
LOCAL_IDENTIFIER = var("LOCAL_IDENTIFIER", "{}.{}".format(HOSTNAME, os.getpid()))

# version info
SAGE_VERSION = var("SAGE_VERSION", version.version)
SAGE_DATE = var("SAGE_DATE", version.date)
SAGE_VERSION_BANNER = var("SAGE_VERSION_BANNER", version.banner)

# virtual environment where sagelib is installed
SAGE_LIB = var("SAGE_LIB", os.path.dirname(os.path.dirname(__file__)))
SAGE_EXTCODE = var("SAGE_EXTCODE", join(SAGE_LIB, "sage", "ext_data"))

# prefix hierarchy where non-Python packages are installed
SAGE_LOCAL = var("SAGE_LOCAL")
SAGE_SHARE = var("SAGE_SHARE", join(SAGE_LOCAL, "share"))
SAGE_DOC = var("SAGE_DOC", join(SAGE_SHARE, "doc", "sage"))
SAGE_LOCAL_SPKG_INST = var("SAGE_LOCAL_SPKG_INST", join(SAGE_LOCAL, "var", "lib", "sage", "installed"))
SAGE_SPKG_INST = var("SAGE_SPKG_INST", join(SAGE_LOCAL, "var", "lib", "sage", "installed"))  # deprecated

# source tree of the Sage distribution
SAGE_ROOT = var("SAGE_ROOT") or None
SAGE_SRC = var("SAGE_SRC", join(SAGE_ROOT, "src"), SAGE_LIB)
SAGE_DOC_SRC = var("SAGE_DOC_SRC", join(SAGE_ROOT, "src", "doc"), SAGE_DOC)
SAGE_PKGS = var("SAGE_PKGS", join(SAGE_ROOT, "build", "pkgs"))
SAGE_ROOT_GIT = var("SAGE_ROOT_GIT", join(SAGE_ROOT, ".git"))

# Sage doc server (local server with PORT if URL is not given)
SAGE_DOC_SERVER_URL = var("SAGE_DOC_SERVER_URL")
# The default port is 0 so that the system will assign a random unused port > 1024
SAGE_DOC_LOCAL_PORT = var("SAGE_DOC_LOCAL_PORT", "0")

# ~/.sage
if sys.platform == 'win32':
    home_dir = os.environ.get("USERPROFILE")
else:  # Unix-like systems (Linux, macOS, etc.)
    home_dir = os.environ.get("HOME")
DOT_SAGE = var("DOT_SAGE", join(home_dir, ".sage"))
SAGE_STARTUP_FILE = var("SAGE_STARTUP_FILE", join(DOT_SAGE, "init.sage"))

# for sage_setup.setenv
SAGE_ARCHFLAGS = var("SAGE_ARCHFLAGS", "unset")
SAGE_PKG_CONFIG_PATH = var("SAGE_PKG_CONFIG_PATH")

# colon-separated search path for databases
# should not be used directly; instead use sage_data_paths
SAGE_DATA_PATH = var("SAGE_DATA_PATH")
_bootstrap_sagelite_pari_data_runtime()
GP_DATA_DIR = var("GP_DATA_DIR")

# database directories, the default is to search in SAGE_DATA_PATH
CREMONA_LARGE_DATA_DIR = var(
    "CREMONA_LARGE_DATA_DIR",
    _optional_runtime_data_dir(
        "sagelite_database_cremona_ellcurve",
        "cremona_ellcurve_path",
        "cremona.db",
        path_is_file=True,
    ),
)
CREMONA_MINI_DATA_DIR = var(
    "CREMONA_MINI_DATA_DIR",
    _optional_runtime_data_dir(
        "sagelite_database_cremona_mini",
        "cremona_mini_path",
        "cremona_mini.db",
        path_is_file=True,
    ),
)
ELLCURVE_DATA_DIR = var(
    "ELLCURVE_DATA_DIR",
    _optional_runtime_data_dir(
        "sagelite_database_ellcurves", "ellcurves_data_path", "rank0"
    ),
)
GRAPHS_DATA_DIR = var(
    "GRAPHS_DATA_DIR",
    _optional_runtime_data_dir(
        "sagelite_database_graphs", "graphs_data_path", "graphs.db"
    ),
)
POLYTOPE_DATA_DIR = var(
    "POLYTOPE_DATA_DIR",
    _optional_runtime_data_dir(
        "sagelite_database_polytopes", "reflexive_polytopes_path", "Full3d"
    ),
    _optional_runtime_data_dir(
        "sagelite_database_polytopes_4d", "reflexive_polytopes_path", "Hodge4d"
    ),
)

# installation directories for various packages
_bootstrap_sagelite_jmol_runtime()
JMOL_DIR = var("JMOL_DIR")
_bootstrap_sagelite_mathjax_runtime()
MATHJAX_DIR = var("MATHJAX_DIR", join(SAGE_SHARE, "mathjax"))
_bootstrap_sagelite_meataxe_runtime()
MTXLIB = var("MTXLIB", join(SAGE_SHARE, "meataxe"))
_bootstrap_sagelite_threejs_runtime()
THREEJS_DIR = var("THREEJS_DIR")
PPLPY_DOCS = var("PPLPY_DOCS", join(SAGE_SHARE, "doc", "pplpy"))
_bootstrap_sagelite_maxima_runtime()
MAXIMA = var("MAXIMA", "maxima")
MAXIMA_FAS = var("MAXIMA_FAS")
MAXIMA_PREFIX = var("MAXIMA_PREFIX")
_bootstrap_sagelite_kenzo_runtime()
KENZO_FAS = var("KENZO_FAS")
_bootstrap_sagelite_nauty_runtime()
SAGE_NAUTY_BINS_PREFIX = var("SAGE_NAUTY_BINS_PREFIX", "")
_bootstrap_sagelite_ecm_runtime()
SAGE_ECMBIN = var("SAGE_ECMBIN", "ecm")
_bootstrap_sagelite_mwrank_runtime()
MWRANK = var("MWRANK", "mwrank")
_bootstrap_sagelite_sympow_runtime()
SYMPOW = var("SYMPOW", "sympow")
_bootstrap_sagelite_tachyon_runtime()
TACHYON = var("TACHYON", "tachyon")
_bootstrap_sagelite_gfan_runtime()
GFAN_BINS_PREFIX = var("GFAN_BINS_PREFIX", "")
_bootstrap_sagelite_latte_runtime()
LATTE_BINS_PREFIX = var("LATTE_BINS_PREFIX", "")
_bootstrap_sagelite_rubiks_runtime()
RUBIKS_BINS_PREFIX = var("RUBIKS_BINS_PREFIX", "")
_bootstrap_sagelite_palp_runtime()
PALP_BINS_PREFIX = var("PALP_BINS_PREFIX", "")
_bootstrap_sagelite_four_ti_2_runtime()
FOURTITWO_HILBERT = var("FOURTITWO_HILBERT")
FOURTITWO_MARKOV = var("FOURTITWO_MARKOV")
FOURTITWO_GRAVER = var("FOURTITWO_GRAVER")
FOURTITWO_ZSOLVE = var("FOURTITWO_ZSOLVE")
FOURTITWO_QSOLVE = var("FOURTITWO_QSOLVE")
FOURTITWO_RAYS = var("FOURTITWO_RAYS")
FOURTITWO_PPI = var("FOURTITWO_PPI")
FOURTITWO_CIRCUITS = var("FOURTITWO_CIRCUITS")
FOURTITWO_GROEBNER = var("FOURTITWO_GROEBNER")
_bootstrap_sagelite_ecl_runtime()
ECL_CONFIG = var("ECL_CONFIG", "ecl-config")
ECL_CONFIG = var(
    "ECL_CONFIG",
    _installed_command_or_fallback(ECL_CONFIG, "ecl-config"),
    force=True,
)
NTL_INCDIR = var("NTL_INCDIR")
NTL_LIBDIR = var("NTL_LIBDIR")
_bootstrap_sagelite_lie_runtime()
SAGE_LIE_COMMAND = var("SAGE_LIE_COMMAND", "lie")
LIE_INFO_DIR = var("LIE_INFO_DIR", join(SAGE_LOCAL, "lib", "LiE"))
_bootstrap_sagelite_singular_runtime()
_bootstrap_sagelite_info_runtime()
SINGULAR_BIN = var("SINGULAR_BIN") or "Singular"

# OpenMP
OPENMP_CFLAGS = var("OPENMP_CFLAGS", "")
OPENMP_CXXFLAGS = var("OPENMP_CXXFLAGS", "")

# Make sure that mpmath < 1.4 does not try to use Sage types
os.environ.pop('MPMATH_SAGE', None)
os.environ['MPMATH_NOSAGE'] = '1'

# misc
SAGE_BANNER = var("SAGE_BANNER", "")
SAGE_IMPORTALL = var("SAGE_IMPORTALL", "yes")

# GAP memory and args

SAGE_GAP_MEMORY = var('SAGE_GAP_MEMORY', None)
_bootstrap_sagelite_gap_runtime()
SAGE_GAP_COMMAND = var('SAGE_GAP_COMMAND', None)
_bootstrap_sagelite_gap3_runtime()
SAGE_GAP3_COMMAND = var("SAGE_GAP3_COMMAND", "gap3")

# The semicolon-separated search path for GAP packages. It is passed
# directly to GAP via the -l flag.
GAP_ROOT_PATHS = _gap_root_paths()
SAGE_ENV["GAP_ROOT_PATHS"] = GAP_ROOT_PATHS

# post process
if DOT_SAGE is not None and ' ' in DOT_SAGE:
    print("Your home directory has a space in it.  This")
    print("will probably break some functionality of Sage.  E.g.,")
    print("the GAP interface will not work. A workaround")
    print("is to set the environment variable HOME to a")
    print("directory with no spaces that you have write")
    print("permissions to before you start sage.")


def sage_include_directories(use_sources=False):
    """
    Return the list of include directories for compiling Sage extension modules.

    INPUT:

    - ``use_sources`` -- boolean (default: ``False``)

    OUTPUT:

    a list of include directories to be used to compile sage code
    1. while building sage (use_sources='True')
    2. while using sage (use_sources='False')

    EXAMPLES:

    Expected output while using Sage::

        sage: import sage.env
        sage: sage.env.sage_include_directories()
        doctest:warning...
        DeprecationWarning: use sage.config.get_include_dirs() instead
        ...
        ['...',
         '.../numpy/...core/include',
         '.../include/python...']

    To check that C/C++ files are correctly found, we verify that we can
    always find the include file ``sage/cpython/cython_metaclass.h``,
    with both values for ``use_sources``::

        sage: file = os.path.join("sage", "cpython", "cython_metaclass.h")
        sage: dirs = sage.env.sage_include_directories(use_sources=True)
        sage: any(os.path.isfile(os.path.join(d, file)) for d in dirs)
        True

    ::

        sage: # optional - !meson_editable (no need, see :issue:`39275`)
        sage: dirs = sage.env.sage_include_directories(use_sources=False)
        sage: any(os.path.isfile(os.path.join(d, file)) for d in dirs)
        True
    """
    from sage.misc.superseded import deprecation
    deprecation(40765, 'use sage.config.get_include_dirs() instead')

    if use_sources:
        dirs = [SAGE_SRC]
    else:
        import sage
        dirs = [os.path.dirname(directory)
                for directory in sage.__path__]
    try:
        import numpy
        dirs.append(numpy.get_include())
    except ModuleNotFoundError:
        pass

    dirs.append(sysconfig.get_config_var('INCLUDEPY'))

    dirs.extend([dir.as_posix() for dir in get_include_dirs()])

    return dirs


default_required_modules = ('fflas-ffpack', 'givaro', 'gsl', 'linbox', 'Singular',
                            'libpng', 'gdlib', 'm4ri', 'zlib', 'ecl')


default_optional_modules = ('lapack',)


def cython_aliases(required_modules=None, optional_modules=None):
    """
    Return the aliases for compiling Cython code. These aliases are
    macros which can occur in ``# distutils`` headers.

    INPUT:

    - ``required_modules`` -- (default: taken from ``default_required_modules``)
      iterable of string values

    - ``optional_modules`` -- (default: taken from ``default_optional_modules``)
      iterable of string values

    EXAMPLES::

        sage: from sage.env import cython_aliases
        sage: cython_aliases()
        {...}
        sage: sorted(cython_aliases().keys())
        ['ECL_CFLAGS',
         ...,
         'ZLIB_LIBRARIES']
        sage: cython_aliases(required_modules=('module-that-is-assumed-to-not-exist'))
        Traceback (most recent call last):
        ...
        PackageNotFoundError: ...
        sage: cython_aliases(required_modules=(), optional_modules=('module-that-is-assumed-to-not-exist'))
        {...}

    TESTS:

    We can use ``cython.parallel`` regardless of whether OpenMP is supported.
    This will run in parallel, if OpenMP is supported::

        sage: cython(                                               # optional - sage.misc.cython
        ....: '''
        ....: #distutils: extra_compile_args = OPENMP_CFLAGS
        ....: #distutils: extra_link_args = OPENMP_CFLAGS
        ....: from cython.parallel import prange
        ....:
        ....: cdef int i
        ....: cdef int n = 30
        ....: cdef int sum = 0
        ....:
        ....: for i in prange(n, num_threads=4, nogil=True):
        ....:     sum += i
        ....:
        ....: print(sum)
        ....: ''')
        435
    """
    import itertools

    import pkgconfig

    if required_modules is None:
        required_modules = default_required_modules

    if optional_modules is None:
        optional_modules = default_optional_modules

    aliases = {}

    for lib, required in itertools.chain(((lib, True) for lib in required_modules),
                                         ((lib, False) for lib in optional_modules)):
        var = lib.upper().replace("-", "") + "_"
        if lib == 'zlib':
            aliases[var + "CFLAGS"] = ""
            try:
                pc = pkgconfig.parse('zlib')
                libs = pkgconfig.libs(lib)
            except pkgconfig.PackageNotFoundError:
                from collections import defaultdict
                pc = defaultdict(list, {'libraries': ['z']})
                libs = "-lz"
        elif lib == 'ecl':
            try:
                # Determine ecl-specific compiler arguments using the ecl-config script
                ecl_cflags = subprocess.run([ECL_CONFIG, "--cflags"], check=True, capture_output=True, text=True).stdout.split()
                ecl_libs = subprocess.run([ECL_CONFIG, "--libs"], check=True, capture_output=True, text=True).stdout.split()
            except subprocess.CalledProcessError:
                if required:
                    raise
                else:
                    continue
            aliases["ECL_CFLAGS"] = list(filter(lambda s: not s.startswith('-I'), ecl_cflags))
            aliases["ECL_INCDIR"] = [s[2:] for s in filter(lambda s: s.startswith('-I'), ecl_cflags)]
            aliases["ECL_LIBDIR"] = [s[2:] for s in filter(lambda s: s.startswith('-L'), ecl_libs)]
            aliases["ECL_LIBRARIES"] = [s[2:] for s in filter(lambda s: s.startswith('-l'), ecl_libs)]
            aliases["ECL_LIBEXTRA"] = list(filter(lambda s: not s.startswith(('-l', '-L')), ecl_libs))
            continue
        else:
            try:
                aliases[var + "CFLAGS"] = pkgconfig.cflags(lib).split()
                pc = pkgconfig.parse(lib)
                libs = pkgconfig.libs(lib)
            except pkgconfig.PackageNotFoundError:
                if required:
                    raise
                else:
                    continue

        # It may seem that INCDIR is redundant because the -I options are also
        # passed in CFLAGS.  However, "extra_compile_args" are put at the end
        # of the compiler command line.  "include_dirs" go to the front; the
        # include search order matters.
        aliases[var + "INCDIR"] = pc['include_dirs']
        aliases[var + "LIBDIR"] = pc['library_dirs']
        aliases[var + "LIBEXTRA"] = list(filter(lambda s: not s.startswith(('-l', '-L')), libs.split()))
        aliases[var + "LIBRARIES"] = pc['libraries']

    # uname-specific flags
    UNAME = os.uname()

    def uname_specific(name, value, alternative):
        if name in UNAME[0]:
            return value
        else:
            return alternative

    aliases["LINUX_NOEXECSTACK"] = uname_specific("Linux", ["-Wl,-z,noexecstack"],
                                                  [])

    # LinBox needs special care because it actually requires C++11 with
    # GNU extensions: -std=c++11 does not work, you need -std=gnu++11
    # (this is true at least with GCC 7.2.0).
    #
    # Further, note that LinBox does not add any C++11 flag in its .pc
    # file (possibly because of confusion between CFLAGS and CXXFLAGS?).
    # This is not a problem in practice since LinBox depends on
    # fflas-ffpack and fflas-ffpack does add such a C++11 flag.
    if "LINBOX_CFLAGS" in aliases:
        aliases["LINBOX_CFLAGS"].append("-std=gnu++11")

    try:
        aliases["M4RI_CFLAGS"].remove("-pedantic")
    except (ValueError, KeyError):
        pass

    # NTL
    aliases["NTL_CFLAGS"] = ['-std=c++11']
    aliases["NTL_INCDIR"] = [NTL_INCDIR] if NTL_INCDIR else []
    aliases["NTL_LIBDIR"] = [NTL_LIBDIR] if NTL_LIBDIR else []
    aliases["NTL_LIBRARIES"] = ['ntl']
    aliases["NTL_LIBEXTRA"] = []

    # OpenMP
    aliases["OPENMP_CFLAGS"] = OPENMP_CFLAGS.split()
    aliases["OPENMP_CXXFLAGS"] = OPENMP_CXXFLAGS.split()

    return aliases


def sage_data_paths(name: str = '') -> set[str]:
    r"""
    Search paths for general data files.

    If specified, the subdirectory ``name`` is appended to the
    directories. Otherwise, the directories are returned as is.

    EXAMPLES::

        sage: from sage.env import sage_data_paths
        sage: sage_data_paths("cremona")
        {'.../cremona'}
    """
    if not SAGE_DATA_PATH:
        paths = {
            join(DOT_SAGE, "db"),
            join(SAGE_SHARE, "sagemath"),
            SAGE_SHARE,
        }
        paths.add(user_data_dir("sagemath"))
        paths.add(user_data_dir())
        for path in site_data_dir("sagemath", multipath=True).split(os.pathsep) + site_data_dir(multipath=True).split(os.pathsep):
            paths.add(path)
    else:
        paths = set(SAGE_DATA_PATH.split(os.pathsep))

    paths.update(_registered_sage_data_paths())

    if not name:
        return {path for path in paths if os.path.exists(path)}

    resolved = {os.path.join(path, name) for path in paths if os.path.exists(path)}
    resolved.update(
        path
        for path in paths
        if os.path.basename(os.path.normpath(path)) == name and os.path.exists(path)
    )
    return resolved


def _registered_sage_data_paths() -> set[str]:
    r"""
    Search paths contributed by companion packages.

    Companion wheels can register an entry point in the
    ``sagemath.data_paths`` group that returns either one directory or an
    iterable of directories. If an entry point returns a direct file path, the
    containing directory is used as the search path. Invalid entry points are
    ignored so that optional data packages never become mandatory runtime
    dependencies.
    """
    paths = set()
    for entry_point in _entry_points(group="sagemath.data_paths"):
        try:
            value = entry_point.load()
            value = value() if callable(value) else value
        except Exception:
            continue
        paths.update(_coerce_sage_data_paths(value))
    paths.update(_sagelite_companion_data_paths())
    return {path for path in paths if os.path.exists(path)}


def _sagelite_companion_data_paths() -> set[str]:
    r"""
    Return data roots exposed directly by installed ``sagelite-*`` wheels.

    Entry points are the normal companion-wheel integration point.  The direct
    imports here are a fallback for environments where wheel metadata is
    stripped or not visible to :mod:`importlib.metadata`.
    """
    paths = set()
    for module_name in (
        "sagelite_cunningham_tables",
        "sagelite_database_cremona_ellcurve",
        "sagelite_database_cremona_mini",
        "sagelite_database_ellcurves",
        "sagelite_database_graphs",
        "sagelite_database_jones_numfield",
        "sagelite_database_kohel",
        "sagelite_database_mutation_class",
        "sagelite_database_odlyzko_zeta",
        "sagelite_database_polytopes",
        "sagelite_database_polytopes_4d",
        "sagelite_database_sloane",
        "sagelite_database_stein_watkins",
        "sagelite_database_stein_watkins_mini",
        "sagelite_database_symbolic_data",
    ):
        paths.update(
            _coerce_sage_data_paths(
                _optional_runtime_value(module_name, "sage_data_path")
            )
        )
    return paths


def _coerce_sage_data_paths(value) -> set[str]:
    r"""
    Normalize a value returned by a ``sagemath.data_paths`` entry point.
    """
    if value is None:
        return set()
    if isinstance(value, (str, bytes, PathLike)):
        path = os.fspath(value)
        return {os.path.dirname(path) if os.path.isfile(path) else path}
    try:
        iterator = iter(value)
    except TypeError:
        return set()
    return {
        os.path.dirname(os.fspath(path))
        if os.path.isfile(path)
        else os.fspath(path)
        for path in iterator
        if isinstance(path, (str, bytes, PathLike))
    }
