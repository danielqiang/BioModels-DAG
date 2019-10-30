from typing import Iterable, Callable, Collection

__all__ = ['SBMLDataConverter']


class SBMLDataConverter:
    """A pipeline link for converting SBML file data to <Node, Edge, Node> 3-tuples
        usable by NetworkX.
    """

    def __init__(self, filepaths: Iterable[str], parser: Callable, *args, **kwargs):
        """
        Constructor. Uses a user-provided SBML parser to generate (Child, Edge, Parent) 3-tuples
        each representing a parent-child relationship between two biological entities.

        :param filepaths: Paths to SBML files.
        :param parser: Callable that takes an SBML file handle and returns an iterator
                        over (Child, Edge, Parent) 3-tuples. Both child and parent must
                        be dictionaries that contain a 'name' key.
        :param args: Additional arguments to pass to parser.
        :param kwargs: Additional keyword arguments to pass to parser.
        """
        self._filepaths = filepaths
        self._parser = parser
        self._args = args
        self._kwargs = kwargs

    def as_generator(self):
        """
        Returns a generator over all (Child Model Data, Edge, Parent Model Data)
        3-tuples in this parser.

        :rtype: generator
        """
        return self._parse_sbml()

    def _parse_sbml(self, print_fpath=True):
        """
        Parses SBML files and returns a generator of
        (Child, Edge, Parent) 3-tuples.

        :param print_fpath: If True, print each fi
            if print_fpath:lename before
                            parsing it.
        :rtype: generator
        """
        for filepath in self._filepaths:
            if print_fpath:
                print(filepath)
            with open(filepath, "r", encoding='utf8') as file:
                yield from self._parser(file, *self._args, **self._kwargs)
