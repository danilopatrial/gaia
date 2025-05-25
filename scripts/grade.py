
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
    raise NotImplementedError(_bp_rp_to_temperature.__name__)


def _apply_brightness(rbg: RGB, brightness_val: float) -> RGB:
    '''
    Apply Brightness Values to a RGB Tuple.
    _
    '''
    raise NotImplementedError(_apply_brightness.__name__)


def _apparent_to_absolute_mag(phot_g_mean_mag: float, parallax: float ) -> float:
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
    raise NotImplementedError(kelvin_to_rgb.__name__)


def apparent_magnitude_to_luminance(
    rgb: RGB,
    phot_g_mean_mag: float,
    min_mag: float = -1.46,
    max_mag: float = 20.0
) -> RGB:
    '''
    Set star brightness based on how bright they appear from Earth.
    _
    - Use this function after getting the RGB values.
    `phot_g_mean_mag: float = GaiaSource.phot_g_mean_mag`
    '''
    raise NotImplementedError(apparent_magnitude_to_luminance.__name__)


def distance_to_luminance(rgb: RGB, parallax: float, max_distance: float = 10_000.0) -> RGB:
    '''
    Set star brightness based on it's distance from Earth.
    _
    `parallax: float = GaiaSource.parallax`
    '''
    raise NotImplementedError(distance_to_luminance.__name__)


def distance_to_hue(rgb: RGB, parallax: float, max_distance: float = 10_000.0) -> RGB:
    '''
    Linearly tints the star toward blue as it gets farther away.
    _
    `parallax: float = GaiaSource.parallax`
    '''
    raise NotImplementedError(distance_to_hue.__name__)


def distance_to_redshift(rgb: RGB, parallax: float, max_distance: float = 10_000.0) -> RGB:
    '''
    Linearly tints the star toward red as it gets farther away.
    _
    `parallax: float = GaiaSource.parallax`
    '''
    raise NotImplementedError(distance_to_redshift.__name__)


def metallicity_to_rgb(dr2_rv_template_fe_h: float, prevent_missing_arg: bool = True) -> RGB:
    '''
    Linearly tints the star based on it's metallicity
    _
    - Metal-poor (-2.5) -> blueish
    - Metal-rich (+0.5) -> reddish

    `dr2_rv_template_fe_h: float = GaiaSource.dr2_rv_template_fe_h`

    `prevent_missing_arg: bool` -> When bp_rp return an empty `str` or `None`.
    '''
    raise NotImplementedError(metallicity_to_rgb.__name__)


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
    raise NotImplementedError(bp_rp_to_spectral_rgb.__name__)


def source_id_to_rgb(source_id: float, prevent_missing_arg: bool = True) -> RGB:
    '''
    Assign a unique color to each cluster (`source_id`)
    _
    `source_id: float = GaiaSource.source_id`

    `prevent_missing_arg: bool` -> When bp_rp return an empty `str` or `None`.
    '''
    raise NotImplementedError(source_id_to_rgb.__name__)


def age_to_rgb(age: float, min_age: float = 0.1, max_age: float = 13.8) -> RGB:
    age: float = max(min_age, min(age, max_age))
    t: float = (age - min_age) / (max_age - min_age)
    r: int = int(100 + 155 * t)
    g: int = int(180 + 75 * (1 - t))
    b: int = int(255 * (1 - t))
    return (r, g, b)


'''def kelvin_to_rgb(bp_rp: float, prevent_missing_arg: bool = True) -> RGB:

    # def. bp_rp as the average temp. of the Sun's photosphere.
    if bp_rp is None and prevent_missing_arg: bp_rp = 5788

    if bp_rp is None: return (0, 0, 0)

    temp: float = 8700 / (bp_rp + 0.55) # converts bp_rp to kelvin.
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


def apparent_mag_to_luminance(phot_g_mean_mag: float, min_mag: float = -1.46, max_mag: float = 20.0) -> float:
    mag: float = max(min_mag, min(phot_g_mean_mag, max_mag))
    return 10 ** (-0.4 * (mag - min_mag))


def apply_brightness(rgb: RGB, brightness_val: float) -> RGB:
    return tuple(min(255, max(0, int(val * brightness_val))) for val in rgb)'''


