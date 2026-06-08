r"""
Feature for testing the presence of ``frobby``.
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


class Frobby(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of
    :ref:`Frobby <spkg_frobby>`.

    EXAMPLES::

        sage: from sage.features.frobby import Frobby
        sage: Frobby().is_present()  # optional - frobby
        FeatureTestResult('frobby', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.frobby import Frobby
            sage: isinstance(Frobby(), Frobby)
            True
        """
        Executable.__init__(
            self,
            name="frobby",
            executable="frobby",
            spkg="frobby",
            url="https://github.com/Macaulay2/frobby",
            type="optional",
        )

    def absolute_filename(self) -> str:
        r"""
        Return the Frobby executable path.

        Normal Sage installations find ``frobby`` on ``PATH``. Wheel
        installations can also provide it through the optional
        ``sagelite-frobby-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_frobby.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [Frobby()]
