from .bases import BaseParser
from typing import Iterable

__all__ = ["extract_data"]


def extract_data(filepaths: Iterable[str], parser: BaseParser, print_fpath=True, **kwargs):
    """
    Pipeline link. Extracts <Node: dict, Edge, Node: dict> 3-tuples each
    representing a parent-child relationship between two biological entities
    from local SBML files using the provided 'parser' object.

    :param filepaths: Paths to SBML files.
    :param parser: Parser instance. Must inherit from BioModelsETL.BaseParser.
    :param print_fpath: If True, print each filename before parsing it.
    :param kwargs: Additional keyword arguments to pass to parser.
    :rtype: generator
    """
    if not isinstance(parser, BaseParser):
        raise ValueError(f"{parser.__class__.__name__} must inherit from BaseParser")
    for filepath in filepaths:
        if print_fpath:
            print(filepath)
        with open(filepath, "r", encoding='utf8') as file:
            yield from parser.parser(file, **kwargs)
