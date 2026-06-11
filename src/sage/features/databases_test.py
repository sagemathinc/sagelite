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
    ) == (str(configured), str(companion))


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


def test_reflexive_polytopes_4d_feature_searches_companion_data_when_config_is_stale(
    monkeypatch, tmp_path
):
    stale = tmp_path / "stale-polytopes"
    companion = tmp_path / "companion" / "reflexive_polytopes"
    (companion / "Hodge4d").mkdir(parents=True)

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})
    monkeypatch.setattr(sage.env, "POLYTOPE_DATA_DIR", str(stale))

    feature = databases.DatabaseReflexivePolytopes("polytopes_db_4d")

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


def test_cunningham_tables_feature_searches_companion_data(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "cunningham_tables"
    companion.mkdir(parents=True)
    (companion / "cunningham_prime_factors.sobj").write_text("cunningham\n")

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})

    feature = databases.DatabaseCunninghamTables()

    assert feature.search_path == [str(companion)]
    assert bool(feature.is_present())


def test_kohel_feature_searches_companion_data(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "kohel"
    db_file = companion / "PolMod" / "Cls" / "pol.001.dbz"
    db_file.parent.mkdir(parents=True)
    db_file.write_bytes(b"kohel\n")

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})

    feature = databases.DatabaseKohel()

    assert feature.search_path == [str(companion)]
    assert bool(feature.is_present())


def test_mutation_class_feature_searches_companion_data(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "cluster_algebra_quiver"
    companion.mkdir(parents=True)
    (companion / "mutation_classes_2.dig6").write_bytes(b"mutation classes\n")

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})

    feature = databases.DatabaseMutationClass()

    assert feature.search_path == [str(companion)]
    assert bool(feature.is_present())


def test_odlyzko_zeta_feature_searches_companion_data(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "odlyzko"
    companion.mkdir(parents=True)
    (companion / "zeros.sobj").write_bytes(b"odlyzko\n")

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})

    feature = databases.DatabaseOdlyzkoZeta()

    assert feature.search_path == [str(companion)]
    assert bool(feature.is_present())


def test_symbolic_data_feature_searches_companion_data(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "symbolic_data"
    (companion / "Data" / "XMLResources" / "INTPS").mkdir(parents=True)

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})

    feature = databases.DatabaseSymbolicData()

    assert feature.search_path == [str(companion)]
    assert bool(feature.is_present())


def test_stein_watkins_mini_feature_searches_companion_data(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "stein_watkins"
    companion.mkdir(parents=True)
    for filename in ("a.000.bz2", "a.001.bz2", "p.00.bz2"):
        (companion / filename).write_bytes(b"stein-watkins\n")

    monkeypatch.setattr(databases, "sage_data_paths", lambda name: {str(companion)})

    feature = databases.DatabaseSteinWatkinsMini()

    assert [file.search_path for file in feature.joined_features()] == [
        [str(companion)],
        [str(companion)],
        [str(companion)],
    ]
    assert bool(feature.is_present())
