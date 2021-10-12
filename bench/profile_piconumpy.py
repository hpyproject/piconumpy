import sys

import cProfile
import pstats

import bench_array1d
import tmp_purepy
import tmp_purepy_array
import tmp_cython
import tmp_hpy_universal

methods = {
    "cpython-c-api": bench_array1d,
    "purepy": tmp_purepy,
    "purepy_array": tmp_purepy_array,
    "cython": tmp_cython,
    "universal": tmp_hpy_universal,
}

module = methods.get(sys.argv[-1], bench_array1d)

n_sleds = 10
n_time = 200

cProfile.runctx(
    "module.bench(n_sleds, n_time)", globals(), locals(), "tmp.pstats"
)

s = pstats.Stats("tmp.pstats")
s.strip_dirs().sort_stats("time").print_stats(10)
