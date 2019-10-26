from typing import TextIO


def reactions_parser(sbml_file: TextIO):
    """
    Extracts all reactions from an SBML file and returns a generator of
    (Model, Edge, Parent Model) 3-tuples each representing a relationship
    between an SBML model and one of its defined reaction components.

    :param sbml_file: SBML file handle.
    :rtype: generator
    """
    import libsbml
    from .helpers import extract_annotation_identifiers, extract_model_data

    model_data = extract_model_data(sbml_file)

    model = libsbml.readSBMLFromFile(sbml_file.name).getModel()
    if model is None:
        return print("Could not extract SBML model for {}.".format(sbml_file.name))
    for reaction in model.getListOfReactions():
        reaction_name = reaction.getName() if reaction.getName() else reaction.getId()

        # Color BioModels green
        model_data['color'] = 'green'

        annotation = reaction.getAnnotationString()

        reaction_data = {
            'name': reaction_name,
            'identifiers': ', '.join(extract_annotation_identifiers(annotation)),
            # Color reactions red
            'color': 'red'
        }
        yield reaction_data, 'isContainedIn', model_data
