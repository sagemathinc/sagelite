r"""
Feature for testing the presence of ``ecm`` or ``gmp-ecm``
"""
# ****************************************************************************
#       Copyright (C) 2032 Dima Pasechnik <dima@pasechnik.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

import os

from . import Executable, FeatureNotPresentError
from sage.env import SAGE_ECMBIN


class Ecm(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of :ref:`GMP-ECM <spkg_ecm>`.

    EXAMPLES::

        sage: from sage.features.ecm import Ecm
        sage: Ecm().is_present()
        FeatureTestResult('ecm', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.ecm import Ecm
            sage: isinstance(Ecm(), Ecm)
            True
        """
        Executable.__init__(self, name='ecm', executable=SAGE_ECMBIN,
                            spkg='ecm', type='standard')

    def absolute_filename(self) -> str:
        r"""
        Return the ecm executable path.

        Normal Sage installations find ecm on ``PATH``. Wheel installations can
        also provide it through the optional ``sagelite-ecm-runtime`` companion
        package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_ecm.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [Ecm()]
