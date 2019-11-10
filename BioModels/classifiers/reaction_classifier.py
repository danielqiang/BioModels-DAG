from BioModels import yield_model_paths, get_reactions

if __name__ == '__main__':
    for fpath in yield_model_paths():
        for reaction in get_reactions(fpath):
            for reactant in reaction.getListOfReactants():
                print(type(reactant))
            for product in reaction.getListOfProducts():
                print(product)
