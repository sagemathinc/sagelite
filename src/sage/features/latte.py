r"""
Features for testing the presence of ``latte_int``
"""

# ****************************************************************************
#       Copyright (C) 2018 Vincent Delecroix
#                     2019 Frédéric Chapoton
#                     2021 Matthias Koeppe
#                     2021 Kwankyu Lee
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

import os
import sys
from importlib import util as importlib_util
from pathlib import Path

from . import Executable, FeatureNotPresentError
from .join_feature import JoinFeature
from sage.env import LATTE_BINS_PREFIX, join


LATTE_URL = "https://www.math.ucdavis.edu/~latte/software.php"


def _sagelite_latte_runtime():
    """
    Return the optional ``sagelite_latte.runtime`` module from ``sys.path``.
    """
    for entry in sys.path:
        runtime_path = Path(entry, "sagelite_latte", "runtime.py")
        if not runtime_path.is_file():
            continue
        spec = importlib_util.spec_from_file_location(
            "_sage_latte_runtime", runtime_path
        )
        if spec is None or spec.loader is None:
            continue
        module = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None


def _sagelite_latte_executable(
        program: str, original_error: FeatureNotPresentError) -> str:
    """
    Return a LattE executable from the optional sagelite companion package.
    """
    runtime = _sagelite_latte_runtime()
    if runtime is None:
        raise original_error

    executable = runtime.executable_path(program)
    if executable.is_file() and os.access(executable, os.X_OK):
        return os.fspath(executable)

    raise original_error


class Latte_count(Executable):
    r"""
    Feature for the executable ``count`` from :ref:`LattE integrale <spkg_latte_int>`.
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.latte import Latte_count
            sage: isinstance(Latte_count(), Latte_count)
            True
        """
        Executable.__init__(self, 'count',
                            executable=join(LATTE_BINS_PREFIX, 'count') or 'count',
                            spkg='latte_int',
                            url=LATTE_URL)

    def absolute_filename(self) -> str:
        r"""
        Return the LattE ``count`` executable path.

        Normal Sage installations find LattE through ``LATTE_BINS_PREFIX`` or
        on ``PATH``.  Wheel installations can also provide it through the
        optional ``sagelite-latte-runtime`` companion package.
        """
        try:
            return _sagelite_latte_executable("count", FeatureNotPresentError(self))
        except FeatureNotPresentError:
            return super().absolute_filename()


class Latte_integrate(Executable):
    r"""
    Feature for the executable ``integrate`` from :ref:`LattE integrale <spkg_latte_int>`.
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.latte import Latte_integrate
            sage: isinstance(Latte_integrate(), Latte_integrate)
            True
        """
        Executable.__init__(self, 'integrate',
                            executable=join(LATTE_BINS_PREFIX, 'integrate') or 'integrate',
                            spkg='latte_int',
                            url=LATTE_URL)

    def absolute_filename(self) -> str:
        r"""
        Return the LattE ``integrate`` executable path.

        Normal Sage installations find LattE through ``LATTE_BINS_PREFIX`` or
        on ``PATH``.  Wheel installations can also provide it through the
        optional ``sagelite-latte-runtime`` companion package.
        """
        try:
            return _sagelite_latte_executable(
                "integrate", FeatureNotPresentError(self)
            )
        except FeatureNotPresentError:
            return super().absolute_filename()


class Latte(JoinFeature):
    r"""
    A :class:`~sage.features.Feature` describing the presence of executables
    from :ref:`LattE integrale <spkg_latte_int>`.

    EXAMPLES::

        sage: from sage.features.latte import Latte
        sage: Latte().is_present()  # optional - latte_int
        FeatureTestResult('latte_int', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.latte import Latte
            sage: isinstance(Latte(), Latte)
            True
        """
        JoinFeature.__init__(self, 'latte_int',
                             (Latte_count(), Latte_integrate()),
                             description='LattE')


def all_features():
    return [Latte()]
