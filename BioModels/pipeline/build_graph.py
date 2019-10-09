import networkx
from typing import Iterable

__all__ = ['build_graph']


def build_graph(data: Iterable):
    """
    Builds a NetworkX DiGraph object from (Child, Edge, Parent) 3-tuples.

    :param data: Iterable of (Child, Edge, Parent) 3-tuples.
    :rtype: networkx.DiGraph
    """
    g = networkx.DiGraph()

    for child_attrs, edge, parent_attrs in data:
        # Color pubmed nodes red, biomodel nodes green
        if parent_attrs['provider'] in ('biomodels.db', 'pubmed'):
            parent_attrs['color'] = 'red' if parent_attrs['provider'] == 'pubmed' else 'green'
        child_attrs['color'] = 'green'

        child_name, parent_name = child_attrs.pop('name'), parent_attrs.pop('name')

        g.add_node(child_name, **child_attrs)
        g.add_node(parent_name, **parent_attrs)
        g.add_edge(child_name, parent_name, label=edge)

    return g
