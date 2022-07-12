import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import exp, log, cosh, sqrt


# z - from the camera to the far
# x - horizontal
# y - vertical

def horizontal_drag_coord(t, m, c_drag, v0, val0):
    if v0 == 0:
        return val0
    tau = m / c_drag * v0
    temp = (1 + t / tau)
    temp[temp < 0] = 1
    ln = np.array([log(val) for val in temp])
    return v0 * tau * ln + val0

x = horizontal_drag_coord
z = horizontal_drag_coord
def y(t, m, a, b, y0): return a * m * t**2 + b * t + y0

def ksi(t, m, c_drag_x, c_drag_z, xv0, x0, zv0, z0): return focal * x(t, m, c_drag_x, xv0, x0) / z(t, m, c_drag_z, zv0, z0) * pixel_to_meter
def eta(t, m, a, b, y0, c_drag_z, zv0, z0): return focal * y(t, m, a, b, y0) / z(t, m, c_drag_z, zv0, z0) * pixel_to_meter


def fit_3d():
    data_t = np.array([0, 0.3, 0.6, 0.9, 1.2])
    data_z = np.array([0, 10, 15, 18, 19])
    data_y = np.array([1, 5, 7, 7, 6])
    vals_z, _ = curve_fit(z, data_t, data_z)
    m, c_drag, zv0, z0 = vals_z

    def y_fixed(t, a, b, y0): return y(t, m, a, b, y0)
    vals_y, _ = curve_fit(y_fixed, data_t, data_y)
    a, b, y0 = vals_y

    print(vals_z)
    print(z(data_t, m, c_drag, zv0, z0))

    t = np.linspace(0, 2, 20)

    fig, axs = plt.subplots(3)
    fig.suptitle('3d coordinates')

    axs[0].set(xlabel='z', ylabel='y')
    axs[0].plot(
        data_z, data_y, '.',
        z(t, m, c_drag, zv0, z0), y(t, m, a, b, y0), '-'
    )

    axs[1].set(xlabel='t', ylabel='y')
    axs[1].plot(
        t,  y(t, m, a, b, y0), '-'
    )

    axs[2].set(xlabel='t', ylabel='z')
    axs[2].plot(
        t, z(t, m, c_drag, zv0, z0), '-'
    )
    plt.show()


def fit_2d():
    track = np.array([
        [323.80, 1093.22],
        [187.68, 640.46],
        [175.71, 626.36],
        [174.96, 655.97],
        [179.48, 755.04],
        [184.92, 829.45],
        [188.68, 902.82]
    ])

    track_ksi = np.array(list(map(lambda v: v - 1080 / 2, track[:, 0])))
    track_eta = np.array(list(map(lambda v: 1920 / 2 - v, track[:, 1])))
    track_t = np.array([0, 0.33, 0.66, 0.99, 1.3, 1.6, 1.9])

    g = -9.8
    # ksi_param_bounds = ((0, 0.5, -30, -5, 50, 0), (1, 15, 30, 5, 80, 10))
    ksi_param_bounds = ((-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf),
                        (np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf))
    vals_ksi, _ = curve_fit(ksi, track_t, track_ksi, bounds=ksi_param_bounds)
    m, c_drag_x, c_drag_z, xv0, x0, zv0, z0 = vals_ksi

    print('m {}, c_drag_x {}, c_drag_z {} xv0 {}, x0 {}, zv0 {}, z0 {}'.format(m, c_drag_x, c_drag_z, xv0, x0, zv0, z0))

    def eta_fixed(t, a, b, y0):
        return eta(t, m, a, b, y0, c_drag_z, zv0, z0)

    vals_eta, _ = curve_fit(eta_fixed, track_t, track_eta)
    a, b, y0 = vals_eta

    t = np.linspace(0, 4, 20)

    fig, axs = plt.subplots(3)
    fig.suptitle('3d and camera projection')

    axs[0].set(xlabel='ksi', ylabel='eta')
    axs[0].plot(
        track_ksi, track_eta, '.',
        ksi(t, m, c_drag_x, c_drag_z, xv0, x0, zv0, z0), eta(t, m, a, b, y0, c_drag_z, zv0, z0), '-'
    )

    axs[1].set(xlabel='t', ylabel='y')
    axs[1].plot(
        t, y(t, m, a, b, y0), '-'
    )

    axs[2].set(xlabel='t', ylabel='z')
    axs[2].plot(
        t, z(t, m, c_drag_z, zv0, z0), '-'
    )

    plt.show()


focal = 0.013
pixel_to_meter = 1920 / 0.03
# test_ksi = focal * 10 / 20 * pixel_to_meter
# print(test_ksi)
# fit_3d()
fit_2d()
