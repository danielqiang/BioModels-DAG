from ..bases import BaseParser
from collections import defaultdict

__all__ = ['ReactionsParser']


class ReactionsParser(BaseParser):
    def parser(self, sbml_file, counter: defaultdict = None, **kwargs):
        """
        Extracts all reactions from an SBML file and returns a generator of
        (Model, Edge, Parent Model) 3-tuples each representing a relationship
        between an SBML model and one of its defined reaction components.

        :param sbml_file: SBML file handle.
        :param counter: Counter dict to extract metadata about SBMl reactions.
                        Use collections.defaultdict(int).

        :rtype: generator
        """
        import libsbml
        from BioModelsETL.utils import extract_annotation_identifiers, extract_model_data

        if type(counter) is dict:
            counter = defaultdict(int, counter)

        model_data = extract_model_data(sbml_file)

        model = libsbml.readSBMLFromFile(sbml_file.name).getModel()
        if model is None:
            return print("Could not extract SBML model for {}.".format(sbml_file.name))

        for reaction in model.getListOfReactions():
            reaction_name = reaction.getName() if reaction.getName() else reaction.getId()

            # Color BioModels green
            model_data['color'] = 'green'

            annotation = reaction.getAnnotationString()

            # Extract metadata into counter object
            if counter:
                counter['numReactions'] += 1
                if annotation == '':
                    counter['numUnannotatedReactions'] += 1
                else:
                    counter['numAnnotatedReactions'] += 1
                if len(list(extract_annotation_identifiers(annotation))) > 1:
                    counter['numMultipleURIReactions'] += 1

            identifiers = set(extract_annotation_identifiers(annotation))
            kegg_identifiers = {i for i in identifiers if 'kegg' in i.lower()}

            if any(i.split('/')[-1] in {'GO:0065003', 'GO:0005488'} for i in identifiers):
                print(sbml_file.name)

            reaction_data = {
                'name': reaction_name,
                'KEGG identifiers': ', '.join(kegg_identifiers),
                'other identifiers': ', '.join(identifiers - kegg_identifiers),
                # Color reactions red
                'color': 'red'
            }
            yield reaction_data, 'isContainedIn', model_data
