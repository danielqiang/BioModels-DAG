from typing import Iterable, Collection

__all__ = ['to_csv']


def to_csv(filepath: str, data: Iterable, headers: Collection = None):
    """
    Writes a CSV file containing the data in 'data'.
    Uses 'headers' as file headers if provided;
    otherwise, omits file headers from the CSV file.

    :param filepath: Path to CSV file.
    :param data: Data to write to CSV file.
                Each item in 'data' is written as a row.
    :param headers: Headers for CSV file.
    """
    import csv

    with open(filepath, "w", newline='') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in data:
            writer.writerow(row)
