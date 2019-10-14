import requests

__all__ = ['get_go_json']


def get_go_json(go_id: str, session: requests.Session = None):
    """
    Requests and returns JSON data from GOlr (http://golr.berkeleybop.org)
    for the element specified by go_id.

    :param go_id: Seven digit identifier prefixed by GO (e.g. GO:0005634) that
                uniquely identifies a gene ontology term element.

                See http://geneontology.org/docs/GO-term-elements for more
                information.
    :param session: Requests session to use for HTTP request. If None, creates
                    a new session.
    :raises ValueError if go_id is incorrectly formatted.

    """
    import re

    if not re.match(r"GO:[0-9]{7}$", go_id):
        raise ValueError(
            "GO id must be of the format 'GO:<7 digit identifier>'. Input: {}".format(go_id)
        )

    with session or requests.Session() as s:
        params = {'wt': 'json', 'q': 'id:"{}"'.format(go_id)}
        return s.get("http://golr-aux.geneontology.io/solr/select", params=params).json()
