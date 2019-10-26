from bs4 import BeautifulSoup
from typing import TextIO, Collection


def compartment_parser(sbml_file: TextIO, all_go_compartments: Collection,
                       skip_single_cmp_models=True):
    """
    Extracts all compartments from an SBML file and returns a generator of
    (Model, Edge, Parent Model) 3-tuples each representing a relationship
    between an SBML model and one of its defined compartments.

    :param sbml_file: SBML file handle.
    :param all_go_compartments: Collection of all known GO compartment names.
                            Acts as a preprocessed data reference for the
                            parser; can be obtained by calling
                            get_all_go_compartments().
    :param skip_single_cmp_models: If True, does not parse 'file' if it
                            is a single compartment model.
    :rtype: generator
    """
    from os.path import basename
    from .helpers import extract_publication_date

    soup = BeautifulSoup(sbml_file, features='lxml')
    compartment_tags = soup.find_all("compartment")

    if len(compartment_tags) < 2 and skip_single_cmp_models:
        return

    model_name = str(basename(sbml_file.name).split('.')[0])
    model_provider = 'biomodels.db'
    model_URI = 'http://identifiers.org/biomodels.db/' + model_name
    model_publication_date = extract_publication_date(soup)

    for compartment_tag in compartment_tags:
        compartment_data = {
            'name': get_name(compartment_tag, all_go_compartments).lower(),
            # Color compartments yellow
            'color': 'yellow',
        }
        model_data = {
            'name': model_name,
            'provider': model_provider,
            'URI': model_URI,
            'created': model_publication_date,
            # Color BioModels green
            'color': 'green'
        }

        go_id = get_go_id(compartment_tag)
        if go_id:
            compartment_data['identifier'] = go_id

        yield model_data, 'isPartOf', compartment_data


def get_go_id(compartment_tag: BeautifulSoup):
    """
    Extracts and returns the GO id annotation from a compartment tag.
    If no GO id annotation exists, return None.

    :param compartment_tag: BeautifulSoup Tag for a single compartment
                            in a multi-compartment model.
    """
    try:
        go_id = compartment_tag.find("rdf:li")['rdf:resource'].split('/')[-1]
        return go_id
    # No annotation containing the GO id exists for the SBML compartment tag.
    except TypeError:
        return None


def get_name(compartment_tag: BeautifulSoup, all_go_compartments):
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
    from BioModels.tools import get_go_json
    from difflib import get_close_matches

    try:
        # Try to extract the Gene Ontology id (GO id)
        go_id = get_go_id(compartment_tag)
        assert go_id
        # Look up the GO id and extract the name of the GO entity
        compartment_name = get_go_json(go_id)['response']['docs'][0]['annotation_class_label']
        return compartment_name

    # AssertionError -> No annotation containing the GO id
    #                   exists for the SBML compartment tag.
    # ValueError -> An annotation containing the GO id exists
    #               but is an invalid GO id (e.g. FMA:20394)
    except (AssertionError, ValueError):
        name = compartment_tag.attrs['name'] \
            if 'name' in compartment_tag.attrs else compartment_tag.attrs['id']
        close_matches = get_close_matches(name.lower(), all_go_compartments, n=1, cutoff=0.8)
        return close_matches[0] if close_matches else name
