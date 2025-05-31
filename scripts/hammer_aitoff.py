from utils    import basic_log_config
from coloring import bp_rp_to_rgb
from render   import render
from numba    import njit

import math

basic_log_config()

database_path:  str = 'D:\\Gaia\\gedr3\\gaia_source'
img_name:       str = 'hammer_aitoff_bp_rp_to_kelvin_coloring'
render_path:    str = '..\\renders\\{}.png'.format(img_name)

width, height = 38400, 21600


@njit
def hammer_aitoff(ra, dec):

    pi = math.pi
    sqrt2 = math.sqrt(2)

    lam = (ra - 180) * pi / 180
    phi = dec * pi / 180

    cos_phi = math.cos(phi)

    z = math.sqrt(1 + cos_phi * math.cos(lam / 2))

    x_proj = (2 * sqrt2 * cos_phi * math.sin(lam / 2)) / z
    y_proj = (sqrt2 * math.sin(phi)) / z

    x_norm = (x_proj + 2 * sqrt2) / (4 * sqrt2)
    y_norm = (y_proj + sqrt2) / (2 * sqrt2)

    x = int(x_norm * width)
    y = int((1 - y_norm) * height)

    return x, y


if __name__ == '__main__':

    render(
        database_path=database_path,
        coo_func=hammer_aitoff,
        coo_args_names=('ra', 'dec'),
        rgb_func=bp_rp_to_rgb,
        rgb_args_names=('bp_rp',),
        render_path=render_path,
        width=width,
        height=height
    )