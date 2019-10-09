from typing import Iterable
from bs4 import BeautifulSoup

__all__ = ['SBMLParser']


class SBMLParser:
    """A parser for extracting relationships between biological models from SBML files"""

    def __init__(self, filepaths: Iterable[str]):
        """
        Parses SBML files and collects (Child Model Data, Edge, Parent Model Data)
        3-tuples each representing a parent-child relationship between two biological
        models. Model Data items are dictionaries containing the model's name,
        web provider and URI.

        Uses the XML tag "bqmodel:isDerivedFrom" to identify a relationship.

        :param filepaths: Paths to SBML files.
        """
        self._filepaths = filepaths

    def as_generator(self):
        """
        Returns a generator over all (Child Model Data, Edge, Parent Model Data)
        3-tuples in this parser.

        :rtype: generator
        """
        return self._parse_SBML()

    def to_csv(self, filepath):
        """
        Writes a CSV file containing all (Child Model Data, Edge, Parent Model Data)
        3-tuples in this parser.

        :param filepath: Path to CSV file.
        """
        import csv

        with open(filepath, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow('Child', 'Edge', 'Parent')

            for row in self._parse_SBML():
                writer.writerow(row)

    def _parse_SBML(self):
        """
        Parses SBML files and returns a generator of
        (Child Model, Edge, Parent Model) 3-tuples.

        :rtype: generator
        """
        for filepath in self._filepaths:
            yield from self._parse(filepath)

    def _parse(self, filepath: str):
        """
        Parses an SBML file and returns a generator of
        (Child Model, Edge, Parent Model) 3-tuples.

        :param filepath: Path to SBML file.
        :rtype: generator
        """
        from os.path import basename

        with open(filepath, "r", encoding='utf8') as f:
            soup = BeautifulSoup(f, features='lxml')

            for parent_URI in self._extract_parent_URIs(soup):
                child_name = str(basename(filepath).split('.')[0])
                child_provider = 'biomodels.db'
                child_URI = 'http://identifiers.org/biomodels.db/' + child_name

                parent_name = parent_URI.split("http://identifiers.org/")[-1].split('/')[-1]
                parent_provider = parent_URI.split("http://identifiers.org/")[-1].split('/')[0]

                child_data = {'name': child_name, 'provider': child_provider, 'URI': child_URI}
                parent_data = {'name': parent_name, 'provider': parent_provider, 'URI': parent_URI}

                yield child_data, 'isDerivedFrom', parent_data

    @staticmethod
    def _extract_parent_URIs(soup: BeautifulSoup):
        for resource in soup.find_all('bqmodel:isderivedfrom'):
            yield from (tag['rdf:resource'] for tag in resource.find_all('rdf:li'))
