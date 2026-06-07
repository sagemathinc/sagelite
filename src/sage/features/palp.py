r"""
Feature for testing the presence of ``palp``
"""
# ****************************************************************************
#       Copyright (C) 2022 Matthias Koeppe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

import os

from sage.env import PALP_BINS_PREFIX

from . import Executable, FeatureNotPresentError
from .join_feature import JoinFeature


class PalpExecutable(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of a :ref:`PALP <spkg_palp>` executable.

    INPUT:

    - ``palpprog`` -- string, one of ``'poly'``, ``'class'``, ``'nef'``, ``'cws'``

    - ``suff`` -- string or ``None``
    """
    def __init__(self, palpprog, suff=None):
        r"""
        TESTS::

            sage: from sage.features.palp import PalpExecutable
            sage: isinstance(PalpExecutable("poly", 5), PalpExecutable)
            True
        """
        if suff:
            self._sagelite_program = f"{palpprog}-{suff}d.x"
            Executable.__init__(self, f"palp_{palpprog}_{suff}d",
                                executable=f"{PALP_BINS_PREFIX}{palpprog}-{suff}d.x",
                                spkg='palp', type='standard')
        else:
            self._sagelite_program = f"{palpprog}.x"
            Executable.__init__(self, f"palp_{palpprog}",
                                executable=f"{PALP_BINS_PREFIX}{palpprog}.x",
                                spkg='palp', type='standard')

    def absolute_filename(self) -> str:
        r"""
        Return the PALP executable path.

        Normal Sage installations find PALP on ``PATH``. Wheel installations can
        also provide it through the optional ``sagelite-palp-runtime`` companion
        package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_palp.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path(self._sagelite_program)
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


class Palp(JoinFeature):
    r"""
    A :class:`~sage.features.Feature` describing the presence of :ref:`PALP <spkg_palp>`.
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.palp import Palp
            sage: isinstance(Palp(), Palp)
            True
        """
        JoinFeature.__init__(self, "palp",
                             [PalpExecutable(palpprog, suff)
                              for palpprog in ("poly", "class", "nef", "cws")
                              for suff in (None, 4, 5, 6, 11)],
                             description='PALP')


def all_features():
    return [Palp()]
