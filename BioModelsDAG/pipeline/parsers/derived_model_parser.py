from ..bases import BaseParser
from bs4 import BeautifulSoup

__all__ = ['DerivedModelParser']


class DerivedModelParser(BaseParser):
    def parser(self, sbml_file, **kwargs):
        """
        Extracts all parent models from an SBML file and returns a generator of
        (Child Model, Edge, Parent Model) 3-tuples representing parent-child
        relationships between SBML models.

        :param sbml_file: SBML file handle.
        :rtype: generator
        """
        from BioModelsDAG.utils import extract_model_data

        soup = BeautifulSoup(sbml_file, features='lxml')

        child_data = extract_model_data(sbml_file, soup=soup)

        for parent_URI in self.extract_parent_URIs(soup):
            parent_name = parent_URI.split("http://identifiers.org/")[-1].split('/')[-1]
            parent_provider = parent_URI.split("http://identifiers.org/")[-1].split('/')[0]

            parent_data = {
                'name': parent_name,
                'provider': parent_provider,
                'URI': parent_URI
            }

            # Color pubmed nodes red, biomodel nodes green
            if parent_data['provider'] in ('biomodels.db', 'pubmed'):
                parent_data['color'] = 'red' if parent_data['provider'] == 'pubmed' else 'green'
            child_data['color'] = 'green'

            yield child_data, 'isDerivedFrom', parent_data

    @staticmethod
    def extract_parent_URIs(soup: BeautifulSoup):
        for resource in soup.find_all('bqmodel:isderivedfrom'):
            for tag in resource.find_all('rdf:li'):
                yield tag['rdf:resource']
