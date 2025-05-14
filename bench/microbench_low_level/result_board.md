# Microbenchmark board

We measure the performance for this function:

```python
def board(X_0):
    x0 = X_0[0]
    y0 = X_0[1]
    u0 = X_0[2]
    v0 = X_0[3]

    g = 9.81
    b = 0.5
    a = 0.25
    c = 0.5
    p = (2 * pi) / 10.0
    q = (2 * pi) / 4.0

    H_x = -a + b * p * sin(p * x0) * cos(q * y0)
    H_xx = b * p ** 2 * cos(p * x0) * cos(q * y0)
    H_y = b * q * cos(p * x0) * sin(q * y0)
    H_yy = b * q ** 2 * cos(p * x0) * cos(q * y0)
    H_xy = -b * q * p * sin(p * x0) * sin(q * y0)

    F = (g + H_xx * u0 ** 2 + 2 * H_xy * u0 * v0 + H_yy * v0 ** 2) / (
        1 + H_x ** 2 + H_y ** 2
    )

    dU = -F * H_x - c * u0
    dV = -F * H_y - c * v0

    return array([u0, v0, dU, dV])
```

One can run the benchmarks with `make bench_board`.

With PyPy3.7, I get:

```
bench board
hostname: voyage
{'cache_tag': 'pypy37',
 'version': sys.pypy_version_info(major=7, minor=3, micro=7, releaselevel='final', serial=0)}
list                          : 3.21e-07 s (  0.9 * Julia)
piconumpy.purepy              : 1.37e-05 s ( 36.9 * Julia)
numpy                         : 1.18e-04 s (316.6 * Julia)
piconumpy.hpy                 : 1.26e-05 s ( 33.8 * Julia)
piconumpy.cpython_capi        : 5.52e-05 s (148.6 * Julia)
```

With CPython:

```
bench board
hostname: voyage
{'cache_tag': 'cpython-39',
 'version': sys.version_info(major=3, minor=9, micro=7, releaselevel='final', serial=0)}
list                          : 5.16e-06 s ( 13.9 * Julia)
piconumpy.purepy              : 8.04e-06 s ( 21.6 * Julia)
numpy                         : 1.01e-05 s ( 27.1 * Julia)
piconumpy.hpy                 : 5.90e-06 s ( 15.9 * Julia)
piconumpy.cpython_capi        : 5.56e-06 s ( 15.0 * Julia)
```

With Python 3.8.5 (GraalVM CE Native 21.3.0)

```
bench board
hostname: voyage
{'cache_tag': 'graalpython-38',
 'version': sys.version_info(major=3, minor=8, micro=5, releaselevel='alpha', serial=0)}
list                          : 1.15e-05 s ( 30.9 * Julia)
piconumpy.purepy              : 1.74e-05 s ( 46.8 * Julia)
numpy                         : ImportError numpy
piconumpy.hpy                 : 4.91e-05 s (132.2 * Julia)
piconumpy.cpython_capi        : 6.19e-05 s (166.7 * Julia)
```
