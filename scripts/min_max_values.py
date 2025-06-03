from pandas import read_csv
from typing import List, Dict, Any

from utils  import progress_bar, basic_log_config

import os
import json
import math
import logging


basic_log_config()

if __name__ != '__main__':
    raise ImportError('This script is not supposed to be imported')


database_path: str | None = "D:\\Gaia\\gedr3\\gaia_source"

if not os.path.isdir(database_path):
    raise NotADirectoryError('Please insert a valid directory path')


csv_files: List[str] = [
    file for file in os.listdir(database_path)
    if file.endswith('.csv') and os.path.isfile(os.path.join(database_path, file))
]

if not csv_files:
    raise FileNotFoundError(f'No CSV file found at {database_path}')


if os.path.exists('min_max_values.json') and os.path.getsize('min_max_values.json') > 0:
    with open('min_max_values.json', 'r', encoding='utf-8') as json_file:
        json_data: Dict[str, Dict[str, Any]] = json.load(json_file)
        min_values = json_data.get('min', {})
        max_values = json_data.get('max', {})
else:
    min_values: Dict[str, Any] = {}
    max_values: Dict[str, Any] = {}


def parse_csv(file: str, min_values: Dict, max_values: Dict) -> None:
    filepath: str = os.path.join(database_path, file)

    for chunk in read_csv(filepath, chunksize=10000):
        for row in chunk.itertuples(index=False):
            row_dict = row._asdict()

            for key, value in row_dict.items():
                if isinstance(value, float) and math.isnan(value):
                    value = "NaN"

                # Skip non-numeric values for min/max comparison
                if isinstance(value, str) and value == "NaN":
                    continue

                try:
                    value = float(value)
                except Exception:
                    continue

                if key not in min_values or value < min_values[key]:
                    min_values[key] = value

                if key not in max_values or value > max_values[key]:
                    max_values[key] = value

    # Debug
    #print(f'Min Parallax: {round(min_values['parallax'], 2)} '
    #      f'Max Parallax: {round(max_values['parallax'], 2)}',
    #      end='\r', flush=True)


len_dir: int = len(csv_files)

for i, file in enumerate(csv_files):

    logging.debug(f'{file}{' '*70}')
    progress_bar(len_dir, i)

    try:
        parse_csv(file, min_values, max_values)

    except Exception as e:
        print(f"Error in {file}: {e}")

    finally:
        with open('min_max_values.json', 'w', encoding='utf-8') as json_file:
            json.dump({"min": min_values, "max": max_values}, json_file, indent=4, ensure_ascii=False)
