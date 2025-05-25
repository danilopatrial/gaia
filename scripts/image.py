
import sys, os, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing_extensions  import *
from classes            import GaiaCSVReader, GaiaSource
from utils              import *
from PIL                import Image

import numpy as np

width, height = 42144, 23706

database_listdir: List[str] = os.listdir('database')

main_image: Image.Image = Image.new('RGB', size=(width, height))
pixels = main_image.load()

for file in database_listdir:
    print(file)
    current_csv: GaiaCSVReader = GaiaCSVReader(os.path.join('database', file))
    for row in current_csv:
        star: GaiaSource = GaiaSource(*row)

        if not star.ra or not star.dec or not star.bp_rp or not star.parallax:
            continue

        x: int = int(float(star.ra) / 360.0 * width)
        y: int = int(height * (1 - (float(star.dec) + 90) / 180.0))
        temp: float = bp_rp_to_temperature(float(star.bp_rp))

        color: tuple = kelvin_to_rgb(temp)

        pixels[x, y] = color


main_image.save('images/render_test.png')
main_image.show()
