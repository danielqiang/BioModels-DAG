from typing import Iterable, Callable

__all__ = ["extract_data"]


def extract_data(filepaths: Iterable[str], parser: Callable, print_fpath=True, *args, **kwargs):
    """
    Pipeline link. Extracts <Node: dict, Edge, Node: dict> 3-tuples each
    representing a parent-child relationship between two biological entities
    from local SBML files. Uses a user-provided SBML parser.

    :param filepaths: Paths to SBML files.
    :param parser: Callable that takes an SBML file handle and returns an iterator
                    over (Child, Edge, Parent) 3-tuples. Both child and parent must
                    be dictionaries that contain a 'name' key.
    :param print_fpath: If True, print each filename before
                        parsing it.
    :param args: Additional arguments to pass to parser.
    :param kwargs: Additional keyword arguments to pass to parser.
    :rtype: generator
    """
    for filepath in filepaths:
        if print_fpath:
            print(filepath)
        with open(filepath, "r", encoding='utf8') as file:
            yield from parser(file, *args, **kwargs)
