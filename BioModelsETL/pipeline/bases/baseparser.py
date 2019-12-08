from abc import ABC, abstractmethod

__all__ = ['BaseParser']


class BaseParser(ABC):
    """Abstract base class for BioModelsETL parsers. All parsers must inherit from this class.
    """

    @abstractmethod
    def parser(self, sbml_file, **kwargs):
        """
        Abstract parser method. Must be overridden in concrete subclass.

        A parser() implementation must accept an SBML file handle and
        return an iterator over <Node, Edge, Node> triples.

        Nodes are dictionaries containing a 'name' key and all hashable values
        (this is required by NetworkX).
        Edges are strings representing edge labels in the NetworkX graph.

        parser() implementations may accept additional keyword arguments.
        Add keyword arguments to the method signature and pass them to
        BioModelsETL.extract_data() to use them.

        :param sbml_file: (typing.TextIO) SBML file handle.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.parser is not defined")
