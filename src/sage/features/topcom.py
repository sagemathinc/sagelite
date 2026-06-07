r"""
Features for testing the presence of topcom executables
"""

# *****************************************************************************
#       Copyright (C) 2022-2024 Matthias Koeppe
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

import os

from . import Executable
from . import FeatureNotPresentError
from .join_feature import JoinFeature


class TOPCOMExecutable(Executable):
    r"""
    A :class:`~sage.features.Feature` which checks for executables from the :ref:`TOPCOM <spkg_topcom>` package.

    EXAMPLES::

        sage: from sage.features.topcom import TOPCOMExecutable
        sage: TOPCOMExecutable('points2allfinetriangs').is_present()    # optional - topcom
        FeatureTestResult('topcom_points2allfinetriangs', True)
    """
    def __init__(self, name):
        r"""
        TESTS::

            sage: from sage.features.topcom import TOPCOMExecutable
            sage: isinstance(TOPCOMExecutable('points2finetriangs'), TOPCOMExecutable)
            True
        """
        Executable.__init__(self, name=f"topcom_{name}",
                            executable=name,
                            spkg="topcom")
        self._topcom_name = name

    def absolute_filename(self) -> str:
        r"""
        Return the TOPCOM executable path.

        Normal Sage installations find TOPCOM on ``PATH``.  Wheel
        installations can also provide it through the optional
        ``sagelite-topcom-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_topcom.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path(self._topcom_name)
        if executable.is_file() and os.access(executable, os.X_OK):
            libdir = executable.parent.parent / "lib"
            if libdir.is_dir():
                old_path = os.environ.get("LD_LIBRARY_PATH")
                libdir = os.fspath(libdir)
                if old_path:
                    if libdir not in old_path.split(os.pathsep):
                        os.environ["LD_LIBRARY_PATH"] = f"{libdir}{os.pathsep}{old_path}"
                else:
                    os.environ["LD_LIBRARY_PATH"] = libdir
            return os.fspath(executable)

        raise original_error


class TOPCOM(JoinFeature):
    r"""
    A :class:`~sage.features.Feature` describing the presence of the executables
    which comes as a part of :ref:`TOPCOM <spkg_topcom>`.

    EXAMPLES::

        sage: from sage.features.topcom import TOPCOM
        sage: TOPCOM().is_present()                             # optional - topcom
        FeatureTestResult('topcom', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.topcom import TOPCOM
            sage: isinstance(TOPCOM(), TOPCOM)
            True
        """
        JoinFeature.__init__(self, "topcom",
                             [TOPCOMExecutable(name)
                              for name in ('points2allfinetriangs',)])


def all_features():
    return [TOPCOM()]
