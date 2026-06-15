import pytest

from sage.features import FeatureTestResult

pari = pytest.importorskip(
    "sage.features.pari",
    reason="installed sagelite wheel does not include sage.features.pari",
)


def test_pari_data_feature_uses_registered_companion_path(monkeypatch, tmp_path):
    root = tmp_path / "pari"
    (root / "galpol").mkdir(parents=True)

    monkeypatch.setattr(pari, "_registered_pari_data_dir", lambda: str(root))
    monkeypatch.setattr(pari, "SAGE_SHARE", str(tmp_path / "missing_share"))
    monkeypatch.setattr(pari, "SAGE_LOCAL", None)

    result = pari.PariData("pari_galpol", "galpol").is_present()

    assert isinstance(result, FeatureTestResult)
    assert result


def test_all_pari_data_features_have_doctest_tag_names():
    assert {feature.name for feature in pari.all_features()} == {
        "pari_elldata",
        "pari_galdata",
        "pari_galpol",
        "pari_nftables",
        "pari_seadata",
    }
