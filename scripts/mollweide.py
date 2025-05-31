from utils    import basic_log_config
from coloring import bp_rp_to_rgb
from render   import render
from numba    import njit

import math

basic_log_config()

database_path:  str = 'D:\\Gaia\\gedr3\\gaia_source'
img_name:       str = 'mollweide_bp_rp_to_kelvin_coloring'
render_path:    str = '..\\renders\\{}.png'.format(img_name)

width, height = 38400, 21600


@njit
def _solve_theta(phi):
    theta = phi
    for _ in range(10):
        numerator = 2 * theta + math.sin(2 * theta) - math.pi * math.sin(phi)
        denominator = 2 + 2 * math.cos(2 * theta)
        delta = numerator / denominator
        theta -= delta
        if abs(delta) < 1e-10:
            break
    return theta

@njit
def mollweide(ra, dec):
    pi = math.pi
    sqrt2 = math.sqrt(2)

    ra  = ra  * (pi / 180)
    dec = dec * (pi / 180)

    # Projection
    lam = ra - pi
    phi = dec
    theta = _solve_theta(phi)

    # Meollweid coordinate range: x_proj ∈ [-2√2, 2√2], y_proj ∈ [-√2, √2]
    x_proj = (2 * sqrt2 / pi) * lam * math.cos(theta)
    y_proj = sqrt2 * math.sin(theta)

    x_norm = (x_proj + 2 * sqrt2) / (4 * sqrt2)
    y_norm = (y_proj + sqrt2) / (2 * sqrt2)

    x = int(x_norm * width)
    y = int((1 - y_norm) * height)

    # clamp
    if x < 0: x = 0
    if x >= width: x = width - 1
    if y < 0: y = 0
    if y >= height: y = height - 1

    return x, y


if __name__ == '__main__':

    render(
        database_path=database_path,
        coo_func=mollweide,
        coo_args_names=('ra', 'dec'),
        rgb_func=bp_rp_to_rgb,
        rgb_args_names=('bp_rp',),
        render_path=render_path,
        width=width,
        height=height
    )