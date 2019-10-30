from BioModels import *
from BioModels.utils import timeit, yield_model_paths


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
    data = SBMLDataConverter(filepaths,
                             parser=reactions_parser,
                             counter=reaction_metadata).as_generator()
    graph = build_graph(data)

    print(reaction_metadata)
    networkx.write_graphml(graph, "../graphs/reactions.graphml")


if __name__ == '__main__':
    main()
