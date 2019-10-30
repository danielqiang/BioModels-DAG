from BioModels import *
from BioModels.utils import timeit, yield_model_paths


@timeit
def main():
    import networkx

    filepaths = yield_model_paths()

    data = SBMLDataConverter(filepaths, parser=species_parser).as_generator()
    graph = build_graph(data)
    networkx.write_graphml(graph, "../graphs/species.graphml")


if __name__ == '__main__':
    main()
