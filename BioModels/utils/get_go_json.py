import requests

__all__ = ['get_go_json', 'go_id_is_valid']


def get_go_json(go_id: str, session: requests.Session = None):
    """
    Requests and returns JSON data from GOlr for the element specified by go_id.
    Returns None if go_id is incorrectly formatted.

    :param go_id: Seven digit identifier prefixed by GO (e.g. GO:0005634) that
                uniquely identifies a gene ontology term element.

                See http://geneontology.org/docs/GO-term-elements for more
                information.
    :param session: Requests session to use for HTTP request. If None, creates
                    a new session.
    """

    if not go_id_is_valid(go_id):
        return None

    with session or requests.Session() as s:
        params = {'wt': 'json', 'q': 'id:"{}"'.format(go_id)}
        return s.get("http://golr-aux.geneontology.io/solr/select", params=params).json()


def go_id_is_valid(go_id: str):
    """
    Returns True if a go_id is correctly formatted. Returns False otherwise.
    :param go_id: Seven digit identifier prefixed by GO (e.g. GO:0005634) that
                uniquely identifies a gene ontology term element.

                See http://geneontology.org/docs/GO-term-elements for more
                information.
    """
    import re

    return re.match(r"GO:[0-9]{7}$", go_id)


if __name__ == '__main__':
    from pprint import pprint

    pprint(get_go_json("GO:1902186"))
