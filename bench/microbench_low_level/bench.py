import sys
from time import perf_counter
from pathlib import Path
from random import random
from math import sqrt, pi, sin, cos

try:
    method = sys.argv[1]
except IndexError:
    method = "purepy"

try:
    name_bench = sys.argv[2]
except IndexError:
    name_bench = "sum_loop"

try:
    size = sys.argv[3]
except IndexError:
    size = None

if method == "_piconumpy_hpy":
    from piconumpy.util_hpy import import_ext

    ext = import_ext()
    array = ext.array
elif method == "list":
    array = list
    if name_bench == "element_wise":
        sys.exit(0)

elif method == "numpy":

    try:
        import numpy as np
    except ImportError:
        print(f"{method:30s}: ImportError numpy")
        sys.exit(0)

    array = np.array
else:
    d = {}
    exec(f"from piconumpy.{method} import array", d)
    array = d["array"]
    if "piconumpy" not in method:
        method = f"piconumpy.{method}"

if "_piconumpy_" in method:
    method = method.replace("_piconumpy_", "piconumpy.")

if method.endswith("hpy"):
    method += " (universal)"

tmp_result_julia = Path(f"tmp/{name_bench}_julia.txt")
if tmp_result_julia.exists():
    with open(tmp_result_julia) as file:
        norm = float(file.read())
else:
    raise RuntimeError(
        f"{tmp_result_julia} does not exist. First execute with `make`"
    )


def sum_loop(arr):
    result = 0.0
    for value in arr:
        result += value
    return result


def sum_loop_index(arr):
    result = 0.0
    for index in range(5000):
        result += arr[index]
    return result


def init_zeros(arr):
    for index in range(len(arr)):
        arr[index] = 0.0


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


def cort(arr):
    return _cort(arr, arr)


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


def instantiate(arr):
    x = arr[0]
    result = array([x, 3 * x, 6 * x, 9 * x])
    result[0] = 2 * result[1]
    return result


def element_wise(arr):

    dt = 0.1
    x0 = arr

    k1 = x0 * dt
    k2 = (x0 + k1 / 2) * dt
    k3 = (x0 + k2 / 2) * dt
    k4 = (x0 + k3) * dt
    # workaround for a pypy bug
    # see https://foss.heptapod.net/pypy/pypy/-/issues/3509
    # x_new = x0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    x_new = x0 + (k1 + k2 * 2 + k3 * 2 + k4) / 6
    return x_new


compute_from_arr = locals()[name_bench]

if size is None:
    if name_bench.startswith("sum_loop") or name_bench == "cort":
        size = 10000
    else:
        size = 4

print(f"{method:30s}:", end="", flush=True)

# warming during ~ 1s
data_as_list = [random() for _ in range(size)]
arr = array(data_as_list)
t_start = perf_counter()
while perf_counter() - t_start < 1.0:
    compute_from_arr(arr)


def median(sequence):
    tmp = sorted(sequence)
    return tmp[len(tmp) // 2]


# measure during ~ 4s
t0 = perf_counter()
times = []
while perf_counter() - t0 < 4.0:
    data_as_list = [random() for _ in range(size)]
    arr = array(data_as_list)
    t_start = perf_counter()
    compute_from_arr(arr)
    times.append(perf_counter() - t_start)

time = median(times)
print(f" {time:.2e} s ({time / norm:5.1f} * Julia)")
