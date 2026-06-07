r"""
Features for testing the presence of ``4ti2``
"""

import os

from . import Executable, FeatureNotPresentError
from .join_feature import JoinFeature


class FourTi2Executable(Executable):
    r"""
    A :class:`~sage.features.Feature` for the :ref:`4ti2 <spkg_4ti2>` executables.
    """
    def __init__(self, name):
        r"""
        TESTS::

            sage: from sage.features.four_ti_2 import FourTi2Executable
            sage: isinstance(FourTi2Executable('hilbert'), FourTi2Executable)
            True
        """
        from sage.env import SAGE_ENV
        self._sagelite_program = name
        Executable.__init__(self,
                            name="4ti2-" + name,
                            executable=SAGE_ENV.get("FOURTITWO_" + name.upper(), None) or name,
                            spkg='4ti2')

    def absolute_filename(self) -> str:
        r"""
        Return the 4ti2 executable path.

        Normal Sage installations find 4ti2 on ``PATH``. Wheel installations can
        also provide it through the optional ``sagelite-4ti2-runtime`` companion
        package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_four_ti_2.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path(self._sagelite_program)
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


class FourTi2(JoinFeature):
    r"""
    A :class:`~sage.features.Feature` describing the presence of all :ref:`4ti2 <spkg_4ti2>` executables.

    EXAMPLES::

        sage: from sage.features.four_ti_2 import FourTi2
        sage: FourTi2().is_present()  # optional - 4ti2
        FeatureTestResult('4ti2', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.four_ti_2 import FourTi2
            sage: isinstance(FourTi2(), FourTi2)
            True
        """
        JoinFeature.__init__(self, '4ti2',
                             [FourTi2Executable(x)
                              # same list is tested in build/pkgs/4ti2/spkg-configure.m4
                              for x in ('hilbert', 'markov', 'graver', 'zsolve', 'qsolve',
                                        'rays', 'ppi', 'circuits', 'groebner')])


def all_features():
    return [FourTi2()]
