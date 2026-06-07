r"""
Features for testing the presence of ``gfan``
"""

# *****************************************************************************
#       Copyright (C) 2022 Matthias Koeppe
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

import os

from . import Executable, FeatureNotPresentError
from sage.env import GFAN_BINS_PREFIX


class GfanExecutable(Executable):
    r"""
    A :class:`~sage.features.Feature` for the :ref:`gfan <spkg_gfan>` executables.
    """
    def __init__(self, cmd=None):
        r"""
        TESTS::

            sage: from sage.features.gfan import GfanExecutable
            sage: isinstance(GfanExecutable('groebnercone'), GfanExecutable)
            True
        """
        if cmd is None:
            name = "gfan"
        else:
            name = f"gfan_{cmd}"
        self._sagelite_program = name
        Executable.__init__(self, name, executable=GFAN_BINS_PREFIX + name,
                            spkg='gfan', type='standard')

    def absolute_filename(self) -> str:
        r"""
        Return the gfan executable path.

        Normal Sage installations find gfan on ``PATH``. Wheel installations can
        also provide it through the optional ``sagelite-gfan-runtime`` companion
        package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_gfan.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path(self._sagelite_program)
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [GfanExecutable()]
