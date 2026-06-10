r"""
Feature for testing the presence of ``giac``
"""

import os

from . import Executable, FeatureNotPresentError, FeatureTestResult


class Giac(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of :ref:`giac <spkg_giac>`.

    EXAMPLES::

        sage: from sage.features.giac import Giac
        sage: Giac().is_present()  # needs giac
        FeatureTestResult('giac', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.giac import Giac
            sage: isinstance(Giac(), Giac)
            True
        """
        Executable.__init__(self, 'giac', executable='giac',
                            spkg='giac', type='optional')

    def absolute_filename(self) -> str:
        r"""
        Return the GIAC executable path.

        Normal Sage installations find ``giac`` on ``PATH``. Wheel
        installations can also provide it through the optional
        ``sagelite-giac-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_giac.runtime import giac_command
        except ImportError:
            raise original_error

        executable = giac_command()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [Giac()]
