r"""
Features for testing the presence of ``rubiks``
"""
# ****************************************************************************
#       Copyright (C) 2020      John H. Palmieri
#                     2021-2022 Matthias Koeppe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

import os

from sage.env import RUBIKS_BINS_PREFIX

from . import Executable
from . import FeatureNotPresentError
from .join_feature import JoinFeature


class RubiksExecutable(Executable):
    r"""
    A :class:`~sage.features.Feature` describing a Rubiks executable.
    """
    def __init__(self, name):
        r"""
        TESTS::

            sage: from sage.features.rubiks import RubiksExecutable
            sage: isinstance(RubiksExecutable("cubex"), RubiksExecutable)
            True
        """
        Executable.__init__(self, name, executable=RUBIKS_BINS_PREFIX + name,
                            spkg='rubiks')
        self._rubiks_name = name

    def absolute_filename(self) -> str:
        r"""
        Return the Rubiks executable path.

        Normal Sage installations find Rubiks executables on ``PATH`` or under
        ``RUBIKS_BINS_PREFIX``.  Wheel installations can also provide them
        through the optional ``sagelite-rubiks-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_rubiks.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path(self._rubiks_name)
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


class cu2(RubiksExecutable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``cu2``.

    EXAMPLES::

        sage: from sage.features.rubiks import cu2
        sage: cu2().is_present()  # optional - rubiks
        FeatureTestResult('cu2', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.rubiks import cu2
            sage: isinstance(cu2(), cu2)
            True
        """
        RubiksExecutable.__init__(self, "cu2")


class size222(RubiksExecutable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``size222``.

    EXAMPLES::

        sage: from sage.features.rubiks import size222
        sage: size222().is_present()  # optional - rubiks
        FeatureTestResult('size222', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.rubiks import size222
            sage: isinstance(size222(), size222)
            True
        """
        RubiksExecutable.__init__(self, "size222")


class optimal(RubiksExecutable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``optimal``.

    EXAMPLES::

        sage: from sage.features.rubiks import optimal
        sage: optimal().is_present()  # optional - rubiks
        FeatureTestResult('optimal', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.rubiks import optimal
            sage: isinstance(optimal(), optimal)
            True
        """
        RubiksExecutable.__init__(self, "optimal")


class mcube(RubiksExecutable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``mcube``.

    EXAMPLES::

        sage: from sage.features.rubiks import mcube
        sage: mcube().is_present()  # optional - rubiks
        FeatureTestResult('mcube', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.rubiks import mcube
            sage: isinstance(mcube(), mcube)
            True
        """
        RubiksExecutable.__init__(self, "mcube")


class dikcube(RubiksExecutable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``dikcube``.

    EXAMPLES::

        sage: from sage.features.rubiks import dikcube
        sage: dikcube().is_present()  # optional - rubiks
        FeatureTestResult('dikcube', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.rubiks import dikcube
            sage: isinstance(dikcube(), dikcube)
            True
        """
        RubiksExecutable.__init__(self, "dikcube")


class cubex(RubiksExecutable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``cubex``.

    EXAMPLES::

        sage: from sage.features.rubiks import cubex
        sage: cubex().is_present()  # optional - rubiks
        FeatureTestResult('cubex', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.rubiks import cubex
            sage: isinstance(cubex(), cubex)
            True
        """
        RubiksExecutable.__init__(self, "cubex")


class Rubiks(JoinFeature):
    r"""
    A :class:`~sage.features.Feature` describing the presence of the
    :class:`cu2`, :class:`cubex`, :class:`dikcube`, :class:`mcube`, :class:`optimal`, and
    :class:`size222` programs from the :ref:`rubiks <spkg_rubiks>` package.

    EXAMPLES::

        sage: from sage.features.rubiks import Rubiks
        sage: Rubiks().is_present()  # optional - rubiks
        FeatureTestResult('rubiks', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.rubiks import Rubiks
            sage: isinstance(Rubiks(), Rubiks)
            True
        """
        JoinFeature.__init__(self, "rubiks",
                             [cu2(), size222(), optimal(), mcube(), dikcube(), cubex()],
                             spkg='rubiks')


def all_features():
    return [Rubiks()]
