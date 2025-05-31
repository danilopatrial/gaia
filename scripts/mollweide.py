from typing   import Tuple
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
def _solve_theta(phi: float) -> float:
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
def mollweide(ra: float, dec: float) -> Tuple[int, int]:
    ra = ra  * (math.pi / 180)
    dec = dec * (math.pi / 180)

    lam = ra - math.pi
    phi = dec

    theta = _solve_theta(phi)

    x = (2 * math.sqrt(2) / math.pi) * lam * math.cos(theta)
    y = math.sqrt(2) * math.sin(theta)

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