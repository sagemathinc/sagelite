r"""
Feature for testing the presence of ``dvipng``
"""
# ****************************************************************************
#       Copyright (C) 2021 Sebastien Labbe <slabqc@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from . import Executable
from . import FeatureNotPresentError


class dvipng(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``dvipng``.

    EXAMPLES::

        sage: from sage.features.dvipng import dvipng
        sage: dvipng().is_present()             # optional - dvipng
        FeatureTestResult('dvipng', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.dvipng import dvipng
            sage: isinstance(dvipng(), dvipng)
            True
        """
        Executable.__init__(self, 'dvipng', executable='dvipng',
                            url='https://savannah.nongnu.org/projects/dvipng/')

    def absolute_filename(self) -> str:
        r"""
        Return the absolute path to the ``dvipng`` executable.

        Normal Sage installations find ``dvipng`` on ``PATH``. Wheel
        installations can also provide it through the optional
        ``sagelite-dvipng-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            try:
                from sagelite_dvipng.runtime import executable_path
            except ImportError:
                raise error

        executable = executable_path()
        if executable.is_file():
            return str(executable)

        raise error


def all_features():
    return [dvipng()]
