from BioModels import *
from BioModels.tools import timeit


@timeit
def main():
    import networkx
    import os

    filepaths = (os.path.join('curated', model) for model in os.listdir("curated"))

    data = GraphDataBuilder(filepaths, parser=parse_derived_model).to_generator()
    graph = build_graph(data)
    networkx.write_graphml(graph, "data/derived_models.graphml")


if __name__ == '__main__':
    main()
