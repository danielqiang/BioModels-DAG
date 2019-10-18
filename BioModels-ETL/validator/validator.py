from bs4 import BeautifulSoup
from os.path import join, basename
import os


def validate():
    for model in os.listdir("../curated"):
        print(model)

        filepath = join("..", "curated", model)
        with open(filepath, "r", encoding='utf8') as f:
            soup = BeautifulSoup(f, features="lxml")

            for tag in soup.find_all('compartment'):
                identifier = _get_id(tag)
                if identifier and identifier.startswith(("GO", "FMA", "BTO")):
                    print(identifier)
                else:
                    print(tag)
        print()


def _get_id(compartment_tag: BeautifulSoup):
    """
    Extracts and returns the identifier annotation from a compartment tag.
    If no identifier annotation exists, return None.

    :param compartment_tag: BeautifulSoup Tag for a single compartment
                            in a multi-compartment model.
    """
    try:
        identifier = compartment_tag.find("rdf:li")['rdf:resource'].split('/')[-1]
        return identifier
    except TypeError:
        return None


validate()
