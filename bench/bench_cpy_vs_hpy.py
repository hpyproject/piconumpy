import sys
import time
import random
from math import pi, cos, sin
from pathlib import Path

here = Path(__file__).absolute().parent

def my_randn(mod, n):
    result = mod.empty(n)
    for i in range(n):
        result[i] = random.normalvariate(0, 1)
    return result

IS_PYPY = hasattr(sys, 'pypy_version_info')

def runge_kutta_step(mod, f, x0, dt, t=None):
    k1 = f(mod, t, x0) * dt
    k2 = f(mod, t, x0 + k1 / 2) * dt
    k3 = f(mod, t, x0 + k2 / 2) * dt
    k4 = f(mod, t, x0 + k3) * dt
    # workaround for a pypy bug
    #x_new = x0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    x_new = x0 + (k1 + (k2 * 2) + (k3 * 2) + k4) / 6
    return x_new


def board(mod,t, X_0):
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
    start = time.time()
    solver(mod, board, x_init, y_init, u_init, v_init, 0.01, n_time)
    end = time.time()
    return end-start

N_SLEDS = 100
N_TIME = 2000

def import_piconumpy_hpy_universal():
    import hpy.universal
    class spec:
        name = '_piconumpy_hpy'
        origin = str(here.parent / 'piconumpy/_piconumpy_hpy.hpy.so')
    return hpy.universal.load_from_spec(spec)

def main():

    import piconumpy._piconumpy_cpython_capi as pnp_capi
    t = bench(pnp_capi, N_SLEDS, N_TIME)
    print(f'CPython C-API:   {t:.2f} seconds')

    if not IS_PYPY:
        import piconumpy._piconumpy_hpy as pnp_hpy
        t = bench(pnp_hpy, N_SLEDS, N_TIME)
        print(f'HPy [CPy ABI]:   {t:.2f} seconds')

    pnp_hpy_universal = import_piconumpy_hpy_universal()
    t = bench(pnp_hpy_universal, N_SLEDS, N_TIME)
    print(f'HPy [Universal]: {t:.2f} seconds')


if __name__ == '__main__':
    main()
