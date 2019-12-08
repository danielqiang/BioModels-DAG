from BioModelsETL import *
from BioModelsETL.utils import timeit, yield_model_paths


@timeit
def main():
    import networkx

    filepaths = yield_model_paths()
    reaction_metadata = {
        "numReactions": 0,
        "numAnnotatedReactions": 0,
        "numUnannotatedReactions": 0,
        "numMultipleURIReactions": 0
    }
    data = extract_data(filepaths,
                        parser=ReactionsParser(),
                        counter=reaction_metadata)
    graph = build_graph(data)

    print(reaction_metadata)
    networkx.write_graphml(graph, "../graphs/reactions.graphml")


if __name__ == '__main__':
    main()
