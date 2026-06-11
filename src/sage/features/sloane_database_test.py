import sys
import types

import pytest

from sage.features import _trivial_unique_representation_cache
from sage.features.sloane_database import SloaneOEIS


@pytest.fixture(autouse=True)
def clean_feature_cache():
    _trivial_unique_representation_cache.clear()
    yield
    _trivial_unique_representation_cache.clear()


def test_sloane_feature_rechecks_database_class_instead_of_singleton(monkeypatch):
    class StaleSloaneEncyclopedia:
        def is_installed(self):
            return False

    class SloaneEncyclopediaClass:
        def is_installed(self):
            return True

    module = types.ModuleType("sage.databases.sloane")
    module.SloaneEncyclopedia = StaleSloaneEncyclopedia()
    module.SloaneEncyclopediaClass = SloaneEncyclopediaClass
    monkeypatch.setitem(sys.modules, "sage.databases.sloane", module)

    assert SloaneOEIS().is_present()
