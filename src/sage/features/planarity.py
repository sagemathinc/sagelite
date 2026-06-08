r"""
Feature for testing the presence of the ``planarity`` executable.
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

from . import Executable, FeatureNotPresentError


class Planarity(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of the
    :ref:`planarity <spkg_planarity>` executable.

    EXAMPLES::

        sage: from sage.features.planarity import Planarity
        sage: Planarity().is_present()  # optional - planarity
        FeatureTestResult('planarity', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.planarity import Planarity
            sage: isinstance(Planarity(), Planarity)
            True
        """
        Executable.__init__(
            self,
            name="planarity",
            executable="planarity",
            spkg="planarity",
            type="standard",
        )

    def absolute_filename(self) -> str:
        r"""
        Return the planarity executable path.

        Normal Sage installations find planarity on ``PATH``. Wheel
        installations can also provide it through the optional
        ``sagelite-planarity-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_planarity.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [Planarity()]
