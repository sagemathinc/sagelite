r"""
Feature for testing the presence of msolve

`msolve <https://msolve.lip6.fr/>`_ is a multivariate polynomial system solver.

.. SEEALSO::

    - :mod:`sage.rings.polynomial.msolve`
"""

# *****************************************************************************
#       Copyright (C) 2022 Marc Mezzarobba
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

import os
import subprocess
from . import Executable
from . import FeatureNotPresentError
from . import FeatureTestResult
from . import executable_outside_python_prefix


class msolve(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of :ref:`msolve <spkg_msolve>`.

    EXAMPLES::

        sage: from sage.features.msolve import msolve
        sage: msolve().is_present()  # optional - msolve
        FeatureTestResult('msolve', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.msolve import msolve
            sage: isinstance(msolve(), msolve)
            True
        """
        Executable.__init__(self, "msolve", executable='msolve',
                            spkg="msolve", type="optional",
                            url='https://msolve.lip6.fr/')

    def absolute_filename(self) -> str:
        r"""
        Return the msolve executable path.

        Normal Sage installations find msolve on ``PATH``.  Wheel
        installations can also provide it through the optional
        ``sagelite-msolve-runtime`` companion package.
        """
        system_executable = executable_outside_python_prefix(self.executable)
        if system_executable:
            return system_executable

        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_msolve.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error

    def is_functional(self):
        r"""
        Test if our installation of msolve is working.

        TESTS::

            sage: from sage.features.msolve import msolve
            sage: msolve().is_functional()  # optional - msolve
            FeatureTestResult('msolve', True)
        """
        msolve_out = subprocess.run([self.absolute_filename(), "-h"], capture_output=True)

#        if msolve_out.returncode != 0:
#            return FeatureTestResult(self, False, reason="msolve -h returned "
#                                f"nonzero exit status {msolve_out.returncode}")
        output = msolve_out.stdout + msolve_out.stderr
        if b'msolve library for polynomial system solving' not in output:
            return FeatureTestResult(self, False,
                                     reason="output of msolve -h not recognized")
        return FeatureTestResult(self, True)


def all_features():
    return [msolve()]
