import pytest

from .test_cpython_capi import Tests as _Tests

try:
    from . import _piconumpy_hpy as piconumpy_cpy_abi
except ImportError:
    piconumpy_cpy_abi = False


@pytest.mark.skipif(not piconumpy_cpy_abi, reason="ImportError _piconumpy_hpy")
class TestsCPyABI(_Tests):
    piconumpy = piconumpy_cpy_abi
