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
import sys
import numpy as np
from piconumpy import array
from math import pi, cos, sin

IS_PYPY = hasattr(sys, 'pypy_version_info')
"""
    + code_functions
    + """

from piconumpy.bench import timeit_verbose

from bench_array1d import bench as bench_numpy, bench_pythran

from tmp_hpy_universal import bench as bench_hpy_universal
from tmp_purepy import bench as bench_piconumpy_purepy
from tmp_purepy_array import bench as bench_piconumpy_purepy_array
from tmp_cython import bench as bench_cython

if not IS_PYPY:
    from tmp_hpy import bench as bench_hpy

# get norm from Julia benchmark
with open("tmp_result_julia.txt") as file:
    norm = float(file.read())

max_length_name = len("piconumpy (CPython C-API)") + 2

fmt_name = f"{{:{max_length_name}s}}"
name = fmt_name.format("Julia")
print(f"{name}:     1 * norm = {norm:4.3g} s")

n_sleds = 10
n_time = 200

g = locals()

def timeit(name_func, name):
    return timeit_verbose(
        name_func + "(n_sleds, n_time)",
        globals=g,
        name=name,
        print_time=False,
        norm=norm,
        max_length_name=max_length_name,
    )

timeit("bench", name="PicoNumpy (CPython C-API)")
if not IS_PYPY:
    timeit("bench_hpy", name="PicoNumpy (HPy CPy ABI)")
timeit("bench_hpy_universal", name="PicoNumpy (HPy Universal)")
timeit("bench_pythran", name="Transonic-Pythran")
timeit("bench_numpy", name="Numpy")
timeit(
    "bench_piconumpy_purepy", name="PicoNumpy (purepy)",
)
timeit(
    "bench_piconumpy_purepy_array", name="PicoNumpy (purepy_array)",
)
timeit("bench_cython", name="PicoNumpy (Cython)")
"""
)

with open("tmp.py", "w") as file:
    file.write(code)
