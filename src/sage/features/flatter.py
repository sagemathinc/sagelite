r"""
Features for testing the presence of ``flatter``
"""

import os

from . import Executable, FeatureNotPresentError


class flatter(Executable):
    """
    A :class:`~sage.features.Feature` describing the presence of ``flatter``.

    EXAMPLES::

        sage: from sage.features.flatter import flatter
        sage: flatter().is_present()  # optional - flatter
        FeatureTestResult('flatter', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.flatter import flatter
            sage: isinstance(flatter(), flatter)
            True
        """
        Executable.__init__(self, "flatter", executable="flatter")

    def absolute_filename(self) -> str:
        r"""
        Return the flatter executable path.

        Normal Sage installations find flatter on ``PATH``. Wheel installations
        can also provide it through the optional ``sagelite-flatter-runtime``
        companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_flatter.runtime import executable_path
        except ImportError:
            raise original_error

        executable = executable_path()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [flatter()]
