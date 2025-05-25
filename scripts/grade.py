
import sys, os, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing_extensions import *
from classes import GaiaSource

type RGB = Tuple[int, int, int]


def _bp_rp_to_temperature(bp_rp: float, prevent_missing_arg: bool = True) -> float:
    '''
    Blue Parameter, Red Parameter to Temperature (Kelvin)
    _

    `bp_rp: float = GaiaSource.bp_rp`

    `prevent_missing_arg: bool` -> When bp_rp return an empty `str` or `None`.
    '''
    if (bp_rp is None or bp_rp == '') and prevent_missing_arg: return 5778 # Sun's avg. temp.
    bp_rp: float = max(-0.4, min(bp_rp, 4.0))
    return 8700 / (bp_rp + 0.55)


def _apply_brightness(rgb: RGB, brightness_val: float) -> RGB:
    '''
    Apply Brightness Values to a RGB Tuple.
    _
    '''
    return tuple(min(255, max(0, int(col * brightness_val))) for col in rgb)


def _apparent_to_absolute_mag(phot_g_mean_mag: float, parallax: float) -> float:
    '''
    Converts `phot_g_mean_mag` to absolute magnitude.
    _
    `phot_g_mean_mag: float = GaiaSource.phot_g_mean_mag`

    `parallax: float = GaiaSource.parallax`
    '''
    if parallax <= 0: return phot_g_mean_mag
    distance_pc: float = 1_000 / parallax
    return phot_g_mean_mag - 5 * (math.log10(distance_pc) - 1)


def _estimate_age(bp_rp: float, g_abs_mag: float) -> float:
    '''
    Estimate star age in billions of years.
    _
    `bp_rp: float = GaiaSource.bp_rp`
    '''

    # NOTE: The function provided is a heuristic model, not a physically rigorous one

    bp_rp:     float = max(0.0, min(bp_rp, 3.0))
    g_abs_mag: float = max(-5.0, min(g_abs_mag, 15.0))

    color_factor: float = (bp_rp / 3.0) ** 1.5
    brightness_factor: float = (g_abs_mag + 5.0) / 20.0

    age_gyr: float = 0.5 + 12.0 * (color_factor * 0.7 + brightness_factor * 0.3)
    return min(age_gyr, 13.8)


def kelvin_to_rgb(bp_rp: float, **kwargs: Any) -> RGB:
    '''
    Estimate RGB values using the star's temperature.
    _
    - The temperature is estimated using bp_rp convertion to kelvin

    `bp_rp: float = GaiaSource.bp_rp`

    `kwargs: Any` -> [`prevent_missing_arg: bool = True`]
    '''
    # def. bp_rp as the average temp. of the Sun's photosphere.

    if (bp_rp is None or bp_rp == ''): return (0, 0, 0)
    prevent_missing_arg: bool = kwargs.get('prevent_missing_arg', True)

    temp: float = _bp_rp_to_temperature(bp_rp, prevent_missing_arg)
    temp: float = max(1000, min(40000, temp)) / 100.0 # Clamp temp. range and scale for formula.

    if temp <= 66:
        red = 255
        green = 99.4708025861 * math.log(temp) - 161.1195681661
        blue = 0 if temp <= 19 else 138.5177312231 * math.log(temp - 10) - 305.0447927307
    else:
        red = 329.698727446 * ((temp - 60) ** -0.1332047592)
        green = 288.1221695283 * ((temp - 60) ** -0.0755148492)
        blue = 255

    def clamp(x: float | int): return max(0, min(int(x), 255))

    return (clamp(red), clamp(green), clamp(blue))


def apparent_magnitude_to_luminance(
    rgb: RGB,
    phot_g_mean_mag: float,
    min_mag: float = -1.46,
) -> RGB:
    '''
    Set star brightness based on how bright they appear from Earth.
    _
    `phot_g_mean_mag: float = GaiaSource.phot_g_mean_mag`
    '''
    lum: float = 10 ** (-0.4 * (phot_g_mean_mag - min_mag))
    return _apply_brightness(rgb, brightness_val=lum)


def distance_to_luminance(rgb: RGB, parallax: float, max_distance: float = 10_000.0) -> RGB:
    '''
    Set star brightness based on it's distance from Earth.
    _
    `parallax: float = GaiaSource.parallax`
    '''
    if parallax <= 0: return rgb
    distance_pc: float = 1_000 / parallax
    distance_pc = max(1, min(distance_pc, max_distance))
    lum: float = 1.0 / (distance_pc ** 2)
    return _apply_brightness(rgb, brightness_val=lum)


def distance_to_hue(rgb: RGB, parallax: float, max_distance: float = 10_000.0) -> RGB:
    '''
    Linearly tints the star toward blue as it gets farther away.
    _
    `parallax: float = GaiaSource.parallax`
    '''
    if parallax <= 0: return rgb
    distance_pc: float = 1_000 / parallax
    factor: float = min(1.0, distance_pc / max_distance)
    blue_tint: RGB = (
        int(rgb[0] * (1 - factor)),
        int(rgb[1] * (1 - factor)),
        int(rgb[2] + (255 - rgb[2]) * factor)
        )
    return tuple(min(255, max(0, col)) for col in blue_tint)

