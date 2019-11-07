from BioModels import *
from BioModels.utils import timeit, yield_model_paths, to_csv


def flatten_reaction_data(data):
    """
    Flattens each (Child, Edge, Parent) 3-tuple from reactions_parser
    into relevant information to write to a CSV file.

    :param data: Generator of (Child, Edge, Parent) 3-tuples returned
                from BioModels.pipeline.parsers.reactions_parser.
    :rtype: generator
    """
    for child, edge, parent in data:
        # Omit color data 
        parent = [v for k, v in parent.items() if k != 'color']
        child = [v for k, v in child.items() if k != 'color']
        yield parent + child


@timeit
def main():
    filepaths = yield_model_paths()
    data = SBMLDataConverter(filepaths,
                             parser=reactions_parser).as_generator()
    data = flatten_reaction_data(data)
    headers = ("Model Name", "Provider", "URI", "Created",
               "Reaction Name", "KEGG Identifiers", "Other Identifiers")
    to_csv("../kegg_reactions.csv", data, headers=headers)


if __name__ == '__main__':
    main()
