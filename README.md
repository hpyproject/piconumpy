# PicoNumpy

[![Build Status](https://travis-ci.org/paugier/piconumpy.svg?branch=master)](https://travis-ci.org/paugier/piconumpy)

**An experiment about Numpy and HPy**

The C API of CPython is one of the cause of the success of Python in scientific
computing. In particular, Numpy (and all the Python scientific stack) is built
on top of this API. However, some characteristics of this API start to be an
issue for the future of scientific Python (see [1], [2], [HPy]).

[1]: https://faster-cpython.readthedocs.io/
[2]: https://morepypy.blogspot.com/2019/12/hpy-kick-off-sprint-report.html
[HPy]: https://github.com/hpyproject/hpy

[HPy] is a very ambitious and promissing project to design a new and better C
API for interacting with Python interpreters. It should allow people to write
Python extensions efficient on different interpreters (CPython, PyPy, Jython,
IronPython, GraalPython, RustPython, etc.).

PyPy would be especially useful for some scientific applications. For example
for Integration and ODEs
([scipy.integrate](https://docs.scipy.org/doc/scipy/reference/integrate.html)),
for which there are a lot of callbacks of very small functions. This repository
contains [a tiny benchmark](bench/without_numpy) showing that as long as Numpy
is not used, PyPy is very efficient for such task. Unfortunately, as soon as
Numpy is used, PyPy becomes very slow!

[bench/without_numpy]: https://github.com/paugier/piconumpy/blob/master/bench/without_numpy/

With PicoNumpy, I'd like to study if [HPy] could help for codes using Numpy and
callbacks of small Python functions.

We start by a [simple but realistic benchmark](bench/bench_array1d.py) (the
slow loops only involve pure-Python and very simple Numpy). We then wrote a
tiny ("pico") implementation of a Numpy like object (just sufficient to run the
benchmark).

The next task is to reimplement PicoNumpy using [HPy] and to check if PyPy
could efficiently accelerate [our main benchmark](bench/bench_array1d.py).

PicoNumpy is really tiny. It just provides an `array` class (one-dimensional)
supporting:

- Instantiation from a list of floats
- Elementwise multiplication and division by a float
- Elementwise addition (of 2 arrays)
- Indexing
- `len`

A good acceleration by PyPy of our example would be a great proof that the
scientific Python community has to invest time and energy on [HPy].

In the script [bench_array1d.py](bench/bench_array1d.py), Transonic is used for
the benchmark and comparison. With Transonic-Pythran, we typically get a 50
speedup compared to CPython (and ~400 versus PyPy, which is still very slow for
such codes using Numpy).

[bench/bench_array1d.py]: https://github.com/paugier/piconumpy/blob/master/bench/bench_array1d.py

## Install and run the benchmarks

**Warning:** PicoNumpy now depends on HPy, which still has to be installed from
the [Git repository](https://github.com/hpyproject/hpy). For now, the
installation is a bit more complex that what is described here (more about this
[here](#more-precise-notes-on-how-to-install-and-run-the-benchmarks-with-PyPy)).

`make` should install the package in editable mode. `cd bench; make` should run
the benchmarks. For the benchmarks, Julia is used for a good comparison point
so the command `julia` has to be available.

For PyPy, the Makefiles are sensible to the environment variable `PYTHON`, so
you could do:

```bash
export PYTHON=pypy3
make
cd bench
make
```

The benchmark code can be profiled for the different implementations with the
commands (you need gprof2dot and graphviz):

```bash
cd bench
make profile METHOD="cpython-c-api"
make profile METHOD="purepy_array"
make profile METHOD="purepy"
make profile METHOD="cython"
```

### More precise notes on how to install and run the benchmarks with PyPy

Download and extract a nightly PyPy build
<https://buildbot.pypy.org/nightly/>. Add to the `PATH` environment variable
the path of the directory containing the `pypy` executable (something like
`~/opt/pypy-c-jit-101190-b661dc329618-linux64/bin`). Then, you should be able
to run:

```bash
pypy -m ensurepip
pypy -m pip install pip -U
pypy -m pip install numpy cython pytest transonic pythran
```

One can check which HPy version is vendored with PyPy:

```bash
pypy -c "import hpy.universal as u; print(u.get_version())"
```

gives `('0.0.3', '2196f14')`.

Now we can build-install PicoNumpy:

```bash
cd ~/Dev/piconumpy
pypy setup.py --hpy-abi=universal develop
```

And run the benchmarks with:

```bash
export PYTHON="pypy"
make clean
make bench_hpy
make
```

## Few results

As of today (12 October 2021), HPy is not yet ready for high performance, but at
least (with HPy 0.0.3) it runs !

### At home (Intel(R) Core(TM) i5-8400 CPU @ 2.80GHz)

- With CPython

```
Julia                      :     1 * norm = 0.0171 s
PicoNumpy (CPython C-API)  :  11.1 * norm
PicoNumpy (HPy CPy ABI)    :  11.6 * norm
PicoNumpy (HPy Universal)  :  12.1 * norm
Transonic-Pythran          : 0.537 * norm
Numpy                      :  33.8 * norm
PicoNumpy (purepy)         :  43.7 * norm
PicoNumpy (purepy_array)   :  44.8 * norm
PicoNumpy (Cython)         :  33.9 * norm
```

- With PyPy3

```
Julia                      :     1 * norm = 0.0171 s
PicoNumpy (CPython C-API)  :  39.2 * norm
PicoNumpy (HPy Universal)  :  13.1 * norm
Transonic-Pythran          : 0.562 * norm
Numpy                      :   286 * norm
PicoNumpy (purepy)         :  5.59 * norm
PicoNumpy (purepy_array)   :  7.41 * norm
PicoNumpy (Cython)         :   282 * norm
```

#### Simpler benchmarks (bench/bench_cpy_vs_hpy.py)

- With CPython

```
{'cache_tag': 'cpython-39',
 'version': sys.version_info(major=3, minor=9, micro=6, releaselevel='final', serial=0)}
CPython C-API:   0.193 seconds (11.2 * Julia)
HPy [Universal]: 0.208 seconds (12.1 * Julia)
HPy [CPy ABI]:   0.201 seconds (11.7 * Julia)
```

- With PyPy3

```
{'cache_tag': 'pypy37',
 'version': sys.pypy_version_info(major=7, minor=3, micro=6, releaselevel='final', serial=0)}
CPython C-API:   0.592 seconds (34.6 * Julia)
HPy [Universal]: 0.207 seconds (12.1 * Julia)
Python list:     0.093 seconds ( 5.4 * Julia)
```
