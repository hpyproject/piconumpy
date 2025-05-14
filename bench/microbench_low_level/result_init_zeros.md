# Microbenchmark sum_init_zeros

We measure the performance for this function:

```python
def init_zeros(arr):
    for index in range(len(arr)):
        arr[index] = 0.0
```

One can run the benchmarks with `make bench_init_zeros`.

With PyPy3.7, I get:

```
bench init_zeros
hostname: voyage
{'cache_tag': 'pypy37',
 'version': sys.pypy_version_info(major=7, minor=3, micro=7, releaselevel='final', serial=0)}
list                          : 2.63e-05 s (  5.4 * Julia)
piconumpy.purepy              : 2.99e-05 s (  6.1 * Julia)
numpy                         : 1.17e-02 s (2403.5 * Julia)
piconumpy.hpy                 : 4.58e-04 s ( 94.1 * Julia)
piconumpy.cpython_capi        : 8.46e-04 s (173.6 * Julia)
```

With CPython:

```
bench init_zeros
hostname: voyage
{'cache_tag': 'cpython-39',
 'version': sys.version_info(major=3, minor=9, micro=7, releaselevel='final', serial=0)}
list                          : 5.34e-04 s (109.6 * Julia)
piconumpy.purepy              : 2.03e-03 s (417.4 * Julia)
numpy                         : 1.17e-03 s (239.3 * Julia)
piconumpy.hpy                 : 7.51e-04 s (154.1 * Julia)
piconumpy.cpython_capi        : 5.44e-04 s (111.5 * Julia)
```

With Python 3.8.5 (GraalVM CE Native 21.3.0)

```
bench init_zeros
hostname: voyage
{'cache_tag': 'graalpython-38',
 'version': sys.version_info(major=3, minor=8, micro=5, releaselevel='alpha', serial=0)}
list                          : 1.37e-05 s (  2.8 * Julia)
piconumpy.purepy              : 1.93e-05 s (  4.0 * Julia)
numpy                         : ImportError numpy
piconumpy.hpy                 : 4.68e-05 s (  9.6 * Julia)
piconumpy.cpython_capi        : 1.74e-04 s ( 35.8 * Julia)
```
