import numpy as np

from numpy import array
from math import pi, cos, sin

from transonic import jit

# begin code functions (don't remove this line)


def runge_kutta_step(f, x0, dt, t=None):
    k1 = f(t, x0) * dt
    k2 = f(t, x0 + k1 / 2) * dt
    k3 = f(t, x0 + k2 / 2) * dt
    k4 = f(t, x0 + k3) * dt
    # workaround for a pypy bug
    #x_new = x0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    x_new = x0 + (k1 + (k2 * 2) + (k3 * 2) + k4) / 6
    return x_new


def board(t, X_0):
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

    return array([u0, v0, dU, dV])


def solver(f, x0, y0, u0, v0, dt, N_t, b=0.5):
    x0 = array(x0.tolist())
    y0 = array(y0.tolist())
    u0 = array(u0.tolist())
    v0 = array(v0.tolist())

    solutions = []
    for k in range(len(x0)):
        values_one_step = array([x0[k], y0[k], u0[k], v0[k]])
        for _ in range(N_t):
            values_one_step = runge_kutta_step(f, values_one_step, dt, b)
        solutions.append(values_one_step)
    return solutions


def bench(n_sleds, n_time):
    x_init = np.zeros(n_sleds)
    y_init = np.random.rand(n_sleds)
    v_init = np.zeros(n_sleds)
    u_init = np.zeros(n_sleds) + 3.5

    solver(board, x_init, y_init, u_init, v_init, 0.01, n_time)


# end code functions (don't remove this line)


bench_pythran = jit(bench)
# Numba does not support this code...
# bench_numba = jit(backend="numba")(bench)
from transonic import wait_for_all_extensions

# warmup (compilation of the Pythran extension)
bench_pythran(1, 1)
wait_for_all_extensions()

if __name__ == "__main__":

    from transonic.util import timeit_verbose as timeit

    n_sleds = 10
    n_time = 200

    g = locals()
    norm = timeit("bench(n_sleds, n_time)", globals=g)
    timeit("bench_pythran(n_sleds, n_time)", globals=g, norm=norm)
    # timeit("bench_numba(n_sleds, n_time)", globals=g, norm=norm)
