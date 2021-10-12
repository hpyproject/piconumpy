import sys
from time import perf_counter
import random
from math import pi, cos, sin
from pathlib import Path
from pprint import pprint

here = Path(__file__).absolute().parent


def my_randn(mod, n):
    result = mod.empty(n)
    for i in range(n):
        result[i] = random.normalvariate(0, 1)
    return result


IS_PYPY = hasattr(sys, "pypy_version_info")


def runge_kutta_step(mod, f, x0, dt, t=None):
    k1 = f(mod, t, x0) * dt
    k2 = f(mod, t, x0 + k1 / 2) * dt
    k3 = f(mod, t, x0 + k2 / 2) * dt
    k4 = f(mod, t, x0 + k3) * dt
    # workaround for a pypy bug
    # see https://foss.heptapod.net/pypy/pypy/-/issues/3509
    # x_new = x0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    x_new = x0 + (k1 + k2 * 2 + k3 * 2 + k4) / 6
    return x_new


def board(mod, t, X_0):
    x0 = X_0[0]
    y0 = X_0[1]
    u0 = X_0[2]
    v0 = X_0[3]

    g = 9.81
    c = 0.5
    a = 0.25
    b = 0.5
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

    return mod.array([u0, v0, dU, dV])


def solver(mod, f, x0, y0, u0, v0, dt, N_t, b=0.5):
    solutions = []
    for k in range(len(x0)):
        values_one_step = mod.array([x0[k], y0[k], u0[k], v0[k]])
        for _ in range(N_t):
            values_one_step = runge_kutta_step(mod, f, values_one_step, dt, b)
        solutions.append(values_one_step)
    return solutions


def bench(mod, n_sleds, n_time):
    x_init = mod.zeros(n_sleds)
    y_init = my_randn(mod, n_sleds)
    v_init = mod.zeros(n_sleds)
    u_init = mod.zeros(n_sleds)
    for i in range(n_sleds):
        u_init[i] += 3.5
    times = []
    for _ in range(20):
        start = perf_counter()
        solver(mod, board, x_init, y_init, u_init, v_init, 0.01, n_time)
        times.append(perf_counter() - start)

    times.sort()
    return times[len(times) // 2]


N_SLEDS = 100
N_TIME = 200


def import_piconumpy_hpy_universal():
    import hpy.universal

    return hpy.universal.load(
        "_piconumpy_hpy", str(here.parent / "piconumpy/_piconumpy_hpy.hpy.so")
    )


def main():

    import piconumpy._piconumpy_cpython_capi as pnp_capi

    pprint({key: sys.implementation.__dict__[key] for key in ("cache_tag", "version")})

    tmp_result_julia = Path("tmp_result_julia.txt")
    if tmp_result_julia.exists():
        with open("tmp_result_julia.txt") as file:
            norm = float(file.read())
        end = ""
        print(f"Julia:           {norm:.3f} seconds")
    else:
        norm = False
        end = "\n"

    t_capi = bench(pnp_capi, N_SLEDS, N_TIME)
    print(f"CPython C-API:   {t_capi:.3f} seconds", end=end)
    if norm:
        print(f" ({t_capi/norm:4.1f} * Julia)")

    pnp_hpy_universal = import_piconumpy_hpy_universal()
    t_hpy_univ = bench(pnp_hpy_universal, N_SLEDS, N_TIME)
    print(f"HPy [Universal]: {t_hpy_univ:.3f} seconds", end=end)

    if norm:
        print(f" ({t_hpy_univ/norm:4.1f} * Julia)")

    if not IS_PYPY:
        import piconumpy._piconumpy_hpy as pnp_hpy

        t_hpy_cpy_abi = bench(pnp_hpy, N_SLEDS, N_TIME)
        print(f"HPy [CPy ABI]:   {t_hpy_cpy_abi:.3f} seconds", end=end)

        if norm:
            print(f" ({t_hpy_cpy_abi/norm:4.1f} * Julia)")

    if IS_PYPY:
        import piconumpy.purepy as pnp_with_list

        t_with_list = bench(pnp_with_list, N_SLEDS, N_TIME)
        print(f"Python list:     {t_with_list:.3f} seconds", end=end)

        if norm:
            print(f" ({t_with_list/norm:4.1f} * Julia)")


if __name__ == "__main__":
    main()
