
'''
Plate Carrée [PC] Projection based on the Star Temperature (Kelvin):
_
- The temperature in kelvin is calculated using the bp_rp parameters. (`bp_rp_to_temperature`)
- *This projection preserves horizontal and vertical alignment, but distorts areas near the poles.
In star maps or galactic images, this often creates the "U-bend" or smile shape of the Milky Way
or other features, especially if the projection is centered differently than the galactic plane.*
'''

from typing   import Tuple
from utils    import basic_log_config
from coloring import bp_rp_to_rgb
from render   import render
from numba    import njit
from PIL      import Image

import sys
import os
import logging


basic_log_config()

database_path:  str = 'D:\\Gaia\\gedr3\\gaia_source'
img_name:       str = 'plate_carree_bp_rp_to_kelvin_coloring'
render_path:    str = '..\\renders\\{}.png'.format(img_name)

width, height = 38400, 21600


@njit
def plate_carree(ra: float, dec: float) -> Tuple[int, int]:
    '''
    Plate Carrée Projection from Right Ascension [ra] and Declination [dec]
    '''
    u = ra / 360.0
    v = (90.0 - dec) / 180.0

    x = int(u * width)
    y = int(v * height)

    if x < 0: x = 0
    if x >= width: x = width - 1
    if y < 0: y = 0
    if y >= height: y = height - 1

    return x, y


if __name__ == '__main__':

    render(
        database_path=database_path,
        coo_func=plate_carree,
        coo_args_names=('ra', 'dec'),
        rgb_func=bp_rp_to_rgb,
        rgb_args_names=('bp_rp',),
        render_path=render_path,
        width=width,
        height=height
    )