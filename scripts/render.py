
from typing   import Callable, Tuple, Any, List
from pandas   import read_csv
from datetime import datetime
from operator import itemgetter
from utils    import progress_bar

import os
import logging


def process_csv(
    filepath: str,
    pixels: Any,
    coo_args_names: Tuple[str, ...],
    rgb_args_names: Tuple[str, ...],
    coo_func: Callable[..., Tuple],
    rgb_func: Callable[..., Tuple],
    chunksize: int = 10000,
) -> None:

    coo_get = itemgetter(*coo_args_names)
    rgb_get = itemgetter(*rgb_args_names)

    for chunk in read_csv(filepath, chunksize=chunksize):
        for row in chunk.itertuple(index=False):
            row_dict = row._asdict()

            if any(row_dict[arg] != row_dict[arg] for arg in coo_args_names + rgb_args_names):
                continue

            coo_args = coo_get(row_dict)
            rgb_args = rgb_get(row_dict)

            x, y = coo_func(*coo_args)
            rgb  = rgb_func(*rgb_args)

            pixels[x, y] = rgb


def check_files(
    database_path: str,
    coo_args_names: Tuple[str, ...],
    rgb_args_names: Tuple[str, ...],
    csv_files: List[str]
) -> None:

    logging.info('Checking files...')

    if not csv_files:
        raise FileNotFoundError('No files found in the database path.')

    for file in csv_files:
        path = os.path.join(database_path, file)

        if not os.access(path, os.R_OK):
            raise PermissionError(f"Cannot read file: {path}")

    sample_path: str = os.path.join(database_path, csv_files[0])
    sample_df = read_csv(sample_path, nrows=1)

    for name in coo_args_names + rgb_args_names:
        if name not in sample_df.columns:
            raise ValueError('Missing expected column: {name}')

    logging.info('[OK] Ready to start. All files checked.')


def render(
    database_path: str,
    pixels: Any,
    coo_func: Callable[..., Tuple],
    coo_args_names: Tuple[str, ...],
    rgb_func: Callable[..., Tuple],
    rgb_args_names: Tuple[str, ...],
    chunk_size: int = 10_000,
) -> None:

    csv_files: List[str] = [
        f for f in os.listdir(database_path)
        if os.path.isfile(os.path.join(database_path, f)) and f.endswith(".csv")
        ]

    num_csvs: int = len(csv_files)

    check_files(database_path, coo_args_names, rgb_args_names, csv_files)

    file_paths: List[str] = [os.path.join(database_path, f) for f in csv_files]

    for i, file in enumerate(file_paths):
        logging.debug(file)
        progress_bar(objective=num_csvs, current=i)

        process_csv(
            file_path=file,
            coo_args_name=coo_args_names,
            rgb_args_name=rgb_args_names,
            coo_func=coo_func,
            rgb_func=rgb_func,
            chunk_size=chunk_size,
            pixels=pixels
        )

    logging.info(f'[DONE] Finished at {datetime.date.today()}')