from BioModels import *
from BioModels.utils import timeit, yield_model_paths


@timeit
def main():
    import networkx
    from collections import defaultdict

    filepaths = yield_model_paths()

    reaction_metadata = defaultdict(int)
    data = SBMLDataConverter(filepaths,
                             parser=reactions_parser,
                             counter=reaction_metadata,
                             print_fpath=False).as_generator()
    graph = build_graph(data)

    print(reaction_metadata)
    # networkx.write_graphml(graph, "../graphs/reactions.graphml")


if __name__ == '__main__':
    main()
