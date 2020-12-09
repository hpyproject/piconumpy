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
