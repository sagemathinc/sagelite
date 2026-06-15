# pylint: disable=missing-function-docstring,missing-class-docstring
import pytest

from sage.manifolds.differentiable.examples.euclidean import EuclideanSpace
from sage.manifolds.differentiable.manifold import DifferentiableManifold


def require_maxima_lib():
    try:
        import sage.interfaces.maxima_lib  # noqa: F401
    except ImportError as err:
        pytest.skip(f"requires Maxima library mode ({err})")


class TestR3VectorSpace:
    @pytest.fixture
    def manifold(self):
        require_maxima_lib()
        return EuclideanSpace(3)

    def test_trace_using_metric_works(self, manifold: DifferentiableManifold):
        metric = manifold.metric('g')
        assert metric.trace(using=metric) == manifold.scalar_field(3)
