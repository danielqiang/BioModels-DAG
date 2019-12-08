from BioModelsETL import extract_data, build_graph, DerivedModelParser
from BioModelsETL.utils import timeit, yield_model_paths


@timeit
def main():
    import networkx

    filepaths = yield_model_paths()

    data = extract_data(filepaths, parser=DerivedModelParser())
    graph = build_graph(data)
    networkx.write_graphml(graph, "graphs/derived_models.graphml")


if __name__ == '__main__':
    main()
