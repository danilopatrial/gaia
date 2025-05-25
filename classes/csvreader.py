
from typing_extensions  import Generator
import csv

class GaiaCSVReader(object):

    '''
    GaiaCSVReader is a simple CSV reader class designed to read and interact with
    data from a Gaia CSV source file.

    It provides an iterator interface to loop over the rows, supports indexing
    (e.g., reader[5]), and can report the number of data rows (excluding the header).
    '''

    __slots__: tuple = ('_filepath')

    def __init__(self, gaia_source_csv_path: str) -> None:
        self._filepath: str = gaia_source_csv_path

    def __iter__(self) -> Generator[list, None, None]:
        with open(self._filepath, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader, None)
            for row in csv_reader: yield row

    def __len__(self) -> int:
        with open(self._filepath, newline='') as csvfile:
            return sum(1 for _ in csv.reader(csvfile)) - 1

    def __getitem__(self, index: int) -> list:
        with open(self._filepath, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader, None)

            for i, row in enumerate(csv_reader):
                if i == index: return row

            raise IndexError('Index out of range.')
