# Microbenchmark sum_loop_index

We measure the performance for this function:

```python
def sum_loop_index(arr):
    result = 0.0
    for index in range(5000):
        result += arr[index]
    return result
```

One can run the benchmarks with `make bench_sum_loop_index`.

With PyPy3.7, I get:

```
bench sum_loop_index
hostname: voyage
{'cache_tag': 'pypy37',
 'version': sys.pypy_version_info(major=7, minor=3, micro=7, releaselevel='final', serial=0)}
list                          : 1.19e-05 s (  2.0 * Julia)
piconumpy.purepy              : 1.64e-05 s (  2.8 * Julia)
numpy                         : 4.18e-03 s (711.4 * Julia)
piconumpy.hpy                 : 1.73e-04 s ( 29.4 * Julia)
piconumpy.cpython_capi        : 8.44e-04 s (143.8 * Julia)
```

With CPython:

```
bench sum_loop_index
hostname: voyage
{'cache_tag': 'cpython-39',
 'version': sys.version_info(major=3, minor=9, micro=7, releaselevel='final', serial=0)}
list                          : 3.91e-04 s ( 66.5 * Julia)
piconumpy.purepy              : 1.11e-03 s (188.3 * Julia)
numpy                         : 8.93e-04 s (152.1 * Julia)
piconumpy.hpy                 : 5.42e-04 s ( 92.3 * Julia)
piconumpy.cpython_capi        : 4.17e-04 s ( 71.0 * Julia)
```

With Python 3.8.5 (GraalVM CE Native 21.3.0)

```
bench sum_loop_index
hostname: voyage
{'cache_tag': 'graalpython-38',
 'version': sys.version_info(major=3, minor=8, micro=5, releaselevel='alpha', serial=0)}
list                          : 1.36e-05 s (  2.3 * Julia)
piconumpy.purepy              : 1.81e-05 s (  3.1 * Julia)
numpy                         : ImportError numpy
piconumpy.hpy                 : 3.68e-05 s (  6.3 * Julia)
piconumpy.cpython_capi        : 1.08e-04 s ( 18.5 * Julia)
```
