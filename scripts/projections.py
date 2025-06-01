from math   import pi, sqrt, sin, cos
from numba  import njit
from typing import List


@njit
def hammer_aitoff(ra, dec, width, height):
    sqrt2 = sqrt(2)

    lam = (ra - 180) * pi / 180
    phi = dec * pi / 180

    cos_phi = cos(phi)

    z = sqrt(1 + cos_phi * cos(lam / 2))

    x_proj = (2 * sqrt2 * cos_phi * sin(lam / 2)) / z
    y_proj = (sqrt2 * sin(phi)) / z

    x_norm = (x_proj + 2 * sqrt2) / (4 * sqrt2)
    y_norm = (y_proj + sqrt2) / (2 * sqrt2)

    x = int(x_norm * width)
    y = int((1 - y_norm) * height)

    return x, y


@njit
def plate_carree(ra, dec, width, height):
    u = ra / 360.0
    v = (90.0 - dec) / 180.0

    x = int(u * width)
    y = int(v * height)

    if x < 0: x = 0
    if x >= width: x = width - 1
    if y < 0: y = 0
    if y >= height: y = height - 1

    return x, y


@njit
def _solve_theta(phi):
    theta = phi
    for _ in range(10):
        numerator = 2 * theta + sin(2 * theta) - pi * sin(phi)
        denominator = 2 + 2 * cos(2 * theta)
        delta = numerator / denominator
        theta -= delta
        if abs(delta) < 1e-10:
            break
    return theta


@njit
def mollweide(ra, dec, width, height):
    sqrt2 = sqrt(2)

    ra  = ra  * (pi / 180)
    dec = dec * (pi / 180)

    lam = ra - pi
    phi = dec
    theta = _solve_theta(phi)

    x_proj = (2 * sqrt2 / pi) * lam * cos(theta)
    y_proj = sqrt2 * sin(theta)

    x_norm = (x_proj + 2 * sqrt2) / (4 * sqrt2)
    y_norm = (y_proj + sqrt2) / (2 * sqrt2)

    x = int(x_norm * width)
    y = int((1 - y_norm) * height)

    if x < 0: x = 0
    if x >= width: x = width - 1
    if y < 0: y = 0
    if y >= height: y = height - 1

    return x, y


__all__: List[str] = [var for var in globals().keys() if not var.startswith('_')]