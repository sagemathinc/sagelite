import pytest

import sage.all
from sage.manifolds.differentiable.examples.symplectic_space import (
    StandardSymplecticSpace,
)
from sage.manifolds.differentiable.symplectic_form import SymplecticForm


def require_maxima_lib():
    try:
        import sage.interfaces.maxima_lib  # noqa: F401
    except ImportError as err:
        pytest.skip(f"requires Maxima library mode ({err})")


class TestR2VectorSpace:
    @pytest.fixture
    def M(self):
        require_maxima_lib()
        return StandardSymplecticSpace(2, 'R2', symplectic_name='omega')

    @pytest.fixture
    def omega(self, M: StandardSymplecticSpace):
        return M.symplectic_form()

    def test_repr(self, M: StandardSymplecticSpace):
        assert str(M) == "Standard symplectic space R2"

    def test_display(self, omega: SymplecticForm):
        assert str(omega.display()) == r"omega = -dq∧dp"


class TestR4VectorSpace:
    @pytest.fixture
    def M(self):
        require_maxima_lib()
        return StandardSymplecticSpace(4, 'R4', symplectic_name='omega')

    @pytest.fixture
    def omega(self, M: StandardSymplecticSpace):
        return M.symplectic_form()

    def test_repr(self, M: StandardSymplecticSpace):
        assert str(M) == "Standard symplectic space R4"

    def test_display(self, omega: SymplecticForm):
        assert str(omega.display()) == r"omega = -dq1∧dp1 - dq2∧dp2"
