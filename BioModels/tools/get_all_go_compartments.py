from bs4 import BeautifulSoup


def get_all_go_compartments(dirpath, skip_single_cmp_models=True):
    """
    Extracts and returns all defined GO compartments from BioModel
    SBML files.

    :param dirpath: Directory containing BioModel SBML files.
    :param skip_single_cmp_models: If True, does not parse sbml_file if it
                        is a single compartment model.
    :rtype: set
    """
    from pathlib import Path

    all_compartments = set()

    for file in Path(dirpath).iterdir():
        print(file)
        with open(str(file.resolve()), "r", encoding='utf8') as f:
            soup = BeautifulSoup(f, features='lxml')

            if skip_single_cmp_models and len(soup.find_all("compartment")) < 2:
                continue
            for compartment in soup.find_all("compartment"):
                all_compartments.update(_get_compartment_names(compartment))

    return all_compartments


def _get_compartment_names(compartment: BeautifulSoup):
    """
    Given a BeautifulSoup compartment, returns a generator over all GO compartment
    names defined by a GO ID URI.

    :param compartment: BeautifulSoup object containing an SBML compartment.
    :rtype: generator
    """
    from . import get_go_json, go_id_is_valid

    for uri_tag in compartment.find_all(attrs={"rdf:resource": True}):
        go_id = uri_tag['rdf:resource'].split("/")[-1]
        if go_id_is_valid(go_id):
            compartment_name = get_go_json(go_id)['response']['docs'][0]['annotation_class_label']
            yield compartment_name


if __name__ == '__main__':
    get_all_go_compartments(r"C:\Users\danie\PythonProjects\BioModels\BioModels\curated")
