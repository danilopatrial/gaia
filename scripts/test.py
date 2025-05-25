
import grade, utils, classes, time, logging
from typing_extensions import *

from classes import GaiaSource

utils.basic_log_config()


def callable_speed(callable: Callable, *args: Any, **kwargs: Any) -> None:
    logging.warning(f'[DEVELOPER TOOL] This function shall not be ran during main execution.')
    iterations: float = 1.6*10e5
    start: float = time.time()
    for _ in range(int(iterations)): callable(*args, **kwargs)
    end: float = time.time()
    logging.debug(
        f'{callable.__name__}: exc time [{iterations:,}x] = {end - start}'
        f' Estimated value for 1000x more iterations: {(end - start) * 1000}')

g = classes.GaiaCSVReader('C:\\Users\\Danilo Patrial\\Python\\Gaia\\database\\GaiaSource_000000-003111.csv')
for line in g: l = line; break

callable_speed(grade._bp_rp_to_temperature, 1)
