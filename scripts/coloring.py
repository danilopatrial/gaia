
from typing import List, Tuple
from numba  import njit

import math


@njit
def bp_rp_to_rgb(bp_rp: float) -> Tuple[int, int, int]:
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

    return rgb


__all__: List[str] = [var for var in globals().keys() if not var.startswith('_')]