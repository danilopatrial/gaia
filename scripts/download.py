
# NOTE: I didn't use this exact code to download the Gaia files, but I'm almost sure it works perfectly,
# however, if you find any error or problem, please report it.

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
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'{filepath} does not exist or is not a file.')

    md5_hash = hashlib.md5()
    with open(filepath, 'rb') as file:
        for chunk in iter(lambda: file.read(8192), b''):
            md5_hash.update(chunk)
    digested_hash = md5_hash.hexdigest()

    if digested_hash != md5sum:
        os.remove(filepath)
        raise HashMismatchError(f'MD5 mismatch: expected {md5sum}, got {digested_hash}')

    return True


def unzip_file(filepath: str) -> None:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'{filepath} does not exist or is not a file.')

    logging.debug(f'Unpacking {os.path.basename(filepath)}')
    output_path = filepath[:-3]  # remove .gz extension

    with gzip.open(filepath, 'rb') as f_in, open(output_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    os.remove(filepath)


def download(md5sum: str, filename: str) -> None:
    url = f'http://cdn.gea.esac.esa.int/Gaia/gedr3/gaia_source/{filename}'
    output_path = os.path.join(OUTPUT_PATH, filename)
    output_path_unzipped = output_path[:-3]  # remove .gz for unzipped file

    if os.path.exists(output_path_unzipped):
        logging.debug(f'{filename} already downloaded and unzipped.')
        return

    if os.path.exists(output_path):
        try:
            check_md5sum(output_path, md5sum)
            logging.debug(f'{filename} already downloaded and verified.')
            unzip_file(output_path)
            return
        except HashMismatchError:
            logging.warning(f'MD5 mismatch for existing file {filename}, re-downloading.')
            os.remove(output_path)

    logging.info(f'Downloading {filename}')
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: f.write(chunk)

    check_md5sum(output_path, md5sum)
    unzip_file(output_path)


def main() -> None:

    logging.warning('This code will recursively attempt to download all files.')

    while True:
        try:
            with open('database\\_MD5SUM.txt', 'r') as file:
                lines: List[str] = file.readlines()

            for line in lines:
                download(*line.strip().split('  '))

            break

        except HashMismatchError as e:
            logging.error(f'Hash Mismatch error while downloading {line}: {e}')

        except requests.exceptions.HTTPError as e:
            logging.error(f'HTTP error while downloading {line}: {e}')

        except requests.exceptions.ConnectionError as e:
            logging.error(f'Connection error while downloading {line}: {e}')

        except requests.exceptions.Timeout as e:
            logging.error(f'Timeout while downloading {line}: {e}')

        except KeyboardInterrupt:
            logging.warning('Download interrupted by user.'); break

        except Exception as e:
            logging.fatal(e); break

        time.sleep(5)

if __name__ == '__main__':
    main()