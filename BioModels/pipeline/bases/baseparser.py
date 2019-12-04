from abc import ABC, abstractmethod

__all__ = ['BaseParser']


class BaseParser(ABC):
    """Base class for BioModels parsers. All parsers must inherit from this class.

    A BioModels parser accepts an SBML file handle and returns an iterator over
    <Node, Edge, Node> triples. Nodes are dictionaries containing a 'name' key
    and all hashable values (required by NetworkX). Edges are strings representing
    edge labels in the NetworkX graph.
    """

    @abstractmethod
    def parser(self, sbml_file, **kwargs):
        """
        Abstract parser method. Must be overridden in concrete subclass.

        parser() implementations may accept additional keyword arguments.
        Add keyword arguments to the method signature and pass them to
        BioModels.extract_data() to use them.

        :param sbml_file: (typing.TextIO) SBML file handle.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.parser is not defined")
