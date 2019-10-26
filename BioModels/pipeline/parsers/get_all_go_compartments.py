def get_all_go_compartments(dirpath):
    """
    Extracts and returns all defined GO compartments from BioModel
    SBML files.

    :param dirpath: Directory containing BioModel SBML files.
    :rtype: set
    """
    from BioModels.tools import get_go_json
    from bs4 import BeautifulSoup
    import os

    all_compartments = set()
    for file in os.listdir(dirpath):
        with open(os.path.join(dirpath, file), "r", encoding='utf8') as f:
            soup = BeautifulSoup(f, features='lxml')

            # Skip single-compartment models
            compartment_tags = soup.find_all("compartment")
            if len(compartment_tags) < 2:
                continue

            for tag in compartment_tags:
                try:
                    go_id = tag.find("rdf:li")['rdf:resource'].split('/')[-1]
                    compartment_name = get_go_json(go_id)['response']['docs'][0][
                        'annotation_class_label']
                    all_compartments.add(compartment_name)
                except (ValueError, TypeError):
                    pass
    return all_compartments
