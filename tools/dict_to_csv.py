from typing import Callable


def dict_to_csv(filepath: str, d: dict, headers: list = None, sort_key: Callable = None):
    import csv

    if headers is not None and len(headers) != 2:
        raise ValueError(
            "If given, exactly two header values must be specified (len(headers) == 2))."
        )

    with open(filepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        if headers:
            writer.writerow(headers)
        iterator = sorted(d.items(), key=sort_key) if sort_key else d.items()
        for k, v in iterator:
            writer.writerow([k, v])
