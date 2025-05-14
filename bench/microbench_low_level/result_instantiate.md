# Microbenchmark instantiate

We measure the performance for this function:

```python
def instantiate(arr):
    x = arr[0]
    result = array([x, 3 * x, 6 * x, 9 * x])
    result[0] = 2 * result[1]
    return result
```

One can run the benchmarks with `make bench_instantiate`.

With PyPy3.7, I get:

```
bench instantiate
hostname: meige8pcpa79
{'cache_tag': 'pypy37',
 'version': sys.pypy_version_info(major=7, minor=3, micro=7, releaselevel='final', serial=0)}
list                          : 1.13e-07 s (  0.9 * Julia)
piconumpy.purepy              : 8.50e-08 s (  0.7 * Julia)
numpy                         : ImportError numpy
piconumpy.hpy                 : 1.69e-06 s ( 13.1 * Julia)
piconumpy.cpython_capi        : 1.53e-05 s (118.3 * Julia)
```

With CPython:

```
bench instantiate
hostname: meige8pcpa79
{'cache_tag': 'cpython-39',
 'version': sys.version_info(major=3, minor=9, micro=7, releaselevel='final', serial=0)}
list                          : 1.19e-06 s (  9.2 * Julia)
piconumpy.purepy              : 2.59e-06 s ( 20.0 * Julia)
numpy                         : 3.63e-06 s ( 28.1 * Julia)
piconumpy.hpy                 : 1.84e-06 s ( 14.3 * Julia)
piconumpy.cpython_capi        : 1.35e-06 s ( 10.5 * Julia)
```

With Python 3.8.5 (GraalVM CE Native 21.3.0)

```
bench instantiate
hostname: meige8pcpa79
{'cache_tag': 'graalpython-38',
 'version': sys.version_info(major=3, minor=8, micro=5, releaselevel='alpha', serial=0)}
list                          : 4.16e-06 s ( 32.3 * Julia)
piconumpy.purepy              : 4.15e-06 s ( 32.2 * Julia)
numpy                         : ImportError numpy
piconumpy.hpy                 : 7.32e-06 s ( 56.8 * Julia)
piconumpy.cpython_capi        : 9.68e-06 s ( 75.0 * Julia)
```
