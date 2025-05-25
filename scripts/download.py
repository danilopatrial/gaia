
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing_extensions import NoReturn, List
import hashlib, requests, zipfile, gzip, shutil, time, logging


#                                              SET LOGGING CONFIG.                                               #

from utils import basic_log_config as _basic_log_config
_basic_log_config()


#                                          WARNINGS AND SECURITY CHECK                                           #

logging.warning(
    '[STORAGE WARNING]:\nRunning the following code will download the entire gedr3/gaia_source database, '
    'which exceeds 1.5 TB in size and will be saved as CSV files.\n'
    'Ensure you have sufficient disk space and bandwidth before proceeding.')

time.sleep(2)

# Security check [The user must input that he want to continue.]
__proceed: bool = input('Are you sure do you want to proceed? [YES/NO]: ').upper() == 'YES'
if __proceed is False: print(); logging.critical(' Operation canceled. Exiting program...'); sys.exit()


#                                          DOWNLOAD [gedr3/gaia_source]                                          #

download_output_path: str | None = 'D:\\Gaia\\gedr3\\gaia_source' # <== Insert Output Path Here!!!

if download_output_path is None or not os.path.isdir(download_output_path):
    msg: str = 'Please Insert a valid directory address.'
    logging.exception(f'{NotADirectoryError.__name__}: {msg}')
    raise NotADirectoryError(msg)

def check_md5sum(filepath: str, md5sum: str) -> bool:
    md5_hash = hashlib.md5()
    with open(filepath, 'rb') as file:
        for chunk in iter(lambda: file.read(8192), b''): md5_hash.update(chunk)
    return md5_hash.hexdigest() == md5sum

def unzip_file(filepath: str) -> NoReturn:
    logging.debug(f'Unpacking {os.path.basename(filepath)}')
    output_filepath: str = filepath[:-3]
    with gzip.open(filepath, 'rb') as f_in:
        with open(output_filepath, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(filepath) # remove zipped file from system.

def download(md5sum: str, filename: str) -> None:
    url: str = f'http://cdn.gea.esac.esa.int/Gaia/gedr3/gaia_source/{filename}'
    output_path: str = os.path.join(download_output_path, filename)

    if os.path.exists(output_path.removesuffix('.gz')):
        return

    if os.path.exists(output_path) and check_md5sum(output_path, md5sum):
        logging.debug(f'{filename} already downloaded and verified.')
        return

    logging.info(f'Downloading {filename} ...')

    with requests.get(url, stream=True) as r:
        r.raise_for_status() # Raises HTTPError, if one occurred.
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)

    if check_md5sum(output_path, md5sum):
        logging.info(f'Downloaded and verified {filename}.')
    else:
        logging.warning(f'MD5 mismatch for {filename}! Removing file, and attempting download again.')
        time.sleep(5); download(md5sum, filename)

    unzip_file(output_path); os.system('cls')


def main() -> None:
    try:
        with open('Gaia\\database\\_MD5SUM.txt', 'r') as file:
            lines: List[str] = file.readlines()
            for line in lines: download(*line.strip().split('  '))
    except Exception as e:
        print(e); time.sleep(5); main() # Recursive Attempt.


if __name__ == '__main__': main()