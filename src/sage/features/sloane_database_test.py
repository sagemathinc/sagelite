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


def test_sloane_feature_detects_registered_data_path(monkeypatch, tmp_path):
    data_dir = tmp_path / "sloane"
    data_dir.mkdir()
    (data_dir / "sloane-oeis.bz2").touch()
    (data_dir / "sloane-names.bz2").touch()

    integer_ring = types.ModuleType("sage.rings.integer_ring")
    integer_ring.ZZ = int
    monkeypatch.setitem(sys.modules, "sage.rings.integer_ring", integer_ring)

    import sage.databases.sloane as sloane_module

    def registered_data_paths(name):
        if name == "sloane":
            return {str(data_dir)}
        return set()

    monkeypatch.setattr(sloane_module, "sage_data_paths", registered_data_paths)

    assert SloaneOEIS().is_present()
