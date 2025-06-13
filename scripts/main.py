from projections import mollweide, hammer_aitoff, plate_carree
from coloring    import bp_rp_to_rgb, bp_rp_parallax_to_rgb
from utils       import basic_log_config
from render      import render
from typing      import Callable, Tuple

import sys
import logging

basic_log_config()


if __name__ == '__main__' and sys.argv[1] == '-r':

    logging.warning('Starting render. This process might be slow.')

    width, height = 38400, 21600                                                                                #

    coo_func: Callable[..., Tuple] = plate_carree   # Projections (i.e. Mollweide, Hammer-Aitoff, Plate Carrée) #
    rgb_func: Callable[..., Tuple] = bp_rp_parallax_to_rgb   # Coloring (i.e. BP-RP to RGB (temperature), )     #

    img_name: str = f'{coo_func.__name__}_{rgb_func.__name__}'
    render_path: str = '..\\renders\\{}.png'.format(img_name)

    logging.info(
        f'[CONFIG]: Projection={coo_func.__name__};'
        f' Coloring={rgb_func.__name__}; Res={width}x{height}'
    )

    render(
        database_path='D:\\Gaia\\gedr3\\gaia_source',                                                           #
        coo_func=coo_func,
        coo_args_names=('ra', 'dec'),                                                                           #
        rgb_func=rgb_func,
        rgb_args_names=('bp_rp', 'parallax'),                                                                   #
        render_path=render_path,
        width=width,
        height=height
        )

    logging.info(f'Image saved at: {render_path}')