from BioModelsETL import *
from BioModelsETL.utils import timeit, yield_model_paths, to_csv


def flatten_reaction_data(data):
    """
    Flattens each (Child, Edge, Parent) 3-tuple from reactions_parser
    into relevant information to write to a CSV file.

    :param data: Generator of (Child, Edge, Parent) 3-tuples returned
                from BioModelsETL.pipeline.parsers.reactions_parser.
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
    data = extract_data(filepaths, parser=ReactionsParser())
    data = flatten_reaction_data(data)
    headers = ("Model Name", "Provider", "URI", "Created",
               "Reaction Name", "KEGG Identifiers", "Other Identifiers")
    to_csv("../kegg_reactions.csv", data, headers=headers)


if __name__ == '__main__':
    main()
