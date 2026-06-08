r"""
Feature for testing the presence of ``qepcad``.
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


class Qepcad(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of
    :ref:`QEPCAD <spkg_qepcad>`.

    EXAMPLES::

        sage: from sage.features.qepcad import Qepcad
        sage: Qepcad().is_present()  # optional - qepcad
        FeatureTestResult('qepcad', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.qepcad import Qepcad
            sage: isinstance(Qepcad(), Qepcad)
            True
        """
        Executable.__init__(
            self,
            name="qepcad",
            executable="qepcad",
            spkg="qepcad",
            url="https://github.com/chriswestbrown/qepcad",
            type="optional",
        )

    def absolute_filename(self) -> str:
        r"""
        Return the QEPCAD executable path.

        Normal Sage installations find ``qepcad`` on ``PATH``. Wheel
        installations can also provide it through the optional
        ``sagelite-qepcad-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_qepcad.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [Qepcad()]
