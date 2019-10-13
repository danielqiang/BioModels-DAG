from typing import TextIO
from bs4 import BeautifulSoup

__all__ = ['parse_derived_model']


def parse_derived_model(file: TextIO):
    """
    Parses an SBML file and returns a generator of
    (Child Model, Edge, Parent Model) 3-tuples.

    :param file: SBML file handle.
    :rtype: generator
    """
    soup = BeautifulSoup(file, features='lxml')

    publication_date = _extract_publication_date(soup)

    for parent_URI in _extract_parent_URIs(soup):
        child_name = str(file.name.split('.')[0])
        child_provider = 'biomodels.db'
        child_URI = 'http://identifiers.org/biomodels.db/' + child_name

        parent_name = parent_URI.split("http://identifiers.org/")[-1].split('/')[-1]
        parent_provider = parent_URI.split("http://identifiers.org/")[-1].split('/')[0]

        child_data = {'name': child_name, 'provider': child_provider,
                      'URI': child_URI, 'created': publication_date}
        parent_data = {'name': parent_name, 'provider': parent_provider, 'URI': parent_URI}

        # Color pubmed nodes red, biomodel nodes green
        if parent_data['provider'] in ('biomodels.db', 'pubmed'):
            parent_data['color'] = 'red' if parent_data['provider'] == 'pubmed' else 'green'
        child_data['color'] = 'green'

        yield child_data, 'isDerivedFrom', parent_data


def _extract_parent_URIs(soup: BeautifulSoup):
    for resource in soup.find_all('bqmodel:isderivedfrom'):
        for tag in resource.find_all('rdf:li'):
            yield tag['rdf:resource']


def _extract_publication_date(soup: BeautifulSoup):
    from dateutil import parser

    dt = soup.find("dcterms:created").find("dcterms:w3cdtf").text
    return str(parser.parse(dt).date())
