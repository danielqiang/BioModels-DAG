from ..bases import BaseParser

__all__ = ['SpeciesParser']


class SpeciesParser(BaseParser):
    def parser(self, sbml_file, **kwargs):
        """
        Extracts all species from an SBML file and returns a generator of
        (Model, Edge, Parent Model) 3-tuples each representing a relationship
        between an SBML model and one of its defined species components.

        :param sbml_file: SBML file handle.
        :rtype: generator
        """
        import libsbml
        from BioModelsDAG.utils import extract_annotation_identifiers, extract_model_data

        model = libsbml.readSBMLFromFile(sbml_file.name).getModel()

        model_data = extract_model_data(sbml_file)
        # Color BioModels green
        model_data['color'] = 'green'

        if model is None:
            return print("Could not extract SBML model for {}.".format(sbml_file.name))
        for species in model.getListOfSpecies():
            species_name = species.getName() if species.getName() else species.getId()

            annotation = species.getAnnotationString()

            species_data = {
                'name': species_name,
                'identifiers': ', '.join(extract_annotation_identifiers(annotation)),
                # Color species blue
                'color': 'blue'
            }
            yield species_data, 'isContainedIn', model_data
