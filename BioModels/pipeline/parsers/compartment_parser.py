from ..bases import BaseParser
from bs4 import BeautifulSoup
from typing import Collection

__all__ = ['CompartmentParser']


class CompartmentParser(BaseParser):
    def parser(self, sbml_file, all_go_compartments: Collection = (),
               skip_single_cmp_models=False, **kwargs):
        """
        Extracts all compartments from an SBML file and returns a generator of
        (Model, Edge, Parent Model) 3-tuples each representing a relationship
        between an SBML model and one of its defined compartments.

        :param sbml_file: SBML file handle.
        :param all_go_compartments: Collection of all known GO compartment names.
                                Acts as a preprocessed data reference for the
                                parser; can be obtained by calling
                                get_all_go_compartments().
        :param skip_single_cmp_models: If True, does not parse sbml_file if it
                                is a single compartment model.
        :rtype: generator
        """
        from BioModels.utils import extract_model_data

        soup = BeautifulSoup(sbml_file, features='lxml')
        compartment_tags = soup.find_all("compartment")

        if len(compartment_tags) < 2 and skip_single_cmp_models:
            return

        model_data = extract_model_data(sbml_file, soup=soup)

        for compartment_tag in compartment_tags:
            compartment_data = {
                'name': self.get_name(compartment_tag, all_go_compartments).lower(),
                # Color compartments yellow
                'color': 'yellow',
            }
            # Color BioModels green
            model_data['color'] = 'green'

            go_id = self.get_go_id(compartment_tag)
            if go_id:
                compartment_data['identifier'] = go_id

            yield model_data, 'isPartOf', compartment_data

    @staticmethod
    def get_go_id(compartment_tag: BeautifulSoup):
        """
        Extracts and returns the GO id annotation from a compartment tag.
        If no GO id annotation exists, return None.

        :param compartment_tag: BeautifulSoup Tag for a single compartment
                                in a multi-compartment model.
        :rtype str
        """
        try:
            go_id = compartment_tag.find("rdf:li")['rdf:resource'].split('/')[-1]
            return go_id
        # No annotation containing the GO id exists for the SBML compartment tag.
        except TypeError:
            return None

    def get_name(self, compartment_tag: BeautifulSoup, all_go_compartments):
        """
        Extracts and returns the compartment name from a compartment tag.

        Uses the GO id annotation if it exists; if not, attempts to
        find a close GO compartment name match. If no satisfactory
        match is found, use the tag's name/id attribute instead.

        :param compartment_tag: BeautifulSoup Tag for a single compartment
                                in a multi-compartment model.
        :param all_go_compartments: Collection of all known GO compartment names.
                                Acts as a preprocessed data reference for the
                                parser; can be obtained by calling
                                get_all_go_compartments()
        :rtype: str
        """
        from BioModels.utils import get_go_json, go_id_is_valid
        from difflib import get_close_matches

        # Try to extract the Gene Ontology id (GO id)
        go_id = self.get_go_id(compartment_tag)
        if go_id and go_id_is_valid(go_id):
            # Look up the GO id and extract the GO compartment name
            return get_go_json(go_id)['response']['docs'][0]['annotation_class_label']

        # No GO id found or invalid GO id. Return a good close string match if found
        # or return the attribute name or id.
        name = compartment_tag.attrs['name'] \
            if 'name' in compartment_tag.attrs else compartment_tag.attrs['id']
        close_matches = get_close_matches(name.lower(), all_go_compartments, n=1, cutoff=0.8)
        return close_matches[0] if close_matches else name
