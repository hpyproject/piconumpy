with open("bench_array1d.py") as file:
    code = file.read()

code = code.split("# begin code functions (don't remove this line)")[1]
code_functions = code.split("# end code functions (don't remove this line)")[0]


def create_tmp_file(name_module):

    if name_module == "_piconumpy_hpy_universal":
        code_import = """
from piconumpy.util_hpy import import_ext
ext = import_ext()
array = ext.array
"""
    else:
        code_import = f"from piconumpy.{name_module} import array"

    code = (
        f"""
from math import pi, cos, sin
import numpy as np
{code_import}
"""
        + code_functions
    )

    if name_module.startswith("_piconumpy_"):
        name = name_module[len("_piconumpy_") :]
    else:
        name = name_module

    with open(f"tmp_{name}.py", "w") as file:
        file.write(code)


create_tmp_file("_piconumpy_hpy_universal")
create_tmp_file("purepy")
create_tmp_file("purepy_array")
create_tmp_file("_piconumpy_cython")
create_tmp_file("_piconumpy_hpy")


code = (
    """
import socket
import sys

from math import pi, cos, sin
from pathlib import Path
from pprint import pprint

import numpy as np

from piconumpy import array

IS_CPY = sys.implementation.name == "cpython"

"""
    + code_functions
    + """

from piconumpy.bench import timeit_verbose

from bench_array1d import bench as bench_numpy, bench_pythran

from tmp_hpy_universal import bench as bench_hpy_universal
from tmp_purepy import bench as bench_piconumpy_purepy
from tmp_purepy_array import bench as bench_piconumpy_purepy_array
from tmp_cython import bench as bench_cython

if IS_CPY:
    from tmp_hpy import bench as bench_hpy

pprint({key: sys.implementation.__dict__[key] for key in ("cache_tag", "version")})
print(f"hostname: {socket.gethostname()}")
# get norm from Julia benchmark

path_julia_result = Path("tmp_result_julia.txt")
assert path_julia_result.exists()
norm = float(path_julia_result.read_text())

max_length_name = len("piconumpy (CPython C-API)") + 2

fmt_name = f"{{:{max_length_name}s}}"
name = fmt_name.format("Julia")
print(f"{name}:     1 * norm = {norm:4.3g} s")

n_sleds = 100
n_time = 200

g = locals()

def timeit(name_func, name, total_duration=2):
    return timeit_verbose(
        name_func + "(n_sleds, n_time)",
        globals=g,
        name=name,
        print_time=False,
        norm=norm,
        max_length_name=max_length_name,
        total_duration=total_duration,
    )

timeit("bench", name="PicoNumpy (CPython C-API)")
if IS_CPY:
    timeit("bench_hpy", name="PicoNumpy (HPy CPy ABI)")
timeit("bench_hpy_universal", name="PicoNumpy (HPy Universal)")
timeit("bench_pythran", name="Transonic-Pythran")
try:
    timeit("bench_numpy", name="Numpy", total_duration=8)
except RuntimeError:
    print("Skip bench_numpy because it's too slow")
timeit(
    "bench_piconumpy_purepy", name="PicoNumpy (purepy)",
)
timeit(
    "bench_piconumpy_purepy_array", name="PicoNumpy (purepy_array)",
)
try:
    timeit("bench_cython", name="PicoNumpy (Cython)", total_duration=8)
except RuntimeError:
    print("Skip bench_cython because it's too slow")
"""
)

with open("tmp.py", "w") as file:
    file.write(code)
