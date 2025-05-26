
# TODO: Be able to download in diferent hard-drives, keep a downloads log,
# better error handling.

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing_extensions import *
import hashlib, requests, zipfile, gzip, shutil, time, logging

from utils import basic_log_config
basic_log_config() # Set Basic Log Config.


logging.warning(
    '[STORAGE WARNING]:\nRunning the following code will download the entire gedr3/gaia_source database, '
    'which exceeds 1.5 TB in size and will be saved as CSV files.\n'
    'Ensure you have sufficient disk space and bandwidth before proceeding.'
    )

time.sleep(2)

__proceed: bool = input('Are you sure do you want to proceed? [YES/NO]: ').upper() == 'YES'
if __proceed is False: print(); logging.fatal(' Operation canceled. Exiting program...'); sys.exit()


OUTPUT_PATH: str | None = None # <=== Insert Output Path Here!!!

if OUTPUT_PATH is None or not os.path.isdir(OUTPUT_PATH):
    raise NotADirectoryError(f'{OUTPUT_PATH} is not a valid directory.')


class HashMismatchError(Exception): ...


def check_md5sum(filepath: str, md5sum: str) -> Literal[True]:

    assert isinstance(filepath, str), 'Filepath arg. must be of type str.'
    assert isinstance(md5sum,   str), 'MD5SUM arg. must be of type str.'

    if not os.path.isdir(filepath):
        raise NotADirectoryError(f'{filepath} is not a valid directory.')

    md5_hash = hashlib.md5()
    with open(filepath, 'rb') as file:
        for chunk in iter(lambda: file.read(8192), b''):
            md5_hash.update(chunk)

    digested_hash: str = md5_hash.hexdigest()

    if digested_hash != md5_hash:
        raise HashMismatchError(f'MD5 mismatch: expected {md5sum}, got {digested_hash}')

    return True


def unzip_file(filepath: str) -> None:

    assert isinstance(filepath, str), 'Filepath arg. must be of type str.'

    if not os.path.isdir(filepath):
        raise NotADirectoryError(f'{filepath} is not a valid directory.')

    logging.debug(f'Unpacking {os.path.basename(filepath)}')
    output_path: str = filepath[:-3] # Remove `.gz` file extension.

    with gzip.open(filepath, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(filepath) # Delete zipped file.


def download(md5sum: str, filename: str) -> None:

    assert isinstance(md5sum,   str), 'MD5SUM arg. must be of type str.'
    assert isinstance(filename, str), 'Filepath arg. must be of type str.'

    url: str = f'http://cdn.gea.esac.esa.int/Gaia/gedr3/gaia_source/{filename}'
    output_path: str = os.path.join(OUTPUT_PATH, filename)