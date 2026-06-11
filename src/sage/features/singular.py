r"""
Features for testing the presence of ``singular`` and the SageMath interfaces to it
"""

# *****************************************************************************
#       Copyright (C) 2022-2023 Matthias Koeppe
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

import os

from . import Executable, FeatureNotPresentError, PythonModule
from .join_feature import JoinFeature
from .sagemath import sage__libs__singular
from sage.env import SINGULAR_BIN


class Singular(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of the :ref:`singular <spkg_singular>` executable.

    .. SEEALSO::

        :class:`Feature sage.libs.singular <~sage.features.sagemath.sage__libs__singular>`

    EXAMPLES::

        sage: from sage.features.singular import Singular
        sage: Singular().is_present()                                                   # needs singular
        FeatureTestResult('singular', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.singular import Singular
            sage: isinstance(Singular(), Singular)
            True
        """
        Executable.__init__(self, "singular", SINGULAR_BIN,
                            spkg='singular', type='standard')

    def absolute_filename(self) -> str:
        """
        Return the Singular executable path.
        """
        missing_error = None
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            missing_error = error

        try:
            from sagelite_singular_runtime.runtime import executable_path
        except Exception as exc:
            raise missing_error from exc

        executable = executable_path()
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            return os.fspath(executable)
        raise missing_error


def all_features():
    return [Singular()]
