from .test_cpython_capi import Tests as _Tests


class Tests(_Tests):
    from . import purepy as piconumpy
