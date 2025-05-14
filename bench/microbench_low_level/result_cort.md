# Microbenchmark cort

We measure the performance for this function:

```python
def cort(arr):
    return _cort(arr, arr)

def _cort(s1, s2):
    num = 0.0
    sum_square_x = 0.0
    sum_square_y = 0.0
    for t in range(len(s1) - 1):
        slope_1 = s1[t + 1] - s1[t]
        slope_2 = s2[t + 1] - s2[t]
        num += slope_1 * slope_2
        sum_square_x += slope_1 * slope_1
        sum_square_y += slope_2 * slope_2
    return num / (sqrt(sum_square_x * sum_square_y))
```

One can run the benchmarks with `make bench_cort`.

With PyPy3.7, I get:

```
bench cort
hostname: voyage
{'cache_tag': 'pypy37',
 'version': sys.pypy_version_info(major=7, minor=3, micro=7, releaselevel='final', serial=0)}
list                          : 4.29e-05 s (  1.8 * Julia)
piconumpy.purepy              : 4.12e-05 s (  1.7 * Julia)
numpy                         : 4.77e-02 s (1975.5 * Julia)
piconumpy.hpy                 : 1.46e-03 s ( 60.5 * Julia)
piconumpy.cpython_capi        : 6.96e-03 s (288.5 * Julia)
```

With CPython:

```
bench cort
hostname: voyage
{'cache_tag': 'cpython-39',
 'version': sys.version_info(major=3, minor=9, micro=7, releaselevel='final', serial=0)}
list                          : 4.42e-03 s (183.4 * Julia)
piconumpy.purepy              : 1.04e-02 s (430.0 * Julia)
numpy                         : 9.76e-03 s (404.4 * Julia)
piconumpy.hpy                 : 5.66e-03 s (234.7 * Julia)
piconumpy.cpython_capi        : 4.77e-03 s (197.7 * Julia)
```

With Python 3.8.5 (GraalVM CE Native 21.3.0)

```
bench cort
hostname: voyage
{'cache_tag': 'graalpython-38',
 'version': sys.version_info(major=3, minor=8, micro=5, releaselevel='alpha', serial=0)}
list                          : 2.44e-05 s (  1.0 * Julia)
piconumpy.purepy              : 3.13e-05 s (  1.3 * Julia)
numpy                         : ImportError numpy
piconumpy.hpy                 : 1.69e-04 s (  7.0 * Julia)
piconumpy.cpython_capi        : 3.55e-04 s ( 14.7 * Julia)
```
