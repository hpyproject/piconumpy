import sys

import pytest

from .util_hpy import import_ext

from .test_cpython_capi import Tests as _Tests

try:
    piconumpy_universal = import_ext()
except ImportError:
    piconumpy_universal = False


@pytest.mark.skipif(
    not piconumpy_universal, reason="ImportError piconumpy HPy Universal"
)
class TestsCPyABI(_Tests):
    piconumpy = piconumpy_universal

    def test_multiply(self):
        if sys.implementation.name == "pypy":
            pytest.xfail("Expected failure with PyPy (but should work)")

        super().test_multiply()

    def test_add(self):
        if sys.implementation.name == "pypy":
            pytest.xfail("Expected failure with PyPy (but should work)")

        super().test_add()
