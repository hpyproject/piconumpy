# PicoNumpy

[![Build Status](https://travis-ci.org/paugier/piconumpy.svg?branch=master)](https://travis-ci.org/paugier/piconumpy)

**An experiment about Numpy and HPy**

The C API of CPython is one of the cause of the success of Python in scientific
computing. In particular, Numpy (and all the Python scientific stack) is built on top of
this API. However, some characteristics of this API start to be an issue for the future
of scientific Python (see [1], [2], [HPy]).

[HPy] is a very ambitious and promising project to design a new and better C API for
interacting with Python interpreters. It should allow people to write Python extensions
efficient on different interpreters (CPython, PyPy, Jython, IronPython, GraalPython,
RustPython, etc.).

PyPy would be especially useful for some scientific applications. For example for
Integration and ODEs
([scipy.integrate](https://docs.scipy.org/doc/scipy/reference/integrate.html)), for which
there are a lot of callbacks of very small functions. This repository contains
[a tiny benchmark](bench/without_numpy) showing that as long as Numpy is not used, PyPy
is very efficient for such task. Unfortunately, as soon as Numpy is used, PyPy becomes
very slow!

With PicoNumpy, I'd like to study if [HPy] could help for codes using Numpy and callbacks
of small Python functions.

We start by a [simple but realistic benchmark](bench/bench_array1d.py) (the slow loops
only involve pure-Python and very simple Numpy). We then wrote a tiny ("pico")
implementation of a Numpy like object (just sufficient to run the benchmark).

The next task is to reimplement PicoNumpy using [HPy] and to check if PyPy could
efficiently accelerate [our main benchmark](bench/bench_array1d.py).

PicoNumpy is really tiny. It just provides an `array` class (one-dimensional) supporting:

- Instantiation from a list of floats
- Element-wise multiplication and division by a float
- Element-wise addition (of 2 arrays)
- Indexing
- `len`

A good acceleration by PyPy of our example would be a great proof that the scientific
Python community has to invest time and energy on [HPy].

In the script [bench_array1d.py](bench/bench_array1d.py), Transonic is used for the
benchmark and comparison. With Transonic-Pythran, we typically get a 50 speed-up compared
to CPython (and ~400 versus PyPy, which is still very slow for such codes using Numpy).

## Install and run the benchmarks

`pip install -e .[full]` should build and install the package in editable mode and all
dependencies necessary for testing, benchmarking and profiling.

For the benchmarks, Julia is used for a good comparison point so the command `julia` has
to be available. Different benchmarks can be run with

```sh
cd bench
make clean
make bench_hpy
make bench_full
```

The benchmark code can be profiled for the different piconumpy implementations with the
commands (you need gprof2dot and graphviz):

```bash
cd bench
make profile METHOD="cpython-c-api"
make profile METHOD="purepy_array"
make profile METHOD="purepy"
make profile METHOD="cython"
```

### Notes on PyPy

PyPy can be downloaded with UV or manually (for example from
<https://buildbot.pypy.org/nightly/> for a nightly build).

With UV, one can run

```sh
uv python install pypy
```

and then get the path towards `pypy` executable with:

```sh
uv python find pypy
```

which can give something like
`~/.local/share/uv/python/pypy-3.11.11-linux-x86_64-gnu/bin/pypy`.

Then, you should be able to create a virtual environment, activate it and build-install
PicoNumpy with

```bash
cd ~/dev/piconumpy
$(uv python find pypy) -m venv .venv_pypy --upgrade-deps
. .venv_pypy/bin/activate
pip install -e .[full]
```

and run the benchmarks with:

```bash
cd bench
make clean
make bench_hpy
make bench_full
```

Note that one can check which HPy version is vendored with PyPy:

```bash
python -c "import hpy.universal as u; print(u.get_version())"
```

### Notes on GraalPy

GraalPy can be downloaded with UV with

```sh
uv python install graalpy
```

Then, one can run

```sh
cd ~/dev/piconumpy
# cannot use --upgrade-deps because pip is patched for GraalPy
$(uv python find graalpy) -m venv .venv_graalpy
. .venv_graalpy/bin/activate
# we don't try to run the full benchmarks using Pythran on GraalPy
pip install -e .[test,profile]
```

and run the benchmarks with:

```bash
cd bench
make clean
make bench_hpy
```

## Few results

### Full benchmarks

- With CPython

```
{'cache_tag': 'cpython-311',
 'version': sys.version_info(major=3, minor=11, micro=2, releaselevel='final', serial=0)}
hostname: meige7ltpa212
Julia                      :     1 * norm = 0.0129 s
PicoNumpy (CPython C-API)  :  6.55 * norm
PicoNumpy (HPy CPy ABI)    :  7.46 * norm
PicoNumpy (HPy Universal)  :  7.92 * norm
Transonic-Pythran          : 0.581 * norm
Numpy                      :  27.1 * norm
PicoNumpy (purepy)         :  18.8 * norm
PicoNumpy (purepy_array)   :  31.7 * norm
PicoNumpy (Cython)         :  23.3 * norm
```

- With PyPy3

```
{'cache_tag': 'pypy311',
 'version': sys.pypy_version_info(major=7, minor=3, micro=19, releaselevel='final', serial=0)}
hostname: meige7ltpa212
Julia                      :     1 * norm = 0.0129 s
PicoNumpy (CPython C-API)  :  35.5 * norm
PicoNumpy (HPy Universal)  :  44.7 * norm
Transonic-Pythran          : 0.609 * norm
Numpy                      :   168 * norm
PicoNumpy (purepy)         :  2.98 * norm
PicoNumpy (purepy_array)   :   8.7 * norm
PicoNumpy (Cython)         :   288 * norm
```

Discussion: PyPy with HPy universal is really too slow (44.7x slower than Julia, 6x slower than
CPython with its C-API and even a bit slower that PyPy with cpyext!). This is a big issue
for HPy!

A reasonable target would be as fast as CPython with its C-API...

Profiling shows that the issue is related to slow element-wise operations as in the micro-benchmark

```sh
cd microbench_low_level
make bench_element_wise
```

- With CPython

```sh
bench element_wise
hostname: meige7ltpa212
{'cache_tag': 'cpython-311',
 'version': sys.version_info(major=3, minor=11, micro=2, releaselevel='final', serial=0)}
piconumpy.purepy              : 7.88e-06 s ( 21.9 * Julia)
numpy                         : 7.88e-06 s ( 21.9 * Julia)
piconumpy.hpy (universal)     : 1.34e-06 s (  3.7 * Julia)
piconumpy.cpython_capi        : 6.12e-07 s (  1.7 * Julia)
```

- With PyPy3

```sh
bench element_wise
hostname: meige7ltpa212
{'cache_tag': 'pypy311',
 'version': sys.pypy_version_info(major=7, minor=3, micro=19, releaselevel='final', serial=0)}
piconumpy.purepy              : 1.46e-06 s (  4.1 * Julia)
numpy                         : 4.39e-05 s (121.9 * Julia)
piconumpy.hpy (universal)     : 4.27e-06 s ( 11.9 * Julia)
piconumpy.cpython_capi        : 1.84e-06 s (  5.1 * Julia)
```

### Simpler benchmarks (bench/bench_cpy_vs_hpy.py)

- With CPython

```
{'cache_tag': 'cpython-311',
 'version': sys.version_info(major=3, minor=11, micro=2, releaselevel='final', serial=0)}
hostname: meige7ltpa212
Julia:           0.013 seconds
CPython C-API:   0.084 seconds ( 6.5 * Julia)
HPy [Universal]: 0.102 seconds ( 7.9 * Julia)
HPy [CPy ABI]:   0.096 seconds ( 7.4 * Julia)
```

- With PyPy3

```
{'cache_tag': 'pypy311',
 'version': sys.pypy_version_info(major=7, minor=3, micro=19, releaselevel='final', serial=0)}
hostname: meige7ltpa212
Julia:           0.013 seconds
CPython C-API:   0.382 seconds (29.6 * Julia)
HPy [Universal]: 0.487 seconds (37.6 * Julia)
Python list:     0.037 seconds ( 2.9 * Julia)
```

- GraalPy

```
{'cache_tag': 'graalpy242-311',
 'version': sys.version_info(major=3, minor=11, micro=7, releaselevel='final', serial=0)}
hostname: meige7ltpa212
Julia:           0.013 seconds
CPython C-API:   2.123 seconds (164.2 * Julia)
HPy [Universal]: 1.541 seconds (119.2 * Julia)
Python list:     0.542 seconds (41.9 * Julia)
```

[1]: https://faster-cpython.readthedocs.io/
[2]: https://morepypy.blogspot.com/2019/12/hpy-kick-off-sprint-report.html
[hpy]: https://github.com/hpyproject/hpy
