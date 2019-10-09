import networkx
import os

from BioModels import SBMLParser, build_graph


def main():
    filepaths = (os.path.join('curated', model) for model in os.listdir("curated"))

    data = SBMLParser(filepaths).to_generator()
    graph = build_graph(data)
    networkx.write_graphml(graph, "data/g.graphml")


if __name__ == '__main__':
    main()
