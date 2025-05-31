from typing   import Callable, Tuple, Any, List
from pandas   import read_csv
from datetime import datetime
from operator import itemgetter
from utils    import progress_bar
from PIL      import Image

import os
import logging


def _process_csv(
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

    preview_chunk = next(read_csv(filepath, chunksize=1))
    preview_row = next(preview_chunk.itertuples(index=False))._asdict()
    test_rgb_args = rgb_get(preview_row)
    test_coo_args = coo_get(preview_row)

    # Ugly but works!
    if isinstance(test_rgb_args, tuple):
        def rgb_wrapper(row_dict):
            return rgb_func(*rgb_get(row_dict))
    else:
        def rgb_wrapper(row_dict):
            return rgb_func(rgb_get(row_dict))

    if isinstance(test_coo_args, tuple):
        def coo_wrapper(row_dict):
            return coo_func(*coo_get(row_dict))
    else:
        def coo_wrapper(row_dict):
            return coo_func(coo_get(row_dict))

    for chunk in read_csv(filepath, chunksize=chunksize):
        for row in chunk.itertuples(index=False):
            row_dict = row._asdict()

            # NaN check
            if any(row_dict[arg] != row_dict[arg] for arg in coo_args_names + rgb_args_names):
                continue

            coo_args = coo_get(row_dict)
            x, y = coo_wrapper(row_dict)

            rgb = rgb_wrapper(row_dict)

            pixels[x, y] = rgb


def _check_files(
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
            raise ValueError(f'Missing expected column: {name}')

    logging.info('[OK] Ready to start. All files checked.')


def render(
    database_path: str,
    coo_func: Callable[..., Tuple],
    coo_args_names: Tuple[str, ...],
    rgb_func: Callable[..., Tuple],
    rgb_args_names: Tuple[str, ...],
    render_path: str,
    width: int,
    height: int,
    chunk_size: int = 10_000,
) -> None:
    Image.MAX_IMAGE_PIXELS = None

    if os.path.isfile(render_path):
        image: Image.Image = Image.open(render_path)
    else:
        image: Image.Image = Image.new('RGB', size=(width, height))

    pixels = image.load()

    try:

        csv_files: List[str] = [
            f for f in os.listdir(database_path)
            if os.path.isfile(os.path.join(database_path, f)) and f.endswith(".csv")
            ]

        num_csvs: int = len(csv_files)

        _check_files(database_path, coo_args_names, rgb_args_names, csv_files)

        file_paths: List[str] = [os.path.join(database_path, f) for f in csv_files]

        for i, file in enumerate(file_paths):
            logging.debug(f'{file}{' '*50}')
            progress_bar(objective=num_csvs, current=i)

            _process_csv(
                filepath=file,
                coo_args_names=coo_args_names,
                rgb_args_names=rgb_args_names,
                coo_func=coo_func,
                rgb_func=rgb_func,
                chunksize=chunk_size,
                pixels=pixels
            )

        logging.info(f'[DONE] Finished at {datetime.now()}')

    except Exception as e:
        raise e
    finally:
        logging.warning('SAVING IMAGE! DO NOT CLOSE THIS APPLICATION.')
        image.save(render_path)
        image.show()


__all__: List[str] = [var for var in globals().keys() if not var.startswith('_')]