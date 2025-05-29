
import sys, os, math, colorama
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List, Any


def progress_bar(objective: int, current: int) -> None:
    colorama.init()
    x: int = int(current * 101 / objective)
    print(f'|\033[1;32m{x * '='}\033[31m{(100 - x) * '='}\033[0m| {current}/{objective}')


def basic_log_config(*args: Any, **kwargs: Any) -> None:
    import logging

    logger: logging.Logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    file_handler: logging.FileHandler = logging.FileHandler('..\\logging\\main.log', mode='w')
    file_handler.setFormatter(formatter)

    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler); logger.addHandler(console_handler)


__all__: List[str] = [var for var in globals().keys() if not var.startswith('_')]