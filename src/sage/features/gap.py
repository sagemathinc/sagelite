r"""
Features for testing the presence of the SageMath interfaces to ``gap`` and of GAP packages
"""
# *****************************************************************************
#       Copyright (C) 2016 Julian Rüth
#                     2018 Jeroen Demeyer
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

import os
from importlib import import_module

from . import Feature, FeatureTestResult, PythonModule
from .join_feature import JoinFeature
from .sagemath import sage__libs__gap


_GAP_PACKAGE_REQUIRED_PROGRAMS = {
    "guava": ("wtdist",),
}


def _gap_directory_path(directory):
    """
    Return a filesystem path for a GAP directory object.
    """
    filename = getattr(directory, "Filename", None)
    if filename is not None:
        directory = filename("")
    sage = getattr(directory, "sage", None)
    if sage is not None:
        return os.fspath(sage())
    return os.fspath(directory)


def _path_is_under(path, roots):
    """
    Return whether ``path`` is contained in one of ``roots``.
    """
    try:
        real_path = os.path.realpath(os.fspath(path))
    except (TypeError, ValueError):
        return False
    for root in roots:
        try:
            real_root = os.path.realpath(os.fspath(root))
            if os.path.commonpath([real_path, real_root]) == real_root:
                return True
        except (OSError, TypeError, ValueError):
            continue
    return False


def _sagelite_gap_package_roots(package):
    """
    Return companion GAP roots for ``package`` if a sagelite companion exists.

    ``None`` means no sagelite companion package is installed.  An empty list
    means a companion is installed but does not expose a complete usable GAP
    package root, so host-system GAP packages must not satisfy the feature.
    """
    module_name = f"sagelite_gap_package_{package.lower()}"
    try:
        import_module(module_name)
    except ImportError:
        return None

    try:
        runtime = import_module(f"{module_name}.runtime")
    except ImportError:
        return []

    gap_root_paths = getattr(runtime, "gap_root_paths", None)
    if gap_root_paths is None:
        return []

    try:
        roots = gap_root_paths() if callable(gap_root_paths) else gap_root_paths
    except Exception:
        return []

    if not roots:
        return []
    return [root for root in os.fspath(roots).split(";") if root]


class GapPackage(Feature):
    r"""
    A :class:`~sage.features.Feature` describing the presence of a GAP package.

    A GAP package is "present" if it *can be* loaded, not if it *has
    been* loaded.

    .. SEEALSO::

        :class:`Feature sage.libs.gap <~sage.features.sagemath.sage__libs__gap>`

    EXAMPLES::

        sage: from sage.features.gap import GapPackage
        sage: GapPackage("grape", spkg='gap_packages')
        Feature('gap_package_grape')
    """
    def __init__(self, package, **kwds):
        r"""
        TESTS::

            sage: from sage.features.gap import GapPackage
            sage: isinstance(GapPackage("grape", spkg='gap_packages'), GapPackage)
            True
        """
        Feature.__init__(self, f"gap_package_{package}", **kwds)
        self.package = package

    def _is_present(self):
        r"""
        Return whether or not the GAP package is present.

        If the package is installed but not yet loaded, it is loaded
        first. This does *not* check that the package is functional.

        EXAMPLES::

            sage: from sage.features.gap import GapPackage
            sage: GapPackage("grape", spkg='gap_packages')._is_present()  # optional - gap_package_grape
            FeatureTestResult('gap_package_grape', True)
        """
        try:
            from sage.libs.gap.libgap import libgap
        except ImportError:
            return FeatureTestResult(self, False,
                                     reason="sage.libs.gap is not available")

        companion_roots = _sagelite_gap_package_roots(self.package)
        if companion_roots == []:
            return FeatureTestResult(
                self,
                False,
                reason=(
                    f"sagelite companion for GAP package {self.package} is "
                    "installed but does not expose a complete GAP package root"
                ),
            )

        # This returns "true" even if the package is already loaded.
        command = 'LoadPackage("{package}")'.format(package=self.package)
        presence = libgap.eval(command)

        if presence:
            required_programs = _GAP_PACKAGE_REQUIRED_PROGRAMS.get(self.package.lower())
            if required_programs:
                try:
                    program_dirs = libgap.DirectoriesPackagePrograms(self.package)
                except Exception as exc:
                    return FeatureTestResult(
                        self,
                        False,
                        reason=(
                            "could not inspect GAP package program directories "
                            f"for {self.package}: {exc}"
                        ),
                    )

                missing = []
                host_matches = []
                for program in required_programs:
                    found = False
                    for directory in program_dirs:
                        path = os.path.join(_gap_directory_path(directory), program)
                        if os.path.isfile(path) and os.access(path, os.X_OK):
                            if (
                                companion_roots is not None
                                and not _path_is_under(path, companion_roots)
                            ):
                                host_matches.append(path)
                                continue
                            found = True
                            break
                    if not found:
                        missing.append(program)

                if missing:
                    if host_matches:
                        return FeatureTestResult(
                            self,
                            False,
                            reason=(
                                f"GAP package {self.package} resolved required "
                                "programs outside the installed sagelite "
                                "companion roots: " + ", ".join(host_matches)
                            ),
                        )
                    return FeatureTestResult(
                        self,
                        False,
                        reason=(
                            f"GAP package {self.package} is missing required "
                            "programs: " + ", ".join(missing)
                        ),
                    )
            return FeatureTestResult(self, True,
                    reason="`{command}` evaluated to `{presence}` in GAP.".format(command=command, presence=presence))
        return FeatureTestResult(self, False,
                reason="`{command}` evaluated to `{presence}` in GAP.".format(command=command, presence=presence))


def all_features():
    return [GapPackage("atlasrep", spkg='gap_packages'),
            GapPackage("ctbllib", spkg='gap_packages'),
            GapPackage("design", spkg='gap_packages'),
            GapPackage("gapdoc", spkg='gap_packages'),
            GapPackage("grape", spkg='gap_packages'),
            GapPackage("guava", spkg='gap_packages'),
            GapPackage("hap", spkg='gap_packages'),
            GapPackage("polenta", spkg='gap_packages'),
            GapPackage("polycyclic", spkg='gap_packages'),
            GapPackage("primgrp", spkg='gap_packages'),
            GapPackage("qpa", spkg='gap_packages'),
            GapPackage("quagroup", spkg='gap_packages'),
            GapPackage("repsn", spkg='gap_packages'),
            GapPackage("smallgrp", spkg='gap_packages'),
            GapPackage("tomlib", spkg='gap_packages'),
            GapPackage("transgrp", spkg='gap_packages')]
