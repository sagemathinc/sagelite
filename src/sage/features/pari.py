r"""
Features for testing PARI data packages.
"""

# *****************************************************************************
#       Copyright (C) 2026 The Sage Developers
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

import os

from sage.env import SAGE_LOCAL, SAGE_SHARE
from sage.features import StaticFile


def _registered_pari_data_dir():
    """
    Return the PARI data directory from the optional sagelite companion wheel.
    """
    try:
        from sagelite_pari_data.runtime import pari_data_dir
    except ImportError:
        return None
    return pari_data_dir()


def _pari_data_search_path():
    """
    Return candidate roots containing PARI data subdirectories.
    """
    paths = []
    registered = _registered_pari_data_dir()
    if registered:
        paths.append(registered)
    paths.append(os.path.join(SAGE_SHARE, "pari"))
    if SAGE_LOCAL:
        paths.append(os.path.join(SAGE_LOCAL, "share", "pari"))
    paths.extend(("/usr/share/pari", "/usr/local/share/pari"))
    return paths


class PariData(StaticFile):
    r"""
    A :class:`~sage.features.Feature` describing a PARI data package.

    EXAMPLES::

        sage: from sage.features.pari import PariData
        sage: PariData("pari_galdata", "galdata")
        Feature('pari_galdata')
    """

    def __init__(self, name, directory):
        r"""
        TESTS::

            sage: from sage.features.pari import PariData
            sage: isinstance(PariData("pari_galdata", "galdata"), PariData)
            True
        """
        StaticFile.__init__(
            self,
            name,
            filename=directory,
            search_path=_pari_data_search_path(),
            spkg=name,
            description=f"PARI data package {directory}",
        )


def all_features():
    return [
        PariData("pari_elldata", "elldata"),
        PariData("pari_galdata", "galdata"),
        PariData("pari_galpol", "galpol"),
        PariData("pari_nftables", "nftables"),
        PariData("pari_seadata", "seadata"),
    ]
