
import sys, os, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing_extensions  import Tuple, Literal, List, Any, NoReturn
from collections        import defaultdict
from classes            import GaiaCSVReader, GaiaSource


def basic_log_config(*args: Any, **kwargs: Any) -> NoReturn:
    import logging

    logger: logging.Logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    file_handler: logging.FileHandler = logging.FileHandler('C:\\Users\\Danilo Patrial\\Python\\Gaia\\logging\\main.log', mode='w')
    file_handler.setFormatter(formatter)

    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler); logger.addHandler(console_handler)


def bp_rp_to_temperature(bp_rp: float) -> float:
    '''BP-RP (Blue Param. - Red Param.) to an estimated Temp. in Kelvin.
    _
    '''
    return 8700 / (bp_rp + 0.55)

def kelvin_to_rgb(temp: float) -> Tuple[int, int, int]:
    '''
    Converts a given temperature (in Kelvin) to a approximate RGB color value
    _
    https://gist.github.com/petrklus/b1f427accdf7438606a6
    '''
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


def kelvin_to_rgb_custom(max_value: float, min_value: float, current_value: float) -> Tuple[int, int, int]:
    '''Map a value to RGB using a custom scale based on min/max range with logarithmic normalization.'''

    t: float = (current_value - min_value) / (max_value - min_value)

    if t < 0.25:
        ratio = t / 0.25
        r = 255
        g = int(255 * ratio)
        b = 0
    elif t < 0.5:
        ratio = (t - 0.25) / 0.25
        r = 255
        g = 255
        b = int(255 * ratio)
    elif t < 0.75:
        ratio = (t - 0.5) / 0.25
        r = int(255 * (1 - ratio))
        g = 255
        b = 255
    else:
        ratio = (t - 0.75) / 0.25
        r = 0
        g = int(255 * (1 - ratio))
        b = 255

    return (r, g, b)


def gather_min_max_values(attributes: list = ['bp_rp', 'ra', 'dec', 'parallax']) -> Tuple[dict, dict]:

    database_listdir: List[str] = os.listdir('database')

    min_values: defaultdict = defaultdict(lambda: float('inf'))
    max_values: defaultdict = defaultdict(lambda: float('-inf'))

    def compare_and_define(x: str, y: str, sign: Literal['<', '>']) -> float:
        if sign == '<': return min(float(x), float(y))
        if sign == '>': return max(float(x), float(y))

    for csvfile in database_listdir:
        csvfile: GaiaCSVReader = GaiaCSVReader(os.path.join('database', csvfile))
        for row in csvfile:
            star: GaiaSource = GaiaSource(*row)

            if any(not getattr(star, attr) for attr in attributes):
                continue

            for attr in attributes:
                val: float = getattr(star, attr)
                min_values[attr] = compare_and_define(min_values[attr], val, '<')
                max_values[attr] = compare_and_define(max_values[attr], val, '>')

    return (max_values, min_values)


__all__: list = ['gather_min_max_values', 'kelvin_to_rgb_custom', 'kelvin_to_rgb', 'bp_rp_to_temperature']