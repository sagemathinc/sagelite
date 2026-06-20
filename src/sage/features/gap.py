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
                for program in required_programs:
                    found = False
                    for directory in program_dirs:
                        path = os.path.join(_gap_directory_path(directory), program)
                        if os.path.isfile(path) and os.access(path, os.X_OK):
                            found = True
                            break
                    if not found:
                        missing.append(program)

                if missing:
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
