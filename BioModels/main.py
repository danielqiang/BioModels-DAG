from BioModels import SBMLDataConverter, derived_model_parser, build_graph
from BioModels.utils import timeit, yield_model_paths


@timeit
def main():
    import networkx

    filepaths = yield_model_paths()

    data = SBMLDataConverter(filepaths, parser=derived_model_parser).as_generator()
    graph = build_graph(data)
    networkx.write_graphml(graph, "data/derived_models.graphml")


if __name__ == '__main__':
    main()
