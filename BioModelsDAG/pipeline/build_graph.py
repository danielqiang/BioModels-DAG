import networkx
from typing import Iterable, Tuple

__all__ = ['build_graph']


def build_graph(data: Iterable[Tuple[dict, str, dict]]):
    """
    Builds a NetworkX DiGraph object from (Child, Edge, Parent) triples.
    Each triple is represented as a directed edge from Child to Parent
    in the DiGraph.

    Child and Parent must be dictionaries containing all hashable values
    and a 'name' key (this is the name of the node in the DiGraph).

    Edge must be a string representing an edge label from Child to Parent.

    :param data: Iterable of (Child, Edge, Parent) triples.
    :rtype: networkx.DiGraph
    """
    g = networkx.DiGraph()

    for child_attrs, edge, parent_attrs in data:
        if 'name' not in child_attrs or 'name' not in parent_attrs:
            raise ValueError(
                "Both child and parent dicts must contain a 'name' key.\n"
                "Provided Child data: {}\n"
                "Provided Parent data: {}\n".format(child_attrs, parent_attrs)
            )
        # Copy dicts so popping 'name' doesn't affect the underlying data
        child_attrs, parent_attrs = child_attrs.copy(), parent_attrs.copy()
        child_name, parent_name = child_attrs.pop('name'), parent_attrs.pop('name')

        # Update node attributes only if the updated version has strictly more data
        # than the previous version
        if child_name not in g or set(child_attrs).issuperset(g.nodes[child_name]):
            g.add_node(child_name, **child_attrs)
        if parent_name not in g or set(parent_attrs).issuperset(g.nodes[parent_name]):
            g.add_node(parent_name, **parent_attrs)
        g.add_edge(child_name, parent_name, label=edge)

    return g
