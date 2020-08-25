from BioModelsDAG import *
from BioModelsDAG.utils import timeit, yield_model_paths
import networkx


@timeit
def main():
    filepaths = yield_model_paths()

    data = extract_data(filepaths, parser=BTOParser())
    graph = build_graph(data)
    networkx.write_graphml(graph, "graphs/bto.graphml")


if __name__ == '__main__':
    main()
