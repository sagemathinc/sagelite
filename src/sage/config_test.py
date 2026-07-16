import sage.config
from sage.config import get_include_dirs


def test_noneditable_install_has_no_editable_root(monkeypatch):
    monkeypatch.setattr(sage.config, "is_editable_install", lambda: False)
    assert sage.config.get_editable_root() is None


def test_cython_metaclass_header_found():
    dirs = get_include_dirs()
    assert any(
        (dir / "sage" / "cpython" / "cython_metaclass.h").is_file() for dir in dirs
    )


def test_get_include_dirs_returns_existing_dirs():
    dirs = get_include_dirs()
    for dir in dirs:
        assert dir.is_dir(), f"Directory {dir} does not exist"
