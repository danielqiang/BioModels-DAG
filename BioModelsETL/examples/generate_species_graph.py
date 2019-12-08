from BioModelsETL import *
from BioModelsETL.utils import timeit, yield_model_paths


@timeit
def main():
    import networkx

    filepaths = yield_model_paths()

    data = extract_data(filepaths, parser=SpeciesParser())
    for i in data:
        print(i)
    # graph = build_graph(data)
    # networkx.write_graphml(graph, "../graphs/species.graphml")


if __name__ == '__main__':
    main()
