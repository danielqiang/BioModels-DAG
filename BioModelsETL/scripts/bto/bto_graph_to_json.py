import rdflib
import pickle
import re
import json


def pickle_bto_graph():
    with open("bto.owl") as f:
        g = rdflib.Graph().parse(file=f)

    with open("bto_graph.pickle", mode="wb") as f:
        pickle.dump(g, f, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    # pickle_bto_graph()
    with open("bto_graph.pickle", mode="rb") as f:
        g = pickle.load(f)

    bto_pattern = re.compile("BTO:\d{7}")
    bto_map = {}
    for s, p, o in g:
        bto_id = str(s).split("http://purl.obolibrary.org/obo/", maxsplit=1)[-1].replace("_", ":")

        if bto_pattern.match(bto_id) and str(p).endswith("label"):
            bto_map[bto_id] = str(o)

    with open("../../examples/bto_lookup.json", mode="w") as f:
        json.dump(bto_map, f)


if __name__ == '__main__':
    main()
    # pickle_bto_graph()
    # with open("bto_lookup.json") as f:
    #     data = json.load(f)
    #     print(len(data))

