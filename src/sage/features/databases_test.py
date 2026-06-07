import pytest
import sage.env

from sage.features import _trivial_unique_representation_cache
from sage.features import databases


@pytest.fixture(autouse=True)
def clean_feature_cache():
    _trivial_unique_representation_cache.clear()
    yield
    _trivial_unique_representation_cache.clear()


def test_search_path_with_registered_data_keeps_configured_path(monkeypatch, tmp_path):
    configured = tmp_path / "stale-configured"
    companion = tmp_path / "companion" / "ellcurves"
    companion.mkdir(parents=True)

    monkeypatch.setattr(
        databases,
        "sage_data_paths",
        lambda name: {str(companion)} if name == "ellcurves" else set(),
    )

    assert databases._search_path_with_registered_data(
        str(configured), "ellcurves"
    ) == [str(configured), str(companion)]


def test_ellcurves_feature_searches_companion_data_when_config_is_stale(
    monkeypatch, tmp_path
):
    stale = tmp_path / "stale-ellcurves"
    companion = tmp_path / "companion" / "ellcurves"
    companion.mkdir(parents=True)
    (companion / "rank0").write_text("ellcurves\n")

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})
    monkeypatch.setattr(sage.env, "ELLCURVE_DATA_DIR", str(stale))

    feature = databases.DatabaseEllcurves()

    assert feature.search_path == [str(stale), str(companion)]
    assert bool(feature.is_present())


def test_graphs_feature_searches_companion_data_when_config_is_stale(
    monkeypatch, tmp_path
):
    stale = tmp_path / "stale-graphs"
    companion = tmp_path / "companion" / "graphs"
    companion.mkdir(parents=True)
    (companion / "graphs.db").write_text("graphs\n")

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})
    monkeypatch.setattr(sage.env, "GRAPHS_DATA_DIR", str(stale))

    feature = databases.DatabaseGraphs()

    assert feature.search_path == [str(stale), str(companion)]
    assert bool(feature.is_present())


def test_reflexive_polytopes_feature_searches_companion_data_when_config_is_stale(
    monkeypatch, tmp_path
):
    stale = tmp_path / "stale-polytopes"
    companion = tmp_path / "companion" / "reflexive_polytopes"
    (companion / "Full3d").mkdir(parents=True)

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})
    monkeypatch.setattr(sage.env, "POLYTOPE_DATA_DIR", str(stale))

    feature = databases.DatabaseReflexivePolytopes()

    assert feature.search_path == [str(stale), str(companion)]
    assert bool(feature.is_present())


def test_cremona_feature_searches_companion_data_when_config_is_stale(
    monkeypatch, tmp_path
):
    mini_stale = tmp_path / "stale-cremona-mini"
    large_stale = tmp_path / "stale-cremona-large"
    companion = tmp_path / "companion" / "cremona"
    companion.mkdir(parents=True)
    (companion / "cremona_mini.db").write_text("cremona\n")

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})
    monkeypatch.setattr(sage.env, "CREMONA_MINI_DATA_DIR", str(mini_stale))
    monkeypatch.setattr(sage.env, "CREMONA_LARGE_DATA_DIR", str(large_stale))

    feature = databases.DatabaseCremona("cremona_mini")

    assert feature.search_path == [
        str(mini_stale),
        str(large_stale),
        str(companion),
    ]
    assert bool(feature.is_present())
