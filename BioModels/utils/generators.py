import libsbml

__all__ = ['get_reactions', 'get_compartments', 'get_species']


def _skip_invalid_model(method):
    """
    Decorator. Skips an SBML model and prints an error if libsbml
    model extraction fails rather than raising an exception.

    :param method: Method expecting a non-null return value from
                libsbml.SBMLDocument.getModel().
    """
    def wrapped(mpath, **kwargs):
        try:
            return method(mpath, **kwargs)
        except AttributeError:
            print("Could not extract SBML model for {}.".format(mpath))

    return wrapped


@_skip_invalid_model
def get_reactions(mpath):
    """
    Returns a generator over libsbml.Reaction objects representing reactions
    in an SBML file.

    :param mpath: Path to SBML model.
    :rtype: generator
    """
    model = libsbml.readSBMLFromFile(mpath).getModel()

    yield from model.getListOfReactions()


@_skip_invalid_model
def get_species(mpath):
    """
    Returns a generator over libsbml.Species objects representing species
    in an SBML file.

    :param mpath: Path to SBML model.
    :rtype: generator
    """
    model = libsbml.readSBMLFromFile(mpath).getModel()

    yield from model.getListOfSpecies()


@_skip_invalid_model
def get_compartments(mpath):
    """
    Returns a generator over libsbml.Compartment objects representing compartments
    in an SBML file.

    :param mpath: Path to SBML model.
    :rtype: generator
    """
    model = libsbml.readSBMLFromFile(mpath).getModel()

    yield from model.getListOfCompartments()
