from BioModelsDAG import yield_model_paths, classify, extract_model_data, to_csv
import libsbml


def yield_classified_reactions():
    for fpath in yield_model_paths():
        with open(fpath, 'r', encoding='utf8') as sbml_file:
            model_data = extract_model_data(sbml_file)
        model = libsbml.readSBMLFromFile(fpath).getModel()
        if model is None:
            continue

        for reaction in model.getListOfReactions():
            yield (reaction.getId(), classify(reaction, model), *model_data.values())


def main():
    headers = ('Reaction ID', 'Reaction Type', 'Model Name', 'Provider', 'URI', 'Created')

    to_csv("../classified_reactions.csv", yield_classified_reactions(), headers=headers)


if __name__ == '__main__':
    main()
