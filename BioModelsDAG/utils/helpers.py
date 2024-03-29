from bs4 import BeautifulSoup
from typing import TextIO

__all__ = [
    'extract_publication_date',
    'extract_annotation_identifiers',
    'extract_model_data'
]


def extract_publication_date(soup: BeautifulSoup):
    """
    Extracts the publication date of an SBML model.

    :param soup: bs4.BeautifulSoup object initialized with
            an SBML model's XML markup.
    :rtype: str
    """
    from dateutil import parser

    dt = soup.find("dcterms:created").find("dcterms:w3cdtf").text
    return str(parser.parse(dt).date())


def extract_annotation_identifiers(annotation_str: str):
    """
    Returns a generator over all URI identifiers present within
    an SBML annotation.

    :param annotation_str: Valid RDF/XML string with a
                            top-level SBML <annotation> tag.
    :rtype: generator
    """
    soup = BeautifulSoup(annotation_str, features='lxml')
    for tag in soup.find_all(attrs={"rdf:resource": True}):
        yield tag['rdf:resource']


def extract_model_data(sbml_file: TextIO, soup: BeautifulSoup = None):
    """
    Returns a dictionary containing the following SBML model data:

    {
        "name": <model name>,
        "provider": "biomodels.db",
        "URI": <model URI>,
        "created": <model publication date>
    }

    Sets the file pointer to the start of sbml_file after extraction.

    :param sbml_file: SBML file handle.
    :param soup: bs4.BeautifulSoup object initialized with sbml_file markup.
                If None, initializes a new bs4.BeautifulSoup object with sbml_file
                markup.
    :rtype: dict
    """
    from os.path import basename

    soup = soup or BeautifulSoup(sbml_file, features='lxml')

    model_name = str(basename(sbml_file.name).split('.')[0])
    model_provider = 'biomodels.db'
    model_uri = 'http://identifiers.org/biomodels.db/' + model_name
    model_publication_date = extract_publication_date(soup)

    sbml_file.seek(0)

    return {
        "name": model_name,
        "provider": model_provider,
        "URI": model_uri,
        "created": model_publication_date
    }
