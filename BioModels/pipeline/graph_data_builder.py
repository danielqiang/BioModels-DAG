from typing import Iterable, Generator, Callable, Collection, Tuple, TextIO, Collection

__all__ = ['GraphDataBuilder']


class GraphDataBuilder:
    """A pipeline link for converting SBML file data to <Node, Edge, Node> 3-tuples
        usable by NetworkX.
    """

    def __init__(self, filepaths: Iterable[str],
                 parser: Callable[[TextIO], Generator[Tuple[dict, dict, dict], None, None]]):
        """
        Constructor. Uses a user-provided SBML parser to generate child-edge-parent 3-tuples
        each representing a parent-child relationship between two biological entities.

        :param filepaths: Paths to SBML files.
        :param parser: Callable that takes an SBML file handle and returns an iterator over
                        child-edge-parent 3-tuples. Both the child and parent must contain
                        a 'name' key.
        """
        self._filepaths = filepaths
        self._parser = parser

    def to_generator(self):
        """
        Returns a generator over all (Child Model Data, Edge, Parent Model Data)
        3-tuples in this parser.

        :rtype: generator
        """
        return self._parse_SBML()

    def to_csv(self, filepath: str, headers: Collection = ('Child', 'Edge', 'Parent')):
        """
        Writes a 3-column CSV file containing all 3-tuples in this parser.
        Uses ('Child', 'Edge', 'Parent') as default column headers.

        :param filepath: Path to CSV file.
        :param headers: Headers for CSV file.
        """
        import csv

        if len(headers) != 3:
            raise ValueError("Exactly 3 headers are required, not {}.".format(len(headers)))

        with open(filepath, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for row in self._parse_SBML():
                writer.writerow(row)

    def _parse_SBML(self, print_fpath=True):
        """
        Parses SBML files and returns a generator of
        (Child Model, Edge, Parent Model) 3-tuples.

        :param print_fpath: If True, print each filename before
                            parsing it.
        :rtype: generator
        """
        for filepath in self._filepaths:
            if print_fpath:
                print(filepath)
            with open(filepath, "r", encoding='utf8') as file:
                yield from self._parser(file)
