r"""
Feature for testing the presence of ``gap3``.
"""

import os

from . import Executable, FeatureNotPresentError
from sage.env import SAGE_GAP3_COMMAND


class Gap3(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of GAP3.

    EXAMPLES::

        sage: from sage.features.gap3 import Gap3
        sage: isinstance(Gap3(), Gap3)
        True
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.gap3 import Gap3
            sage: Gap3()
            Feature('gap3')
        """
        Executable.__init__(
            self,
            "gap3",
            executable=SAGE_GAP3_COMMAND,
            spkg="gap3",
            type="experimental",
        )

    def absolute_filename(self) -> str:
        r"""
        Return the GAP3 executable path.

        Normal Sage installations find GAP3 through ``SAGE_GAP3_COMMAND`` or
        on ``PATH``. Wheel installations can also provide it through the
        optional ``sagelite-gap3-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        try:
            from sagelite_gap3.runtime import gap3_command
        except ImportError:
            raise original_error

        executable = gap3_command()
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [Gap3()]
