r"""
Feature for testing the presence of ``lcalc``
"""

# *****************************************************************************
#       Copyright (C) 2026 The Sage Developers
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

import os

from . import Executable


class Lcalc(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of
    :ref:`lcalc <spkg_lcalc>`.

    EXAMPLES::

        sage: from sage.features.lcalc import Lcalc
        sage: Lcalc().is_present()  # needs lcalc
        FeatureTestResult('lcalc', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.lcalc import Lcalc
            sage: isinstance(Lcalc(), Lcalc)
            True
        """
        Executable.__init__(
            self,
            name="lcalc",
            executable="lcalc",
            spkg="lcalc",
            type="standard",
        )

    def absolute_filename(self) -> str:
        r"""
        Return the ``lcalc`` executable path.

        Normal Sage installations find ``lcalc`` on ``PATH``. Wheel
        installations can also provide it through the optional
        ``sagelite-lcalc-runtime`` companion package.
        """
        try:
            from sagelite_lcalc.runtime import lcalc_command
        except ImportError:
            return super().absolute_filename()

        executable = lcalc_command()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        return super().absolute_filename()


def all_features():
    return [Lcalc()]
