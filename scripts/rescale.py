from PIL import Image

import os

Image.MAX_IMAGE_PIXELS = None

_8k:    tuple = (7680, 4320)
_4k:    tuple = (3840, 2160)
_1080p: tuple = (1920, 1080)
_720p:  tuple = (1280, 720 )

def rescale(image_path: str, output_path: str = '..\\images', size: tuple = _4k) -> None:
    image = Image.open(image_path)
    rescaled = image.resize(size)
    rescaled.save(os.path.join(output_path, os.path.basename(image_path)))

if __name__ == '__main__':
    rescale('..\\renders\\hammer_aitoff_bp_rp_to_rgb.png', size=_1080p)