def distance_to_redshift(rgb: RGB, parallax: float, max_distance: float = 10_000.0) -> RGB:
    '''
    Linearly tints the star toward red as it gets farther away.
    _
    `parallax: float = GaiaSource.parallax`
    '''
    if parallax <= 0: return rgb
    distance_pc: float = 1_000 / parallax
    factor: float = min(1.0, distance_pc / max_distance)
    red_tint: RGB = (
        int(rgb[0] + (255 - rgb[0]) * factor),
        int(rgb[1] * (1 - factor)),
        int(rgb[2] * (1 - factor))
    )
    return tuple(min(255, max(0, col)) for col in red_tint)


def metallicity_to_rgb(
    rgb: RGB,
    dr2_rv_template_fe_h: float,
    min_feh: float = -2.5,
    max_feh: float = 0.5,
    prevent_missing_arg: bool = True
) -> RGB:
    '''
    Linearly tints the star based on it's metallicity
    _
    - Metal-poor (-2.5) -> blueish
    - Metal-rich (+0.5) -> reddish

    `dr2_rv_template_fe_h: float = GaiaSource.dr2_rv_template_fe_h`

    `prevent_missing_arg: bool` -> When bp_rp return an empty `str` or `None`.
    '''
    if dr2_rv_template_fe_h is None:
        if prevent_missing_arg: return rgb
        else: dr2_rv_template_fe_h = min_feh

    if prevent_missing_arg and not dr2_rv_template_fe_h: return rgb
    t: float = (dr2_rv_template_fe_h - min_feh) / (max_feh - min_feh)
    r = int(rgb[0] + (255 - rgb[0]) * t)
    g = int(rgb[1] * (1 - 0.2 * t))
    b = int(rgb[2] + (255 - rgb[2]) * (1 - t))
    return (min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b)))


def bp_rp_to_spectral_rgb(bp_rp: float, prevent_missing_arg: bool = True) -> RGB:
    '''
    Assign canonical RGB colors to stars, based on astronomical convention.
    _
    `bp_rp: float = GaiaSource.bp_rp`

    `prevent_missing_arg: bool` -> When bp_rp return an empty `str` or `None`.
    '''
    #  Spectral Type   Color          Temperature Range (K)   RGB (approx.) 
    #  -------------   ------------   ---------------------   ------------- 
    #  O               Blue           >30,000                 #9bb0ff       
    #  B               Blue-white     10,000-30,000           #aabfff       
    #  A               White          7,500-10,000            #cad7ff       
    #  F               Yellow-white   6,000-7,500             #f8f7ff       
    #  G               Yellow         5,200-6,000             #fff4ea       
    #  K               Orange         3,700-5,200             #ffd2a1       
    #  M               Red            <3,700                  #ffcc6f       
    if (bp_rp is None or bp_rp == '') and prevent_missing_arg:
        return (0, 0, 0)

    if bp_rp < -0.2:
        hex_color = "#9bb0ff"  # O
    elif bp_rp < 0.0:
        hex_color = "#aabfff"  # B
    elif bp_rp < 0.3:
        hex_color = "#cad7ff"  # A
    elif bp_rp < 0.58:
        hex_color = "#f8f7ff"  # F
    elif bp_rp < 0.81:
        hex_color = "#fff4ea"  # G
    elif bp_rp < 1.4:
        hex_color = "#ffd2a1"  # K
    else:
        hex_color = "#ffcc6f"  # M

    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return (r, g, b)


def source_id_to_rgb(source_id: float, prevent_missing_arg: bool = False) -> RGB:
    '''
    Assign a unique color to each cluster (`source_id`)
    _
    `source_id: float = GaiaSource.source_id`

    `prevent_missing_arg: bool` -> When bp_rp return an empty `str` or `None`.
    Prevent missing arg is set to False because None is hashable and will
    generate a unique color. Meaningless color.
    '''
    def hue_to_rgb(p: float, q: float, t: float) -> float:
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p

    def hsl_to_rgb(h: float, s: float, l: float) -> RGB:

        if s == 0:
            r = g = b = l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)

        return (int(r * 255), int(g * 255), int(b * 255))

    if (source_id is None or source_id == '') and prevent_missing_arg:
        return (0, 0, 0)

    h = abs(hash(source_id)) % 360
    return hsl_to_rgb(h / 360.0, 0.5, 0.6)


def age_to_rgb(
    bp_rp: float,
    phot_g_mean_mag: float,
    parallax: float,
    min_age: float = 0.1,
    max_age: float = 13.8
) -> RGB:
    '''
    Assign a unique color based on the star's age.
    _
    `bp_rp: float = GaiaSource.bp_rp`

    `phot_g_mean_mag: float = GaiaSource.phot_g_mean_mag`

    `parallax: float = GaiaSource.parallax`
    '''
    g_abs_mag: float = _apparent_to_absolute_mag(phot_g_mean_mag, parallax)
    age: float = _estimate_age(bp_rp, g_abs_mag)
    age: float = max(min_age, min(age, max_age))
    t: float = (age - min_age) / (max_age - min_age)
    r: int = int(100 + 155 * t)
    g: int = int(180 + 75 * (1 - t))
    b: int = int(255 * (1 - t))
    return (r, g, b)