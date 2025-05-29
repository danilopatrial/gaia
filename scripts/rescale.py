
from PIL import Image

import os

Image.MAX_IMAGE_PIXELS = None

def rescale(image_path: str, output_path: str = '..\\images', size: tuple = (3840, 2160)) -> None:
    image = Image.open(image_path)
    rescaled = image.resize(size)
    rescaled.save(os.path.join(output_path, os.path.basename(image_path)))

if __name__ == '__main__':
    rescale('..\\renders\\plate_carree_bp_rp_to_kelvin_coloring.png')