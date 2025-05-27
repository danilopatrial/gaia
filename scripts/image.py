
from utils import basic_log_config

from typing_extensions import *
from PIL               import Image
from numba             import njit

import math
import pandas as pd
import sys
import os
import logging
import time

basic_log_config() # <== Set basic logging config.
Image.MAX_IMAGE_PIXELS = None


DATABASE_PATH:  str = '"D:\\Gaia\\gedr3\\gaia_source"'
IMAGE_PATH:     str = 'images\\equirectangular_kelvin-color_render.png'

WIDTH, HEIGHT = 3840, 2160

if os.path.isfile(IMAGE_PATH):
    IMAGE: Image.Image = Image.open(IMAGE_PATH)
else:
    IMAGE: Image.Image = Image.new('RGB', size=(WIDTH, HEIGHT))

PIXELS = IMAGE.load()



@njit
def bp_rp_parallax_to_rgb(bp_rp, parallax):
    if bp_rp < -0.4: bp_rp = -0.4
    if bp_rp > 4.0: bp_rp = 4.0
    temp_kelvin = 8700 / (bp_rp + 0.55)
    temp = min(40000, max(1000, temp_kelvin)) / 100.0

    if temp <= 66:
        red = 255.0
        green = 99.4708025861 * math.log(temp) - 161.1195681661
        blue = 0.0 if temp <= 19 else 138.5177312231 * math.log(temp - 10) - 305.0447927307
    else:
        red = 329.698727446 * ((temp - 60.0) ** -0.1332047592)
        green = 288.1221695283 * ((temp - 60.0) ** -0.0755148492)
        blue = 255.0

    rgb = (min(255, max(0, int(red))),
           min(255, max(0, int(green))),
           min(255, max(0, int(blue))))

    if parallax <= 0: return rgb
    lum = 1.0 / ((1000.0 / parallax) ** 2)
    return (min(255, int(rgb[0] * lum)),
            min(255, int(rgb[1] * lum)),
            min(255, int(rgb[2] * lum)))

@njit
def ra_dec_to_coo(ra, dec):
    u = ra / 360.0
    v = (90.0 - dec) / 180.0

    x = int(u * WIDTH)
    y = int(v * HEIGHT)

    if x < 0: x = 0
    if x >= WIDTH: x = WIDTH - 1
    if y < 0: y = 0
    if y >= HEIGHT: y = HEIGHT - 1

    return x, y


print(float('')); exit()
if __name__ == '__main__' and sys.version_info >= (3, 9):

    csv_files: List[str] = os.listdir(DATABASE_PATH)
    length: int = len(csv_files)

    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(os.path.join(DATABASE_PATH, csv_file))
        print(f'{i}/{length}', end='\r', flush=True)

        for i, star in df.iterrows():
            bp_rp, parallax = star['bp_rp'], star['parallax']
            ra, dec = star['ra'], star['dec']

            if pd.isna(bp_rp) or pd.isna(ra) or pd.isna(dec):
                continue

            bp_rp = float(bp_rp)
            parallax = float(bp_rp) if not pd.isna(parallax) else 0

            x, y = ra_dec_to_coo(ra, dec)
            rgb = bp_rp_parallax_to_rgb(bp_rp, parallax)
            PIXELS[x, y] = rgb


    IMAGE.save(IMAGE_PATH)
    IMAGE.show()