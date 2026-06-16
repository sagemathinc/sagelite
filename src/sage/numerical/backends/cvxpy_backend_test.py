import pytest
from sage.structure.sage_object import SageObject
from sage.numerical.backends.generic_backend_test import GenericBackendTests
from sage.numerical.backends.generic_backend import GenericBackend
from sage.numerical.mip import MixedIntegerLinearProgram


pytest.importorskip("cvxpy")


class TestCVXPYBackend(GenericBackendTests):

    @pytest.fixture
    def backend(self) -> GenericBackend:
        return MixedIntegerLinearProgram(solver="CVXPY").get_backend()

    def test_sage_unittest_testsuite(self, sage_object: SageObject):
        # CVXPYBackend intentionally does not implement the full GenericBackend
        # mutation interface.
        from sage.misc.sage_unittest import TestSuite
        TestSuite(sage_object).run(
            verbose=True,
            raise_on_failure=True,
            skip=(
                "_test_pickling",
                "_test_add_col",
                "_test_copy_some_mips",
                "_test_solve",
                "_test_solve_trac_18572",
            ),
        )
